# """
# Módulo de definição do modelo `Arquivo`, que representa arquivos no sistema virtual.
# """

# from typing import Literal

# from pydantic import Field, field_validator, model_validator

# from models.item_model import ItemDeSistema


# class ArquivoItem(ItemDeSistema):
#     id_arquivo: str = Field(default=..., min_length=1)
#     tipo: Literal["ARQUIVO"] = Field(default="ARQUIVO", frozen=True)
#     extensao: str = Field(default=..., pattern=r"^\.[a-zA-Z0-9]+$")
#     linhas: int = Field(default=..., ge=0)
#     encoding: str = Field(default=..., pattern=r"^[\w\-]+$")  # Ex: utf-8, latin-1

#     # === VALIDADORES DE CAMPO ===

#     @field_validator("id_arquivo")
#     def validar_id_arquivo(self, v: str) -> str:
#         if not v.strip():
#             raise ValueError("ID do arquivo não pode estar vazio.")
#         return v

#     @field_validator("extensao")
#     def validar_extensao_valida(self, v: str) -> str:
#         if not v.startswith("."):
#             raise ValueError("A extensão deve começar com ponto (ex: .txt).")
#         if len(v) < 2:
#             raise ValueError("Extensão inválida.")
#         return v.lower()

#     @field_validator("encoding")
#     def validar_encoding(self, v: str) -> str:
#         encoding_suportados: set[str] = {"utf-8", "latin-1", "ascii", "utf-16"}
#         if v.lower() not in encoding_suportados:
#             raise ValueError(f"Encoding '{v}' não suportado.")
#         return v.lower()

#     @field_validator("linhas")
#     def validar_linhas(self, v: int) -> int:
#         if v <= 0:
#             raise ValueError("Número de linhas não pode ser negativo, nem nulo.")
#         return v

#     # === VALIDADOR DE MODELO (GERAL) ===

#     @model_validator(mode="after")
#     def validar_consistencias_gerais(self) -> "ArquivoItem":
#         if self.extensao in [".jpg", ".png", ".bin"] and self.encoding != "utf-8":
#             raise ValueError("Arquivos binários devem usar encoding utf-8 (ou encoding default).")
#         if self.extensao in [".py", ".txt", ".md"] and self.linhas == 0:
#             raise ValueError("Arquivos de texto não devem ter 0 linhas.")
#         return self

# # criar métodos to_dict(), to_json() e __str__
