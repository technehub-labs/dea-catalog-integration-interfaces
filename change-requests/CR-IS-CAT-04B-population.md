# CR-IS-CAT-04B: Integration Interface Catalogue Population

| Field | Value |
|---|---|
| **CR** | CR-IS-CAT-04B |
| **Title** | IF catalogue population, taxonomy, record standard and cross-catalogue integration |
| **Status** | Implemented in this PR |
| **Layer** | Catalogue (Digital Profile) |
| **Programme** | Information Systems Semantic Architecture |
| **Parent CR** | `CR-IS-CAT-04A` (foundation) |
| **Repository** | `technehub-labs/dea-catalog-integration-interfaces` |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-11-11 |

## 1. Executive summary

This CR populates the Integration Interface catalogue with **627 records**: 622 derived deterministically from the merged ISS population (one interface per service exposure, inheriting the bound service's vendor corroboration and classification profile), 1 derived exposure that coincides with a legacy anchor (the API Gateway Service public interface), and 5 hand-authored legacy anchor records whose ids the ISF and ISC registries already reference. It ratifies the classification taxonomy, establishes the record standard, lands the relationship registry (627 `dea:exposes` edges), vendors the ISS and ISC target-id snapshots at pinned commits, and adds gates 6 through 8 to CI.

Every exposure the ISS catalogue forward-declared under this CR in its own `CR-IS-CAT-03E` resolves at merge. The ISF registry's `rel:identity-service-exposes-identity-api` and the ISC registry's `isc-rel-007`, `isc-rel-014`, `isc-rel-102` and `isc-rel-203` all resolve.

### 1.1 Deviation from one-CR-per-PR

The ISS wave (03B through 03E) landed as one PR with the deviation documented in each CR. This CR lands taxonomy, record standard, population and integration as **one CR** rather than four, for the same reason the sibling wave did: the gates only have meaning against a populated tree. A taxonomy gate on an empty catalogue proves nothing; a reference-integrity gate without records has nothing to check. Slicing this into four PRs would keep main red between merges because each intermediate state fails a gate. The deviation is documented here once rather than in four documents.

## 2. Scope

### In scope

1. `docs/TAXONOMY.md`: the three classification axes with closed vocabularies, the deterministic interface-kind mapping, and the classification-versus-identification statement (TAXONOMY 3).
2. `docs/RECORD-STANDARD.md`: the field-by-field record template and the evidence bar.
3. 627 records under `entities/v1-alpha/interfaces/<system-class>/<dashed-id>/interface.yaml`, with per-system `index.yaml` files.
4. `scripts/build_target_snapshots.py` and the vendored `docs/is-semantic-architecture/target-id-snapshots.yaml`: 623 ISS ids (with every service's `exposed_via`) at pinned commit `99ee85017e3b1ae9e77d2f471781791ff942b8c2`; 276 ISC ids at pinned commit `1530a667a9eace490fa3344d9afa32fabfb93e64`.
5. Relationship registry `relationships/v1-alpha/relationships.yaml`: 627 `dea:exposes` edges, one per record.
6. Gates 6 through 8 and the CI extension to eight steps.
7. Pointer `catalog.status`: scaffold to populated; README and CHANGELOG updates.

### Out of scope

1. **Any API record or `dea:specifies` edge.** The API catalogue programme owns them.
2. **Any change to the ISS or ISC catalogues.** Their forward declarations are resolved by this catalogue admitting the targets; their snapshots stay pinned where they are until their own CRs advance them.
3. **The repository rename.** Org-level, recorded as pending.
4. **The metamodel `catalog_repo` contradiction.** Recorded in `CR-IS-CAT-04A` section 3.1; a metamodel-side correction remains outstanding.

## 3. Derivation method (G-10)

The population is derived deterministically from the merged ISS main, reproducible from the vendored snapshot:

1. Every ISS service record carries exactly one `exposed_via` id. Each becomes an IF record with the id the ISS record already declared, so the ISS forward declarations resolve without any ISS-side change.
2. Each derived record inherits from the bound service: the 3 vendor corroborations in `external_references`, the `consumer_class`, the `interaction_pattern`, and the `sector` and `system-class` context tags. The `interface_kind` is derived from the interaction pattern by the mapping ratified in TAXONOMY section 2.
3. Each derived record binds back via `service_binding` to the ISS record it was derived from, `binding_status: bound`.
4. Five legacy anchors are admitted by hand-authored records meeting the same standard: `dea:integration-interface-identity-api` (bound to the identity service; referenced by the ISF registry under `CR-IS-CAT-01D`), `dea:integration-interface-api-gateway-public` (bound to the API Gateway Service; referenced by `isc-rel-007` and by the ISS record's own exposure, replacing the derived record that would otherwise carry this id), and three component-bound interfaces referenced by the ISC registry: `dea:integration-interface-identity-broker-public` (`isc-rel-014`), `dea:integration-interface-employee-portal-internal` (`isc-rel-102`), `dea:integration-interface-agent-orchestrator-internal` (`isc-rel-203`).

Identity note: `dea:integration-interface-identity-api` is a **second** interface for the identity service, whose generated exposure `dea:integration-interface-identity-service` also exists. Both are legal: a service may be exposed through more than one boundary, and the ISF registry's reference is to the API boundary specifically.

### 3.1 Coverage

623 ISS services declare 623 exposures; 623 IF records carry them (622 derived plus the api-gateway-public anchor). The five anchors bring the total to 627. Gate 8 asserts the coverage in both directions: every ISS-declared exposure has an IF record binding back to the declaring service, and every binding resolves against the snapshot.

### 3.2 Kind distribution

rest-api 406, file-transfer 157, message-topic 36, event-stream 27, rpc 1 (the agent-orchestrator internal interface, asserted directly with vendor corroboration). The distribution follows the ISS interaction-pattern distribution by construction; it is reported here for the record, not as a target.

## 4. Gates landed

| Gate | Script | Catches |
|---|---|---|
| Taxonomy | `scripts/check_record_taxonomy.py` | Multi-cell axes, tag/field disagreement, both or neither binding, duplicate records sharing system class, binding and three-tuple |
| Evidence | `scripts/check_record_evidence.py` | Missing metamodel clause, admitting CR, fewer than 3 distinct vendor systems, thin descriptions, missing bindings |
| Reference integrity | `scripts/check_reference_integrity.py` | Bindings that do not resolve against the vendored snapshots, missing anchors, ISS exposures without IF records, bindings that contradict the declaring service |

## 5. Snapshot policy (D4)

The ISS snapshot is vendored at `99ee85017e3b1ae9e77d2f471781791ff942b8c2` (the merge commit of the ISS population wave) and the ISC snapshot at `1530a667a9eace490fa3344d9afa32fabfb93e64`, both re-verified live at slice time. Gate 8 never fetches: CI reads the vendored YAML. Advancing a pin is a CR in this repository, not a run-time act.

## 6. Outstanding items

| Item | Owner | Severity |
|---|---|---|
| API catalogue pending; `dea:specifies` edges will relate API records to IF records | API catalogue programme | low |
| `dea-metamodel` `dea:IntegrationInterface.catalog_repo` contradiction | metamodel CR | medium |
| Repository rename to the allocated name | org admin transfer | low |
| ISS and ISC forward-declaration registers still describe this catalogue as empty; their CRs should be advanced to record resolution at their next population wave | sibling catalogue CRs | low |

## 7. Verification

| Check | Result |
|---|---|
| Gate 1 parse | 0 failures across the tree |
| Gate 2 pointer | 0 findings |
| Gate 3 schema projection | 627 records validated, 0 findings |
| Gate 4 writing rules | 0 findings |
| Gate 5 record posture | 627 canonical ids, population gates present |
| Gate 6 taxonomy | 627 records, one cell per axis, one binding each, 0 findings |
| Gate 7 evidence | 627 records with clause, CR, corroboration and description, 0 findings |
| Gate 8 reference integrity | 627 service bindings resolved, 3 component bindings resolved, 6 anchors present, 0 coverage findings |
| Registry | 627 `dea:exposes` edges, one per record |
| Records admitted | 627 (623 resolving ISS exposures, 5 legacy anchors, 1 overlap: api-gateway-public is both) |

## 8. What this CR deliberately does not do

1. Admit any API record or `dea:specifies` edge.
2. Change any ISS or ISC record or registry.
3. Advance any sibling snapshot pin.
4. Rename the repository.
5. Correct the metamodel contradiction.

## 9. References

- `CR-IS-CAT-04A`: this catalogue's foundation CR
- `dea-catalog-information-system-services` `CR-IS-CAT-03D`/`03E`: the ISS population whose exposures this CR resolves, and the forward-declaration policy it follows
- `dea-catalog-system-functions` `CR-IS-CAT-01D`: the ISF registry reference resolved by the identity-api anchor
- `dea-catalog-application-components` CR-IS-CAT-02D: the ISC registry references resolved by the four component anchors
- `dea-metamodel` `CR-021`: the D-4 disposition this catalogue enforces
