"""
utils_comuns.py
---------------
Funções utilitárias genéricas e independentes do contexto de Sistema Operacional, Arquivo ou Pasta.

Estas funções são reutilizáveis em qualquer camada do projeto,
servindo como blocos de construção para as demais operações.

Objetivo:
    - Fornecer padronização e normalização de dados.
    - Evitar repetição de lógica comum entre módulos.
    - Garantir consistência na formatação de informações.

Objetos principais que utilizam:
    - SistemaOperacional
    - SistemaArquivo
    - SistemaPasta
"""

from datetime import datetime
from pathlib import Path


def normalizar_caminho(caminho: str | Path) -> Path:
    """
    Converte uma string ou Path para um objeto Path absoluto e resolvido.

    - Expande `~` para diretório do usuário.
    - Resolve links simbólicos.
    - Retorna um Path pronto para operações seguras.

    Args:
        caminho (str | Path): Caminho a ser normalizado.

    Returns:
        Path: Caminho absoluto e resolvido.
    """
    return Path(caminho).expanduser().resolve()


def formatar_tamanho(bytesize: float) -> str:
    """
    Converte um valor de tamanho em bytes para formato legível.

    - Suporta B, KB, MB, GB, TB, PB.
    - Mantém duas casas decimais.

    Args:
        bytesize (float): Tamanho em bytes.

    Returns:
        str: Tamanho formatado, ex: '1.23 MB'
    """
    for unidade in ["B", "KB", "MB", "GB", "TB"]:
        if bytesize < 1024:
            return f"{bytesize:.2f} {unidade}"
        bytesize /= 1024
    return f"{bytesize:.2f} PB"


def coletar_datas_aprimoradas(timestamp: float) -> dict[str, float | str]:
    """
    Converte um timestamp num dicionário com formatos úteis de data/hora.

    - Inclui timestamp original.
    - Inclui formato ISO 8601 (para API).
    - Inclui formato legível (para interface).

    Args:
        timestamp (float): Timestamp Unix.

    Returns:
        dict[str, float | str]: Datas formatadas.
    """
    dt: datetime = datetime.fromtimestamp(timestamp=timestamp)
    return {"timestamp": timestamp, "iso": dt.isoformat(), "legivel": dt.strftime(format="%d/%m/%Y %H:%M")}
