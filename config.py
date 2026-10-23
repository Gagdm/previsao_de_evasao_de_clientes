"""Constantes compartilhadas por todos os notebooks."""
from pathlib import Path

import pandas as pd

# Caminhos
RAIZ = Path(__file__).resolve().parent
BASE_BRUTA = RAIZ / "data" / "raw" / "base_churn_vf2.csv"
PROCESSADOS = RAIZ / "data" / "processed"
BASE_LIMPA = PROCESSADOS / "base_limpa.csv"
BASE_PARTICIONADA = PROCESSADOS / "base_particionada.csv"
VERSAO_A = PROCESSADOS / "versao_a_supervisionada.csv"
VERSAO_B = PROCESSADOS / "versao_b_mista.csv"
VERSAO_C = PROCESSADOS / "versao_c_numerica.csv"

# Problema (Aula 1)
DATA_CORTE = pd.Timestamp("2026-09-21")
FIM_JANELA = DATA_CORTE + pd.Timedelta(days=60)  # 2026-11-20
MATURACAO_MINIMA_MESES = 2

# Experimento (Aula 3)
RANDOM_STATE = 42
TAMANHO_TESTE = 0.30

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
