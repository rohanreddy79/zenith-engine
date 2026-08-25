//! Procedural macros for `sqrl`.
//!
//! Provides the [`macro@workflow`] attribute, which turns an `async fn` into a
//! registerable workflow definition, and the [`macro@step`] attribute, a
//! validation-only marker for step implementation functions.
//!
//! Generated code refers to the `sqrl` facade crate via absolute `::sqrl::...`
//! paths, so these macros must be used through that crate (they are re-exported
//! from its root).
#![forbid(unsafe_code)]
#![deny(missing_docs)]

use proc_macro::TokenStream;
use proc_macro2::TokenStream as TokenStream2;
use quote::quote;
use syn::parse::Parser;

/// Declares a durable workflow from an `async fn`.
///
/// The annotated function must have exactly the shape
/// `async fn name(ctx: &Ctx, input: I) -> Result<O>`: async, exactly two
/// arguments, the first a reference to the workflow context, no generics, no
/// `self` receiver, and a `Result<...>` return type.
///
/// The function item is replaced by a unit struct of the same name (and
/// visibility) that implements `sqrl::WorkflowDefProvider`, so the identifier
/// can be passed straight to the builder's `register(...)`. The original body
/// is preserved as an associated `run` method for direct calls in tests and
/// composition.
///
/// # Arguments
///
/// * `name = "..."` — registered workflow name; defaults to the function's
///   identifier.
/// * `version = <int>` — workflow version; defaults to `1`.
///
/// Both are optional and may appear in any order.
///
/// # Example
///
/// ```
/// use serde::{Deserialize, Serialize};
/// use sqrl::{Ctx, Result};
///
/// #[derive(Debug, Clone, Serialize, Deserialize)]
/// struct Order {
///     sku: String,
///     qty: u32,
/// }
///
/// #[sqrl::workflow(name = "checkout", version = 1)]
/// async fn checkout(ctx: &Ctx, order: Order) -> Result<u32> {
///     let total: u32 = ctx
///         .step("price", move || {
///             let qty = order.qty;
///             async move { Ok::<u32, String>(qty * 10) }
///         })
///         .await?;
///     Ok(total)
/// }
///
/// // `checkout` is now a unit struct implementing `WorkflowDefProvider`:
/// //     builder.register(checkout)
/// fn assert_provider<P: sqrl::WorkflowDefProvider>(_witness: P) {}
/// assert_provider(checkout);
/// ```
#[proc_macro_attribute]
pub fn workflow(attr: TokenStream, item: TokenStream) -> TokenStream {
    expand_workflow(attr.into(), item.into())
        .unwrap_or_else(|e| e.to_compile_error())
        .into()
}

/// Marks an `async fn` as a step implementation.
///
/// This attribute validates that the function is `async` and returns a
/// `Result<...>` type, then emits the item **unchanged** — it generates no
/// code. It exists so step functions are explicit, greppable, and documented
/// at their definition site.
///
/// # Example
///
/// ```
/// #[sqrl::step]
/// async fn charge_card(amount: u64, key: String) -> Result<u64, String> {
///     // ... side-effecting work, journaled by the caller via ctx.step(...) ...
///     let _ = key;
///     Ok(amount)
/// }
/// ```
#[proc_macro_attribute]
pub fn step(attr: TokenStream, item: TokenStream) -> TokenStream {
    expand_step(attr.into(), item.into())
        .unwrap_or_else(|e| e.to_compile_error())
        .into()
}

/// Parsed `#[workflow(...)]` arguments.
#[derive(Debug, Default)]
struct WorkflowArgs {
    name: Option<String>,
    version: Option<u32>,
}

/// Parses `name = "..."` and/or `version = <int>` (any order, both optional).
fn parse_workflow_args(tokens: TokenStream2) -> syn::Result<WorkflowArgs> {
    let mut out = WorkflowArgs::default();
    if tokens.is_empty() {
        return Ok(out);
    }
    let metas = syn::punctuated::Punctuated::<syn::MetaNameValue, syn::Token![,]>::parse_terminated
        .parse2(tokens)?;
    for meta in metas {
        if meta.path.is_ident("name") {
            if out.name.is_some() {
                return Err(syn::Error::new_spanned(
                    &meta.path,
                    "duplicate `name` argument",
                ));
            }
            let syn::Expr::Lit(syn::ExprLit {
                lit: syn::Lit::Str(s),
                ..
            }) = &meta.value
            else {
                return Err(syn::Error::new_spanned(
                    &meta.value,
                    "`name` expects a string literal, e.g. `name = \"checkout\"`",
                ));
            };
            let value = s.value();
            if value.is_empty() {
                return Err(syn::Error::new_spanned(s, "`name` must not be empty"));
            }
            out.name = Some(value);
        } else if meta.path.is_ident("version") {
            if out.version.is_some() {
                return Err(syn::Error::new_spanned(
                    &meta.path,
                    "duplicate `version` argument",
                ));
            }
            let syn::Expr::Lit(syn::ExprLit {
                lit: syn::Lit::Int(i),
                ..
            }) = &meta.value
            else {
                return Err(syn::Error::new_spanned(
                    &meta.value,
                    "`version` expects an integer literal, e.g. `version = 2`",
                ));
            };
            out.version = Some(i.base10_parse::<u32>()?);
        } else {
            return Err(syn::Error::new_spanned(
                &meta.path,
                "unsupported argument; expected `name = \"...\"` and/or `version = <int>`",
            ));
        }
    }
    Ok(out)
}

/// The pieces of a validated workflow fn signature the expansion needs.
struct WorkflowFnParts<'a> {
    /// First argument, verbatim (pattern and `&Ctx`-style type as written).
    ctx_arg: &'a syn::PatType,
    /// Second argument, verbatim.
    input_arg: &'a syn::PatType,
    /// The input type only (for the `typed_def` closure).
    input_ty: &'a syn::Type,
}

/// Validates the shape required by `#[workflow]`:
/// `async fn name(ctx: &Ctx, input: I) -> Result<O>`.
fn validate_workflow_fn(func: &syn::ItemFn) -> syn::Result<WorkflowFnParts<'_>> {
    let sig = &func.sig;
    require_async(sig, "workflow")?;

    if let Some(wc) = &sig.generics.where_clause {
        return Err(syn::Error::new_spanned(
            wc,
            "#[sqrl::workflow] functions cannot be generic (remove the `where` clause)",
        ));
    }
    if !sig.generics.params.is_empty() {
        return Err(syn::Error::new_spanned(
            &sig.generics,
            "#[sqrl::workflow] functions cannot be generic",
        ));
    }

    for arg in &sig.inputs {
        if let syn::FnArg::Receiver(recv) = arg {
            return Err(syn::Error::new_spanned(
                recv,
                "#[sqrl::workflow] functions cannot take `self`; use a free `async fn`",
            ));
        }
    }
    if sig.inputs.len() != 2 {
        return Err(syn::Error::new(
            sig.paren_token.span.join(),
            "#[sqrl::workflow] functions must take exactly two arguments: `(ctx: &Ctx, input: I)`",
        ));
    }

    let (ctx_arg, input_arg) = match (&sig.inputs[0], &sig.inputs[1]) {
        (syn::FnArg::Typed(c), syn::FnArg::Typed(i)) => (c, i),
        _ => {
            return Err(syn::Error::new_spanned(
                &sig.inputs,
                "#[sqrl::workflow] functions cannot take `self`",
            ))
        }
    };

    if !matches!(&*ctx_arg.ty, syn::Type::Reference(_)) {
        return Err(syn::Error::new_spanned(
            &ctx_arg.ty,
            "the first #[sqrl::workflow] argument must be a reference to the \
             workflow context, e.g. `ctx: &Ctx`",
        ));
    }

    require_result_return(sig, "workflow")?;

    Ok(WorkflowFnParts {
        ctx_arg,
        input_arg,
        input_ty: &input_arg.ty,
    })
}

/// Errors unless the fn is `async`.
fn require_async(sig: &syn::Signature, macro_name: &str) -> syn::Result<()> {
    if sig.asyncness.is_none() {
        return Err(syn::Error::new_spanned(
            sig.fn_token,
            format!("#[sqrl::{macro_name}] requires an `async fn`"),
        ));
    }
    Ok(())
}

/// Errors unless the return type is written as some `Result<...>` type.
fn require_result_return<'a>(
    sig: &'a syn::Signature,
    macro_name: &str,
) -> syn::Result<&'a syn::Type> {
    let msg = format!("#[sqrl::{macro_name}] functions must return a `Result<...>` type");
    let syn::ReturnType::Type(_, ty) = &sig.output else {
        return Err(syn::Error::new_spanned(sig.fn_token, msg));
    };
    if !is_result_type(ty) {
        return Err(syn::Error::new_spanned(ty, msg));
    }
    Ok(ty)
}

/// True if the type is spelled as `Result<...>` (any path prefix accepted).
fn is_result_type(ty: &syn::Type) -> bool {
    match ty {
        syn::Type::Path(tp) => tp
            .path
            .segments
            .last()
            .is_some_and(|seg| seg.ident == "Result"),
        syn::Type::Paren(p) => is_result_type(&p.elem),
        syn::Type::Group(g) => is_result_type(&g.elem),
        _ => false,
    }
}

/// `#[workflow]` expansion on `proc_macro2` streams (testable core).
fn expand_workflow(attr: TokenStream2, item: TokenStream2) -> syn::Result<TokenStream2> {
    let args = parse_workflow_args(attr)?;
    let func: syn::ItemFn = syn::parse2(item)?;
    let parts = validate_workflow_fn(&func)?;

    let name = args.name.unwrap_or_else(|| func.sig.ident.to_string());
    let version = args.version.unwrap_or(1);

    let attrs = &func.attrs;
    let vis = &func.vis;
    let ident = &func.sig.ident;
    let output = &func.sig.output;
    let body = &func.block;
    let ctx_arg = parts.ctx_arg;
    let input_arg = parts.input_arg;
    let input_ty = parts.input_ty;

    Ok(quote! {
        #(#attrs)*
        #[allow(non_camel_case_types)]
        #[derive(Clone, Copy)]
        #vis struct #ident;

        impl #ident {
            /// Call the workflow function directly (tests, composition).
            #vis async fn run(#ctx_arg, #input_arg) #output #body
        }

        impl ::sqrl::WorkflowDefProvider for #ident {
            fn workflow_def() -> ::sqrl::WorkflowDef {
                ::sqrl::typed_def(
                    #name,
                    #version,
                    |ctx: ::sqrl::Ctx, input: #input_ty| async move {
                        #ident::run(&ctx, input).await
                    },
                )
            }
        }
    })
}

/// `#[step]` expansion: validate, then pass the item through unchanged.
fn expand_step(attr: TokenStream2, item: TokenStream2) -> syn::Result<TokenStream2> {
    if !attr.is_empty() {
        return Err(syn::Error::new_spanned(
            attr,
            "#[sqrl::step] takes no arguments",
        ));
    }
    let func: syn::ItemFn = syn::parse2(item.clone())?;
    require_async(&func.sig, "step")?;
    require_result_return(&func.sig, "step")?;
    Ok(item)
}

#[cfg(test)]
mod tests {
    use super::*;
    use quote::quote;

    fn parse_fn(src: &str) -> syn::ItemFn {
        syn::parse_str(src).expect("test input should parse as a fn item")
    }

    fn workflow_err(src: &str) -> String {
        validate_workflow_fn(&parse_fn(src))
            .map(|_| ())
            .expect_err("expected validation to fail")
            .to_string()
    }

    // ---- attribute-args parsing ----

    #[test]
    fn args_default_when_empty() {
        let args = parse_workflow_args(TokenStream2::new()).unwrap();
        assert_eq!(args.name, None);
        assert_eq!(args.version, None);
    }

    #[test]
    fn args_explicit_name_and_version_any_order() {
        let args = parse_workflow_args(quote!(name = "checkout", version = 3)).unwrap();
        assert_eq!(args.name.as_deref(), Some("checkout"));
        assert_eq!(args.version, Some(3));

        let args = parse_workflow_args(quote!(version = 3, name = "checkout")).unwrap();
        assert_eq!(args.name.as_deref(), Some("checkout"));
        assert_eq!(args.version, Some(3));
    }

    #[test]
    fn args_name_only_and_version_only() {
        let args = parse_workflow_args(quote!(name = "wf")).unwrap();
        assert_eq!(args.name.as_deref(), Some("wf"));
        assert_eq!(args.version, None);

        let args = parse_workflow_args(quote!(version = 7)).unwrap();
        assert_eq!(args.name, None);
        assert_eq!(args.version, Some(7));
    }

    #[test]
    fn args_duplicate_key_is_error() {
        let err = parse_workflow_args(quote!(name = "a", name = "b")).unwrap_err();
        assert!(err.to_string().contains("duplicate"), "{err}");
        let err = parse_workflow_args(quote!(version = 1, version = 2)).unwrap_err();
        assert!(err.to_string().contains("duplicate"), "{err}");
    }

    #[test]
    fn args_unknown_key_is_error() {
        let err = parse_workflow_args(quote!(nam = "a")).unwrap_err();
        assert!(err.to_string().contains("unsupported argument"), "{err}");
    }

    #[test]
    fn args_wrong_literal_kinds_are_errors() {
        let err = parse_workflow_args(quote!(name = 1)).unwrap_err();
        assert!(err.to_string().contains("string literal"), "{err}");
        let err = parse_workflow_args(quote!(version = "1")).unwrap_err();
        assert!(err.to_string().contains("integer literal"), "{err}");
        let err = parse_workflow_args(quote!(name = "")).unwrap_err();
        assert!(err.to_string().contains("must not be empty"), "{err}");
    }

    // ---- workflow signature validation ----

    #[test]
    fn valid_workflow_fn_passes() {
        let func =
            parse_fn("async fn checkout(ctx: &Ctx, order: Order) -> Result<Receipt> { todo!() }");
        assert!(validate_workflow_fn(&func).is_ok());
        // Fully-qualified Result types are accepted too.
        let func =
            parse_fn("async fn f(c: &Ctx, x: u32) -> std::result::Result<u32, Error> { todo!() }");
        assert!(validate_workflow_fn(&func).is_ok());
    }

    #[test]
    fn non_async_fn_is_error() {
        let err = workflow_err("fn f(ctx: &Ctx, x: u32) -> Result<u32> { todo!() }");
        assert!(err.contains("async"), "{err}");
    }

    #[test]
    fn wrong_arity_is_error() {
        let err = workflow_err("async fn f(ctx: &Ctx) -> Result<u32> { todo!() }");
        assert!(err.contains("exactly two"), "{err}");
        let err = workflow_err("async fn f(ctx: &Ctx, x: u32, y: u32) -> Result<u32> { todo!() }");
        assert!(err.contains("exactly two"), "{err}");
    }

    #[test]
    fn generic_fn_is_error() {
        let err = workflow_err("async fn f<T>(ctx: &Ctx, x: T) -> Result<T> { todo!() }");
        assert!(err.contains("generic"), "{err}");
        let err = workflow_err(
            "async fn f(ctx: &Ctx, x: u32) -> Result<u32> where u32: Copy { todo!() }",
        );
        assert!(err.contains("generic"), "{err}");
    }

    #[test]
    fn self_receiver_is_error() {
        let err = workflow_err("async fn f(&self, x: u32) -> Result<u32> { todo!() }");
        assert!(err.contains("self"), "{err}");
    }

    #[test]
    fn non_reference_first_arg_is_error() {
        let err = workflow_err("async fn f(ctx: Ctx, x: u32) -> Result<u32> { todo!() }");
        assert!(err.contains("reference"), "{err}");
    }

    #[test]
    fn non_result_return_is_error() {
        let err = workflow_err("async fn f(ctx: &Ctx, x: u32) -> u32 { todo!() }");
        assert!(err.contains("Result"), "{err}");
        let err = workflow_err("async fn f(ctx: &Ctx, x: u32) { todo!() }");
        assert!(err.contains("Result"), "{err}");
    }

    // ---- expansion smoke tests ----

    #[test]
    fn expansion_contains_key_pieces() {
        let attr = quote!(name = "checkout", version = 3);
        let item = quote! {
            /// Orchestrates a checkout.
            pub async fn checkout(ctx: &Ctx, order: Order) -> Result<Receipt> { todo!() }
        };
        let expanded = expand_workflow(attr, item).unwrap();
        // The expansion must be well-formed Rust items.
        syn::parse2::<syn::File>(expanded.clone()).expect("expansion should parse as items");
        let out = expanded.to_string();
        assert!(out.contains("WorkflowDefProvider"), "{out}");
        assert!(out.contains("typed_def"), "{out}");
        assert!(out.contains("\"checkout\""), "{out}");
        assert!(out.contains("3u32"), "{out}");
        assert!(out.contains("struct checkout"), "{out}");
        assert!(out.contains("fn run"), "{out}");
        assert!(out.contains("Orchestrates a checkout."), "{out}");
    }

    #[test]
    fn expansion_defaults_name_and_version() {
        let item = quote!(
            async fn checkout(ctx: &Ctx, order: Order) -> Result<Receipt> {
                todo!()
            }
        );
        let out = expand_workflow(TokenStream2::new(), item)
            .unwrap()
            .to_string();
        assert!(out.contains("\"checkout\""), "{out}");
        assert!(out.contains("1u32"), "{out}");
    }

    #[test]
    fn expansion_rejects_invalid_fn() {
        let item = quote!(
            fn checkout(ctx: &Ctx, order: Order) -> Result<Receipt> {
                todo!()
            }
        );
        assert!(expand_workflow(TokenStream2::new(), item).is_err());
    }

    // ---- step ----

    #[test]
    fn step_passes_valid_fn_through_unchanged() {
        let item = quote! {
            async fn charge_card(order: Order, key: String) -> Result<Charge, PaymentError> {
                todo!()
            }
        };
        let out = expand_step(TokenStream2::new(), item.clone()).unwrap();
        assert_eq!(out.to_string(), item.to_string());
    }

    #[test]
    fn step_rejects_non_async_and_non_result() {
        let item = quote!(
            fn f(x: u32) -> Result<u32, E> {
                todo!()
            }
        );
        let err = expand_step(TokenStream2::new(), item).unwrap_err();
        assert!(err.to_string().contains("async"), "{err}");

        let item = quote!(
            async fn f(x: u32) -> u32 {
                todo!()
            }
        );
        let err = expand_step(TokenStream2::new(), item).unwrap_err();
        assert!(err.to_string().contains("Result"), "{err}");
    }

    #[test]
    fn step_rejects_arguments() {
        let item = quote!(
            async fn f(x: u32) -> Result<u32, E> {
                todo!()
            }
        );
        let err = expand_step(quote!(name = "x"), item).unwrap_err();
        assert!(err.to_string().contains("no arguments"), "{err}");
    }
}
