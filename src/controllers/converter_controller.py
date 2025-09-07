# """
# Módulo de controle para arquivos, pastas e conversão de HTML em outros formatos.
# """

# import logging
# from pathlib import Path
# from typing import Any

# from converters import HtmlToCsvConverter, HtmlToJsonConverter, HtmlToPdfConverter
# from models.file_model import ModeloDeArquivo

# from models.folder_model import ModeloDePasta

# # Setup de log
# logger = logging.getLogger("converter")


# class FileController:
#     """Responsável por criar instâncias de ModeloDeArquivo."""

#     @staticmethod
#     def create_file(actual_file_path: Path) -> ModeloDeArquivo:
#         return ModeloDeArquivo(file_path=actual_file_path)


# class FolderController:
#     """Responsável por criar instâncias de ModeloDePasta."""

#     @staticmethod
#     def create_folder(actual_folder_path: Path) -> ModeloDePasta:
#         return ModeloDePasta(folder_path=actual_folder_path)


# class InfoViewer:
#     """Exibe informações de arquivos e pastas (para debug/monitoramento)."""

#     @staticmethod
#     def display_file_info(file_obj: ModeloDeArquivo) -> None:
#         logger.info(
#             "Arquivo [ID=%s, Nome=%s, Extensão=%s, Tamanho=%s]",
#             file_obj.file_id,
#             file_obj.file_name,
#             file_obj.file_extension,
#             file_obj.file_size_formatted,
#         )

#     @staticmethod
#     def display_folder_info(folder_obj: ModeloDePasta) -> None:
#         logger.info(
#             "Pasta [ID=%s, Nome=%s, Tamanho=%s, Subarquivos=%s, Subpastas=%s]",
#             folder_obj.id_folder,
#             folder_obj.name_folder,
#             folder_obj.size_formatted_folder,
#             folder_obj.subfiles_folder,
#             folder_obj.subfolders_folder,
#         )


# class ConversionController:
#     """Orquestra a conversão de arquivos HTML para outros formatos."""

#     converters = {
#         "pdf": HtmlToPdfConverter(),
#         "csv": HtmlToCsvConverter(),
#         "json": HtmlToJsonConverter(),
#     }

#     @classmethod
#     def convert(cls, file_obj: ModeloDeArquivo, formats: list[str]) -> dict[str, Any]:
#         if file_obj.file_extension.lower() != ".html":
#             raise ValueError("Apenas arquivos HTML são suportados")

#         results: dict[str, Any] = {}
#         errors: list[str] = []

#         for fmt in formats:
#             converter = cls.converters.get(fmt)
#             if not converter:
#                 errors.append(f"{fmt}: formato não suportado")
#                 continue

#             try:
#                 results[fmt] = converter.convert(file_obj.file_content)
#             except (ValueError, RuntimeError) as e:
#                 # Captura exceções específicas, não Exception genérico
#                 logger.error("Erro ao converter %s → %s: %s", file_obj.file_name, fmt, e)
#                 errors.append(f"{fmt}: {str(e)}")

#         logger.info("Resumo conversão: %s", errors or "tudo OK")
#         return results
