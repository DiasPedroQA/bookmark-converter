# """
# main.py
# -------

# Exemplo de uso da FileExplorerController e OSModel.
# """

# from pathlib import Path

# from controllers.os_controller import ExploreNode, FileExplorerController
# from utils.global_tools import FileInfo, SystemInfo


# def main() -> None:
#     """Demonstra o uso da FileExplorerController."""

#     explorer = FileExplorerController()

#     # Mostrar infos do sistema
#     system_info: SystemInfo = explorer.show_system_info()
#     for key, value in system_info.items():
#         print(f"{key}: {value}")
#     print()

#     # Enriquecer arquivo
#     example_file: Path = Path(__file__)
#     enriched_info: FileInfo = explorer.enrich_file_info(file_path=example_file)
#     for key, value in enriched_info.items():
#         print(f"{key}: {value}")
#     print()

#     # Explorar diretório
#     root_dir: Path = Path.home()
#     exploration: ExploreNode = explorer.explore(
#         ext="py",
#         max_depth=2,
#         path=root_dir,
#         tamanho_min=0,
#         tamanho_max=200_000,
#         keyword="test",
#     )

#     # Print recursivo
#     def print_tree(node: ExploreNode, indent: int = 0) -> None:
#         prefix: str = "  " * indent
#         print(f"{prefix}- {node['current']}")
#         for f in node["files"]:
#             print(f"{prefix}  [FILE] {f.get('nome', '???')}")
#         for folder in node["folders"]:
#             print_tree(node=folder, indent=indent + 1)

#     print_tree(exploration)


# if __name__ == "__main__":
#     main()
