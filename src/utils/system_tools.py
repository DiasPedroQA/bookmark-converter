# ============================================================
# [SISTEMA] Operacoes do sistema operacional, filtros e listagens
# ============================================================


import getpass
import os
import platform
import socket
from datetime import datetime
from pathlib import Path


def system_method_obter_nome_sistema_operacional() -> str:
    """Retorna o nome do sistema operacional atual."""
    return platform.system()


def system_method_obter_versao_kernel() -> str:
    """Retorna a versão do kernel do sistema."""
    return platform.version()


def system_method_obter_info_plataforma() -> str:
    """Retorna as informações da plataforma."""
    return platform.platform()


def system_method_obter_caminho_usuario() -> str:
    """Retorna o caminho da pasta de usuario do sistema operacional."""
    return str(Path.home().expanduser())


def system_method_obter_nome_usuario() -> str:
    """Retorna o caminho da pasta de usuario do sistema operacional."""
    return getpass.getuser()


def system_method_obter_endereco_ip() -> str:
    """Retorna o endereco IP local da maquina."""
    return socket.gethostbyname(socket.gethostname())


def system_method_obter_espaco_disco_livre(caminho: str | Path = "/") -> int:
    """Retorna o espaco livre em bytes no disco."""
    st: os.statvfs_result = os.statvfs(str(caminho))
    return st.f_bavail * st.f_frsize


def system_method_debug_print(mensagem: str) -> None:
    """Imprime uma mensagem de depuracao com timestamp."""
    print(f"[DEBUG {datetime.now().strftime(format='%Y-%m-%d %H:%M:%S')}] {mensagem}")
