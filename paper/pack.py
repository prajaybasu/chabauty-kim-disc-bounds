"""Package the paper and its certificate inputs for distribution."""

from pathlib import Path
from shutil import copy2
from tempfile import TemporaryDirectory
import tarfile

paper = Path(__file__).resolve().parent
repo = paper.parent
archive = paper / "build" / "finite-polylogarithms-source.tar.gz"

with TemporaryDirectory() as tmp:
    stage = Path(tmp)
    for path in (*paper.glob("*.tex"), paper / "references.bib", paper / "build/main.bbl"):
        copy2(path, stage / path.name)

    ancillary = stage / "anc"
    evidence = ancillary / "chabauty-kim"
    evidence.mkdir(parents=True)
    copy2(paper / "README.md", ancillary)
    for name in ("certificate.py", "check_screen.c", "check_lifts.py", "check_torsion.py", "lifts.jsonl",
                 "wolstenholme.py", "family_budget.py", "mixed_rank.py",
                 "genus_three_jacobian.py", "genus_three_discs.py", "genus_three_discs.csv"):
        copy2(repo / "chabauty-kim" / name, evidence)

    lean = repo / "lean"
    package = ancillary / "lean"
    modules = package / "ChabautyKimDiscs"
    modules.mkdir(parents=True)
    for name in ("lakefile.toml", "lake-manifest.json", "lean-toolchain",
                 "ChabautyKimDiscs.lean", "AuditAxioms.lean"):
        copy2(lean / name, package)
    for module in (lean / "ChabautyKimDiscs").glob("*.lean"):
        copy2(module, modules)

    with tarfile.open(archive, "w:gz", format=tarfile.USTAR_FORMAT) as tar:
        for path in sorted(stage.rglob("*")):
            if path.is_file():
                info = tar.gettarinfo(str(path), arcname=str(path.relative_to(stage)))
                info.uid = info.gid = 0
                info.uname = info.gname = ""
                with path.open("rb") as stream:
                    tar.addfile(info, stream)
print(archive.name)
