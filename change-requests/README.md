# Change requests

Every change to this catalogue lands through a change request. One CR per PR, with deviations documented in the CRs themselves.

| CR | Scope | State |
|---|---|---|
| `CR-IS-CAT-04A` | Foundation: method, pointer, schema projection, CI. No records. | implemented |
| `CR-IS-CAT-04B` | Population: taxonomy, record standard, 627 records, registry, snapshots, gates 6-8 | implemented |

`CR-IS-CAT-04B` lands taxonomy, record standard, population and integration as one CR rather than four, deviating from the one-CR-per-PR convention. The deviation is documented in the CR's section 1.1: the gates only have meaning against a populated tree, and slicing into four PRs would keep main red between merges.

## Documents

- [CR-IS-CAT-04A: Integration Interface Catalogue Foundation](./CR-IS-CAT-04A-foundation.md)
- [CR-IS-CAT-04B: Integration Interface Catalogue Population](./CR-IS-CAT-04B-population.md)
