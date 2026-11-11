# Foundations: Integration Interface Catalogue

> Method before content. This document defines what this catalogue admits, how
> a record earns its place, and which decisions later change requests may cite
> by number instead of re-deriving.

Established by `CR-IS-CAT-04A` (foundation) and populated by `CR-IS-CAT-04B`.
It follows the methodology-first rule applied across the IS-family catalogues:
admission criteria, evidence process and gates land before records.

## 1. Cardinal scope: the boundary test

> Can the same interaction boundary be operationalised by two materially
> different vendor implementations?
>
> **Yes** -> this is an integration interface. Record it here.
> **No** -> it is an implementation detail, not a boundary; it belongs in no
> catalogue record.

The Integration Interface is the interaction boundary through which a service
contract or a component is actually exchanged: the means, the interaction
pattern, the shape of the exchange. The CR-021 D-4 disposition keeps two
neighbouring concepts out of scope:

- The **service contract** (what is exchanged, to whom, under what terms)
  belongs to `dea-catalog-information-system-services` (ISS). An IF record
  binds to it through `service_binding`; it never restates the offering.
- The **API contract artefact** (the request/response shape that specifies a
  boundary) belongs to the API catalogue, which will reference IF records
  through `dea:specifies`. An IF record carries no endpoints, no operations
  and no vendor protocol detail.

## 2. Exclusions

| Not this | Why | Where it lives |
|---|---|---|
| A service catalogue | The service names the contract; the interface specifies the means that operationalise it | `dea-catalog-information-system-services` (ISS) |
| A component catalogue | A component encapsulates structure and responsibility; the interface is the boundary it exposes | `dea-catalog-application-components` (ISC) |
| An API catalogue | The API contract artefact specifies an interface; it is not the boundary itself | API catalogue (pending, `dea:specifies`) |
| An integration runtime | Message brokers, gateways and buses are implementations that operationalise boundaries | Vendor evidence only, per G-12 |

## 3. Classification axes

Declared as direction here; ratified with closed vocabularies in
`docs/TAXONOMY.md` (CR-IS-CAT-04B).

| Axis | Vocabulary |
|---|---|
| Interface kind | rest-api, message-topic, event-stream, file-transfer, rpc, database-access, mixed, other |
| Consumer class | internal-application, internal-analyst, internal-machine, external-partner, external-customer, mixed |
| Interaction pattern | request-response, event-push, event-subscribe, streaming, batch, mixed |

A record occupies exactly one cell per axis. The consumer class and
interaction pattern are inherited from the bound ISS record (or, for
component-bound records, asserted directly and corroborated); the interface
kind is derived from the interaction pattern by a deterministic mapping
ratified in TAXONOMY section 2.

## 4. Admission criteria

1. **Substitutability.** At least 3 distinct vendor systems corroborate that
   the boundary exists and is operationalisable by materially different
   implementations (G-12: vendors are evidence, never canonical).
2. **Exactly one binding.** A record carries either a `service_binding` to an
   ISS record or a `component_binding` to an ISC record, never both, never
   neither.
3. **Evidence citable.** `governance.source_and_evidence` names the metamodel
   clause, the admitting CR and the vendor corroboration.
4. **Identifier canonical.** The id is `dea:integration-interface-...` in the
   IF namespace; external identifiers live in `external_references` (E004).
5. **Lifecycle declared.** Every record states its `lifecycle_status` from the
   metamodel lifecycle vocabulary.
6. **Deterministic derivation.** Population-scale admission is derived by
   reproducible generators (G-10), never by hand-typed bulk content.

## 5. Cross-catalogue reference policy (D4/D5, mirroring ISS and ISC)

Every reference resolves against a vendored target-id snapshot pinned to a
commit, never a live fetch at run time. `service_binding` resolves against the
vendored ISS snapshot; `component_binding` against the vendored ISC snapshot.
An unresolvable reference is a hard CI failure; there is no forward-declaration
escape in this catalogue, because the targets (ISS, ISC) are both populated.

Repository reality reconciliation (recorded at foundation, re-verified at
population slice time, 2026-11-11):

| Alias | Allocated repository | Actual repository |
|---|---|---|
| ISF | `dea-catalog-information-system-functions` | `dea-catalog-system-functions` |
| ISC | `dea-catalog-information-system-components` | `dea-catalog-application-components` |
| ISS | `dea-catalog-information-system-services` | `dea-catalog-information-system-services` (matches) |
| IF | `dea-catalog-information-system-integration-interfaces` | `dea-catalog-integration-interfaces` (this repository, mid-rename) |

Reference resolution is by identifier, not by repository name, so the rename
debt blocks nothing. The metamodel entity `dea:IntegrationInterface` carries
the same `catalog_repo` contradiction ISS recorded in its CR-03A section 3.1:
the `catalog_repo` field names `dea-catalog-api-contracts` while the definition
field names `dea-catalog-information-system-integration-interfaces` per
CR-IS-CAT-04. **This catalogue follows the definition field**, records the
contradiction rather than silently resolving it, and defers the metamodel-side
correction to a metamodel CR.

## 6. Relationship registry

Relationship connections are expressed through the registry
(`relationships/v1-alpha/relationships.yaml`), not as inline state on the
record, per metamodel CR-3. The population registry carries one `dea:exposes`
edge per record: the bound service or component exposes the interface. API
`dea:specifies` edges will be added by the API catalogue programme, not here.

## 7. Decision-points register

| # | Decision | Statement |
|---|---|---|
| D1 | Boundary test | The interface is the interaction boundary; substitutability decides admission (section 1) |
| D2 | One binding per record | Exactly one of service_binding and component_binding (section 4.2) |
| D3 | Service contract ownership | The record binds to the contract; it never restates the offering |
| D4 | Snapshot resolution | Bindings resolve against pinned snapshots; no live fetches (section 5) |
| D5 | No forward declarations inbound | ISS and ISC are populated, so bindings must resolve; the forward-declaration register stays in the sibling catalogues |
| D6 | API separation | No endpoint, operation or vendor protocol detail on any record; the API contract artefact specifies the boundary from the API catalogue via dea:specifies |
| D7 | Rename debt recorded | The repository is mid-rename; resolution is by identifier, so nothing blocks |
| D8 | Registry not inline | Typed edges live in the registry, not as inline relationship state |
| D9 | Legacy anchors admitted | The five interfaces referenced by the ISF and ISC registries are admitted alongside the derived population |

## 8. Gates

| Gate | Script | Catches |
|---|---|---|
| Parse | `scripts/check_parse.py` | Malformed YAML or JSON anywhere in the tree |
| Pointer | `scripts/check_pointer.py` | Pointer missing fields, or drifted from its allocation |
| Schema projection | `scripts/check_schema_projection.py` | Normative drift, and any record that fails the schema |
| Writing rules | `scripts/check_writing_rules.py` | D-004 glyphs and D-005 triple semicolon |
| Record posture | `scripts/check_record_posture.py` | Records without population gates; a scaffold that claims population |
| Taxonomy | `scripts/check_record_taxonomy.py` | Multi-cell axes, tag/field disagreement, binding defects |
| Evidence | `scripts/check_record_evidence.py` | Missing clause, CR, corroboration or description |
| Reference integrity | `scripts/check_reference_integrity.py` | Unresolvable bindings, missing anchors, coverage gaps |
