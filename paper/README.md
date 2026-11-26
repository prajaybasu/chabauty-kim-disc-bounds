# A zero estimate for triangular logarithmic systems and residue discs in Chabauty–Kim loci

The manuscript is **main.tex**. Its four sections after the introduction are **zero.tex** (multiplicity and the lower bound), **discs.tex** (fixed-depth disc counts), **exceptional.tex** (depth-four and torsion certificates), and **discussion.tex** (rank, density and projective questions). Bibliographic records are in **references.bib**.

## Build the paper

In the repository, run the following from this directory with pdfLaTeX, BibTeX, GNU Make or BSD Make, and Python 3.

~~~sh
make
make archive
~~~

The PDF and source archive are written under **build/**. The archive includes the compiled bibliography **main.bbl**. After unpacking, run pdfLaTeX twice on **main.tex** to build with the supplied bibliography. If you edit the citations, run pdfLaTeX, BibTeX on **main**, then pdfLaTeX twice.

## Reproduce the mathematics

In the repository, the sibling directories **lean/** and **chabauty-kim/** hold the formal development and numerical evidence. In the source archive they are under **anc/**.

- From **lean/**, run **lake exe cache get** and **lake build**. The project pins its Lean and mathlib versions. The audit rejects dependencies on any axioms beyond propositional extensionality, choice and the quotient axiom.
- From **chabauty-kim/**, run the exhaustive screens below. They require SageMath 10.9 and FLINT 3. The independent integer lift check requires NumPy and gmpy2. Its expected output is **lifts.jsonl**.
- **python3 check_torsion.py** checks the four exceptional second digits at conductors three and four from the published searches.
- **mixed_rank.py --certify 1 2 3** checks the all-prime rank claims by exact integer minors and modular ranks. Run with **sage -python**.
- **genus_three_jacobian.py** reproduces the 45-prime table with **sage -python**. The program emits CSV on standard output. **genus_three_discs.py** gives a separate Coleman-integral computation. The expected table is **genus_three_discs.csv**.

For the two Wolstenholme primes, build the independent checker once and compare all four tables. For the base-three Wieferich prime, compare the canonical 16-row output as well.

~~~sh
work=$(mktemp -d)
cc -O2 -std=c11 check_screen.c -lflint -o "$work/check_screen"
sage -python certificate.py --digits 12 \
  --verify-screen "$work/check_screen" --lifts "$work/lifts.jsonl"
cmp lifts.jsonl "$work/lifts.jsonl"
for p in 16843 2124679; do
  "$work/check_screen" --tables-only "$p" "$work/field" &&
    sage -python wolstenholme.py "$p" --field-table "$work/field" || exit 1
done
~~~

The archive uses the standalone Lean library `ChabautyKimDiscs` and its pinned dependencies. The final paragraph of the manuscript identifies the formal statements, arithmetic certificates and cited analytic inputs for each part of the argument.
