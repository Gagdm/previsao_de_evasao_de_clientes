"""Pré-processamento do MP1 empacotado como um transformador do scikit-learn.

O Relatório 03 aplicou as transformações "à mão" (imputação por grupo de fibra, indicador de
ausência, padronização e one-hot), ajustando-as no treino inteiro. Isso basta para gerar a
Versão A, mas não para a validação cruzada do MP2: se o imputador e o escalador forem ajustados
no treino inteiro, cada dobra de validação já terá "contribuído" para as medianas, modas, médias
e desvios usados nela. Empacotando as mesmas regras em um transformador, elas passam a ser
reajustadas em cada dobra, dentro de um ``Pipeline``, e o vazamento desaparece por completo.

Quando ajustado no treino inteiro, o transformador reproduz exatamente as colunas da Versão A
(os notebooks do MP2 verificam isso).
"""
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, StandardScaler

import config

# Colunas que o transformador recebe: os atributos da base particionada, ainda brutos.
COLUNAS_ENTRADA = [*config.NUMERICAS, *config.CATEGORICAS, *config.BINARIAS]


class PreprocessadorChurn(BaseEstimator, TransformerMixin):
    """Imputação + indicador de ausência + padronização + one-hot, ajustados só no `fit`."""

    def fit(self, X, y=None):
        X = pd.DataFrame(X)[COLUNAS_ENTRADA]
        # Imputação (Relatório 03, Seção 3): mediana da mensalidade por grupo de fibra e moda
        # das demais colunas com ausentes.
        self.medianas_mensalidade_ = X.groupby("fibra_optica")["mensalidade_rs"].median()
        self.modas_ = {coluna: X[coluna].mode()[0] for coluna in ["atrasos_6m", *config.CATEGORICAS]}
        imputado = self._imputar(X)
        # Escalonamento (Seção 4) e one-hot (Seção 5), aprendidos sobre os dados já imputados.
        self.escalador_ = StandardScaler().fit(imputado[config.NUMERICAS])
        self.codificador_ = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        self.codificador_.fit(imputado[config.CATEGORICAS])
        self.colunas_onehot_ = list(self.codificador_.get_feature_names_out(config.CATEGORICAS))
        # Mesma ordem de colunas da Versão A (sem id_cliente, split e churn).
        self.colunas_saida_ = [*config.NUMERICAS, *self.colunas_onehot_, *config.BINARIAS, "mensalidade_ausente"]
        return self

    def _imputar(self, X):
        X = X.copy()
        X["mensalidade_rs"] = X["mensalidade_rs"].fillna(X["fibra_optica"].map(self.medianas_mensalidade_))
        return X.fillna(self.modas_)

    def transform(self, X):
        X = pd.DataFrame(X)[COLUNAS_ENTRADA]
        # O indicador é criado antes da imputação, enquanto ainda se sabe o que faltava.
        ausente = X["mensalidade_rs"].isna().astype(int)
        imputado = self._imputar(X)
        numericas = pd.DataFrame(self.escalador_.transform(imputado[config.NUMERICAS]),
                                 columns=config.NUMERICAS, index=X.index)
        onehot = pd.DataFrame(self.codificador_.transform(imputado[config.CATEGORICAS]).astype(int),
                              columns=self.colunas_onehot_, index=X.index)
        saida = pd.concat([numericas, onehot, imputado[config.BINARIAS].astype(int)], axis=1)
        saida["mensalidade_ausente"] = ausente
        return saida[self.colunas_saida_]

    def get_feature_names_out(self, input_features=None):
        return np.array(self.colunas_saida_, dtype=object)

    def para_escala_original(self, coluna, valor_z):
        """Converte um valor padronizado (z) de volta para a unidade original da variável."""
        i = config.NUMERICAS.index(coluna)
        return valor_z * self.escalador_.scale_[i] + self.escalador_.mean_[i]


def variavel_de_origem(coluna):
    """Agrupa as colunas one-hot na variável original (ex.: tipo_contrato_Mensal -> tipo_contrato)."""
    for categorica in config.CATEGORICAS:
        if coluna.startswith(categorica + "_"):
            return categorica
    return coluna
