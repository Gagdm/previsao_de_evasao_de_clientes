# Previsão de Evasão de Clientes

Modelo para identificar clientes de uma operadora com risco de cancelar o serviço (churn) nos
próximos 60 dias. Projeto da disciplina Sistemas Inteligentes (CIn-UFPE), dividido em três
miniprojetos: preparação dos dados (MP1), algoritmos supervisionados (MP2) e não supervisionados (MP3).

## Equipe

| Nome | GitHub | Notebook |
| --- | --- | --- |
| Integrante 1 | @usuario1 | 01 |
| Integrante 2 | @usuario2 | 02 |
| Integrante 3 | @usuario3 | 03 |

## Notebooks

Rode na ordem: cada um lê o arquivo gerado pelo anterior.

| # | Etapa | Conteúdo | Gera | Abrir |
| --- | --- | --- | --- | --- |
| 1 | Limpeza e consolidação | Aulas 1 e 2 · passos 1 a 9 | `data/processed/base_limpa.csv` | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Gagdm/previsao_de_evasao_de_clientes/blob/main/notebooks/01_limpeza_e_consolidacao.ipynb) |
| 2 | Divisão treino/teste e EDA | Aula 3 · passo 10 | `data/processed/base_particionada.csv` | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Gagdm/previsao_de_evasao_de_clientes/blob/main/notebooks/02_divisao_e_analise_exploratoria.ipynb) |
| 3 | Transformações e versões | Aula 3 · passos 11 a 13 | `data/processed/versao_a_supervisionada.csv`, `versao_b_mista.csv`, `versao_c_numerica.csv` | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Gagdm/previsao_de_evasao_de_clientes/blob/main/notebooks/03_transformacoes_e_versoes.ipynb) |

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

1. Abra o seu notebook pelo botão **Abrir no Colab**.
2. Rode a primeira célula. Ela baixa o repositório atualizado e instala as bibliotecas.
3. Para salvar o notebook: **Arquivo → Salvar uma cópia no GitHub**, branch `main`, mesmo caminho
   em `notebooks/`.
4. Para salvar os CSVs gerados: a última célula baixa os arquivos para o seu computador. Depois,
   no GitHub, entre em `data/processed/` → **Add file → Upload files** → arraste os CSVs → **Commit changes**.

## Regras do grupo

- Cada um edita só o próprio notebook. Dois commits no mesmo `.ipynb` geram conflito difícil de resolver.
- Datas, `random_state` e o de-para ficam só em `config.py`.
- Nada é editado à mão em `data/raw/`: toda correção é feita em código.
- Medianas, modas e o scaler são calculados só com as linhas de treino.
