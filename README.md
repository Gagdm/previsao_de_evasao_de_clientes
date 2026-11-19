# Previsão de Evasão de Clientes

Modelo para identificar clientes de uma operadora com risco de cancelar o serviço (churn) nos
próximos 60 dias. Projeto da disciplina Sistemas Inteligentes (CIn-UFPE), dividido em três
miniprojetos: preparação dos dados (MP1), algoritmos supervisionados (MP2) e não supervisionados (MP3).

## Equipe

- Davi Lyra Dubeux
- Gabriel Alves
- Isabela Nascimento
- Karina Lima
- Lara Luchi

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

data/processed/base_particionada.csv  +  PreprocessadorChurn (= Versão A)
        │  04 — árvore de decisão (pré-poda, pós-poda, regras)
        ▼
resultados/arvore_escolhida.json
        │  05 — XGBoost (GridSearchCV × Optuna) e comparação com a árvore
        ▼
resultados/xgboost_escolhido.json
```

O MP1 (notebooks 01 a 03) prepara os dados e gera as três versões da base. O MP2 (notebooks 04 e 05)
parte de `base_particionada.csv` e aplica as transformações do notebook 03 por meio do
`PreprocessadorChurn` (`preprocessing.py`), dentro de um `Pipeline`. Ajustado no treino inteiro,
ele reproduz exatamente a Versão A (os notebooks verificam isso); dentro da validação cruzada, é
reajustado em cada dobra, o que elimina a contaminação entre as dobras.

## Notebooks

Rode na ordem: cada notebook depende de arquivos gerados pelos anteriores (veja o fluxo acima). Os
notebooks estão escritos em formato de relatório, com a teoria de cada etapa, a interpretação dos
resultados e o código comentado.

### MP1 — Preparação dos dados

#### 01 — Limpeza e consolidação [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Gagdm/previsao_de_evasao_de_clientes/blob/main/notebooks/01_limpeza_e_consolidacao.ipynb)

Mede a qualidade da base original nas quatro dimensões (completude, validade, consistência e
unicidade) e corrige o que encontra: remove clientes duplicados, padroniza as categorias escritas
de formas diferentes e transforma valores sentinela (−85, 9999, 99) em ausentes. Depois, transforma
as datas em informação útil (quantidade de chamados, tempo de casa), cria o rótulo `churn` e
remove clientes com menos de 2 meses de casa. Aplica apenas correções que não dependem de
estatísticas da base. Gera `data/processed/base_limpa.csv` (4.976 clientes, 35,4% de churn).

#### 02 — Divisão treino/teste e análise exploratória [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Gagdm/previsao_de_evasao_de_clientes/blob/main/notebooks/02_divisao_treino_teste_analise_exploratoria.ipynb)

Separa 70% dos clientes para treino e 30% para teste, de forma estratificada (mesma proporção de
churn nos dois) e com `random_state=42`. Em seguida, analisa **apenas o treino** com estatística
descritiva, distribuições, taxa de churn por grupo e por faixa, correlações e outliers, e termina
com recomendações para o notebook 03. Gera `data/processed/base_particionada.csv`, com a coluna
`split` (`treino` ou `teste`).

#### 03 — Transformações e versões [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Gagdm/previsao_de_evasao_de_clientes/blob/main/notebooks/03_transformacoes_e_versoes.ipynb)

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

### MP2 — Algoritmos supervisionados

Protocolo comum aos dois notebooks: validação cruzada estratificada em 5 dobras dentro do treino
(`random_state=42`), escolha de hiperparâmetros pela **AUC-PR** e limiar de decisão escolhido nas
previsões fora da dobra para atingir **80% de recall** da classe churn (`config.RECALL_ALVO`). O teste
é usado uma única vez, ao final. O F2 é reportado, mas não é usado como critério: com 35,4% de churn,
prever "cancela" para todos os clientes já dá F2 = 0,733, mais que a melhor árvore obtida.

#### 04 — Árvore de decisão [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Gagdm/previsao_de_evasao_de_clientes/blob/main/notebooks/04_arvore_de_decisao.ipynb)

Mede o sobreajuste da árvore sem restrições, estuda a pré-poda (curvas de validação de `max_depth`,
`min_samples_leaf`, `max_leaf_nodes` e `min_impurity_decrease`; `GridSearchCV` com 588 combinações) e a
pós-poda por custo-complexidade (`ccp_alpha`, com a regra de um erro padrão), testa uma árvore híbrida
e escolhe o limiar. Avalia no teste (gap treino × teste, matriz de confusão, ROC, precisão-recall,
curvas de aprendizado), extrai as regras SE-ENTÃO na unidade original e compara a importância por
impureza com a importância por permutação. Gera `resultados/arvore_escolhida.json`.

Resultado: a pré-poda por tamanho de folha (40 clientes) superou a pós-poda (AUC-PR 0,627 × 0,592);
a árvore escolhida (híbrida, 48 folhas) tem AUC-PR de 0,615 no teste e antecipa 76% dos cancelamentos
acionando metade da base. Perfil de risco: contrato mensal, cliente recente e chamados/atrasos.

#### 05 — XGBoost e comparação [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Gagdm/previsao_de_evasao_de_clientes/blob/main/notebooks/05_xgboost_e_comparacao.ipynb)

Avalia o XGBoost padrão, mede o compromisso `n_estimators` × `learning_rate` com curvas de erro por
iteração, compara `GridSearchCV` (128 combinações) com Optuna (TPE + MedianPruner, 10 hiperparâmetros,
incluindo `min_child_weight` e `scale_pos_weight`), avalia no teste e interpreta o modelo (ganho,
frequência, permutação e valores SHAP calculados pelo próprio XGBoost). Por fim, compara com a árvore
no mesmo ponto de operação, com intervalos de confiança por *bootstrap* pareado. Precisa de
`resultados/arvore_escolhida.json` (gerado pelo 04). Gera `resultados/xgboost_escolhido.json`.

Os parágrafos de **leitura dos resultados** do notebook 05 são gerados a partir dos números calculados
na própria execução.

Resultado: com os padrões da biblioteca, o XGBoost sobreajusta (gap treino × validação de 0,399 na
AUC-PR) e perde para a árvore. Depois da busca, a grade e o Optuna empataram (AUC-PR de validação
0,660 × 0,663, diferença menor que um erro padrão) e ficou o modelo da grade: 500 árvores de
profundidade 2, taxa de aprendizado 0,03, `subsample` 0,8, `colsample_bytree` 0,7 e `gamma` 1. No
teste, a AUC-PR é de 0,680 (árvore: 0,615) e a AUC-ROC, de 0,803 (árvore: 0,756); no limiar de
recall 80%, antecipa 79,8% dos cancelamentos com precisão de 54,2%, acionando 52,1% da base. Pelo
*bootstrap* pareado, a vantagem na AUC-PR é significativa (IC 95% de +0,040 a +0,090), mas a
diferença de precisão no ponto de operação não é. Em resumo: o XGBoost ordena melhor os clientes por
risco, e a árvore entrega praticamente a mesma campanha com regras legíveis. Os dois modelos apontam
os mesmos fatores de risco: tipo de contrato, tempo de casa e chamados.

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
├── resultados/         # hiperparâmetros, limiares e métricas dos modelos escolhidos (MP2)
├── config.py           # constantes compartilhadas (caminhos, datas, random_state, de-para, recall-alvo)
├── preprocessing.py   # transformações do notebook 03 como transformador do scikit-learn (MP2)
└── requirements.txt    # bibliotecas usadas
```

## Como trabalhar

1. Abra o notebook pelo botão **Abrir no Colab**.
2. Rode a primeira célula. Ela baixa o repositório atualizado e instala as bibliotecas.
3. Para salvar o notebook: **Arquivo → Salvar uma cópia no GitHub**, branch `main`, mesmo caminho
   em `notebooks/`.
4. Para salvar os arquivos gerados: a última célula baixa os arquivos para o seu computador. Depois,
   no GitHub, entre na pasta de destino → **Add file → Upload files** → arraste os arquivos →
   **Commit changes**. No MP1, os CSVs vão para `data/processed/`; no MP2, os `.json` vão para
   `resultados/`. O notebook 05 precisa do `arvore_escolhida.json` no repositório, porque cada
   notebook do Colab roda em uma sessão separada.
