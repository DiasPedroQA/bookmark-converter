"""
Modelo de dados para representar e manipular arquivos do sistema operacional.
Inclui nome, caminho, extensão, tamanho, datas, permissões e conteúdo do arquivo.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from src.utils.file_tools import read_text_content
from src.utils.main_tools import (
    get_dates,
    get_id,
    get_name,
    get_permissions,
    get_size,
    is_hidden_path,
    validate_path,
)


@dataclass
class ModeloDeArquivo:
    """
    Representa um arquivo no sistema de arquivos.

    Atributos:
        caminho_de_arquivo (Path): Caminho absoluto do arquivo.
    """

    caminho_de_arquivo: Path

    @property
    def nome(self) -> str:
        """Nome do arquivo."""
        return get_name(path_neutral=self.caminho_de_arquivo)

    @property
    def id_arquivo(self) -> str:
        """Id do arquivo."""
        return get_id(path_neutral=self.caminho_de_arquivo)

    @property
    def extensao(self) -> list[str]:
        """Extensão do arquivo, incluindo o ponto (ex: .txt)."""
        return self.caminho_de_arquivo.suffixes

    @property
    def tamanho_formatado(self) -> str:
        """
        Tamanho do arquivo formatado de forma legível (ex: 2.34 MB).

        Returns:
            str: Tamanho formatado com unidade.
        """
        size: int | float = get_size(path_neutral=self.caminho_de_arquivo)
        for unidade in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024:
                return f"{size:.2f} {unidade}"
            size /= 1024
        return f"{size:.2f} PB"

    @property
    def datas(self) -> dict[str, datetime]:
        """
        Datas importantes relacionadas ao arquivo.

        Returns:
            dict[str, datetime]: Datas de acesso, criação e modificação.
        """
        return get_dates(path_neutral=self.caminho_de_arquivo)

    @property
    def permissoes(self) -> dict[str, bool]:
        """
        Permissões do arquivo para leitura, escrita e execução.

        Returns:
            dict[str, bool]: Dicionário com chaves leitura, escrita e execução.
        """
        return get_permissions(path_neutral=self.caminho_de_arquivo)

    @property
    def conteudo(self) -> str:
        """
        Tenta ler o conteúdo do arquivo como texto (UTF-8).

        Returns:
            str: Conteúdo textual do arquivo.
        """
        return read_text_content(file_path=self.caminho_de_arquivo)

    def informacoes(self) -> dict[str, str | Path | list[str] | dict[str, datetime] | dict[str, bool]] | None:
        """
        Retorna uma representação completa do arquivo em formato de dicionário.

        Returns:
            dict: Dicionário com todas as informações relevantes do arquivo.
        """
        if not is_hidden_path(path_neutral=self.caminho_de_arquivo):
            return {
                "nome": self.nome,
                "caminho": validate_path(path_neutral=self.caminho_de_arquivo),
                "extensao": self.extensao,
                "tamanho_formatado": self.tamanho_formatado,
                "datas": self.datas,
                "permissoes": self.permissoes,
                "conteudo": self.conteudo,
            }
        return None
