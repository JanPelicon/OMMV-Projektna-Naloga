# Effect of chroma subsampling on image quality

A python implementation that performs chroma subsampling for various chroma subsampling types (4:4:2, 4:4:1, 4:4:0, 4:2:2, 4:2:1, 4:2:0, 4:1:1, 4:1:0, 3:1:1).
We also provide an experimental method of adaptive chroma subsampling that determines the subsampling type depending on the standard deviation of an image region. 

# Vpliv podvzorčenja v krominančnem prostoru na kakovost zapisa slikovnega gradiva

Implementacija krominančnega podvzorčenja v pythonu za različne tipe podvzorčenja (4:4:2, 4:4:1, 4:4:0, 4:2:2, 4:2:1, 4:2:0, 4:1:1, 4:1:0, 3:1:1).
V repozitorij je zajeto tudi eksperimentalno adaptivno krominančno podvzorčenje, ki določi tip podvzorčenja glede na standardni odklon danega območja slike.

## Information about author and course 

Jan Pelicon
Mentor: Urban Burnik

A project for 
Multimedia Content Processing \ Obdelava Multimedijskih Vsebin (64M27)
Second-cycle interdisciplinary Master's study programme - Multimedia FRI/FE 2021

Presented at [ERK 2021](https://erk.fe.uni-lj.si/erk21.html).

## Run

```sh
python chroma_subsampling.py --help
python adaptive_chroma_subsampling.py --help
```

Examples:

```sh
python chroma_subsampling.py --average --ratios --show "4:4:2,4:2:0,3:1:1"
python adaptive_chroma_subsampling.py --average --ratios --show "4:2:0,3:1:1"
```
