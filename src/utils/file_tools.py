"""
file_tools.py
-------------------
Funções utilitárias para manipulação de arquivos de texto.

Objetivos:
    - Ler e escrever conteúdo de arquivos texto.
    - Garantir validação e segurança.
"""

from pathlib import Path

from utils.main_tools import validate_path

# ---------------------
# Funções públicas
# ---------------------


def read_text_content(file_path: str | Path, encoding: str = "utf-8") -> str:
    """
    Lê o conteúdo de um arquivo de texto.

    Args:
        file_path (str | Path): Caminho do arquivo.
        encoding (str): Codificação para leitura (default utf-8).

    Returns:
        str: Conteúdo do arquivo.

    Raises:
        FileNotFoundError: Se o caminho não existir ou não for arquivo.
        UnicodeDecodeError: Se a decodificação falhar.
        PermissionError: Se não houver permissão de leitura.
    """
    path: Path = validate_path(path_neutral=file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Não é um arquivo válido: {path}")
    with path.open(mode="r", encoding=encoding) as f:
        return f.read()


def write_text_content(file_path: str | Path, content: str, encoding: str = "utf-8") -> None:
    """
    Escreve conteúdo de texto em um arquivo, sobrescrevendo o existente.

    Args:
        file_path (str | Path): Caminho do arquivo.
        content (str): Texto a ser escrito.
        encoding (str): Codificação para escrita (default utf-8).

    Raises:
        PermissionError: Se não houver permissão de escrita.
    """
    path = Path(file_path)
    with path.open(mode="w", encoding=encoding) as f:
        f.write(content)
        f.close()


# def create_text_file(file_path: str | Path, content: str, encoding: str = "utf-8") -> None:
#     """
#     Cria um arquivo texto (sobrescreve se existir).

#     Usa internamente write_text_content para evitar duplicação.
#     """
#     write_text_content(file_path=file_path, content=content, encoding=encoding)
