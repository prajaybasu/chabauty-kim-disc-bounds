TEX = pdflatex -interaction=nonstopmode -halt-on-error
SECTIONS = main.tex zero.tex discs.tex exceptional.tex discussion.tex

.PHONY: all archive
all: build/main.pdf

build/main.pdf: $(SECTIONS) references.bib Makefile
	mkdir -p build
	$(TEX) -output-directory=build main.tex
	cd build && BIBINPUTS=..: bibtex main
	$(TEX) -output-directory=build main.tex
	$(TEX) -output-directory=build main.tex

archive: build/main.pdf
	python3 pack.py
