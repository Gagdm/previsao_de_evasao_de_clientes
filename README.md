# Previsão de Evasão de Clientes

Modelo para identificar clientes de uma operadora com risco de cancelar o serviço (churn) nos
próximos 60 dias. Projeto da disciplina Sistemas Inteligentes (CIn-UFPE), dividido em três
miniprojetos: preparação dos dados (MP1), algoritmos supervisionados (MP2) e não supervisionados (MP3).

## O problema

A operadora quer agir antes do cancelamento. Para isso, olhamos a situação de cada cliente em uma
**data de corte** (21/09/2026) e verificamos se ele cancelou nos **60 dias seguintes** (até
20/11/2026). Quem cancelou nessa janela recebe `churn = 1`; quem permaneceu, `churn = 0`.
Tecnicamente, é um problema de classificação binária, com prioridade para o *recall* da classe de
churn.

## Fluxo dos dados

```
data/raw/base_churn_vf2.csv
        │  01 — limpeza e consolidação
        ▼
data/processed/base_limpa.csv
        │  02 — divisão treino/teste e análise exploratória
        ▼
data/processed/base_particionada.csv
        │  03 — imputação, escalonamento e one-hot (ajustados só no treino)
        ▼
data/processed/base_transformada.csv
        │  03 — recorte de colunas por tipo de algoritmo
        ▼
versao_a_supervisionada.csv · versao_b_mista.csv · versao_c_numerica.csv
```

## Notebooks

Rode na ordem: cada notebook lê o arquivo gerado pelo anterior. Os notebooks estão escritos em
formato de relatório, com a teoria de cada etapa, a interpretação dos resultados e o código comentado.

### 01 — Limpeza e consolidação [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Gagdm/previsao_de_evasao_de_clientes/blob/main/notebooks/01_limpeza_e_consolidacao.ipynb)

Mede a qualidade da base original nas quatro dimensões (completude, validade, consistência e
unicidade) e corrige o que encontra: remove clientes duplicados, padroniza as categorias escritas
de formas diferentes e transforma valores sentinela (−85, 9999, 99) em ausentes. Depois, transforma
as datas em informação útil (quantidade de chamados, tempo de casa), cria o rótulo `churn` e
remove clientes com menos de 2 meses de casa. Aplica apenas correções que não dependem de
estatísticas da base. Gera `data/processed/base_limpa.csv` (4.976 clientes, 35,4% de churn).

### 02 — Divisão treino/teste e análise exploratória [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Gagdm/previsao_de_evasao_de_clientes/blob/main/notebooks/02_divisao_treino_teste_analise_exploratoria.ipynb)

Separa 70% dos clientes para treino e 30% para teste, de forma estratificada (mesma proporção de
churn nos dois) e com `random_state=42`. Em seguida, analisa **apenas o treino** com estatística
descritiva, distribuições, taxa de churn por grupo e por faixa, correlações e outliers, e termina
com recomendações para o notebook 03. Gera `data/processed/base_particionada.csv`, com a coluna
`split` (`treino` ou `teste`).

### 03 — Transformações e versões [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Gagdm/previsao_de_evasao_de_clientes/blob/main/notebooks/03_transformacoes_e_versoes.ipynb)

Preenche os valores ausentes (mensalidade pela mediana do grupo de fibra óptica, demais colunas
pela moda), cria o indicador `mensalidade_ausente`, padroniza as variáveis numéricas
(`StandardScaler`) e codifica as categóricas em one-hot. Todos os parâmetros são calculados **só
com o treino** e aplicados ao treino e ao teste.

O resultado completo é salvo em `base_transformada.csv`, que reúne todas as colunas transformadas
(as categóricas em texto e em one-hot). Ela é a fonte das três versões, cada uma no formato de um
tipo de algoritmo:

| Arquivo | Uso | Atributos | `churn` |
| --- | --- | --- | --- |
| `versao_a_supervisionada.csv` | classificação (MP2) | numéricas escaladas, one-hot, binárias, `mensalidade_ausente` | alvo |
| `versao_b_mista.csv` | K-prototypes (MP3) | numéricas escaladas, categóricas em texto, binárias (índices categóricos `[4, 5, 6, 7]`) | só referência |
| `versao_c_numerica.csv` | K-means e DBSCAN (MP3) | numéricas escaladas, one-hot, binárias | só referência |

## Como usar as bases na modelagem

- `id_cliente` e `split` são colunas de controle: **nunca** entram como atributo.
- Treine e ajuste hiperparâmetros só com `split == "treino"`. O teste é usado uma única vez, na
  avaliação final.
- Nas versões B e C, `churn` serve apenas para descrever os grupos depois do agrupamento; não pode
  ser usado como atributo.
- `base_transformada.csv` não deve ir direto para um algoritmo: as categóricas aparecem duas vezes
  (em texto e em one-hot). Use uma das versões.
- Qualquer nova transformação que aprenda com os dados (balanceamento, seleção de variáveis) deve
  ser ajustada só no treino, de preferência dentro de um `Pipeline` do scikit-learn.

## Estrutura

```
previsao_de_evasao_de_clientes/
├── data/
│   ├── raw/            # base original, nunca editada à mão
│   └── processed/      # arquivos gerados pelos notebooks
├── notebooks/          # um notebook por etapa
├── config.py           # constantes compartilhadas (caminhos, datas, random_state, de-para)
└── requirements.txt    # bibliotecas usadas
```

## Como trabalhar

1. Abra o notebook pelo botão **Abrir no Colab**.
2. Rode a primeira célula. Ela baixa o repositório atualizado e instala as bibliotecas.
3. Para salvar o notebook: **Arquivo → Salvar uma cópia no GitHub**, branch `main`, mesmo caminho
   em `notebooks/`.
4. Para salvar os CSVs gerados: a última célula baixa os arquivos para o seu computador. Depois,
   no GitHub, entre em `data/processed/` → **Add file → Upload files** → arraste os CSVs → **Commit changes**.
