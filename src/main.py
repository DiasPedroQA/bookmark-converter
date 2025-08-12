# main.py

"""
Ponto de entrada da aplicação. Controla a execução da coleta de dados
do sistema operacional do usuário logado e exibe/expõe os resultados.

Este módulo pode ser usado como script ou importado como lib.
"""

from pathlib import Path

from models.arquivo_model import ModeloDeArquivo
from models.pasta_model import ModeloDePasta

exemplo_path_home: Path = Path.home().expanduser()

arquivo_real: Path = exemplo_path_home / "teste.html"
item_arquivo = ModeloDeArquivo(file_path=arquivo_real)
print("\n\n item_arquivo =", item_arquivo)
print(f"\n- file_id => {item_arquivo.file_id}")
print(f"\n- file_name => {item_arquivo.file_name}")
print(f"\n- file_extension => {item_arquivo.file_extension}")
print(f"\n- file_size => {item_arquivo.file_size_formatted}")
print(f"\n- file_dates => {item_arquivo.file_dates}")
print(f"\n- informacoes => {item_arquivo.file_info()}")
print(f"\n- file_permissions => {item_arquivo.file_permissions}")
print(f"\n- file_content pre => {item_arquivo.file_content}")
print(f"\n- file_write_content => {item_arquivo.file_write_content(new_content="""<!DOCTYPE html>
<html lang="pt-br">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Documento Atualizado 2</title>
    </head>

    <body><h1>ATUALIZADO</h1></body>

</html>""")}")
print(f"\n- file_content pos => {item_arquivo.file_content}")

pasta_real: Path = exemplo_path_home / "Downloads" / "Firefox"
item_pasta = ModeloDePasta(folder_path=pasta_real)
print("\n\n item_pasta =", item_pasta)
print(f"\n- folder_name => {item_pasta.folder_name}")
print(f"\n- folder_id => {item_pasta.folder_id}")
print(f"\n- folder_size_formatted => {item_pasta.folder_size_formatted}")
print(f"\n- folder_dates => {item_pasta.folder_dates}")
print(f"\n- folder_permissions => {item_pasta.folder_permissions}")
print(f"\n- folder_subfiles => {item_pasta.folder_subfiles}")
print(f"\n- folder_subfolders => {item_pasta.folder_subfolders}")
print(f"\n- folder_empty_subfolders => {item_pasta.folder_empty_subfolders()}")
print(f"\n- folder_depth => {item_pasta.folder_depth()}")
print(f"\n- folder_search_by_extension => {item_pasta.folder_search_by_extension(extension=".html")}")
print(f"\n- folder_list_recursive => {item_pasta.folder_list_recursive(max_levels=10)}")
print(f"\n- folder_info => {item_pasta.folder_info()}")













#  ----------------------------------------------------------------------------

# import json
# from pathlib import Path

# from controllers.system_control import (
#     controller_gerar_json_so,
#     controller_listar_filhos_home,
# )
# from views.system_view import exportar_csv, exportar_json


# def exibir_json_formatado(json_str: str) -> None:
#     """Exibe um JSON formatado no terminal."""
#     try:
#         objeto = json.loads(json_str)
#         print(json.dumps(objeto, indent=4, ensure_ascii=False))
#     except json.JSONDecodeError:
#         print("❌ JSON inválido recebido.")


# def executar_pipeline_principal(exportar: bool = False) -> None:
#     """Executa o pipeline principal do projeto."""
#     print("🔍 Coletando dados do sistema operacional...\n")

#     json_so: str | None = controller_gerar_json_so()
#     if not json_so:
#         print("❌ Não foi possível montar o objeto do sistema.")
#         return

#     exibir_json_formatado(json_str=json_so)

#     if exportar:
#         exportar_json(json_str=json_so, caminho_destino=Path("dados_sistema.json"))

#     filhos: tuple[list[Path], list[Path]] | None = controller_listar_filhos_home()
#     if filhos:
#         pastas, arquivos = filhos
#         print(f"\n📁 Pastas: {len(pastas)} | 📄 Arquivos: {len(arquivos)}")
#         exportar_csv(filhos_pastas=pastas, filhos_arquivos=arquivos, destino=Path("filhos_home.csv"))


# if __name__ == "__main__":
#     # Defina `True` para salvar os dados em JSON e CSV
#     executar_pipeline_principal(exportar=True)
