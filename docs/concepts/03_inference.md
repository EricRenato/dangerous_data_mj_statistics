# 🎯 Inferência — Intervalo de Confiança & Teste de Hipótese

> Etapa 3 do portfólio. Acompanha `analysis/python/03_inference.ipynb`.
> Aqui saímos da **descrição** (Etapa 2) e passamos a **tirar conclusões** sobre a
> população a partir da amostra.

---

## 🎯 Intervalo de confiança (IC)

Uma estimativa **pontual** (a média = 16,65 semanas) quase nunca é exata. O **IC**
dá uma **faixa plausível** para o valor verdadeiro, com um nível de confiança.

| Estimativa | Resultado |
|---|---|
| Média de semanas no chart | **16,65** |
| IC 95% | **[14,9 ; 18,4]** semanas |
| Proporção de #1 | 42% — IC 95% **[23% ; 61%]** |

> **Interpretação correta:** "95% de confiança" refere-se ao **método** — se
> repetíssemos a amostragem muitas vezes, ~95% dos ICs conteriam a média real.
> Não é "95% de chance do valor estar aqui".

---

## ⚖️ Teste de hipótese — a pergunta do clipe

**O clipe afeta o tempo no chart?** (17 vs 14 semanas na descritiva)

| Elemento | Definição |
|---|---|
| **H₀** (nula) | as médias são **iguais** (clipe não importa) |
| **H₁** (alternativa) | as médias são **diferentes** |
| **α** | 0,05 — risco aceito de errar rejeitando H₀ |
| **Regra** | rejeita H₀ se **p-valor < α** |

### Resultados

| Teste | p-valor | Decisão |
|---|---|---|
| t de Welch | **0,096** | não rejeita H₀ |
| Mann-Whitney U | **0,166** | não rejeita H₀ |
| **Cohen's d** | **0,71** | efeito **médio-grande** |

---

## 🧠 A grande lição: significância ≠ relevância

Achado aparentemente contraditório, mas **fundamental**:

- O **tamanho do efeito é médio-grande** (d = 0,71) — a diferença *parece* relevante.
- Mas o **p-valor > 0,05** — não há evidência estatística para afirmá-la.

**Por quê?** O grupo "sem clipe" tem só **n = 3**. Amostra minúscula = **baixo poder
estatístico** → o teste não consegue detectar nem um efeito real.

> ⚠️ "Não rejeitar H₀" **não** prova que o clipe não tem efeito. Significa apenas
> que **não temos dados suficientes** para afirmar que tem. Ausência de evidência
> ≠ evidência de ausência.

---

## 🚧 Ressalvas que todo analista sério registra

- **Poder estatístico baixo** (n=3 num grupo).
- **Confundidores:** clipe pode ser *proxy* de investimento de marketing/era do álbum.
- **Correlação ≠ causalidade:** comparar grupos não prova causa.

---

## 🖼️ Figuras (`analysis/python/figures/`)
- `03_ci_mean_weeks.png` — IC 95% da média vs referência de 15 semanas
- `03_video_vs_weeks.png` — boxplot com/sem clipe + pontos individuais

---

## ➡️ Próximo passo
- **ANOVA** (`04`): o desempenho difere entre **gêneros** / **álbuns**?
- **Regressão** (`05`): prever `weeks_chart_us` a partir de `peak_us` (r = −0,75).
