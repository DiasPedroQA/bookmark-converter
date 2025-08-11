"""
file_utils.py
----------------
Utilitários para manipulação completa de arquivos de texto.

Reúne funções para obter metadados detalhados e ler/escrever conteúdo
de arquivos texto, reutilizando funções base do main_utils.py.
"""

from pathlib import Path

from src.utils.main_tools import validar_caminho


def ler_conteudo_texto(caminho_comum: str | Path, encoding: str = "utf-8") -> str:
    """
    Lê o conteúdo do arquivo texto.

    Args:
        caminho_comum (str | Path): Caminho do arquivo.
        encoding (str): Codificação para leitura (default utf-8).

    Returns:
        str: Conteúdo do arquivo.

    Raises:
        FileNotFoundError, UnicodeDecodeError, PermissionError
    """
    validar_caminho(caminho_comum=caminho_comum)
    p = Path(caminho_comum)
    if not p.is_file():
        raise FileNotFoundError(f"Não é um arquivo: {p}")
    with p.open("r", encoding=encoding) as f:
        return f.read()


def escrever_conteudo_texto(caminho_comum: str | Path, conteudo: str, encoding: str = "utf-8") -> None:
    """
    Escreve conteúdo texto no arquivo, sobrescrevendo o existente.

    Args:
        caminho_comum (str | Path): Caminho do arquivo.
        conteudo (str): Texto a ser escrito.
        encoding (str): Codificação para escrita (default utf-8).
    """
    p = Path(caminho_comum)
    with p.open("w", encoding=encoding) as f:
        f.write(conteudo)


# ARQUIVO = "/home/pedro-pm-dias/teste.html"

# # ler conteúdo
# texto: str = ler_conteudo_texto(caminho_comum=ARQUIVO)
# print(f"\n texto => {texto}")

# # escrever conteúdo novo
# try:
#     escrever_conteudo_texto(caminho_comum=ARQUIVO, conteudo="""<!DOCTYPE html>
# <html lang="pt-br">

#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>Documento Atualizado</title>
#     </head>

#     <body>
#         <h1>ATUALIZADO</h1>
#     </body>

# </html>""")
#     print("\n Escrita bem sucedida!")
# except Exception as err:
#     print(f"Erro: {err}")
