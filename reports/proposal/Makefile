TEXSRC = $(wildcard ./*.tex)

proposal: proposal.pdf

all: proposal.pdf

pdf: proposal.pdf

proposal.pdf: biblio.bib $(TEXSRC)
	pdflatex proposal
	bibtex proposal
	pdflatex proposal
	pdflatex proposal

clean: 
	\rm -f *.dvi *.aux *.ps *~ *.log *.blg *.bbl *.fls *.fdb_latexmk *.synctex.gz *.out
