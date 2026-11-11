# Taxonomy: Integration Interface Classification Axes

> Ratified by `CR-IS-CAT-04B`. A record occupies exactly one cell per axis; the
> gates enforce it.

## 1. Why three axes, not four

The ISS taxonomy classifies a contract by kind, consumer, interaction and
maturity. An interface inherits the contract's consumer and interaction
profile; what it adds is the kind of boundary. The contract-maturity axis has
no interface analogue: an interface does not settle, it is bound or it is not.
The binding state (`bound`, `planned`, `deprecated`) carries that information
without duplicating the ISS axis.

## 2. The axes

| Axis | Field | Vocabulary |
|---|---|---|
| Interface kind | `interface_kind` | rest-api, message-topic, event-stream, file-transfer, rpc, database-access, mixed, other |
| Consumer class | `consumer_class` | internal-application, internal-analyst, internal-machine, external-partner, external-customer, mixed |
| Interaction pattern | `interaction_pattern` | request-response, event-push, event-subscribe, streaming, batch, mixed |

The consumer class and interaction pattern are inherited verbatim from the
bound ISS record. For component-bound records they are asserted directly and
corroborated by the same 3-vendor evidence bar.

The interface kind is derived from the bound service's interaction pattern by
this deterministic mapping (G-10), which is part of this ratification:

| Service interaction pattern | Interface kind |
|---|---|
| request-response | rest-api |
| event-push | message-topic |
| event-subscribe | message-topic |
| streaming | event-stream |
| batch | file-transfer |
| mixed | mixed |

The remaining vocabulary cells (rpc, database-access, other) are reserved for
interfaces whose boundary kind is not derived from a service pattern: the
agent-orchestrator internal interface is admitted as rpc on direct vendor
corroboration, and database-access exists for boundary records that expose
data-store access rather than a service contract.

## 3. Classification is not identification

The three-tuple classifies; it does not identify. At population scale the
vocabulary sizes make three-tuple collisions among distinct records
mathematically inevitable: 8 kinds times 6 consumer classes times 6 patterns is
288 cells for 627 records. Two records are duplicates only when they share the
system class, the binding, the three-tuple and the name. Records that share a
three-tuple but bind different contracts are distinct records in one
classification cell, which is a fact about the vocabulary sizes, not a finding
against the records. The same holds one level down: a service may expose more
than one boundary, so records that share a binding but carry different names
(the identity service exposes both dea:integration-interface-identity-api and
dea:integration-interface-identity-service) are distinct boundaries of one
contract. The taxonomy gate (Gate 6) encodes exactly this.

## 4. Tag mirrors

Each promoted field has exactly one tag mirror (`interface-kind:...`,
`consumer-class:...`, `interaction-pattern:...`), plus the `sector:` and
`system-class:` context tags inherited from the bound record. The gate asserts
the mirrors agree with the fields. The mirrors exist so a consumer grepping
tags sees the classification without parsing the record body.
