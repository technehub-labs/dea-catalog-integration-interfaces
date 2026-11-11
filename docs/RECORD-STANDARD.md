# Record Standard: Integration Interface Records

> Established by `CR-IS-CAT-04B`. Every record under `entities/v1-alpha/` must
> meet this standard; Gate 7 enforces the machine-checkable subset.

## 1. Field-by-field requirements

| Field | Requirement |
|---|---|
| `id` | `dea:integration-interface-<slug>`; canonical, in the IF namespace (E004) |
| `type` | const `IntegrationInterface` |
| `name` | 1 to 200 characters; human-facing, vendor-neutral |
| `description` | at least 40 characters, at most 2000; states what boundary the record specifies, names the bound contract or component, cites the D-4 separation and the evidence bar |
| `version` | semver, `1.0.0` at admission |
| `lifecycle_status` | one of proposed, planned, active, deprecated, retired |
| `interface_kind` | one ratified cell (TAXONOMY 2) |
| `consumer_class` | one ratified cell, inherited from the bound record |
| `interaction_pattern` | one ratified cell, inherited from the bound record |
| `external_references` | at least 3 distinct vendor systems, evidence only (G-12) |
| `tags` | the five mirrors: interface-kind, consumer-class, interaction-pattern, sector, system-class |
| `service_binding` or `component_binding` | exactly one, with a resolvable target id and a binding status |
| `governance` | functional_owner, steward, approval_status, review_date, source_and_evidence |
| `metadata` | cr, created_by, created_date, notes |

## 2. The evidence bar

`governance.source_and_evidence` must contain, verbatim:

- `Metamodel clause:` citing `dea-metamodel schemas/entities/integration-interface.json` (IntegrationInterface, L5-integration, CR-021 D-4);
- `Admitting CR:` naming the CR that admitted the record;
- the vendor corroboration: at least 3 distinct vendor systems, each with its identifier, marked evidence only per G-12.

The vendor systems cited on an interface record are inherited from the bound
ISS or ISC record at derivation time. That is deliberate: an interface whose
contract nobody corroborates cannot borrow corroboration from a different
contract.

## 3. Prohibited content (D-4 / D-6)

A record must not carry endpoints, operations, schemas, protocol versions,
vendor product names in prose, or any API specification state. The API contract
artefact that specifies this boundary is a separate entity in the API
catalogue, related via `dea:specifies`. Vendor products appear only in
`external_references` and the evidence citation.

## 4. Derivation notes

The population records derive from the merged ISS main (623 records) by a
deterministic generator (G-10): one interface per service exposure, inheriting
the service's vendor corroboration, consumer class, interaction pattern and
sector and system-class context. The five legacy anchors referenced by the ISF
and ISC registries are admitted by the same CR with hand-authored records that
meet this standard. Every derivation is reproducible from the pinned ISS and
ISC snapshots committed under `docs/is-semantic-architecture/`.
