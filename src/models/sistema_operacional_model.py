"""
Módulo sistema_operacional_model.py

Modelo que representa o sistema operacional local, suas informações básicas
e oferece métodos para listar arquivos, pastas e validar caminhos com base nas regras do SO.

Utiliza funções utilitárias de:
- sistema_arquivos (filtros, buscas por extensão)
- sistema_pastas (filtros, listagem recursiva de pastas vazias)
- main_tools (normalização de caminhos)
- utils_so (validação de permissões e formatos de caminho)
"""

import platform
from dataclasses import dataclass, field
from getpass import getuser
from pathlib import Path

from models.arquivo_model import ModeloDeArquivo
from models.pasta_model import ModeloDePasta
from utils.folder_tools import (
    list_empty_folders,
    search_by_extension,
)
from utils.main_tools import (
    is_hidden_path,
)


@dataclass(frozen=True, slots=True)
class SistemaOperacional:
    """
    Representa o sistema operacional local e provê métodos para manipular o sistema
    de arquivos do usuário atual, incluindo listagens e validações.

    Attributes:
        nome_so (str): Nome do sistema operacional.
        versao (str): Versão do sistema operacional.
        usuario_logado (str): Nome do usuário logado.
        pasta_usuario (Path): Diretório home do usuário.
        arquitetura (str): Arquitetura da máquina (ex: '64bit').
    """

    nome_so: str = field(default_factory=platform.system)
    versao: str = field(default_factory=platform.version)
    usuario_logado: str = field(default_factory=getuser)
    pasta_usuario: Path = field(default_factory=Path.home)
    arquitetura: str = field(default_factory=lambda: platform.architecture()[0])

    @property
    def arquivos_publicos(self) -> list[ModeloDeArquivo]:
        """
        Lista os arquivos visíveis (não ocultos) na pasta home do usuário,
        representados como objetos ModeloDeArquivo.

        Returns:
            list[ModeloDeArquivo]: Lista de arquivos.
        """
        try:
            itens: list[Path] = [
                p for p in self.pasta_usuario.iterdir() if p.is_file() and not is_hidden_path(path_neutral=p)
            ]
            return [ModeloDeArquivo(file_path=p) for p in itens]
        except PermissionError:
            return []

    @property
    def pastas_publicas(self) -> list[ModeloDePasta]:
        """
        Lista as pastas visíveis (não ocultas) na pasta home do usuário,
        representadas como objetos ModeloDePasta.

        Returns:
            list[ModeloDePasta]: Lista de pastas.
        """
        try:
            return [
                ModeloDePasta(folder_path=p)
                for p in self.pasta_usuario.iterdir()
                if p.is_dir() and not is_hidden_path(path_neutral=p)
            ]
        except PermissionError:
            return []

    def listar_pastas_vazias_home(self) -> list[Path]:
        """
        Retorna todas as pastas vazias dentro da pasta home, recursivamente.

        Returns:
            list[Path]: Pastas vazias.
        """
        try:
            return list_empty_folders(base_folder=self.pasta_usuario)
        except PermissionError:
            return []

    def listar_maiores_arquivos_home(self, qnte_lim_files: int = 5):
        """
        Retorna os maiores arquivos da pasta home, limitados pela quantidade passada.

        Args:
            qnte_lim_files (int): Quantidade limite de arquivos a retornar.

        Returns:
            list[Path]: Lista dos maiores arquivos.
        """
        try:
            arquivos: list[ModeloDeArquivo] = [
                ModeloDeArquivo(file_path=p)
                for p in self.pasta_usuario.iterdir()
                if p.is_file() and not is_hidden_path(path_neutral=p)
            ]
            return sorted(arquivos, key=lambda p: p.file_path.stat().st_size, reverse=True)[:qnte_lim_files]
        except PermissionError:
            return []

    def buscar_por_extensao_home(self, extensao: str) -> list[Path]:
        """
        Busca arquivos na pasta home que tenham a extensão especificada (case-insensitive).

        Args:
            extensao (str): Extensão do arquivo (ex: '.txt').

        Returns:
            list[Path]: Lista de arquivos encontrados.
        """
        try:
            return search_by_extension(base_folder=self.pasta_usuario, extension=extensao)
        except PermissionError:
            return []

    def informacoes(self) -> dict[str, str | list[str]]:
        """
        Retorna informações básicas do sistema operacional, usuário e arquivos/pastas públicos.

        Returns:
            Dict[str, Union[str, list[str]]]: Dicionário com as informações.
        """
        return {
            "nome_so": self.nome_so,
            "versao": self.versao,
            "usuario_logado": self.usuario_logado,
            "pasta_usuario": str(self.pasta_usuario),
            "arquitetura": self.arquitetura,
            "arquivos_publicos": [str(arquivo.file_path) for arquivo in self.arquivos_publicos],
            "pastas_publicas": [str(pasta.folder_path) for pasta in self.pastas_publicas],
        }
