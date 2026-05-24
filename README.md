# 🎵 dangerous_data_mj_statistics

Statistical analysis applied to a real Michael Jackson dataset —
built as part of my MBA in Data Science, AI and Analytics at USP/ESALQ.

---

## 📌 About the Project

This project uses Michael Jackson's discography as a laboratory for applying descriptive statistics, probability distributions,
and hypothesis testing concepts, making abstract theory tangible through real, familiar data.
No synthetic data. No generic examples.
Every analysis uses real singles, albums, chart positions and sales figures.

---

## 📊 Dataset

**MJ_Dataset_Oficial_v2.xlsx**

| Variable | Type | Description |
|---|---|---|
| Single         | Qualitative | Song title |
| Album          | Qualitative | Source album |
| Year           | Quantitative (discrete) | Release year |
| Peak EUA       | Quantitative (discrete) | Best position on Billboard Hot 100 |
| Sem. Chart EUA | Quantitative (discrete) | Weeks on Billboard Hot 100 |
| Vendas Album (mi) | Quantitative (continuous) | Album worldwide sales (millions) |
| Tem Clipe      | Qualitative (binary) | Official music video: Yes/No |
| Gênero Musical | Qualitative | Musical genre |
| Duração (min)  | Quantitative (continuous) | Single duration in minutes |
| Grammys        | Quantitative (discrete) | Grammy Awards for the album |

**26 singles | 6 studio albums | 1979–2025**

---

## 📂 Repository Structure

```
dangerous_data_mj_statistics/
│
├── data/
│   └── MJ_Dataset_Oficial_v2.xlsx       # Main dataset
│
├── analysis/
│   ├── 01_tipos_variaveis.xlsx           # Variable types
│   ├── 02_estatisticas_descritivas.xlsx  # Descriptive statistics
│   ├── 03_distribuicoes.xlsx             # Probability distributions
│   ├── 04_testes_hipoteses.xlsx          # Hypothesis testing
│   └── 05_correlacao_regressao.xlsx      # Correlation & regression
│
├── scripts/
│   └── (Python scripts — coming soon 🔜)
│
├── docs/
│   └── Fundamentos_III_MJ_Completo.txt  # Study guide (PT-BR)
│
└── README.md
```

---

## 📈 Analyses Covered

### ✅ Completed
- **Variable Types** — Identifying qualitative vs quantitative variables
- **Descriptive Statistics** — Mean, median, std deviation, outlier detection
- **Probability Distributions** — Binomial, Poisson, Normal applied to MJ data
- **Hypothesis Testing** — Z-test, t-test, Chi-square, F-test, Pearson correlation
- **Confidence Intervals** — 95% CI for weeks on chart
- **ANOVA** — Peak EUA comparison across musical eras
- **Linear Regression** — Predicting weeks on chart from Peak position

### 🔜 Coming Soon
- Python implementation of all analyses (pandas + scipy)
- Power BI dashboard
- CDI reconciliation model (Oracle SQL)

---

## 🔍 Key Findings

| Question | Result |
|---|---|
| Do MJ singles stay more than 15 weeks on chart?     | ✅ Yes — T=1.99, p=2.9% (reject H0) |
| Does Peak EUA correlate with weeks on chart?        | ✅ Yes — r=−0.75, significant |
| Does having a music video impact chart performance? | 📊 Analyzed — see hypothesis testing |
| Is Thriller a statistical outlier in album sales?   | ✅ Yes — confirmed by IQR rule |
| Does musical genre affect reaching #1?              | 📊 Chi-square test applied |

---

## 🛠️ Tools

![Excel](https://img.shields.io/badge/Excel-217346?style=flat&logo=microsoft-excel&logoColor=white)
![SQL](https://img.shields.io/badge/Oracle_SQL-F80000?style=flat&logo=oracle&logoColor=white)
![Python](https://img.shields.io/badge/Python-coming_soon-blue?style=flat&logo=python&logoColor=white)

---

## 🎓 Academic Context

**Course:** MBA in Data Science, AI and Analytics
**Institution:** USP/ESALQ — Universidade de São Paulo / ESALQ
**Module:** Fundamentos de Estatística
**Instructor:** Prof. Dr. Wilson Tarantin Junior

---

## 👤 Author

**Eric Renato **
Data Analyst | 15+ years in corporate financial systems
 	
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/eric-renato)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/EricRenato)

---

## 📋 License

This project is for educational purposes.
Michael Jackson data compiled from public sources:
ChartMasters.org · Billboard · RIAA · AllMusic.

---

"Started with "Wanna Be Startin' Somethin'" and along the journey I realized how "Bad" he was and I'll end up explaining "HIStory"."
