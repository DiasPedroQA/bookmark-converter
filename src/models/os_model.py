# """
# os_model.py
# -----------

# Advanced OS model for system and disk information.
# """

# from __future__ import annotations

# import getpass
# import logging
# import os
# import platform
# import socket
# from pathlib import Path
# from typing import Any

# from utils import global_method_formatar_tamanho_caminho

# logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")


# class OSModel:
#     """Model that abstracts system information and disk resources."""

#     def __init__(self, root: str | Path = "/") -> None:
#         """
#         Initialize OS information and main resources.

#         Args:
#             root: Base path to check disk usage (default is '/').
#         """
#         self.root: Path = Path(root).resolve()
#         self.os_name: str = platform.system()
#         self.hostname: str = socket.gethostname()
#         self.username: str = getpass.getuser()
#         self.home: Path = Path.home().expanduser()
#         self.kernel_version: str = platform.version()
#         self.platform: str = platform.platform()
#         self.ip: str | None = self._get_ip()
#         self.disk_free: int | None = self._get_disk_free(self.root)

#     # ============================================================
#     # [PRIVATE HELPERS]
#     # ============================================================

#     def _get_ip(self) -> str | None:
#         """Get local IP address in a robust way (ignores only-loopback)."""
#         try:
#             with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
#                 s.connect(("8.8.8.8", 80))
#                 return s.getsockname()[0]
#         except OSError as e:
#             logging.warning("Failed to get IP: %s", e)
#             return None

#     def _get_disk_free(self, path: str | Path) -> int | None:
#         """Return free disk space in bytes for the given path."""
#         try:
#             path = Path(path)
#             st: os.statvfs_result = os.statvfs(str(path))
#             return st.f_bavail * st.f_frsize
#         except OSError as e:
#             logging.warning("Failed to get disk free space for %s: %s", path, e)
#             return None

#     # ============================================================
#     # [PUBLIC METHODS]
#     # ============================================================

#     def to_dict(self) -> dict[str, str | int | None]:
#         """Return system info as dictionary with human-friendly disk size."""
#         return {
#             "os_name": self.os_name,
#             "hostname": self.hostname,
#             "username": self.username,
#             "home": str(self.home),
#             "ip": self.ip,
#             "kernel_version": self.kernel_version,
#             "platform": self.platform,
#             "disk_free": (
#                 global_method_formatar_tamanho_caminho(tamanho_bytes=self.disk_free)
#                 if self.disk_free is not None
#                 else None
#             ),
#         }

#     def refresh(self) -> None:
#         """
#         Refresh dynamic properties (IP, disk space).
#         Useful for long-running processes where values may change.
#         """
#         self.ip = self._get_ip()
#         self.disk_free = self._get_disk_free(path=self.root)

#     # ============================================================
#     # [DUNDERS]
#     # ============================================================

#     def __repr__(self) -> str:
#         return (
#             f"<OSModel os='{self.os_name}' "
#             f"user='{self.username}' "
#             f"ip='{self.ip or '-'}' "
#             f"disk_free={self.disk_free or 0:,} bytes>"
#         )

#     def __eq__(self, other: Any) -> bool:
#         """Equality based on hostname and username (basic identity)."""
#         if not isinstance(other, OSModel):
#             return False
#         return self.hostname == other.hostname and self.username == other.username
