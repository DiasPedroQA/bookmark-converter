# """main.py"""

# from models import FolderModel, OSModel

# sistema_atual = OSModel()

# sys_path: str = sistema_atual.sys_data_user_home

# user_root_folder = FolderModel(caminho_da_pasta=sys_path)


# print(f"\n - __repr__ => {sistema_atual}")
# # print(f"\n - get_system_info => {sistema_atual.so_method_obter_info_so()}")
# print(f"\n - user_root_folder => {user_root_folder}")


# print(f"\n - folder_data_caminho_validado => {user_root_folder.folder_data_caminho_validado}")

# print(f"\n - folder_data_id => {user_root_folder.folder_data_id}")

# print(f"\n - folder_data_name => {user_root_folder.folder_data_name}")

# print(f"\n - folder_data_size_bytes => {user_root_folder.folder_data_size_bytes}")

# print(f"\n - folder_data_size_formatado => {user_root_folder.folder_data_size_formatado}")

# print(f"\n - folder_data_is_visibel => {user_root_folder.folder_data_is_visibel}")

# print(f"\n - folder_data_dates => {user_root_folder.folder_data_dates}")

# print(f"\n - folder_data_permissions => {user_root_folder.folder_data_permissions}")



# print("\n", user_root_folder._content_loaded)
# print("\n", user_root_folder._files)
# print("\n", user_root_folder._subfolders)
# print("\n", user_root_folder.total_files)
# print("\n", user_root_folder.total_subfolders)


#  ------------------------------------------------------------------------------------------------------------
#  ------------------------------------------------------------------------------------------------------------
#  ------------------------------------------------------------------------------------------------------------
#  ------------------------------------------------------------------------------------------------------------



# if __name__ == "__main__":
#     test_file = FileModel(caminho_do_arquivo="/home/pedro-pm-dias/teste.html")

#     print("\n", test_file)
#     print("\n", test_file.file_method_to_dict())
#     print("\n", test_file.file_method_read_content())
#     test_file.file_method_write_content(
#         content="""<!DOCTYPE html>
#     <html lang="pt-br">

#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>Documento Atualizado 42</title>
#     </head>

#     <body><h1>ATUALIZADO 42</h1></body>
#     </html>"""
#     )
#     print("\n", test_file.file_method_read_content())

# # Caminho da pasta que queremos explorar
# pasta_path = Path("/home/pedro-pm-dias/Downloads/Firefox")

# # Cria a instância da pasta
# pasta = FolderModel(caminho_da_pasta=pasta_path)

# # -----------------------------
# # Carregar conteúdo recursivamente
# # -----------------------------
# pasta.folder_method_load_content(recursive=True, exclude_hidden=True, max_depth=3)

# # -----------------------------
# # Acessar arquivos
# # -----------------------------
# arquivos: list[FileModel] = pasta.folder_method_get_files()
# for arquivo in arquivos:
#     print("\n", arquivo)

# # -----------------------------
# # Acessar subpastas
# # -----------------------------
# subpastas: list[FolderModel] = pasta.folder_method_get_subfolders()
# for sub in subpastas:
#     print("\n", sub)

# # -----------------------------
# # Resumo da pasta
# # -----------------------------
# resumo: dict[str, int] = pasta.folder_method_get_content_inicial()
# print(f"Total de arquivos: {resumo['files']}")
# print(f"Total de subpastas: {resumo['folders']}")

# # -----------------------------
# # Tamanho total
# # -----------------------------
# print(f"Tamanho total da pasta: {pasta.folder_method_get_total_size()} bytes")

# # -----------------------------
# # Converter para dicionário
# # -----------------------------
# pasta_dict: dict[str, str | bool | dict[str, str] | dict[str, bool] | int | list[dict] | None] = (
#     pasta.folder_method_to_dict(folder=pasta, recursive=True)
# )


# # Visualização organizada
# # print(json.dumps(pasta_dict, indent=4, ensure_ascii=False))


# print(pasta.folder_method_is_empty())
# print(pasta.folder_method_get_total_size())
