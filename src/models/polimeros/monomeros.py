"""
Modelos Pydantic de validação de atributos para sistemas de arquivos locais.

Este módulo define modelos de validação que retornam resultados detalhados (sucesso ou erro)
de forma padronizada, usando os campos:
- valor_entrada: valor analisado
- status: resultado booleano da validação
- mensagem: explicação textual do resultado

Cada classe cobre um atributo específico de arquivos ou pastas:
- Identificador SHA-256
- Nome de arquivo ou diretório
- Caminho da pasta-mãe
- Caminho absoluto
- Tipo de item (arquivo ou pasta)
- Tamanho em bytes
- Datas (criação, modificação, acesso)
- Permissão de leitura/escrita

Esses modelos são úteis para validação, testes, feedbacks de API e rastreamento de erros.
"""

import re
from datetime import datetime
from typing import Self
import uuid

from pydantic import BaseModel, Field, model_validator


# class ResultadoIdentificador(BaseModel):

#     valor_entrada: str = Field(default=..., min_length=3, max_length=64)
#     status: bool = Field(default=False)
#     mensagem: str = Field(default="Identificador inválido.")

#     @model_validator(mode="after")
#     def validar_identificador(self) -> Self:
#         if re.fullmatch(pattern=r"^[a-f0-9]{6}(-[a-f0-9]{6}){4}$", string=self.valor_entrada):
#             self.status = True
#             self.mensagem = "Identificador válido."
#         else:
#             self.status = False
#             self.mensagem = "Formato inválido para identificador."
#         return self


class ResultadoIdentificador(BaseModel):
    """
    Valida se um identificador segue o formato SHA-256 truncado com hífens.
    """
    valor_entrada: str = Field(default=...)
    status: bool = True
    mensagem: str = "UUID v5 válido."

    @model_validator(mode="after")
    def checar_uuid(self) -> Self:
        """Verifica se o identificador tem o padrão esperado com hífens."""
        try:
            parsed = uuid.UUID(hex=self.valor_entrada)
            if parsed.version != 5:
                raise ValueError("UUID não é v5.")
        except Exception as e:
            raise ValueError(f"UUID inválido: {e}") from e
        return self


class ResultadoNome(BaseModel):
    """
    Valida nome de arquivo ou diretório.
    """

    valor_entrada: str = Field(default=..., min_length=3, max_length=255)
    status: bool = Field(default=False)
    mensagem: str = Field(default="Nome inválido.")

    @model_validator(mode="after")
    def validar_nome(self) -> Self:
        """Verifica se o nome é válido e não reservado."""
        proibidos = r"[\\/*?<>|:]"
        reservados: set[str] = {"CON", "PRN", "AUX", "NUL"}
        if (
            self.valor_entrada
            and not self.valor_entrada.startswith(".")
            and not re.search(pattern=proibidos, string=self.valor_entrada)
            and self.valor_entrada.upper() not in reservados
        ):
            self.status = True
            self.mensagem = "Nome válido."
        else:
            self.status = False
            self.mensagem = "Nome inválido."
        return self


class ResultadoPastaMae(BaseModel):
    """
    Valida se o caminho da pasta mãe não está vazio.
    """

    valor_entrada: str = Field(default=..., min_length=5)
    status: bool = Field(default=False)
    mensagem: str = Field(default="Pasta mãe inválida.")

    @model_validator(mode="after")
    def validar_pasta_mae(self) -> Self:
        """Verifica se o caminho não é vazio ou só espaços."""
        if self.valor_entrada.strip():
            self.status = True
            self.mensagem = "Pasta mãe válida."
        else:
            self.status = False
            self.mensagem = "Pasta mãe inválida."
        return self


class ResultadoCaminhoAbsoluto(BaseModel):
    """
    Valida se o caminho é absoluto (começa com '/').
    """

    valor_entrada: str = Field(default=...)
    status: bool = Field(default=False)
    mensagem: str = Field(default="Caminho inválido.")

    @model_validator(mode="after")
    def validar_caminho_absoluto(self) -> Self:
        """Verifica se o caminho começa com barra."""
        if self.valor_entrada.startswith("/"):
            self.status = True
            self.mensagem = "Caminho absoluto válido."
        else:
            self.status = False
            self.mensagem = "Caminho absoluto inválido."
        return self


class ResultadoTipoItem(BaseModel):
    """
    Valida se o tipo é 'ARQUIVO' ou 'PASTA'.
    """

    valor_entrada: str = Field(default=...)
    status: bool = Field(default=False)
    mensagem: str = Field(default="Tipo inválido.")

    @model_validator(mode="after")
    def validar_tipo(self) -> Self:
        """Verifica se o tipo é permitido."""
        tipo: str = self.valor_entrada.strip().upper()
        if tipo in {"ARQUIVO", "PASTA"}:
            self.status = True
            self.mensagem = "Tipo válido."
            self.valor_entrada = tipo
        else:
            self.status = False
            self.mensagem = "Tipo inválido."
        return self


class ResultadoTamanhoBytes(BaseModel):
    """
    Valida se o tamanho em bytes é não-negativo.
    """

    valor_entrada: float = Field(default=..., ge=0)
    status: bool = Field(default=False)
    mensagem: str = Field(default="Tamanho inválido.")

    @model_validator(mode="after")
    def validar_tamanho(self) -> Self:
        """Verifica se o valor é >= 0."""
        if self.valor_entrada >= 0:
            self.status = True
            self.mensagem = "Tamanho válido."
        else:
            self.status = False
            self.mensagem = "Tamanho inválido."
        return self


class ResultadoDataCriacao(BaseModel):
    """
    Valida se a data de criação não está no futuro.
    """

    valor_entrada: datetime = Field(default=...)
    status: bool = Field(default=False)
    mensagem: str = Field(default="Data inválida.")

    @model_validator(mode="after")
    def validar_data_criacao(self) -> Self:
        """Compara com a data atual."""
        if self.valor_entrada <= datetime.now():
            self.status = True
            self.mensagem = "Data válida."
        else:
            self.status = False
            self.mensagem = "Data inválida: no futuro."
        return self


class ResultadoDataModificacao(BaseModel):
    """
    Valida a data de modificação (sempre válida por padrão).
    """

    valor_entrada: datetime = Field(default=...)
    status: bool = Field(default=False)
    mensagem: str = Field(default="Data válida.")

    @model_validator(mode="after")
    def validar_data_modificacao(self) -> Self:
        """Aceita qualquer data."""
        self.status = True
        self.mensagem = "Data válida."
        return self


class ResultadoDataAcesso(BaseModel):
    """
    Valida a data de acesso (sempre válida por padrão).
    """

    valor_entrada: datetime = Field(default=...)
    status: bool = Field(default=False)
    mensagem: str = Field(default="Data válida.")

    @model_validator(mode="after")
    def validar_data_acesso(self) -> Self:
        """Aceita qualquer data."""
        self.status = True
        self.mensagem = "Data válida."
        return self


# class ResultadoPermissao(BaseModel):
#     """
#     Valida se o valor de permissões é booleano.
#     """

#     valor_entrada: bool | str = Field(default=...)
#     status: bool = Field(default=False)
#     mensagem: str = Field(default="Permissão inválida.")

#     @model_validator(mode="after")
#     def validar_permissoes(self) -> Self:
#         """Verifica se é booleano."""
#         if isinstance(self.valor_entrada, bool):
#             self.status = True
#             self.mensagem = "Permissão válida."
#         else:
#             self.status = False
#             self.mensagem = "Permissão inválida: deve ser booleano."
#         return self


class ResultadoPermissao(BaseModel):
    """
    Valida se o campo de permissões representa um valor booleano.
    """

    valor_entrada: bool = Field(default=...)
    status: bool = Field(default=False)
    mensagem: str = Field(default="")

    @model_validator(mode="after")
    def validar_permissao(self) -> Self:
        """Convertendo string para bool, se necessário"""
        if isinstance(self.valor_entrada, str):
            if self.valor_entrada.lower() in ["true", "1", "yes"]:
                self.valor_entrada = True
            elif self.valor_entrada.lower() in ["false", "0", "no"]:
                self.valor_entrada = False
            else:
                self.status = False
                self.mensagem = "Permissão inválida: valor string não reconhecido como booleano."
                return self

        if isinstance(self.valor_entrada, bool):
            self.status = True
            self.mensagem = "Permissão válida."
        else:
            self.status = False
            self.mensagem = "Permissão inválida: tipo não reconhecido."
        return self
