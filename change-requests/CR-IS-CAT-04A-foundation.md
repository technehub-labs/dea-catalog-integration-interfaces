# CR-IS-CAT-04A: Integration Interface Catalogue Foundation

| Field | Value |
|---|---|
| **CR** | CR-IS-CAT-04A |
| **Title** | Integration Interface catalogue foundation (methodology-first bring-up) |
| **Status** | Implemented in this PR |
| **Layer** | Catalogue (Digital Profile) |
| **Programme** | Information Systems Semantic Architecture |
| **Parent CR** | `dea-metamodel` `CR-021` (IntegrationInterface entity introduction, D-4 disposition) |
| **Repository** | `technehub-labs/dea-catalog-integration-interfaces` |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-11-11 |

## 1. Executive summary

This CR establishes the Integration Interface catalogue as a **method**, not as content. It lands the pointer, the schema projection, the classification axes, the admission criteria, the cross-catalogue reference policy, and five CI gates. It admits **no records**.

It follows the methodology-first rule established for the sibling catalogues: the first increment of a catalogue establishes admission criteria, the evidence process, and the framework-overlay rules. Records come later, gated on the population CR.

## 2. Scope

### In scope

1. `metamodel-pointer.yaml` pinned to OpenDEAM v0.7.0, with the repository rename debt recorded as pending.
2. `schemas/integration-interface.schema.json`, a projection of the metamodel entity schema with the catalogue-instance layer added (classification axes, bindings, governance).
3. `docs/FOUNDATIONS.md`: cardinal scope, exclusions, three classification axes, six admission criteria, the cross-catalogue reference policy, the repository reality reconciliation, and a nine-entry decision-points register.
4. `README.md`: catalogue boundary table, entity definition, five key tenets, relationship inventory, cross-catalogue reference table, change-control matrix.
5. Five CI gates (`scripts/check_*.py`) wired into `.github/workflows/validate-catalogue.yml`.
6. `.gitignore`, landed before any Python exists in the repository.

### Out of scope

1. **Any IF record.** Population is `CR-IS-CAT-04B`.
2. **The classification vocabularies in full.** Declared as direction in FOUNDATIONS section 3, ratified in `CR-IS-CAT-04B`.
3. **The per-record documentation template.** That is `CR-IS-CAT-04B`.
4. **The `entities/` and `relationships/` directories.** Declared in the README structure block, marked as not built, arriving with the population CR.
5. **Resolution of the sibling forward references.** The ISS population forward-declares 623 exposures to this catalogue; the ISF registry forward-declares `dea:integration-interface-identity-api`; the ISC registry forward-declares four component exposures. All remain correctly declared in their own repositories until `CR-IS-CAT-04B` admits the records.
6. **The API catalogue and the `dea:specifies` edges.** Owned by the API catalogue programme.
7. **The repository rename** to `dea-catalog-information-system-integration-interfaces`. Org-level; recorded as pending in the pointer and in FOUNDATIONS section 5.

## 3. Audit findings

The repository was confirmed empty against the GitHub API: no default branch, no commits, no files. Bring-up therefore started from nothing.

Two findings from the audit shaped this CR.

### 3.1 The metamodel carries an internal contradiction on IF catalog ownership

`dea-metamodel/metamodel/dea-metamodel.yaml` entity `dea:IntegrationInterface` declares:

```yaml
catalog_repo: dea-catalog-api-contracts
```

while the `definition` field of the same entity states:

> Catalog ownership: the dea-catalog-information-system-integration-interfaces repository (new per CR-IS-CAT-04).

This mirrors the contradiction the ISS foundation CR recorded in its section 3.1: an allocation field and a definition field of the same authoritative record disagree. The `catalog_repo: dea-catalog-api-contracts` value predates the CR-021 D-4 separation that split the API contract artefact from the interaction boundary.

**Disposition in this CR: the pointer records `dea-catalog-integration-interfaces` (the actual repository), following the definition field's intent.** The correction is recorded, not silently resolved: a catalogue-side CR cannot correct a metamodel-side field, and doing so here would create a second source of truth for allocation. It is registered as an outstanding item in section 6.

### 3.2 The repository does not carry its allocated name

The OpenDEAM root model allocates `dea-catalog-information-system-integration-interfaces`; the repository is `dea-catalog-integration-interfaces`. Verified against the GitHub API.

**Disposition in this CR: the rename is recorded as pending in the pointer, with the target named.** Reference resolution is by identifier, not by repository name, so the rename debt blocks nothing. It is recorded in `docs/FOUNDATIONS.md` section 5 so a reader does not have to rediscover the gap.

## 4. The method this CR establishes

### 4.1 Cardinal scope: the boundary test

> Can the same interaction boundary be operationalised by two materially different vendor implementations?
>
> **Yes** -> this is an integration interface. Record it here.
> **No** -> it is an implementation detail, not a boundary; it belongs in no catalogue record.

The CR-021 D-4 disposition does the boundary drawing: the interface is the interaction boundary; the service contract (ISS) is what is exchanged; the API contract artefact is the specification of the boundary and belongs to the API catalogue, related back through `dea:specifies`.

### 4.2 Three classification axes

Interface kind, consumer class, interaction pattern. Declared in FOUNDATIONS section 3; the vocabularies are ratified in `CR-IS-CAT-04B`. The contract-maturity axis of the ISS taxonomy has no interface analogue; the binding state carries the equivalent information.

### 4.3 Six admission criteria

Boundary test passes; exactly one binding; evidence citable; identifier canonical; lifecycle declared; derivation deterministic. Stated in full in `docs/FOUNDATIONS.md` section 4.

### 4.4 Cross-catalogue reference policy

Every binding resolves against a pinned snapshot. Because ISS and ISC are both populated at this CR's date, this catalogue admits **no forward declarations inbound**: every binding must resolve, which is a stronger position than the sibling catalogues needed at their foundations, and the reference-integrity gate encodes it as a hard failure with bidirectional coverage assertions.

## 5. Decision-points register

Nine decisions are recorded in `docs/FOUNDATIONS.md` section 7 as D1 through D9. Later CRs cite them by number rather than re-deriving them. D1 (boundary test), D2 (one binding per record), D3 (contract ownership), D4 (snapshot resolution), D5 (no inbound forward declarations), D6 (API separation), D7 (rename debt recorded), D8 (registry not inline), D9 (legacy anchors admitted).

## 6. Outstanding items this CR does not resolve

| Item | Owner | Severity |
|---|---|---|
| `dea-metamodel` `dea:IntegrationInterface.catalog_repo` contradicts its own `definition` on catalogue ownership | metamodel CR | medium |
| ISF, ISC and IF repositories remain mid-rename against their allocation | org admin transfer | medium |
| The ISS, ISF and ISC forward references await the IF population | `CR-IS-CAT-04B` | low, correctly gated |
| The API catalogue and its `dea:specifies` edges remain pending | API catalogue programme | low |

## 7. Gates landed

| Gate | Script | Catches |
|---|---|---|
| Parse | `scripts/check_parse.py` | Malformed YAML or JSON anywhere in the tree, not only under `entities/` |
| Pointer | `scripts/check_pointer.py` | Pointer missing required fields, or drifted from its allocation |
| Schema projection | `scripts/check_schema_projection.py` | Normative field dropped, `type` const changed, lifecycle enum drifted from the metamodel vocabulary |
| Writing rules | `scripts/check_writing_rules.py` | D-004 forbidden glyphs and D-005 triple semicolon |
| Record posture | `scripts/check_record_posture.py` | Records appearing without the population gates, or a scaffold catalogue that claims to be populated |

`CR-IS-CAT-04B` adds the taxonomy, evidence and reference-integrity gates and extends CI to eight steps.

## 8. Verification

| Check | Result |
|---|---|
| Gate 1 parse | 0 failures across the tree |
| Gate 2 pointer | 0 findings |
| Gate 3 schema projection | 0 findings |
| Gate 4 writing rules | 0 findings |
| Gate 5 record posture | 0 findings, catalogue correctly marked scaffold |
| `metamodel-pointer.yaml` against OpenDEAM v0.7.0 | class alias `IFI`, entity id, layer L5, building block L5-integration, repository all verified |
| Schema against metamodel | 9 normative fields mirrored, lifecycle enum matches the metamodel vocabulary |
| D-004 / D-005 | clean |
| Records admitted | 0, as intended |

## 9. What this CR deliberately does not do

1. Admit a record.
2. Ratify the classification vocabularies (`CR-IS-CAT-04B`).
3. Define the per-record documentation template (`CR-IS-CAT-04B`).
4. Resolve the sibling forward references.
5. Correct the metamodel's catalog-ownership contradiction.
6. Create the `entities/` or `relationships/` directories.
7. Rename the repository.

## 10. References

- `dea-metamodel` `schemas/entities/integration-interface.json`: normative entity schema
- `dea-metamodel` `change-requests/CR-021-integration-interface.md`: entity introduction, D-4 disposition, `dea:specifies`
- `dea-metamodel` `change-requests/CR-017-information-systems-domain-semantic-integration.md`: parent programme
- `dea-metamodel` `change-requests/CR-020-information-system-service.md`: the service contract an interface operationalises
- `dea-architecture-framework` `model/opendeam-model.yaml`: allocation of IF to this repository
- `dea-catalog-information-system-services` CR-IS-CAT-03A/03E: the foundation and forward-declaration precedent this CR follows, and the 623 exposures awaiting `CR-IS-CAT-04B`
- `dea-catalog-application-components` CR-IS-CAT-02F: forward-reference verification, the policy this CR adopts
