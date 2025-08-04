"""
sistema_operacional.py

Modelo Pydantic que representa o ambiente operacional da máquina local,
incluindo nome do sistema, versão, arquitetura, informações do usuário logado,
validação de caminho e metadados da pasta home.

Esse módulo é utilizado como base para diagnósticos, coleta de dados e geração
de relatórios no pipeline principal da aplicação.
"""

import platform
from pathlib import Path
from typing import Annotated
from pydantic import BaseModel, Field


class SistemaOperacional(BaseModel):
    """
    Representa informações detalhadas sobre o sistema operacional em uso,
    incluindo nome, versão, arquitetura, pasta home do usuário logado,
    permissões e metadados associados ao diretório principal do usuário.
    
    Esse modelo serve como base para relatórios, diagnósticos e análises
    do ambiente operacional da máquina em tempo de execução.
    """

    # === Identificação do sistema ===
    nome_do_sistema: Annotated[str, Field(description="Nome do sistema operacional (ex: Linux)")] = platform.system()
    versao: Annotated[str, Field(description="Versão do sistema operacional")] = platform.version()
    arquitetura: Annotated[str, Field(description="Arquitetura do sistema (ex: 64bit)")] = platform.architecture()[0]

    # === Caminhos ===
    usuario_logado: Annotated[str, Field(description="Nome do usuário logado informado manualmente")]
    caminho_pasta_usuario: Annotated[Path, Field(description="Caminho absoluto da pasta home do usuário")]

    filhos_pasta_home: Annotated[list[Path], Field(
        description="Lista de filhos (sub arquivos e sub pastas) dentro da pasta home"
    )] = []

    # === Validações ===
    caminho_valido: Annotated[dict[str, bool], Field(
        description="Status das validações do caminho (formato/padrão)"
    )]
    permissao_leitura: Annotated[bool, Field(
        description="Permissão de leitura na pasta home"
    )] = False

    # === Metadados ===
    data_acesso: Annotated[str | None, Field(description="Data do último acesso à pasta home")] = None
    data_criacao: Annotated[str | None, Field(description="Data da criação da pasta home")] = None
    data_modificacao: Annotated[str | None, Field(description="Data da última modificação da pasta home")] = None
    tamanho_caminho: Annotated[str | None, Field(description="Tamanho estimado da pasta home (formato legível)")] = None

    class Config:
        """
        Configurações do modelo Pydantic para permitir tipos arbitrários e
        remoção automática de espaços em strings. O modelo não é imutável.
        """
        arbitrary_types_allowed = True
        str_strip_whitespace = True
        frozen = False
