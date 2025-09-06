"""
os_model.py
-----------
Modelo avançado para informações do sistema operacional.
"""

from __future__ import annotations

import getpass
import logging
import os
import platform
import socket
from pathlib import Path
from typing import Any


class OSModel:
    """Modelo avançado para informações do sistema operacional e disco."""

    def __init__(self, root: str | Path = "/") -> None:
        self.root: Path = Path(root).resolve()
        self.os_name: str = platform.system()
        self.hostname: str = socket.gethostname()
        self.username: str = getpass.getuser()
        self.home: Path = Path.home().expanduser()
        self.kernel_version: str = platform.version()
        self.platform: str = platform.platform()

        # Propriedades dinâmicas
        self.ip: str | None = None
        self.disk_free: int | None = None
        self.refresh()

    # ============================================================
    # [PRIVATE HELPERS]
    # ============================================================

    def _get_ip(self) -> str | None:
        """Obtém o IP local de forma robusta (ignora loopback)."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except OSError as e:
            logging.warning("Falha ao obter IP: %s", e)
            return None

    def _get_disk_free(self, path: Path) -> int | None:
        """Retorna espaço livre em disco (bytes) para o path dado."""
        try:
            st: os.statvfs_result = os.statvfs(str(path))
            return st.f_bavail * st.f_frsize
        except OSError as e:
            logging.warning("Falha ao obter espaço livre de %s: %s", path, e)
            return None

    # ============================================================
    # [PUBLIC METHODS]
    # ============================================================

    def refresh(self) -> None:
        """Atualiza propriedades dinâmicas (IP e espaço em disco)."""
        self.ip = self._get_ip()
        self.disk_free = self._get_disk_free(self.root)

    def to_dict(self) -> dict[str, str | int | None]:
        """Retorna informações do sistema como dicionário."""
        return {
            "os_name": self.os_name,
            "hostname": self.hostname,
            "username": self.username,
            "home": str(self.home),
            "ip": self.ip,
            "kernel_version": self.kernel_version,
            "platform": self.platform,
            "disk_free": self.disk_free,
        }

    # ============================================================
    # [DUNDERS]
    # ============================================================

    def __repr__(self) -> str:
        return (
            f"<OSModel os='{self.os_name}' "
            f"user='{self.username}' "
            f"hostname='{self.hostname}' "
            f"home='{self.home}' "
            f"ip='{self.ip or '-'}' "
            f"kernel='{self.kernel_version}' "
            f"platform='{self.platform}' "
            f"disk_free='{(self.disk_free or 0):,} bytes'>"
        )

    def __eq__(self, other: Any) -> bool:
        """Igualdade baseada em hostname e usuário."""
        return isinstance(other, OSModel) and self.hostname == other.hostname and self.username == other.username
