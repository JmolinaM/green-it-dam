# tfm-docs — Memoria del TFM en LaTeX

Documento LaTeX de la memoria del TFM **"Integración transversal de la sostenibilidad digital: prácticas de laboratorio en Informática"**.

## Estructura prevista

```
tfm-docs/
├── main.tex              # documento raíz
├── portada.tex           # portada URJC
├── secciones/
│   ├── 01-intro.tex
│   ├── 02-marco-teorico.tex
│   ├── 03-curriculo.tex
│   ├── 04-propuesta.tex
│   ├── 05-evaluacion.tex
│   └── 06-conclusiones.tex
├── bibliografia.bib      # referencias BibTeX
├── figuras/              # imágenes y diagramas
└── anexos/
    ├── anexo-a.tex       # Ficha C huella digital
    ├── anexo-b.tex       # Materiales Jigsaw P0
    └── anexo-c.tex       # Guiones de prácticas P1–P4
```

## Compilación

```
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

O con latexmk:

```
latexmk -pdf main.tex
```

## Estado

Pendiente de conversión desde Markdown (`../TFM/secciones/`).
