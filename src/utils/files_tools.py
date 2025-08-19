# ============================================================
# [ARQUIVOS] Manipulacao e formatacao de propriedades
# ============================================================


import re
from pathlib import Path

from utils.global_tools import global_method_check_valid_path


def file_method_gerar_slug(texto: str) -> str:
    """Converte texto em um slug."""
    return re.sub(r"[^a-z0-9]+", "-", texto.lower()).strip("-")


def file_method_ler_conteudo_texto(caminho_arquivo: str | Path, codificacao: str = "utf-8") -> str:
    """Le o conteudo de um arquivo de texto."""
    arquivo_validado: Path = global_method_check_valid_path(caminho_generico=caminho_arquivo)
    if not arquivo_validado.is_file():
        raise FileNotFoundError(f"Nao e um arquivo valido: {arquivo_validado}")
    return arquivo_validado.read_text(encoding=codificacao)


def file_method_escrever_conteudo_texto(caminho_arquivo: str | Path, conteudo: str, codificacao: str = "utf-8") -> None:
    """Escreve conteudo de texto em um arquivo."""
    Path(caminho_arquivo).write_text(conteudo, encoding=codificacao)
