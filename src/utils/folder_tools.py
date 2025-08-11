"""
utils_pastas.py
---------------
Funções para manipulação e análise de diretórios.

Objetivos:
- Listar conteúdo de pastas com filtros e detalhes.
- Calcular tamanho, profundidade e estatísticas de diretórios.
- Garantir segurança e consistência via normalização e validação.

Principais consumidores:
- SistemaPasta
- SistemaOperacional (para validação)
"""

from pathlib import Path

from src.utils.main_tools import is_hidden_path, validar_caminho


def listar_subcaminhos(pasta_base: Path, ignorar_ocultos: bool = True) -> list[Path]:
    """
    Lista arquivos e pastas dentro de uma pasta.

    Args:
        pasta_base (Path): Diretório base para listagem.
        ignorar_ocultos (bool): Se True, ignora itens ocultos (nomes começando com '.').

    Returns:
        list[Path]: Caminhos filhos válidos.
    """
    if not validar_caminho(caminho_comum=pasta_base) or not pasta_base.is_dir():
        return []

    try:
        return [item for item in pasta_base.iterdir() if not (ignorar_ocultos and is_hidden_path(caminho_comum=item))]
    except PermissionError:
        return []


def filtrar_pastas(itens: list[Path]) -> list[Path]:
    """
    Retorna apenas os diretórios da lista.

    Args:
        itens (list[Path]): Lista de caminhos.

    Returns:
        list[Path]: Apenas diretórios.
    """
    return [item for item in itens if item.is_dir()]


def filtrar_arquivos(itens: list[Path]) -> list[Path]:
    """
    Retorna apenas os arquivos da lista.

    Args:
        itens (list[Path]): Lista de caminhos.

    Returns:
        list[Path]: Apenas arquivos.
    """
    return [item for item in itens if item.is_file()]


def listar_pastas_vazias(pasta_base: Path) -> list[Path]:
    """
    Retorna as pastas vazias dentro da pasta base.

    Args:
        pasta_base (Path): Diretório base para busca.

    Returns:
        list[Path]: Pastas que não possuem conteúdo.
    """
    itens: list[Path] = listar_subcaminhos(pasta_base=pasta_base)
    pastas: list[Path] = filtrar_pastas(itens=itens)
    return [pasta for pasta in pastas if not any(pasta.iterdir())]


def calcular_profundidade(pasta_base: Path) -> int:
    """
    Calcula a profundidade máxima da árvore de diretórios.

    Args:
        pasta_base (Path): Diretório base.

    Returns:
        int: Profundidade máxima (0 se pasta vazia ou inválida).
    """
    if not validar_caminho(caminho_comum=pasta_base) or not pasta_base.is_dir():
        return 0

    max_depth = 0
    base_parts: int = len(pasta_base.parts)

    for path in pasta_base.rglob("*"):
        if path.is_dir():
            depth: int = len(path.parts) - base_parts
            if depth > max_depth:
                max_depth: int = depth
    return max_depth


def buscar_por_extensao(pasta_base: Path, extensao: str) -> list[Path]:
    """
    Busca arquivos na pasta base com a extensão especificada (case insensitive).
    Suporta extensões compostas, tipo '.tar.gz'.

    Args:
        pasta_base (Path): Diretório base para busca.
        extensao (str): Extensão completa com ponto, ex: '.txt' ou '.tar.gz'

    Returns:
        list[Path]: Arquivos que correspondem à extensão.
    """
    if not validar_caminho(caminho_comum=pasta_base) or not pasta_base.is_dir():
        return []

    ext_lower: str = extensao.lower()
    # Quebra extensão em lista pra comparar com suffixes
    ext_list: list[str] = ext_lower.split(".")

    # Remove o primeiro item se for vazio (porque começa com '.')
    if ext_list and ext_list[0] == "":
        ext_list = ext_list[1:]

    try:
        resultados: list[Path] = []
        for arquivo in pasta_base.iterdir():
            if arquivo.is_file():
                # suffixes é lista com os pontos, ex: ['.tar', '.gz']
                suffixes_lower: list[str] = [suf.lower().lstrip(".") for suf in arquivo.suffixes]
                if suffixes_lower[-len(ext_list) :] == ext_list:
                    resultados.append(arquivo)
        print(f"{len(resultados)} arquivo(s) (ext={extensao}) encontrado(s)")
        return resultados
    except PermissionError:
        return []


# if __name__ == "__main__":
#     exemplo_path: Path = Path("~").expanduser()
#     lista_caminhos: list[Path] = listar_subcaminhos(pasta_base=exemplo_path)
#     print("filtrar_pastas ->", filtrar_pastas(itens=lista_caminhos))
#     print("filtrar_arquivos ->", filtrar_arquivos(itens=lista_caminhos))
#     print("listar_pastas_vazias ->", listar_pastas_vazias(pasta_base=exemplo_path))
#     print("calcular_profundidade ->", calcular_profundidade(pasta_base=exemplo_path))
#     print("buscar_por_extensao ->", buscar_por_extensao(pasta_base=exemplo_path, extensao="html"))
