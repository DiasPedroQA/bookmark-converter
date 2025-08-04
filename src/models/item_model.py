"""
Docstring para models.item_model
"""


# import uuid
# from datetime import datetime
# from pathlib import Path
# from typing import Self

# from pydantic import BaseModel, Field, model_validator

# UUID_NAMESPACE: uuid.UUID = uuid.NAMESPACE_DNS


# class ModeladorDeItens(BaseModel):
#     """Modelo unificado para representar um item validado ou com falhas de validação."""

#     identificador: str | None = Field(
#         default=None,
#         description="UUID v5 gerado a partir do namespace e do nome, se válido.",
#         pattern=r"^[a-f0-9\-]{36}$",
#     )
#     nome_item: str | None = None
#     pasta_mae_item: str | None = None
#     caminho_absoluto_item: str | None = None
#     tipo_item: str | None = None  # ARQUIVO ou PASTA
#     tamanho_bytes_item: float | None = Field(default=None, ge=0)
#     data_criacao_item: datetime | None = None
#     data_modificacao_item: datetime | None = None
#     data_acesso_item: datetime | None = None
#     # permissoes_item: bool | None = None  # apenas se tem leitura
#     permissoes_item: dict[str, bool] | None = None  # <-- Agora guarda tudo: leitura, escrita, execução
#     status: bool = False
#     mensagem: str = "Falha na validação de um ou mais atributos."

#     @classmethod
#     def modelar(cls, dados: dict) -> "ModeladorDeItens":
#         caminho = Path(dados.get("caminho_absoluto", ""))
#         nome: str = dados.get("nome") or caminho.name
#         tipo = dados.get("tipo")

#         return cls(
#             identificador=str(uuid.uuid5(namespace=UUID_NAMESPACE, name=str(caminho))) if caminho else None,
#             nome_item=nome,
#             pasta_mae_item=str(caminho.parent) if caminho else None,
#             caminho_absoluto_item=str(caminho),
#             tipo_item=tipo,
#             tamanho_bytes_item=dados.get("tamanho"),
#             data_criacao_item=dados.get("datas", {}).get("data_criacao"),
#             data_modificacao_item=dados.get("datas", {}).get("data_modificacao"),
#             data_acesso_item=dados.get("datas", {}).get("data_acesso"),
#             permissoes_item=dados.get("permissoes"),  # <- Agora vem o dicionário inteiro!
#         )

#     @model_validator(mode="after")
#     def validar_campos(self) -> Self:
#         erros: list[str] = []

#         if not self.nome_item or not self.nome_item.strip():
#             erros.append("Nome inválido.")
#         if not self.caminho_absoluto_item or not Path(self.caminho_absoluto_item).is_absolute():
#             erros.append("Caminho absoluto inválido.")
#         if self.tipo_item not in ("ARQUIVO", "PASTA"):
#             erros.append(f"Tipo inválido: {self.tipo_item}")
#         if self.tamanho_bytes_item is not None and self.tamanho_bytes_item < 0:
#             erros.append("Tamanho não pode ser negativo.")
#         # if self.permissoes_item is not None and not isinstance(self.permissoes_item, bool):
#         #     erros.append("Permissões devem ser booleanas.")
#         if self.permissoes_item is not None and not isinstance(self.permissoes_item, dict):
#             erros.append("Permissões devem ser um dicionário com chaves como leitura, escrita, execucao.")

#         if erros:
#             self.status = False
#             self.mensagem = " | ".join(erros)
#         else:
#             self.status = True
#             self.mensagem = "Item validado com sucesso."

#         return self


# ### ✅ Exemplo de uso:

# # item = ModeladorDeItens.modelar(entrada)
# # print(item.model_dump())

import json
from pydantic import BaseModel, Field, model_validator, ConfigDict

# from typing import Optional, Literal, Union, list, dict


class DatasAprimoradas(BaseModel):
    """Modelo para datas em múltiplos formatos."""

    timestamp: float = Field(default=..., description="Timestamp Unix")
    iso: str = Field(default=..., description="Data em formato ISO 8601")
    legivel: str = Field(default=..., description="Data formatada para humanos")


class Tamanho(BaseModel):
    """Modelo para representação de tamanhos."""

    bytes: int = Field(default=..., ge=0, description="Tamanho em bytes")
    blocos: int = Field(default=..., ge=0, description="Tamanho em blocos de disco")
    legivel: str = Field(default=..., description="Tamanho formatado para humanos")


class ConteudoItem(BaseModel):
    """Modelo para itens individuais dentro de um diretório."""

    nome: str = Field(default=..., description="Nome do item")
    tamanho: int | None = Field(default=None, description="Tamanho em bytes (None para pastas)")
    modificacao: float = Field(default=..., description="Timestamp da última modificação")
    extensao: str | None = Field(default=None, description="Extensão do arquivo (None para pastas)")


class ConteudoAprimorado(BaseModel):
    """Modelo para o conteúdo de um diretório."""

    arquivos: list[ConteudoItem] = Field(default_factory=list, description="Lista de arquivos")
    pastas: list[ConteudoItem] = Field(default_factory=list, description="Lista de subdiretórios")
    resumo: dict[str, int] = Field(default_factory=dict, description="Contagem total de itens")
    tipos: dict[str, int] = Field(default_factory=dict, description="Contagem por extensão")


class PermissoesDetalhadas(BaseModel):
    """Modelo para permissões no estilo Unix."""

    usuario: str = Field(default=..., description="Permissões do dono (rwx)")
    grupo: str = Field(default=..., description="Permissões do grupo (rwx)")
    outros: str = Field(default=..., description="Permissões para outros (rwx)")
    octal: str = Field(default=..., description="Permissões em formato octal")
    sticky: bool = Field(default=False, description="Bit sticky ativado")
    setuid: bool = Field(default=False, description="Bit setuid ativado")
    setgid: bool = Field(default=False, description="Bit setgid ativado")


class Seguranca(BaseModel):
    """Modelo para informações de segurança."""

    proprietario: str = Field(default=..., description="Usuário dono do item")
    grupo: str = Field(default=..., description="Grupo dono do item")
    hash_sha256: str | None = Field(default=None, description="Hash SHA256 do conteúdo")
    hash_md5: str | None = Field(default=None, description="Hash MD5 do conteúdo")
    selinux: str | None = Field(default=None, description="Contexto SELinux")


class SistemaArquivos(BaseModel):
    """Modelo para informações do sistema de arquivos."""

    tipo: str = Field(default=..., description="Tipo do sistema de arquivos")
    ponto_montagem: str | None = Field(None, description="Ponto de montagem")
    opcoes: str | None = Field(None, description="Opções de montagem")


class Sistema(BaseModel):
    """Modelo para informações do sistema."""

    coletado_em: DatasAprimoradas = Field(default=..., description="Data/hora da coleta")
    ferramenta: dict[str, str] = Field(default_factory=dict, description="Informações da ferramenta")
    sistema_arquivos: SistemaArquivos = Field(default=..., description="Dados do sistema de arquivos")


class ItemInfo(BaseModel):
    """Modelo para informações básicas do item."""

    nome: str = Field(default=..., description="Nome do item")
    tipo: str = Field(default=..., description="Tipo do item")
    caminho: dict[str, str | None] = Field(default=..., description="Caminhos absoluto e relativo")


class EstatisticasAprimoradas(BaseModel):
    """Modelo para estatísticas do item."""

    tamanho: Tamanho = Field(default=..., description="Informações de tamanho")
    itens: dict[str, int] = Field(default=..., description="Contagem de itens por tipo")
    datas: dict[str, DatasAprimoradas] = Field(default=..., description="Datas relevantes")
    profundidade: int | None = Field(None, description="Profundidade máxima (para pastas)")


class Cabecalho(BaseModel):
    """Modelo para metadados do cabeçalho."""

    versao: str = Field(default=..., description="Versão do formato")
    coletado_em: str = Field(default=..., description="Data/hora da coleta em ISO")


class ModeladorDeItens(BaseModel):
    """Modelo principal para representar metadados de arquivos e pastas."""

    model_config = ConfigDict(extra="ignore")

    cabecalho: Cabecalho = Field(default=..., description="Metadados do cabeçalho")
    item: ItemInfo = Field(default=..., description="Informações básicas do item")
    estatisticas: EstatisticasAprimoradas = Field(default=..., description="Estatísticas detalhadas")
    permissoes: PermissoesDetalhadas = Field(default=..., description="Permissões detalhadas")
    conteudo: ConteudoAprimorado | None = Field(default=None, description="Conteúdo (apenas para pastas)")
    seguranca: Seguranca = Field(default=..., description="Informações de segurança")
    sistema: Sistema = Field(default=..., description="Dados do sistema")
    versao_metadados: int = Field(default=..., description="Versão do esquema de metadados")

    @model_validator(mode="before")
    def validar_estrutura(self, data: dict) -> dict:
        """Valida a estrutura do JSON e ajusta campos conforme o tipo do item."""
        tipo: str = data.get("item", {}).get("tipo")

        # Validação para pastas
        if tipo == "PASTA":
            if data.get("conteudo") is None:
                raise ValueError("Pasta deve ter conteúdo detalhado")
            if data["estatisticas"].get("profundidade") is None:
                raise ValueError("Pasta deve ter profundidade definida")

        # Validação para arquivos
        elif tipo == "ARQUIVO":
            if data.get("conteudo") is not None:
                raise ValueError("Arquivo não deve ter conteúdo detalhado")
            if data["estatisticas"].get("profundidade") is not None:
                raise ValueError("Arquivo não deve ter profundidade definida")
            if data["seguranca"].get("hash_sha256") is None:
                raise ValueError("Arquivo deve ter hash SHA256")
            if data["seguranca"].get("hash_md5") is None:
                raise ValueError("Arquivo deve ter hash MD5")

        return data

    @classmethod
    def from_json(cls, json_data: dict | str) -> "ModeladorDeItens":
        """Cria uma instância a partir de dados JSON.

        Args:
            json_data: Dados JSON como dicionário ou string JSON

        Returns:
            Instância de ModeladorDeItens validada

        Raises:
            ValueError: Se os dados não corresponderem ao esperado
        """
        if isinstance(json_data, str):
            json_data = json.loads(json_data)

        return cls.model_validate(json_data)
