"""
Modelo de dados para representar e manipular arquivos do sistema operacional.
Inclui nome, caminho, extensão, tamanho, datas, permissões e conteúdo do arquivo.
"""

import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class SistemaArquivo:
    """
    Representa um arquivo no sistema de arquivos.

    Atributos:
        caminho_de_arquivo (Path): Caminho absoluto do arquivo.
    """

    caminho_de_arquivo: Path

    @property
    def nome(self) -> str:
        """Nome do arquivo."""
        return self.caminho_de_arquivo.name

    @property
    def extensao(self) -> list[str]:
        """Extensão do arquivo, incluindo o ponto (ex: .txt)."""
        return self.caminho_de_arquivo.suffixes

    @property
    def tamanho_bytes(self) -> int:
        """Tamanho do arquivo em bytes."""
        return self.caminho_de_arquivo.stat().st_size

    @property
    def tamanho_formatado(self) -> str:
        """
        Tamanho do arquivo formatado de forma legível (ex: 2.34 MB).

        Returns:
            str: Tamanho formatado com unidade.
        """
        size: int | float = self.tamanho_bytes
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
        stat: os.stat_result = self.caminho_de_arquivo.stat()
        return {
            "data_acesso": datetime.fromtimestamp(stat.st_atime),
            "data_criacao": datetime.fromtimestamp(stat.st_ctime),
            "data_modificacao": datetime.fromtimestamp(stat.st_mtime),
        }

    @property
    def permissoes(self) -> dict[str, bool]:
        """
        Permissões do arquivo para leitura, escrita e execução.

        Returns:
            dict[str, bool]: Dicionário com chaves leitura, escrita e execução.
        """
        return {
            "leitura": os.access(self.caminho_de_arquivo, os.R_OK),
            "escrita": os.access(self.caminho_de_arquivo, os.W_OK),
            "execucao": os.access(self.caminho_de_arquivo, os.X_OK),
        }

    @property
    def conteudo(self) -> str | None:
        """
        Tenta ler o conteúdo do arquivo como texto (UTF-8).

        Returns:
            str | None: Conteúdo textual ou None se for muito grande ou ilegível.
        """
        try:
            if self.tamanho_bytes > 1024 * 1024:  # Evita abrir arquivos muito grandes
                return None
            return self.caminho_de_arquivo.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            return None

    def informacoes(self) -> dict:
        """
        Retorna uma representação completa do arquivo em formato de dicionário.

        Returns:
            dict: Dicionário com todas as informações relevantes do arquivo.
        """
        return {
            "nome": self.nome,
            "caminho": str(self.caminho_de_arquivo),
            "extensao": self.extensao,
            "tamanho_bytes": self.tamanho_bytes,
            "tamanho_formatado": self.tamanho_formatado,
            "datas": self.datas,
            "permissoes": self.permissoes,
            "conteudo": self.conteudo,
        }
