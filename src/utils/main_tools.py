"""
Módulo utilitário para coleta de propriedades de arquivos e pastas usando apenas pathlib.

Fornece funções para extrair metadados comuns a arquivos e diretórios, incluindo
identificação, caminhos, tamanho, datas, permissões, visibilidade e ponto de montagem.
"""

import os
import uuid
from datetime import datetime
from pathlib import Path


def _get_caminho_absoluto(caminho_comum: str | Path) -> Path:
    """
    Retorna o caminho absoluto de um arquivo ou pasta.

    Args:
        caminho_comum (str | Path): Caminho do arquivo ou pasta.

    Returns:
        Path: Caminho absoluto.
    """
    return Path(caminho_comum).resolve()


def get_id(caminho_comum: str | Path) -> str:
    """
    Gera um identificador único para o item com base no UUID5 do caminho absoluto.

    Args:
        caminho_comum (str | Path): Caminho do arquivo ou pasta.

    Returns:
        str: UUID único como string.
    """
    caminho_abs = str(_get_caminho_absoluto(caminho_comum=caminho_comum))
    return str(uuid.uuid5(uuid.NAMESPACE_URL, caminho_abs))


def get_nome(caminho_comum: str | Path) -> str:
    """
    Retorna o nome do arquivo ou pasta (basename).

    Args:
        caminho_comum (str | Path): Caminho do arquivo ou pasta.

    Returns:
        str: Nome do item.
    """
    return Path(caminho_comum).name


def get_caminho_relativo(caminho_comum: str | Path, base: str | Path) -> Path:
    """
    Retorna o caminho relativo a partir de um diretório base.

    Args:
        caminho_comum (str | Path): Caminho do arquivo ou pasta.
        base (str | Path): Caminho base para cálculo.

    Returns:
        Path: Caminho relativo em relação à base.
    """
    return Path(caminho_comum).resolve().relative_to(Path(base).resolve())


def obter_tamanho(caminho_comum: str | Path, limite_nivel: int = 30) -> int:
    """
    Retorna o tamanho total em bytes de um arquivo ou pasta.

    Para pasta, soma o tamanho dos arquivos até o limite de profundidade,
    ignorando links simbólicos e tratando exceções comuns.

    Args:
        caminho_comum (str | Path): Caminho do arquivo ou pasta.
        limite_nivel (int): Profundidade máxima para escanear pastas.

    Returns:
        int: Tamanho total em bytes.
    """
    caminho_comum = Path(caminho_comum)
    if caminho_comum.is_file():
        try:
            return caminho_comum.stat().st_size
        except (FileNotFoundError, PermissionError, OSError):
            return 0

    if not caminho_comum.is_dir():
        return 0

    total_bytes = 0

    def scan(dir_path: Path, nivel_atual: int) -> None:
        nonlocal total_bytes
        if nivel_atual > limite_nivel:
            return
        try:
            for item in dir_path.iterdir():
                if item.is_symlink():
                    continue
                if item.is_file():
                    try:
                        total_bytes += item.stat().st_size
                    except (FileNotFoundError, PermissionError, OSError):
                        pass
                elif item.is_dir():
                    scan(dir_path=item, nivel_atual=nivel_atual + 1)
        except (FileNotFoundError, PermissionError, OSError):
            pass

    scan(dir_path=caminho_comum, nivel_atual=1)
    return total_bytes


def get_datas(caminho_comum: str | Path) -> dict[str, datetime]:
    """
    Retorna as datas de criação, modificação e acesso.

    Observação:
        - No Windows: data_criacao = criação real.
        - No Linux/macOS: data_criacao pode representar "change time" do metadata.

    Args:
        caminho_comum (str | Path): Caminho do arquivo ou pasta.

    Returns:
        dict: Datas com chaves 'criacao', 'modificacao', 'acesso'.
    """
    st: os.stat_result = Path(caminho_comum).stat()
    return {
        "criacao": datetime.fromtimestamp(st.st_ctime),
        "modificacao": datetime.fromtimestamp(st.st_mtime),
        "acesso": datetime.fromtimestamp(st.st_atime),
    }


def get_permissoes(caminho_comum: str | Path) -> dict[str, bool]:
    """
    Retorna permissões de leitura, escrita e execução para o processo atual.

    Args:
        caminho_comum (str | Path): Caminho do arquivo ou pasta.

    Returns:
        dict: Permissões com chaves 'leitura', 'escrita', 'execucao'.
    """
    caminho_comum = Path(caminho_comum)
    return {
        "leitura": os.access(caminho_comum, os.R_OK),
        "escrita": os.access(caminho_comum, os.W_OK),
        "execucao": os.access(caminho_comum, os.X_OK),
    }


def is_hidden_path(caminho_comum: str | Path) -> bool:
    """
    Verifica se um arquivo ou pasta é oculto.

    Args:
        caminho_comum (str | Path): Caminho do arquivo ou pasta.

    Returns:
        bool: True se for oculto, False caso contrário.
    """
    return Path(caminho_comum).name.startswith(".")


def get_montagem_origem(caminho_comum: str | Path) -> str:
    """
    Retorna o ponto de montagem (volume/dispositivo) onde o item está localizado.

    Args:
        caminho_comum (str | Path): Caminho do arquivo ou pasta.

    Returns:
        str: Caminho do ponto de montagem.
    """
    return Path(caminho_comum).anchor


def validar_caminho(caminho_comum: str | Path) -> Path:
    """
    Valida se o caminho_comum existe no sistema de arquivos.

    Args:
        caminho_comum (str | Path): Caminho do arquivo ou pasta.

    Raises:
        FileNotFoundError: Se o caminho não existir.

    Returns:
        Path: Caminho absoluto validado.
    """
    caminho_abs: Path = _get_caminho_absoluto(caminho_comum=caminho_comum)
    if not caminho_abs.exists():
        raise FileNotFoundError(f"Caminho não encontrado: {caminho_abs}")
    return caminho_abs


# if __name__ == "__main__":
#     exemplo_path: Path = Path("~").expanduser()
#     print(get_id(caminho_comum=exemplo_path))
#     print(get_nome(caminho_comum=exemplo_path))
#     print(get_caminho_relativo(caminho_comum=exemplo_path, base=Path.home()))
#     print(get_datas(caminho_comum=exemplo_path))
#     print(get_permissoes(caminho_comum=exemplo_path))
#     print("obter_tamanho ->", obter_tamanho(caminho_comum=exemplo_path))
#     print(is_hidden_path(caminho_comum=exemplo_path))
#     print(get_montagem_origem(caminho_comum=exemplo_path))
#     print(validar_caminho(caminho_comum=exemplo_path))
