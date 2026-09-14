# ECDSA

Seminar project on the Elliptic Curve Digital Signature Algorithm: the written report and a small Python demo.

## Report

LaTeX sources live in `report/`. A compiled copy is at `report/report.pdf`.

```bash
cd report
pdflatex report.tex
bibtex report
pdflatex report.tex
pdflatex report.tex
```

## Demo

Python ECDSA implementation, a signed chat between Alice and Bob, and a Pollard's Rho example.

```bash
python start.py
```

On Windows this opens Alice, Bob, and a live log window.

```bash
python pollards_rho.py
```

## Plots

Scripts for the report figures. Needs `matplotlib` and `numpy`.

```bash
python plot1.py   # group operation points
python plot2.py   # points mapped onto a torus
```
