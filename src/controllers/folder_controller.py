# """
# folder_controller.py
# ---------------------
# Controlador responsável por criar e manipular instâncias do ModeloDePasta.
# """

# from pathlib import Path
# from models.folder_model import ModeloDePasta


# class FolderController:
#     """
#     Controller para operações com pastas.
#     """

#     @staticmethod
#     def create_folder(actual_folder_path: Path) -> ModeloDePasta:
#         """
#         Cria e retorna uma instância de ModeloDePasta.
#         """
#         return ModeloDePasta(folder_path=actual_folder_path)

#     @staticmethod
#     def display_folder_info(folder_obj: ModeloDePasta) -> None:
#         """
#         Exibe informações detalhadas sobre a pasta.
#         """
#         print("\n--- FOLDER INFO ---")
#         print(f"Nome: {folder_obj.name_folder}")
#         print(f"ID: {folder_obj.id_folder}")
#         print(f"Tamanho: {folder_obj.size_formatted_folder}")
#         print(f"Datas: {folder_obj.dates_folder}")
#         print(f"Permissões: {folder_obj.permissions_folder}")
#         print(f"Subarquivos: {folder_obj.subfiles_folder}")
#         print(f"Subpastas: {folder_obj.subfolders_folder}")
