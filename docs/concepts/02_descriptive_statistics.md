# 📊 Estatística Descritiva — resumindo o catálogo de MJ

> Etapa 2 do portfólio. Acompanha o notebook
> `analysis/python/02_descriptive_statistics.ipynb`.

---

## 🎯 O conceito

**Estatística descritiva** resume e descreve um conjunto de dados — *sem* tirar
conclusões para além dele (isso é inferência, vem depois). Três famílias de medidas:

| Família | Medidas | Para quê |
|---|---|---|
| **Tendência central** | média, mediana, moda | onde está o "centro" |
| **Dispersão** | amplitude, desvio padrão, IQR, CV | quão espalhado |
| **Forma** | assimetria (skewness), curtose | o "formato" da distribuição |

---

## 🔑 Média × Mediana — a lição central

Quando a distribuição é **assimétrica**, média e mediana divergem:

| Vendas de álbum (mi) | Valor |
|---|---|
| Média | ~32 |
| Mediana | ~27 |

A média é **puxada para cima** por *Thriller* (70 mi). Reportar a **média** aqui
daria a falsa impressão de que o álbum "típico" de MJ vende mais do que vende.
👉 **Em dados assimétricos, a mediana descreve melhor o típico.**

---

## 🎯 Thriller é outlier? Dois critérios

| Critério | Regra | Resultado |
|---|---|---|
| **IQR (Tukey)** | valor > Q3 + 1,5·IQR | 70 > 54,9 → **outlier** ✅ |
| **Z-score** | \|z\| > 2 | maior z-score do catálogo → **atípico** ✅ |

⚠️ **Ressalva honesta:** com n=6 álbuns, isso é **ilustrativo/descritivo**, não um
teste inferencial robusto. Registrar essa limitação é o que separa análise séria
de "número bonito".

---

## 📈 O que os dados disseram (descritivo)

| Pergunta do README | Resposta descritiva |
|---|---|
| Singles ficam >15 semanas no chart? | **69%** ficam; mediana = **16 semanas** |
| Clipe afeta tempo no chart? | com clipe **17** vs sem clipe **14** semanas (média) — *sugere* efeito |
| Pico × semanas no chart | correlação **r = −0,75** (forte; melhor posição → mais tempo) |

> Estes são **indícios descritivos**. Provar que o efeito do clipe é
> *estatisticamente significativo* exige **teste de hipótese** (próxima etapa).

---

## 🖼️ Figuras geradas (`analysis/python/figures/`)

- `02_histograms.png` — distribuição das variáveis dos singles
- `02_boxplots.png` — centro, dispersão e outliers
- `02_thriller_outlier.png` — Thriller destacado vs limite do IQR
- `02_peak_vs_weeks.png` — pico × longevidade no chart

---

## ➡️ Próximo passo

**Inferência:** intervalo de confiança para a média de semanas em chart e o
**teste de hipótese** formal — *o clipe realmente afeta a longevidade, ou a
diferença de 17 vs 14 é só acaso?*
