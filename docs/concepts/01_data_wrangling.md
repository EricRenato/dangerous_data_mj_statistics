# 🧹 Data Wrangling — do Excel bruto ao dado *tidy*

> Etapa 1 do portfólio. Aqui o dado deixa de ser uma planilha bonita e vira
> uma base confiável para estatística. *"Data wrangling costuma consumir 80%
> do tempo de um projeto de dados — e é onde se ganha ou se perde a análise."*

---

## 🎯 O conceito

**Data wrangling** (ou *data munging*) é o processo de **transformar dados
brutos e desorganizados em um formato limpo, estruturado e pronto para análise**.

O objetivo é chegar ao **tidy data** (Hadley Wickham, 2014):

| Princípio | Significado |
|---|---|
| 1️⃣ | Cada **variável** é uma **coluna** |
| 2️⃣ | Cada **observação** é uma **linha** |
| 3️⃣ | Cada **tipo de unidade** é uma **tabela** separada |

---

## 🔎 Problemas reais encontrados no MJ Dataset

Este dataset é ótimo para aprender porque tem imperfeições **reais**, não de
laboratório:

| # | Problema na fonte | Decisão de wrangling |
|---|---|---|
| 1 | Decimais em padrão BR (`4,98`) lidos como texto | `br_to_float()`: troca `,`→`.` e converte para `float` |
| 2 | Faltantes marcados com `—` (em-dash) | mapeados para `NaN` via lista `NA_TOKENS` |
| 3 | **Vendas/Grammys do álbum repetidos em cada single** (pseudo-replicação) | separados na tabela `albums` (Princípio 3) |
| 4 | Nota do autor: *"preciso corrigir, atrelar ao ID"* | criada chave `single_id` estável + `album_id` validado |
| 5 | `Earth Song` sem posição nos EUA (não lançada lá) | faltante **legítimo** preservado como `NaN` (≠ zero!) |
| 6 | Gênero com alta cardinalidade (`Afrobeat/Pop`) | derivada `genre_primary` (primeiro termo) |
| 7 | Série de vendas em formato **wide** (1 coluna por álbum) | `melt()` para formato **long** (tidy) |

---

## 🧩 Faltante ≠ Zero — o erro que distorce tudo

`Earth Song` não foi lançada nos EUA. Seu `peak_us` é **faltante**, não zero.

- Se preenchermos com **0**, a média de posições fica artificialmente "melhor".
- Se preenchermos com um número alto, fica artificialmente "pior".
- O correto é **`NaN`**: a observação simplesmente não existe naquele chart,
  e as funções estatísticas a ignoram (`mean()` do pandas pula `NaN`).

Este é um dos pontos onde **contexto** importa mais que técnica.

---

## 🏗️ A separação que evita a pseudo-replicação

No Excel, "Vendas Álbum (mi)" aparecia nas **27 linhas de singles**. *Thriller*
tem 70 mi repetido 7 vezes (uma por single).

❌ **Errado:** `singles["album_sales_mi"].mean()` → as vendas dos álbuns com mais
singles pesam mais, enviesando o resultado.

✅ **Certo:** vendas vivem na tabela `albums` (6 linhas, uma por álbum). Para
análises de single, usamos `singles`; para vendas, usamos `albums`; e ligamos
as duas por `album_id` quando preciso (um `merge`/`JOIN`).

---

## 📦 Saídas (tabelas tidy geradas)

| Arquivo | Grão (1 linha = ...) | Linhas |
|---|---|---|
| `data/processed/mj_singles.csv` | 1 single | 27 |
| `data/processed/mj_albums.csv` | 1 álbum | 6 |
| `data/processed/mj_tours.csv` | 1 turnê | 3 |
| `data/processed/mj_milestones.csv` | 1 recorde | 10 |
| `data/processed/mj_sales_timeline.csv` | 1 álbum × 1 ano | 221 |

> ℹ️ Nota: o README cita "26 singles", mas a planilha-fonte contém **27 linhas**
> de single. A divergência foi preservada (não inventamos nem apagamos dados) e
> fica registrada aqui como ponto de verificação com a fonte.

---

## ▶️ Como reproduzir

```bash
pip install -r requirements.txt
python analysis/python/01_data_wrangling.py
```

O script é **idempotente**: lê `data/raw/`, escreve `data/processed/` e imprime
um relatório de qualidade (contagem de faltantes + integridade referencial).

---

## ➡️ Próximo passo

Com os dados *tidy*, seguimos para **estatística descritiva**
(`02_descriptive_statistics`): medidas de tendência central, dispersão e a
primeira investigação — *Thriller é estatisticamente um outlier?*
