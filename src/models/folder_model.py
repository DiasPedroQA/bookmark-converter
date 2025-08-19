# # FolderModel Reformulado com global_tools.py

# """
# FolderModel reformulado.

# Representa pastas do sistema e fornece métodos para buscar arquivos,
# subpastas e metadados, usando utilitários de global_tools.py.
# """

# from __future__ import annotations

# from datetime import datetime
# from pathlib import Path

# from utils.global_tools import (
#     global_method_check_valid_path,
#     global_method_formatar_tamanho_caminho,
#     global_method_obter_datas_caminho,
#     global_method_obter_id_caminho,
#     global_method_obter_nome_caminho,
#     global_method_obter_permissoes_caminho,
#     global_method_obter_tamanho_caminho,
# )


# class FolderModel:
#     """Representa uma pasta no sistema de arquivos."""

#     def __init__(self, caminho_da_pasta: str | Path) -> None:
#         """
#         Docstring para __init__

#         :param self: Descrição
#         :param caminho_da_pasta: Descrição
#         :type caminho_da_pasta: str | Path
#         """
#         self.folder_data_caminho_validado: Path = global_method_check_valid_path(caminho_generico=caminho_da_pasta)
#         if not self.folder_data_caminho_validado.is_dir():
#             raise ValueError(f"Path is not a directory: {self.folder_data_caminho_validado}")

#         # Metadados básicos
#         self.folder_data_id: str = global_method_obter_id_caminho(caminho_generico=self.folder_data_caminho_validado)
#         self.folder_data_name: str = global_method_obter_nome_caminho(
#             caminho_generico=self.folder_data_caminho_validado
#         )
#         self.folder_data_size_bytes: int = global_method_obter_tamanho_caminho(
#             caminho_generico=self.folder_data_caminho_validado
#         )
#         self.folder_data_size_formatado: str = global_method_formatar_tamanho_caminho(
#             tamanho_bytes=global_method_obter_tamanho_caminho(caminho_generico=self.folder_data_caminho_validado)
#         )
#         self.folder_data_dates: dict[str, datetime] = global_method_obter_datas_caminho(
#             caminho_generico=self.folder_data_caminho_validado
#         )
#         self.folder_data_permissions: dict[str, bool] = global_method_obter_permissoes_caminho(
#             caminho_generico=self.folder_data_caminho_validado
#         )

#         # Conteúdos da pasta
#         self._content_loaded: bool = False
#         self._files: list[Path] = []
#         self._subfolders: list[Path] = []

#         # Contagem de itens
#         self.total_files: int = 0
#         self.total_subfolders: int = 0

#     def __repr__(self) -> str:
#         """Mostra pasta + contagem de arquivos e subpastas carregados."""
#         return (
#             f"<FolderModel (tamanho={self.folder_data_size_formatado}, caminho={self.folder_data_caminho_validado}) >"
#         )

#     def load_content(self) -> None:
#         """
#         Docstring para load_content

#         :param self: Descrição
#         """
#         if not self._content_loaded:
#             folders_childs: list[Path] = folder_method_buscar_filhos(pasta=self.folder_data_caminho_validado)
#             subpastas: list[Path] = folder_method_buscar_apenas_pastas(itens=folders_childs)
#             subarquivos: list[Path] = folder_method_buscar_apenas_arquivos(itens=folders_childs)

#             self._files: list[Path] = subarquivos
#             self.total_files: int = len(subarquivos)

#             self._subfolders: list[Path] = subpastas
#             self.total_subfolders: int = len(subpastas)

#             self._content_loaded: bool = True
