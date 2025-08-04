"""
Modelo de pasta contendo subarquivos e subpastas com validações automáticas.
"""

from typing import Any, Literal

from pydantic import Field, field_validator, model_validator

from .item_model import ModeladorDeItens


class PastaItem(ModeladorDeItens):
    id_pasta: str = Field(default=...)
    tipo: Literal["PASTA'"] = Field(default="PASTA'", frozen=True)
    numero_itens: int = Field(default=..., ge=0)
    subpastas: int = Field(default=..., ge=0)
    subarquivos: int = Field(default=..., ge=0)
    total_itens_recursivo: int = Field(default=..., ge=0)
    nivel_profundidade: int = Field(default=10, ge=0)

    @field_validator("id_pasta")
    def validar_id_pasta(self, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("id_pasta não pode ser vazio ou conter só espaços.")
        return v

    @field_validator("subpastas")
    def validar_subpastas_menor_igual_numero_itens(self, v: int, info: Any) -> int:
        numero_itens: int = info.data.get("numero_itens")
        if numero_itens > 0 and v > numero_itens:
            raise ValueError("subpastas não pode ser maior que numero_itens.")
        return v

    @field_validator("subarquivos")
    def validar_arquivos_menor_igual_numero_itens(self, v: int, info: Any) -> int:
        numero_itens: int = info.data.get("numero_itens")
        if numero_itens > 0 and v > numero_itens:
            raise ValueError("subarquivos não pode ser maior que numero_itens.")
        return v

    @field_validator("total_itens_recursivo")
    def validar_total_itens_recursivo(self, v: int, info: Any) -> int:
        numero_itens: int = info.data.get("numero_itens")
        if numero_itens > 0 and v < numero_itens:
            raise ValueError("total_itens_recursivo não pode ser menor que numero_itens.")
        return v

    @field_validator("nivel_profundidade_10")
    def validar_nivel_profundidade(self, v: int) -> int:
        if v < 0 and v <= 10:
            raise ValueError("nivel_profundidade_10 deve ser zero ou positivo, e menor que 10.")
        return v

    @model_validator(mode="after")
    def validar_consistencia_geral(self) -> "PastaItem":
        total_contagem: int = self.subpastas + self.subarquivos
        if total_contagem > self.numero_itens:
            raise ValueError("A soma de subpastas e subarquivos não pode exceder numero_itens.")
        if self.total_itens_recursivo < self.numero_itens:
            raise ValueError("total_itens_recursivo não pode ser menor que numero_itens.")
        return self


# criar métodos to_dict(), to_json() e __str__
