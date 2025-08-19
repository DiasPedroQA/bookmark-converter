# """
# file_controller.py
# -------------------
# Controlador responsável por criar e manipular instâncias do ModeloDeArquivo.
# """

# from pathlib import Path
# from models.arquivo_model import ModeloDeArquivo


# class FileController:
#     """
#     Controller para operações com arquivos.
#     """

#     @staticmethod
#     def create_file(actual_file_path: Path) -> ModeloDeArquivo:
#         """
#         Cria e retorna uma instância de ModeloDeArquivo.
#         """
#         return ModeloDeArquivo(file_path=actual_file_path)

#     @staticmethod
#     def display_file_info(file_obj: ModeloDeArquivo) -> None:
#         """
#         Exibe informações detalhadas sobre o arquivo.
#         """
#         print("\n--- FILE INFO ---")
#         print(f"ID: {file_obj.file_id}")
#         print(f"Nome: {file_obj.file_name}")
#         print(f"Extensão: {file_obj.file_extension}")
#         print(f"Tamanho: {file_obj.file_size_formatted}")
#         print(f"Datas: {file_obj.file_dates}")
#         print(f"Permissões: {file_obj.file_permissions}")
#         print(f"Conteúdo inicial: {file_obj.file_content}")
