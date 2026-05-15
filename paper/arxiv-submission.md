# arxiv submission package

Submission metadata and procedural notes for the Draft 5 preprint.

---

## Files for upload

**Primary:** `paper/paper-draft-v5.pdf` (760 KB).

arxiv accepts PDF-only submissions for non-physics categories. The markdown source (`paper/paper-draft-v5.md`) is in the repository for reference, and a future revision could be re-rendered to LaTeX if a journal submission requires `.tex` source.

## Title

> Concept-Conditional Cross-Tradition Binding in Semantic Embedding Space: A Method and an Application to Mysticism

## Author

**Single author: T. David Kinlaw**
- Affiliation: Independent Researcher / Redbird Software LLC
- Contact: david@redbirdsoftwarellc.com

## Abstract (for the arxiv form)

The arxiv form has a ~1920-character limit for the abstract. Use a tightened version of the §Abstract from the PDF, omitting the parenthetical implementation details (cross-model, cross-granularity) that read better in the full paper than in a metadata field. Suggested form below — adjust to taste before submission:

```
We introduce concept-conditional cross-tradition binding (CCB), a bias-aware
embedding-based statistic for testing whether textual passages from
unconnected source traditions are more similar when conditioned on shared
structural concepts than when not. We stress-test the method on the 65-year-
old cross-cultural mysticism convergence debate (Stace, 1960; Katz, 1978;
Forman, 1990; Hood, 1975), whose central question is textual in form yet
has resisted direct textual empirical test for six decades. Across two
corpora (a 143-passage curated paraphrase-heavy set and a 920-chunk
verified-translation whole-book set), five of seven pre-registered
structural concepts (AWARENESS, RECOGNITION, WORLD, ULTIMATE, SUBSTRATE)
show statistically significant cross-tradition binding at p ≤ 0.0015,
replicated across proprietary (OpenAI text-embedding-3-large) and
open-source (MiniLM-L6-v2 via ONNX Runtime) embedding models, at passage
and sentence granularities. A pre-registered technical-only-tagger
experiment refines the §6.8 vocabulary-breadth mechanism into two
distinct components (casual-usage noise floor + coverage-distribution
asymmetry) and recovers the strongest cross-tradition concept-binding
result: Advaita Vedanta × Theravada Buddhism at cosine 0.531 on the
RECOGNITION concept under technical-only liberation vocabulary, with
no historical contact between the traditions and neither writing
toward the comparison. We do not claim the perennialist position is
correct or the constructivist critique refuted; we claim a class of
evidence both sides of the debate have to engage with on the merits
is now produceable. Translator-as-confound, regex-tagging bias,
adversarial passage selection, and non-English source analysis remain
unaddressed; the paper names them prominently and lists what a fuller
application of CCB to this debate would require. Code, corpora, and
results released MIT.
```

(Character count: approximately 1850. arxiv counts whitespace; check the form.)

## arxiv categories

**Primary recommendation:** `cs.CL` (Computation and Language)

The paper's contribution is an NLP statistic; cs.CL is the closest fit. The application is the mysticism convergence debate, which doesn't have a natural arxiv home (no `philosophy.relig` or similar).

**Cross-list (secondary) recommendations:**

- `cs.IR` (Information Retrieval) — embeddings + similarity-search-adjacent methodology
- `stat.AP` (Statistics — Applications) — permutation testing on a substantive domain
- Optionally `cs.AI` (Artificial Intelligence) — broader visibility

Adding all three cross-lists is reasonable for a methodology paper of this scope.

## License declaration

**For the PDF:** Use arxiv's CC-BY 4.0 ("non-exclusive distribution license to arXiv plus CC-BY"). This permits reuse with attribution and is standard for methodology preprints.

**For code/data (separate from the arxiv license):** MIT, declared in the repository LICENSE file.

## Endorsement requirement

**This is the practical blocker.** arxiv requires endorsement for first submissions to cs.* categories. The endorsement system:

- A current arxiv author in cs.CL (or the relevant category) with sufficient submission history can endorse you via a one-time endorsement code.
- You request an endorsement code via the arxiv "Need endorsement?" link after registering: https://arxiv.org/auth/need-endorsement
- The endorser does not need to be a co-author or read the paper — they need to vouch that you are a real researcher whose work is suitable for the category.

Paths to obtain endorsement for cs.CL:

1. **Existing arxiv-author contacts.** If you've coauthored with anyone who has cs.CL submissions, that's the cheapest path.
2. **Reach out to one of the consulted-expert prospects.** Hemal Trivedi (Georgetown) likely has co-authored submissions in psychology-of-religion-adjacent venues; check his arxiv profile for cs.CL or related submissions. Zhuo Job Chen (UNC Charlotte) is more on the psychometric side; less likely to have arxiv. Michiel van Elk (Leiden) is a likelier endorser given his neuroimaging/computational work. **Frame the endorsement request as a small favor separate from co-authorship**: "I am submitting this preprint solo and need a cs.CL endorsement code; would you mind providing one if you've submitted to that category? No co-authorship implied; this is procedural."
3. **arxiv institutional auto-endorsement.** If the author has access to an academic affiliation email (alumni? collaborator at GT?), institutional email can sometimes auto-endorse. Unlikely available for an Independent Researcher account.

If endorsement is genuinely blocking, the practical fallback is to publish a citable preprint elsewhere first and obtain endorsement in parallel:

- **OSF Preprints** (https://osf.io/preprints) — no endorsement, instant DOI, citable. PsyArXiv (the psychology-of-religion subset of OSF Preprints) is methodologically permissive for cross-disciplinary methodology papers.
- **SSRN** — no endorsement, fast turnaround, citable.
- **Zenodo** — no endorsement, archival, citable, integrates with GitHub for code-and-paper bundles.

Recommended order if endorsement is not immediately available:

1. Upload Draft 5 PDF + code-and-data DOI to **Zenodo** for an immediate citable artifact tied to a GitHub release.
2. Submit to **OSF Preprints** for community visibility.
3. Pursue arxiv endorsement in parallel; submit to arxiv when ready.

A Zenodo release also enables `pip install`-style citation badges in the repository README, which arxiv readers will look for.

## Suggested timeline

- Day 0 (today): Tag a Zenodo release of the public repo at commit `<commit-sha>`. Get a DOI immediately.
- Day 0–7: Request arxiv endorsement from one or two appropriate contacts (see above).
- Day 7–14: Submit to OSF Preprints (no endorsement) for parallel visibility.
- Day 14+ (when endorsed): Submit to arxiv. arxiv submission takes a few business days to appear.

The Zenodo + OSF combination gives citable preprint status immediately; arxiv is for prestige and discoverability and can land after.

## Pre-submission checklist

- [ ] Author full name and affiliation correct on form
- [ ] Abstract under 1920 characters (check after final edits)
- [ ] Categories selected (cs.CL primary, plus cs.IR and stat.AP cross-lists)
- [ ] License: CC-BY 4.0 for arxiv distribution
- [ ] PDF readable on arxiv preview (test before final submit)
- [ ] Repository URL in §11 of the PDF matches the public repo (✓ — added in Draft 5)
- [ ] All references resolved; no dangling [TODO] or [author] placeholders
- [ ] Contact email correct
- [ ] Endorsement code obtained (or alternative venue selected)

## Submission notes

- arxiv allows revisions (replace submissions) without re-endorsement. Draft 6 with multi-translator results, when ready, can replace Draft 5 on the same arxiv ID.
- arxiv assigns an arxiv ID (e.g., `2605.XXXXX` format) and a DOI. Cite the paper as the arxiv ID once live.
- Submit weekdays during US business hours for fastest moderation review.

## After submission

- Update the repository README with the arxiv ID and link
- Update `paper/paper-draft-v5.md` §11 to reference the arxiv version alongside the GitHub repo
- Consider posting to relevant communities (HackerNews, /r/MachineLearning, /r/PhilosophyOfReligion, contemplative-NLP Discord/Slack channels if any) — methodologically novel cross-disciplinary preprints do well in those channels
- Add the arxiv ID to your project page / personal website if applicable
