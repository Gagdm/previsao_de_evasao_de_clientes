# Previsão de Evasão de Clientes

Modelo para identificar clientes de uma operadora com risco de cancelar o serviço (churn) nos
próximos 60 dias. Projeto da disciplina Sistemas Inteligentes (CIn-UFPE), dividido em três
miniprojetos: preparação dos dados (MP1), algoritmos supervisionados (MP2) e não supervisionados (MP3).

## Notebooks

Rode na ordem: cada notebook lê o arquivo gerado pelo anterior.

### 01 — Limpeza e consolidação [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Gagdm/previsao_de_evasao_de_clientes/blob/main/notebooks/01_limpeza_e_consolidacao.ipynb)

Avalia a qualidade da base original e a corrige: remove clientes duplicados, padroniza as
categorias escritas de formas diferentes e trata valores impossíveis. Depois, transforma as
datas em informação útil (quantidade de chamados, tempo de casa) e cria o rótulo `churn`.
Gera `data/processed/base_limpa.csv`.

### 02 — Divisão treino/teste e análise exploratória [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Gagdm/previsao_de_evasao_de_clientes/blob/main/notebooks/02_divisao_e_analise_exploratoria.ipynb)

Separa 70% dos clientes para treino e 30% para teste, mantendo a mesma proporção de churn nos
dois. Em seguida, analisa os dados de treino com estatística descritiva, taxa de churn por grupo
e correlações. Gera `data/processed/base_particionada.csv`.

### 03 — Transformações e versões [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Gagdm/previsao_de_evasao_de_clientes/blob/main/notebooks/03_transformacoes_e_versoes.ipynb)

Preenche os valores ausentes e coloca as variáveis numéricas na mesma escala, usando parâmetros
calculados só com o treino. Gera três versões da base, uma para cada tipo de algoritmo:

- `versao_a_supervisionada.csv`: classificação, no MP2.
- `versao_b_mista.csv`: K-prototypes, no MP3.
- `versao_c_numerica.csv`: K-means e DBSCAN, no MP3.

## Estrutura

```
previsao_de_evasao_de_clientes/
├── data/
│   ├── raw/            # base original, nunca editada à mão
│   └── processed/      # arquivos gerados pelos notebooks
├── notebooks/          # um notebook por etapa
├── config.py           # constantes compartilhadas (datas, random_state, de-para)
└── requirements.txt    # bibliotecas usadas
```

## Como trabalhar

1. Abra o notebook pelo botão **Abrir no Colab**.
2. Rode a primeira célula. Ela baixa o repositório atualizado e instala as bibliotecas.
3. Para salvar o notebook: **Arquivo → Salvar uma cópia no GitHub**, branch `main`, mesmo caminho
   em `notebooks/`.
4. Para salvar os CSVs gerados: a última célula baixa os arquivos para o seu computador. Depois,
   no GitHub, entre em `data/processed/` → **Add file → Upload files** → arraste os CSVs → **Commit changes**.
