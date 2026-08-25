# 0004 — Serialization: self-describing MessagePack (rmp-serde named mode)

## Context
Journal payloads outlive the code that wrote them. The format must be
inspectable (CLI), evolvable (add fields without breaking old journals),
compact enough, and available for arbitrary serde types. Candidates:
postcard (compact, positional, NOT self-describing) vs rmp-serde
(MessagePack).

## Decision
rmp-serde in **named** mode (`to_vec_named`): struct fields and enum
variants encode by name. Applied to engine records, snapshots, manifests,
and user payloads, always beneath the envelope's `format_version` byte.
Payloads over the configured limit (default 1 MiB) are rejected with a
typed error telling users to store blobs externally and journal a
reference.

## Consequences
+ Field reordering and defaulted additions are compatible (tested);
  journals are debuggable with any msgpack tool; `sqrl inspect` is trivial.
− Field names cost bytes vs postcard (~1.5–2×; measured in Phase-2 write
  amplification). Chosen deliberately: this is a durability product and
  opaque positional encoding is the wrong default for data that must be
  readable years later.
