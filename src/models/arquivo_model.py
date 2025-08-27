# # FileModel Reformulado com global_tools.py

# """
# Modelo para representar arquivos usando funções auxiliares do global_tools.

# Fornece uma interface limpa para dados de arquivos, delegando todas as operações
# para as funções do global_tools.py mantendo a separação de responsabilidades.
# """

# from datetime import datetime
# from pathlib import Path

# from utils import (
#     file_method_escrever_conteudo_texto,
#     file_method_ler_conteudo_texto,
#     global_method_obter_id_caminho,
#     global_method_check_valid_path,
#     global_method_formatar_tamanho_caminho,
#     global_method_obter_datas_caminho,
#     global_method_obter_nome_caminho,
#     global_method_obter_permissoes_caminho,
#     global_method_obter_tamanho_caminho,
# )


# class FileModel:
#     """Modelo para representação e manipulação de arquivos do sistema.

#     Atributos:
#         id (str): Identificador único baseado no caminho do arquivo
#         name (str): Nome do arquivo com extensão
#         caminho_do_arquivo (Path): Caminho completo do arquivo (acessível via str(self.file_data_caminho_validado))
#         extension (str): Extensões do arquivo (incluindo múltiplas extensões)
#         size_bytes (int): Tamanho em bytes
#         size_formatado (str): Tamanho formatado (ex: "1.23 MB")
#         is_visibel (bool): Se o arquivo não está marcado como oculto
#         dates (dict): Datas de criação, modificação e acesso como datetime
#         permissions (dict): Permissões de leitura, escrita e execução

#     Métodos principais:
#         read_content(): Lê todo o conteúdo do arquivo como texto
#         write_content(): Escreve conteúdo no arquivo
#         to_dict(): Serializa os dados para um dicionário
#     """

#     def __init__(self, caminho_do_arquivo: str | Path) -> None:
#         """
#         Inicializa o modelo com os dados do arquivo.
#         Todas as propriedades são obtidas através das funções do global_tools.

#         Args:
#             caminho_do_arquivo: Caminho para o arquivo (str ou Path)

#         Raises:
#             ValueError: Se o caminho não for um arquivo válido
#             FileNotFoundError: Se o arquivo não existir
#         """
#         self.file_data_caminho_validado: Path = global_method_check_valid_path(caminho_generico=caminho_do_arquivo)
#         self._validate()
#         if not self.file_data_caminho_validado.is_file():
#             raise ValueError(f"Path is not a valid file: {self.file_data_caminho_validado}")

#         # Metadados básicos
#         self.file_data_id: str = global_method_obter_id_caminho(caminho_generico=self.file_data_caminho_validado)
#         self.file_data_name: str = global_method_obter_nome_caminho(caminho_generico=self.file_data_caminho_validado)
#         self.file_data_extension: str = "".join(self.file_data_caminho_validado.suffixes)
#         self.file_data_size_bytes: int = global_method_obter_tamanho_caminho(
#             caminho_generico=self.file_data_caminho_validado
#         )
#         self.file_data_size_formatado: str = global_method_formatar_tamanho_caminho(
#             tamanho_bytes=self.file_data_size_bytes
#         )
#         # self.file_data_is_visibel: bool = global_method_item_e_visivel(caminho_generico=self.file_data_caminho_validado)

#         # Metadados obtidos das funções auxiliares
#         self.file_data_dates: dict[str, datetime] = global_method_obter_datas_caminho(
#             caminho_generico=self.file_data_caminho_validado
#         )
#         self.file_data_permissions: dict[str, bool] = global_method_obter_permissoes_caminho(
#             caminho_generico=self.file_data_caminho_validado
#         )

#     def _validate(self) -> None:
#         """Valida se o caminho é um arquivo válido"""
#         if not self.file_data_caminho_validado.is_file():
#             raise ValueError(f"Path is not a file: {self.file_data_caminho_validado}")

#     def _refresh_metadata(self) -> None:
#         """
#         Atualiza todas as propriedades que podem mudar após modificações
#         no arquivo, usando as funções do global_tools.
#         """
#         self.file_data_size_bytes = global_method_obter_tamanho_caminho(
#             caminho_generico=self.file_data_caminho_validado
#         )
#         self.file_data_size_formatado = global_method_formatar_tamanho_caminho(tamanho_bytes=self.file_data_size_bytes)
#         self.file_data_dates = global_method_obter_datas_caminho(caminho_generico=self.file_data_caminho_validado)
#         self.file_data_permissions = global_method_obter_permissoes_caminho(
#             caminho_generico=self.file_data_caminho_validado
#         )

#     def file_method_read_content(self, encoding: str = "utf-8") -> str:
#         """Lê o conteúdo do arquivo usando file_method_ler_conteudo_texto do global_tools"""
#         return file_method_ler_conteudo_texto(caminho_arquivo=self.file_data_caminho_validado, codificacao=encoding)

#     def file_method_write_content(self, content: str, encoding: str = "utf-8") -> None:
#         """
#         Escreve no arquivo usando file_method_escrever_conteudo_texto do global_tools
#         e atualiza os metadados automaticamente.
#         """
#         file_method_escrever_conteudo_texto(
#             caminho_arquivo=self.file_data_caminho_validado, conteudo=content, codificacao=encoding
#         )
#         self._refresh_metadata()

#     def file_method_to_dict(self) -> dict[str, str | int | bool | dict[str, str] | dict[str, bool]]:
#         """Serializa os dados do arquivo para um dicionário"""
#         return {
#             "id": self.file_data_id,
#             "name": self.file_data_name,
#             "caminho_do_arquivo": str(self.file_data_caminho_validado),
#             "extension": self.file_data_extension,
#             "size_bytes": self.file_data_size_bytes,
#             "size_formatado": self.file_data_size_formatado,
#             # "is_visibel": self.file_data_is_visibel,
#             "dates": {k: v.isoformat() for k, v in self.file_data_dates.items()},
#             "permissions": self.file_data_permissions,
#         }

#     def __repr__(self) -> str:
#         """Representação simples do objeto para debugging"""
#         return f"FileModel(name='{self.file_data_name}', caminho_do_arquivo='{self.file_data_caminho_validado}', size='{self.file_data_size_formatado}')"
