"""
Modelo para representar e manipular arquivos no sistema operacional.

Fornece propriedades e métodos para acessar informações detalhadas sobre
nome, caminho, extensão, tamanho, datas, permissões e conteúdo.
Ideal para uso em controllers ou serviços que precisem
de dados completos sobre um arquivo.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from utils.file_tools import read_text_content, write_text_content
from utils.main_tools import (
    get_dates_path,
    get_id_path,
    get_name_path,
    get_permissions_path,
    get_size_path,
    is_hidden_path,
    validate_path,
)


@dataclass(frozen=True, slots=True)
class ModeloDeArquivo:
    """
    Representa um arquivo no sistema de arquivos.

    Atributos:
        file_path (Path): Caminho absoluto do arquivo. Validado na inicialização.
    """

    file_path: Path

    def __post_init__(self) -> None:
        """
        Valida se o caminho existe e aponta para um arquivo real.

        Levanta:
            FileNotFoundError: Se o caminho não existir ou não for um arquivo.
        """
        caminho_validado: Path = validate_path(path_neutral=self.file_path)
        if not Path(caminho_validado).is_file():
            raise FileNotFoundError(f"Arquivo não encontrado: {self.file_path}")

    @property
    def file_name(self) -> str:
        """
        Retorna o nome do arquivo sem o caminho.

        Returns:
            str: Nome do arquivo.
        """
        return get_name_path(path_neutral=self.file_path)

    @property
    def file_id(self) -> str:
        """
        Retorna um identificador único baseado no caminho.

        Returns:
            str: ID único do arquivo.
        """
        return get_id_path(path_neutral=self.file_path)

    @property
    def file_extension(self) -> str | list[str]:
        """
        Retorna a extensão do arquivo.

        Returns:
            str | list[str]: Extensão única (ex: ".txt") ou lista de extensões
            para arquivos com múltiplos sufixos (ex: ".tar.gz").
        """
        sufixos: list[str] = self.file_path.suffixes
        return sufixos[-1] if len(sufixos) == 1 else sufixos

    @property
    def file_size_formatted(self) -> str:
        """
        Retorna o tamanho do arquivo em formato legível.

        Returns:
            str: Tamanho formatado (ex: "2.34 MB").
        """
        size: int | float = get_size_path(path_neutral=self.file_path)
        for unidade in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024:
                return f"{size:.2f} {unidade}"
            size /= 1024
        return f"{size:.2f} PB"

    @property
    def file_dates(self) -> dict[str, datetime]:
        """
        Retorna as datas associadas ao arquivo.

        Returns:
            dict[str, datetime]: Datas de criação, modificação e último acesso.
        """
        return get_dates_path(path_neutral=self.file_path)

    @property
    def file_permissions(self) -> dict[str, bool]:
        """
        Retorna as permissões de leitura, escrita e execução.

        Returns:
            dict[str, bool]: Dicionário com permissões.
        """
        return get_permissions_path(path_neutral=self.file_path)

    @property
    def file_content(self) -> str:
        """
        Lê o conteúdo do arquivo como texto.

        Returns:
            str: Conteúdo textual do arquivo.
        """
        return read_text_content(file_path=self.file_path)

    def file_write_content(self, new_content: str) -> None:
        """
        Sobrescreve o conteúdo do arquivo com novo texto.

        Args:
            new_content (str): Novo conteúdo a ser gravado.

        Raises:
            PermissionError: Se não houver permissão de escrita.
            FileNotFoundError: Se o arquivo não existir.
            OSError: Para outros erros de E/S.
        """
        try:
            write_text_content(file_path=self.file_path, content=new_content)
        except PermissionError as e:
            raise PermissionError(f"Permissão negada para escrever no arquivo: {self.file_path}") from e
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Arquivo não encontrado: {self.file_path}") from e
        except OSError as e:
            raise OSError(f"Erro ao escrever no arquivo {self.file_path}: {e.strerror}") from e

    def file_info(self) -> dict[str, str | Path | list[str] | dict[str, datetime] | dict[str, bool]]:
        """
        Retorna um dicionário com todas as informações relevantes do arquivo.

        Ignora arquivos ocultos.

        Returns:
            dict: Informações completas do arquivo ou vazio se oculto.
        """
        if is_hidden_path(path_neutral=self.file_path):
            return {}
        return {
            "file_id": self.file_id,
            "file_name": self.file_name,
            "file_path": str(self.file_path),
            "file_extension": self.file_extension,
            "file_size_formatted": self.file_size_formatted,
            "file_dates": self.file_dates,
            "file_permissions": self.file_permissions,
        }
