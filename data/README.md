# 📦 Datasets — 2D Bin Packing Problem

Este diretório contém as instâncias utilizadas para experimentos no trabalho de **Otimização Combinatória**, com foco no **problema clássico de empacotamento bidimensional (2D Bin Packing Problem)**.

---

# 📚 Referências e Descrição dos Datasets

Este documento descreve as coleções de instâncias utilizadas no trabalho, com base no repositório [OR-Datasets (Oscar Oliveira)](https://github.com/Oscar-Oliveira/OR-Datasets).  
Inclui informações sobre origem, tipo de problema, tamanho das instâncias e referências bibliográficas.

---

## 🧾 Tabela resumo das coleções

| Dataset | Tipo | Fonte original |
|----------|------|----------------|
| **BENG** | 2D Bin Packing clássico | Bengtsson (1982) |
| **CLASS** | 2D Finite Bin Packing | Berkey & Wang (1987); Martello & Vigo (1998) |
| **HOPPER** | 2D Bin Packing | Hopper (2000) |
| **HT2001a** | 2D Bin Packing | Hopper & Turton (2001) |
| **JAKOBS** | 2D Bin Packing (retangular) | Jakobs (1996) |
| **MB2D** | 2D Bin Packing | Mack & Bortfeldt (2012) |

---

## 📁 Descrição das pastas

### 🟩 BENG — Bengtsson (1982)
- **Local:** [`/data/BENG`](https://github.com/Oscar-Oliveira/OR-Datasets/tree/master/Cutting-and-Packing/2D/BENG)
- **Referência:**  
  Bengtsson, B.E.E. (1982). *Packing Rectangular Pieces — A Heuristic Approach*. *The Computer Journal*, 25(3), 353–357.  
  [PackLib² entry](https://www.ibr.cs.tu-bs.de/alg/packlib/article/b-prpha-82.shtml)

---

### 🟩 CLASS — Berkey & Wang (1987); Martello & Vigo (1998)
- **Local:** [`/data/CLASS`](https://github.com/Oscar-Oliveira/OR-Datasets/tree/master/Cutting-and-Packing/2D/CLASS)
- **Referências:**  
  - Berkey, J.O.; Wang, P.Y. (1987). *Two-Dimensional Finite Bin-Packing Algorithms*. *Journal of the Operational Research Society*, 38(5), 423–429.  
  - Martello, S.; Vigo, D. (1998). *Exact Solution of the Two-Dimensional Finite Bin Packing Problem*. *Management Science*, 44(3), 388–399.  

---

### 🟩 HOPPER — Hopper (2000)
- **Local:** [`/data/HOPPER`](https://github.com/Oscar-Oliveira/OR-Datasets/tree/master/Cutting-and-Packing/2D/HOPPER).  
- **Referência:**  
  Hopper, E. (2000). *Two-Dimensional Packing Utilising Evolutionary Algorithms and Other Meta-Heuristic Approaches*. PhD Thesis, Cardiff University.  
  [Link institucional (Cardiff)](https://orca.cardiff.ac.uk/id/eprint/55690/)

---

### 🟩 HT2001a — Hopper & Turton (2001)
- **Local:**  
  - [`/data/HT2001a`](https://github.com/Oscar-Oliveira/OR-Datasets/tree/master/Cutting-and-Packing/2D/HT2001a)  
- **Referência:**  
  Hopper, E.; Turton, B.C.H. (2001). *An Empirical Investigation of Meta-Heuristic and Heuristic Algorithms for a 2D Packing Problem*. *European Journal of Operational Research*, 128(1), 34–57.  
  [EJOR DOI link](https://doi.org/10.1016/S0377-2217(00)00051-3)

---

### 🟩 JAKOBS — Jakobs (1996)
- **Local:** [`/data/JAKOBS`](https://github.com/Oscar-Oliveira/OR-Datasets/tree/master/Cutting-and-Packing/2D/JAKOBS) 
- **Referência:**  
  Jakobs, S. (1996). *On Genetic Algorithms for the Packing of Polygons*. *European Journal of Operational Research*, 88(1), 165–181.  
  [EJOR DOI link](https://doi.org/10.1016/0377-2217(94)00289-5)

---

### 🟩 MB2D — Mack & Bortfeldt (2012)
- **Local:** [`/data/MB2D`](https://github.com/Oscar-Oliveira/OR-Datasets/tree/master/Cutting-and-Packing/2D/MB2D)
- **Referência:**  
  Mack, D.; Bortfeldt, A. (2012). *A Heuristic for Solving Large Bin Packing Problems in Two and Three Dimensions*. *Central European Journal of Operations Research*, 20(3), 545–563.  
  [CEJOR DOI link](https://doi.org/10.1007/s10100-010-0179-1)

---

---

## 🧠 Observações finais
- Todas as instâncias vêm do repositório de Oscar Oliveira (2023) e mantêm compatibilidade com formatos originais de literatura.  
- Os campos `Cost`, `Value` e `DemandMax` são padronizações genéricas e não usados no 2D BPP clássico.  
- Todas as instâncias assumem **bins idênticos**, **sem rotação de peças** e **orientação fixa**.  

---

**Base de dados:** [OR-Datasets / Cutting-and-Packing / 2D](https://github.com/Oscar-Oliveira/OR-Datasets/tree/master/Cutting-and-Packing/2D)  
**Licença dos dados originais:** CC BY-NC-SA 4.0


## ⚙️ Estrutura dos arquivos

Cada instância é armazenada no formato JSON conforme o padrão do repositório [OR-Datasets](https://github.com/Oscar-Oliveira/OR-Datasets).  
Exemplo:

```json
{
  "Name": "BENG1",
  "Objects": [
    {"Length": 25, "Height": 10, "Stock": null, "Cost": 250}
  ],
  "Items": [
    {"Length": 8, "Height": 6, "Demand": 2, "DemandMax": null, "Value": 48},
    ...
  ]
}