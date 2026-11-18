"""Constantes compartilhadas por todos os notebooks."""
from pathlib import Path

import pandas as pd

# Caminhos
RAIZ = Path(__file__).resolve().parent
BASE_BRUTA = RAIZ / "data" / "raw" / "base_churn_vf2.csv"
PROCESSADOS = RAIZ / "data" / "processed"
BASE_LIMPA = PROCESSADOS / "base_limpa.csv"
BASE_PARTICIONADA = PROCESSADOS / "base_particionada.csv"
BASE_TRANSFORMADA = PROCESSADOS / "base_transformada.csv"
VERSAO_A = PROCESSADOS / "versao_a_supervisionada.csv"
VERSAO_B = PROCESSADOS / "versao_b_mista.csv"
VERSAO_C = PROCESSADOS / "versao_c_numerica.csv"

# Problema (Aula 1)
DATA_CORTE = pd.Timestamp("2026-09-21")
FIM_JANELA = DATA_CORTE + pd.Timedelta(days=60)  # 2026-11-20
MATURACAO_MINIMA_MESES = 2

# Resultados dos modelos (MP2)
RESULTADOS = RAIZ / "resultados"
ARVORE_ESCOLHIDA = RESULTADOS / "arvore_escolhida.json"
XGBOOST_ESCOLHIDO = RESULTADOS / "xgboost_escolhido.json"

# Experimento (Aula 3)
RANDOM_STATE = 42
TAMANHO_TESTE = 0.30
N_DOBRAS = 5          # validação cruzada estratificada dentro do treino (MP2)
BETA = 2              # F2: reportado como métrica complementar (MP2)
RECALL_ALVO = 0.80    # ponto de operação: antecipar 80% dos cancelamentos (MP2)

# Colunas
ID = "id_cliente"
ALVO = "churn"
NUMERICAS = ["tempo_cliente_meses", "mensalidade_rs", "chamados_totais", "atrasos_6m"]
CATEGORICAS = ["tipo_contrato", "forma_pagamento"]
BINARIAS = ["fibra_optica", "debito_automatico"]

# Qualidade (Aula 2): aplique .str.strip().str.lower() antes do de-para
DE_PARA = {
    "tipo_contrato": {"mensal": "Mensal", "anual": "Anual", "bienal": "Bienal"},
    "forma_pagamento": {"boleto": "Boleto", "cartao": "Cartão", "cartão": "Cartão", "pix": "Pix"},
}
SENTINELAS = {"mensalidade_rs": [-85, 9999], "atrasos_6m": [99]}
FAIXAS_VALIDAS = {"mensalidade_rs": (10, 500), "atrasos_6m": (0, 6)}
