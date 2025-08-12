"""
Modelo para representar e manipular pastas no sistema de arquivos.

Fornece propriedades e métodos para acessar informações detalhadas sobre
nome, caminho, tamanho, datas, permissões, subarquivos e subpastas.
Também permite listagem recursiva limitada por profundidade.
Ideal para uso em controllers ou serviços que precisem
de dados completos sobre um diretório.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from utils.main_tools import (
    get_dates_path,
    get_id_path,
    get_name_path,
    get_permissions_path,
    get_size_path,
    validate_path,
)

from utils.folder_tools import (
    filter_for_folders,
    filter_for_files,
    list_all_non_empty_children,
    list_empty_folders,
    calculate_depth,
    search_by_extension,
)


@dataclass(frozen=True, slots=True)
class ModeloDePasta:
    """
    Representa uma pasta no sistema de arquivos, fornecendo métodos e
    propriedades para acessar informações detalhadas sobre seu conteúdo,
    tamanho, permissões, datas e busca recursiva.

    Attributes:
        folder_path (Path): Caminho absoluto da pasta. Validado na inicialização.
    """

    folder_path: Path

    def __post_init__(self) -> None:
        """
        Valida se o caminho existe e é uma pasta válida.

        Raises:
            NotADirectoryError: Se o caminho não for uma pasta válida.
        """
        caminho_validado: Path = validate_path(path_neutral=self.folder_path)
        if not caminho_validado.is_dir():
            raise NotADirectoryError(f"Pasta não encontrada: {self.folder_path}")

    @property
    def folder_name(self) -> str:
        """
        Obtém o nome da pasta.

        Returns:
            str: Nome da pasta.
        """
        return get_name_path(path_neutral=self.folder_path)

    @property
    def folder_id(self) -> str:
        """
        Obtém um identificador único baseado no caminho da pasta.

        Returns:
            str: ID único da pasta.
        """
        return get_id_path(path_neutral=self.folder_path)

    @property
    def folder_size_formatted(self) -> str:
        """
        Obtém o tamanho total da pasta em formato legível.

        Returns:
            str: Tamanho formatado (ex: "2.34 MB").
        """
        size: int | float = get_size_path(path_neutral=self.folder_path)
        for unidade in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024:
                return f"{size:.2f} {unidade}"
            size /= 1024
        return f"{size:.2f} PB"

    @property
    def folder_dates(self) -> dict[str, datetime]:
        """
        Obtém as datas associadas à pasta.

        Returns:
            dict[str, datetime]: Datas de criação, modificação e último acesso.
        """
        return get_dates_path(path_neutral=self.folder_path)

    @property
    def folder_permissions(self) -> dict[str, bool]:
        """
        Obtém as permissões da pasta.

        Returns:
            dict[str, bool]: Permissões de leitura, escrita e execução.
        """
        return get_permissions_path(path_neutral=self.folder_path)

    @property
    def folder_subfiles(self) -> list[Path]:
        """
        Lista os arquivos diretamente dentro da pasta (não recursivo),
        ignorando arquivos ocultos.

        Returns:
            list[Path]: Lista de arquivos.
        """
        children: list[Path] = list_all_non_empty_children(self.folder_path, ignore_hidden=True)
        return filter_for_files(children)

    @property
    def folder_subfolders(self) -> list[Path]:
        """
        Lista as subpastas diretamente dentro da pasta (não recursivo),
        ignorando pastas ocultas e vazias.

        Returns:
            list[Path]: Lista de subpastas.
        """
        children: list[Path] = list_all_non_empty_children(self.folder_path, ignore_hidden=True)
        return filter_for_folders(children)

    def folder_empty_subfolders(self) -> list[Path]:
        """
        Lista as subpastas vazias dentro da pasta.

        Returns:
            list[Path]: Lista de subpastas vazias.
        """
        return list_empty_folders(base_folder=self.folder_path)

    def folder_depth(self) -> int:
        """
        Calcula a profundidade máxima da árvore de diretórios a partir da pasta.

        Returns:
            int: Profundidade máxima (0 se inválida).
        """
        return calculate_depth(self.folder_path)

    def folder_search_by_extension(self, extension: str) -> list[Path]:
        """
        Busca arquivos na pasta base com a extensão especificada (case-insensitive).
        Suporta extensões compostas como '.tar.gz'.

        Args:
            extension (str): Extensão, ex: '.txt' ou '.tar.gz'.

        Returns:
            list[Path]: Arquivos correspondentes.
        """
        return search_by_extension(self.folder_path, extension)

    def _folder_depth(self, path: Path) -> int:
        """
        Calcula a profundidade de um caminho em relação à pasta base.

        Args:
            path (Path): Caminho a ser analisado.

        Returns:
            int: Nível de profundidade.
        """
        try:
            return len(path.relative_to(self.folder_path).parts)
        except ValueError:
            return 0

    def folder_list_recursive(self, max_levels: int = 10) -> dict[str, list[str]]:
        """
        Lista arquivos e pastas recursivamente até um número máximo de níveis,
        ignorando arquivos e pastas ocultos.

        Args:
            max_levels (int): Profundidade máxima para listagem.

        Returns:
            dict[str, list[str]]: Dicionário com listas de arquivos e pastas.
        """
        arquivos: list[str] = []
        pastas: list[str] = []
        for item in self.folder_path.rglob(pattern="*"):
            if self._folder_depth(path=item) > max_levels:
                continue
            if item.is_file() and not item.name.startswith("."):
                arquivos.append(str(item))
            elif item.is_dir() and not item.name.startswith("."):
                pastas.append(str(item))
        return {"folder_files": arquivos, "folder_folders": pastas}

    def folder_info(
        self,
    ) -> dict[str, str | dict[str, datetime] | dict[str, bool] | list[Path] | int | dict[str, list[str]]]:
        """
        Retorna um dicionário com as principais informações da pasta.

        Returns:
            dict: Informações completas da pasta.
        """
        return {
            "folder_id": self.folder_id,
            "folder_name": self.folder_name,
            "folder_path": str(self.folder_path),
            "folder_size_formatted": self.folder_size_formatted,
            "folder_dates": self.folder_dates,
            "folder_permissions": self.folder_permissions,
            "folder_subfiles": self.folder_subfiles,
            "folder_subfolders": self.folder_subfolders,
            "folder_empty_subfolders": self.folder_empty_subfolders(),
            "folder_depth": self.folder_depth(),
            "folder_list_recursive": self.folder_list_recursive(max_levels=10),
        }
