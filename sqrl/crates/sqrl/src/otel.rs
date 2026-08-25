//! Optional OpenTelemetry export (`otel` feature).
//!
//! * [`init`] installs a global tracing subscriber with an OTLP span
//!   exporter, so sqrl's workflow/step lifecycle spans (and your own
//!   `tracing` instrumentation) flow to any OTLP collector.
//! * [`register_metrics`] exports engine + storage counters (starts,
//!   completions, failures, retries, backpressure rejections, snapshots,
//!   fsyncs, records, bytes written) sampled from
//!   [`crate::Sqrl::stats_blocking`].
//!
//! Endpoint configuration follows the standard OTel environment variables
//! (`OTEL_EXPORTER_OTLP_ENDPOINT`, default `http://localhost:4317`).

use crate::{Error, Sqrl};
use opentelemetry::global;
use opentelemetry::KeyValue;
use std::sync::Arc;

/// Keeps the OTLP pipelines alive; drop to flush and shut down.
pub struct OtelGuard {
    tracer_provider: opentelemetry_sdk::trace::SdkTracerProvider,
    meter_provider: Option<opentelemetry_sdk::metrics::SdkMeterProvider>,
}

impl Drop for OtelGuard {
    fn drop(&mut self) {
        let _ = self.tracer_provider.shutdown();
        if let Some(mp) = self.meter_provider.take() {
            let _ = mp.shutdown();
        }
    }
}

fn resource(service_name: &str) -> opentelemetry_sdk::Resource {
    opentelemetry_sdk::Resource::builder()
        .with_attribute(KeyValue::new("service.name", service_name.to_string()))
        .build()
}

/// Install a global tracing subscriber exporting sqrl's spans over OTLP.
/// Call once, early. Returns a guard that flushes on drop.
pub fn init(service_name: &str) -> Result<OtelGuard, Error> {
    use tracing_subscriber::layer::SubscriberExt;
    use tracing_subscriber::util::SubscriberInitExt;

    let exporter = opentelemetry_otlp::SpanExporter::builder()
        .with_tonic()
        .build()
        .map_err(|e| Error::App(format!("otel span exporter: {e}")))?;
    let tracer_provider = opentelemetry_sdk::trace::SdkTracerProvider::builder()
        .with_batch_exporter(exporter)
        .with_resource(resource(service_name))
        .build();
    use opentelemetry::trace::TracerProvider as _;
    let tracer = tracer_provider.tracer("sqrl");
    global::set_tracer_provider(tracer_provider.clone());

    tracing_subscriber::registry()
        .with(tracing_subscriber::EnvFilter::from_default_env())
        .with(tracing_opentelemetry::layer().with_tracer(tracer))
        .try_init()
        .map_err(|e| Error::App(format!("otel subscriber: {e}")))?;

    Ok(OtelGuard {
        tracer_provider,
        meter_provider: None,
    })
}

/// Export engine/storage counters as OTLP metrics, sampled from `sqrl` on
/// the exporter's schedule. Extends the guard returned by [`init`].
pub fn register_metrics(guard: &mut OtelGuard, sqrl: &Arc<Sqrl>) -> Result<(), Error> {
    let exporter = opentelemetry_otlp::MetricExporter::builder()
        .with_tonic()
        .build()
        .map_err(|e| Error::App(format!("otel metric exporter: {e}")))?;
    let meter_provider = opentelemetry_sdk::metrics::SdkMeterProvider::builder()
        .with_periodic_exporter(exporter)
        .with_resource(resource("sqrl"))
        .build();
    global::set_meter_provider(meter_provider.clone());
    let meter = global::meter("sqrl");

    macro_rules! counter {
        ($name:literal, $desc:literal, $pick:expr) => {{
            let sqrl = Arc::clone(sqrl);
            let pick: fn(&sqrl_core::EngineMetrics, &sqrl_core::storage::StorageStats) -> u64 =
                $pick;
            meter
                .u64_observable_counter($name)
                .with_description($desc)
                .with_callback(move |obs| {
                    let mut total = 0u64;
                    for (m, s) in sqrl.stats_blocking() {
                        total += pick(&m, &s);
                    }
                    obs.observe(total, &[]);
                })
                .build();
        }};
    }
    counter!("sqrl.workflows.started", "workflows started", |m, _| m
        .starts);
    counter!("sqrl.workflows.completed", "workflows completed", |m, _| m
        .completions);
    counter!("sqrl.workflows.failed", "workflows failed", |m, _| m
        .failures);
    counter!("sqrl.workflows.cancelled", "workflows cancelled", |m, _| m
        .cancellations);
    counter!(
        "sqrl.steps.dispatched",
        "step executions dispatched",
        |m, _| m.step_dispatches
    );
    counter!("sqrl.steps.retries", "step retries", |m, _| m.step_retries);
    counter!(
        "sqrl.backpressure.rejections",
        "admission rejections",
        |m, _| m.backpressure_rejections
    );
    counter!("sqrl.snapshots", "snapshots taken", |m, _| m
        .snapshots_taken);
    counter!("sqrl.timers.fired", "durable timers fired", |m, _| m
        .timers_fired);
    counter!("sqrl.storage.fsyncs", "fsync barriers", |_, s| s.fsyncs);
    counter!(
        "sqrl.storage.records",
        "journal records appended",
        |_, s| s.records_appended
    );
    counter!("sqrl.storage.bytes", "bytes written to the WAL", |_, s| s
        .bytes_written);

    guard.meter_provider = Some(meter_provider);
    Ok(())
}
