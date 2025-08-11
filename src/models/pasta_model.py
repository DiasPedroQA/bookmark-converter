"""
Módulo que define a classe SistemaPasta para manipulação de diretórios no sistema de arquivos.
Inclui listagem de arquivos e pastas, propriedades como tamanho, permissões, datas, e mais.
"""

import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class SistemaPasta:
    """Classe para representar e manipular informações de uma pasta no sistema de arquivos."""

    caminho_de_pasta: Path

    @property
    def nome(self) -> str:
        """Retorna o nome da pasta."""
        return self.caminho_de_pasta.name

    @property
    def sub_arquivos(self) -> list[Path]:
        """Retorna uma lista de arquivos contidos na pasta (não recursivo)."""
        return [p for p in self.caminho_de_pasta.iterdir() if p.is_file()]

    @property
    def sub_pastas(self) -> list[Path]:
        """Retorna uma lista de subpastas contidas na pasta (não recursivo)."""
        return [p for p in self.caminho_de_pasta.iterdir() if p.is_dir()]

    @property
    def total_arquivos(self) -> int:
        """Retorna o total de arquivos na pasta (não recursivo)."""
        return len(self.sub_arquivos)

    @property
    def total_pastas(self) -> int:
        """Retorna o total de subpastas na pasta (não recursivo)."""
        return len(self.sub_pastas)

    @property
    def tamanho_bytes(self) -> int:
        """Calcula o tamanho total, em bytes, de todos os arquivos dentro da pasta (recursivo)."""
        total = 0
        for p in self.caminho_de_pasta.rglob(pattern="*", case_sensitive=False):
            if p.is_file():
                try:
                    total += p.stat().st_size
                except OSError:
                    pass
        return total

    @property
    def tamanho_formatado(self) -> str:
        """Retorna o tamanho total da pasta em formato legível (KB, MB, etc)."""
        size: int | float = self.tamanho_bytes
        for unidade in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024:
                return f"{size:.2f} {unidade}"
            size /= 1024
        return f"{size:.2f} PB"

    def _profundidade(self, caminho_de_pasta: Path) -> int:
        """Calcula a profundidade de um caminho em relação à pasta base."""
        try:
            return len(caminho_de_pasta.relative_to(self.caminho_de_pasta).parts)
        except ValueError:
            return 0

    def listar_recursivo(self, max_niveis: int = 10) -> dict[str, list[str]]:
        """Lista arquivos e pastas recursivamente até um número máximo de níveis."""
        arquivos, pastas = [], []
        try:
            for item in self.caminho_de_pasta.rglob("*"):
                if self._profundidade(caminho_de_pasta=item) > max_niveis:
                    continue
                if item.is_file() and not item.name.startswith("."):
                    arquivos.append(str(item))
                elif item.is_dir() and not item.name.startswith("."):
                    pastas.append(str(item))
        except OSError as e:
            print(f"Erro ao percorrer pasta: {e}")

        return {"arquivos": arquivos, "pastas": pastas}

    @property
    def datas(self) -> dict[str, datetime]:
        """Retorna um dicionário com as datas de acesso, criação e modificação da pasta."""
        stat: os.stat_result = self.caminho_de_pasta.stat()
        return {
            "data_acesso": datetime.fromtimestamp(stat.st_atime),
            "data_criacao": datetime.fromtimestamp(stat.st_ctime),
            "data_modificacao": datetime.fromtimestamp(stat.st_mtime),
        }

    @property
    def permissoes(self) -> dict[str, bool]:
        """Retorna as permissões de leitura, escrita e execução da pasta."""
        return {
            "leitura": os.access(self.caminho_de_pasta, os.R_OK),
            "escrita": os.access(self.caminho_de_pasta, os.W_OK),
            "execucao": os.access(self.caminho_de_pasta, os.X_OK),
        }

    def informacoes(self) -> dict:
        """Retorna um dicionário com as principais informações da pasta."""
        return {
            "nome": self.nome,
            "caminho": str(self.caminho_de_pasta),
            "datas": self.datas,
            "permissoes": self.permissoes,
            "total_arquivos": self.total_arquivos,
            "total_pastas": self.total_pastas,
            "tamanho_bytes": self.tamanho_bytes,
            "tamanho_formatado": self.tamanho_formatado,
        }
