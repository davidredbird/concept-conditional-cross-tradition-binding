# The General Methodology

This project is structured around a *specific* convergent concept — nondualism — because it has the sharpest qualitative articulation in the comparative-mysticism literature and the longest-running unresolved debate (Stace, 1960; Katz, 1978). The methodology itself is fully general; the artifact is reusable on any claimed convergent concept.

## The pattern

For any concept C that has been claimed to appear convergently across traditions, disciplines, or methodologies, the experiment shape is:

1. **Specify C** with neutral operational features (the "what counts as expressing C" criteria).
2. **Assemble a corpus** of texts that arguably express C across the broadest plausible set of sources (different cultures, methodologies, historical eras, disciplines). Add controls: texts from the same sources that explicitly *don't* express C, and texts from unrelated discourse.
3. **Embed** with multiple modern semantic models.
4. **Test for cross-source clustering** beyond what's explained by translator style, vocabulary, era, or genre.
5. **Discover or pre-register interpretable axes** that characterize the convergent structure if it exists.
6. **Produce a translation table** mapping the structural features to their expression in each source tradition.
7. **Report** what survives controls (validated convergence) and what doesn't (refuted or method-specific).

The first run, currently in progress, instantiates this pattern with C = "nondualism."

## Concepts worth running the same experiment on

Each of these has been claimed to recur across traditions. Each one would make a distinct experiment with its own corpus.

### Ethical / behavioral

- **The Golden Rule.** Versions appear in Christianity, Judaism, Confucianism, Buddhism, Islam, Jainism, Hinduism, ancient Greek ethics. Convergence is famously claimed; rigor of the convergence has not been tested computationally.
- **Compassion / universal love.** Buddhist *karuna*, Christian *agape*, Sufi *muhabba*, Confucian *ren*. Worth testing whether these are really the same thing or merely translated similarly.
- **Non-attachment / detachment.** Buddhist *anupadana*, Stoic *apatheia*, Christian renunciation, Sufi *zuhd*, Daoist *wu wei*.

### Cosmological / metaphysical

- **Cyclical vs. linear time.** Hindu yugas, Greek cycles, biblical eschatology, modern cosmology (cyclic universes).
- **Triadic / threefold structure.** Christian Trinity, Hindu Trimurti, Daoist Three Treasures, Hegelian dialectic, Freudian id/ego/superego. Is this a real pattern or pareidolia?
- **The Great Chain of Being / hierarchical reality.** Neoplatonic emanation, Hindu lokas, medieval scholastic hierarchy, Kabbalistic sefirot, modern emergence theories.
- **Eternal recurrence / return.** Stoic, Hindu, Nietzschean, certain modern cosmologies.

### Anthropological / psychological

- **The Hero's Journey / initiatic structure.** Campbell's universal monomyth. Often asserted; tested mostly in literary terms. A computational test of the structural convergence across cultures would be a real contribution.
- **Mystical death and rebirth.** Initiation rituals across cultures, baptism, shamanic dismemberment, kundalini, psychedelic ego death.
- **The three stages / paths.** Purgative / illuminative / unitive in Christian mysticism; Theravada path stages; tantric stages; Sufi *maqamat*.

### Epistemic / methodological

- **The ineffability of the ultimate.** Apophatic theology, *neti neti*, the unspeakable Tao, Wittgenstein's mystical, the limits of language in formal systems (Gödel). Modern thinkers explicitly converging with ancient ones.
- **The dependence of perception on the perceiver.** Predictive processing, idealism, Kantian categories, Buddhist *paticca samuppada*, observer-dependence in QM.
- **The role of attention in shaping reality.** Iain McGilchrist territory; Buddhist *sati*; Christian *attentio*; phenomenological *epoché*.

### Eschatological / soteriological

- **Universal restoration / apocatastasis.** Origen, certain strands of Sufism, Hindu *moksha* for all, secular utopian arcs. Worth testing.
- **The fall and return structure.** Plotinus, Christian fall/redemption, Hindu/Gnostic emanation-and-return, Hegelian alienation-and-overcoming.

### Aesthetic / experiential

- **The sublime / numinous.** Otto's *mysterium tremendum*, Burke's sublime, Kantian sublime, Hindu *rasa*, Japanese *yugen*.
- **The recognition of beauty as recognition of truth.** Platonic, Christian medieval, Hindu, certain modern physics aesthetics (Dirac, Penrose).

## Designing the artifact for reuse

The scripts in this repo are currently parameterized by a single corpus and a fixed analysis pipeline. For the methodology to be a reusable framework, they should evolve toward:

1. **Corpus-as-config.** A corpus is just a JSONL with a known schema; the script takes `--corpus path` and runs the same pipeline regardless of subject matter.
2. **Per-concept pre-registered features.** Each concept gets its own glossary file with operational definitions. The same SAE/contrastive analysis pipeline reads the features and validates them.
3. **Stable output shape.** Every run produces the same shape of artifact: a tradition-similarity matrix, a feature-validation table, statistical tests against H0, visualizations. This makes results comparable across experiments.
4. **A meta-table.** Across multiple runs, we accumulate: for each tested concept, was convergence detected? With what controls? What survived? This *meta-table* is the thing that would actually move the perennialism debate forward — not "look, nondualism converges" but "we tested 12 candidate convergent concepts under uniform methodology; here are the 4 that survived rigorous controls and the 8 that didn't."

The current pipeline is already concept-agnostic at the code level — `category_pair_stats`, `cluster_and_score`, `tradition_similarity_matrix` all operate on the data, not the topic. The corpus and glossary are where concept-specific content lives. A v2 of the methodology would formalize this separation more explicitly and provide tooling for building new corpora quickly.

## What this means for the current run

Nothing changes about Experiment 1 in flight. It's the first instantiation of the general methodology. The deliverable is:

- A validated (or refuted) convergence finding for nondualism specifically.
- A methodological proof-of-concept demonstrating that the general framework works.
- An open framework that anyone (including future-you, or other researchers) can pick up to run convergence tests on Golden Rule, Hero's Journey, the sublime, or any other candidate concept.

That third item is potentially the largest contribution. A single convergence finding is a paper; a reusable framework for testing convergence claims is an infrastructure that could outlive the original paper.
