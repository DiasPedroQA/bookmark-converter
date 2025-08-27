# """
# file_explorer_controller.py
# ---------------------------

# Controller avançada para exploração hierárquica de arquivos e pastas,
# herdando dados do sistema operacional via OSModel.

# Funcionalidades:
# - Exploração recursiva de arquivos e pastas.
# - Filtragem por extensão, tamanho e palavra-chave no nome.
# - Ignora arquivos/pastas ocultos.
# - Enriquecimento de informações de cada arquivo/pasta usando global_tools.
# - Exibição de informações do sistema (OSModel) diretamente pela controller.
# """

# from __future__ import annotations

# import logging
# from pathlib import Path
# from typing import TypedDict

# from models.os_model import OSModel
# from utils.global_tools import (
#     FileInfo,
#     RawFileInfo,
#     SystemInfo,
#     global_method_formatar_infos_caminho,
#     global_method_infos_caminho,
# )
# from utils.system_tools import (
#     folder_method_buscar_apenas_pastas,
#     folder_method_buscar_arquivos_por_extensoes,
# )

# logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")


# class ExploreNode(TypedDict):
#     """Nó da árvore de exploração de diretórios."""

#     current: str
#     files: list[FileInfo]
#     folders: list["ExploreNode"]


# class FileExplorerController(OSModel):
#     """Controller que explora arquivos/pastas de forma hierárquica e filtrada.

#     Herda de OSModel, fornecendo informações do sistema operacional, IP, home do usuário e disco.
#     """

#     def __init__(self, root: str | Path | None = None) -> None:
#         """Inicializa a controller com base no caminho root ou no home do usuário."""
#         if root is None:
#             root = Path.home()
#         super().__init__(root=root)

#     def show_system_info(self) -> SystemInfo:
#         """Retorna todas as informações do sistema disponíveis no OSModel."""
#         return self.to_dict()

#     def enrich_file_info(self, file_path: str | Path) -> FileInfo:
#         """Enriquece um arquivo/pasta com informações detalhadas formatadas."""
#         infos: RawFileInfo = global_method_infos_caminho(caminho_generico=file_path)
#         return global_method_formatar_infos_caminho(infos=infos)

#     def explore(
#         self,
#         path: str | Path | None = None,
#         ext: str | None = None,
#         max_depth: int | None = None,
#         current_depth: int = 0,
#         tamanho_min: int = 0,
#         tamanho_max: int | None = None,
#         keyword: str | None = None,
#     ) -> ExploreNode:
#         """
#         Explora arquivos e pastas de forma hierárquica a partir de path (ou self.home por default).

#         Args:
#             path: Caminho inicial de exploração (default = self.home).
#             ext: Extensão dos arquivos a buscar (ex: "py"). None = sem filtro.
#             max_depth: Profundidade máxima da recursão. None = ilimitado.
#             current_depth: Profundidade atual (interno).
#             tamanho_min: Tamanho mínimo do arquivo em bytes.
#             tamanho_max: Tamanho máximo do arquivo em bytes.
#             keyword: Palavra-chave que deve estar no nome do arquivo/pasta.

#         Returns:
#             ExploreNode: Estrutura hierárquica com arquivos e subpastas.
#         """
#         p: Path = self.home if path is None else Path(path)
#         node: ExploreNode = {"current": str(p), "files": [], "folders": []}

#         # Condição de parada
#         if not p.exists() or not p.is_dir():
#             return node
#         if max_depth is not None and current_depth > max_depth:
#             return node

#         try:
#             # Se filtro de extensão foi passado -> busca customizada
#             arquivos: list[Path]
#             if ext:
#                 ext = f".{ext.lstrip('.').lower()}"
#                 arquivos = folder_method_buscar_arquivos_por_extensoes(pasta_base=p, extensoes=[ext])
#             else:
#                 arquivos = [f for f in p.iterdir() if f.is_file()]

#             # Aplicar filtros adicionais
#             arquivos_filtrados: list[Path] = []
#             for f in arquivos:
#                 try:
#                     tamanho: int = f.stat().st_size
#                 except OSError:
#                     continue

#                 if tamanho < tamanho_min or (tamanho_max and tamanho > tamanho_max):
#                     continue
#                 if keyword and keyword.lower() not in f.name.lower():
#                     continue
#                 arquivos_filtrados.append(f)

#             # Enriquecer arquivos
#             for f in arquivos_filtrados:
#                 node["files"].append(self.enrich_file_info(file_path=f))

#             # Recursão em subpastas
#             pastas: list[Path] = folder_method_buscar_apenas_pastas(itens=list(p.iterdir()))
#             for sub in pastas:
#                 if sub.name.startswith("."):
#                     continue
#                 sub_node: ExploreNode = self.explore(
#                     path=sub,
#                     ext=ext,
#                     max_depth=max_depth,
#                     current_depth=current_depth + 1,
#                     tamanho_min=tamanho_min,
#                     tamanho_max=tamanho_max,
#                     keyword=keyword,
#                 )
#                 node["folders"].append(sub_node)

#         except PermissionError as e:
#             logging.warning(msg=f"Sem permissão: {e}")
#         except FileNotFoundError as e:
#             logging.warning(msg=f"Pasta não encontrada: {e}")

#         return node
