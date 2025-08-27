"""XYZ"""

# %%
from __future__ import annotations

import getpass
import os
import platform
import socket
from pathlib import Path


# %%
class OSModel:
    """Model that abstracts system information and disk resources."""

    def __init__(self, root: str | Path = "/") -> None:
        """
        Initialize OS information and main resources.

        Args:
            root: Base path to check disk usage (default is '/').
        """
        self.root: Path = Path(root).resolve()
        self.os_name: str = platform.system()
        self.hostname: str = socket.gethostname()
        self.username: str = getpass.getuser()
        self._home: Path = Path.home().expanduser()  # agora é privado
        self.kernel_version: str = platform.version()
        self.platform: str = platform.platform()
        self.ip: str | None = self._get_ip()
        self.disk_free: int | None = self._get_disk_free(self.root)

    # ============================================================
    # [GETTERS / PROPERTIES]
    # ============================================================

    @property
    def home(self) -> Path:
        """Return user home directory as Path object."""
        return self._home

    # ============================================================
    # [PRIVATE HELPERS]
    # ============================================================

    def _get_ip(self) -> str | None:
        """Get local IP address in a robust way (ignores only-loopback)."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except OSError as e:
            print("Failed to get IP: %s", e)
            return None

    def _get_disk_free(self, path: str | Path) -> int | None:
        """Return free disk space in bytes for the given path."""
        try:
            p: Path = Path(path)
            st: os.statvfs_result = os.statvfs(str(p))
            return st.f_bavail * st.f_frsize
        except OSError as e:
            print("Failed to get disk free space for %s: %s", path, e)
            return None

    # ============================================================
    # [PUBLIC METHODS]
    # ============================================================

    def to_dict(self) -> dict[str, str | int | None]:
        """Return system info as dictionary with human-friendly disk size."""
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
            f"kernel_version='{self.kernel_version}' "
            f"platform='{self.platform}' "
            f"disk_free='{(self.disk_free or 0):,} bytes'>"
        )


modelo = OSModel()

# print("Home (Path):", modelo.home)


# %%
class FileExplorerController:
    """Controller to explore directories with validation and filtering."""

    def __init__(self, base_path: Path) -> None:
        """
        Initialize with a base directory.

        Args:
            base_path: Path to start exploration.
        """
        self.base_path: Path = base_path.resolve()
        self._validate_path(base_path)  # Corrigido: removido argumento nomeado 'path'

    # ============================================================
    # [DUNDERS]
    # ============================================================

    def __repr__(self) -> str:
        return f"<FileExplorerController base='{self.base_path}'>"

    # ============================================================
    # [VALIDATION]
    # ============================================================

    def _validate_path(self, actual_path: Path) -> Path | None:
        """Validate if path is visible and has read permission."""
        # if not actual_path.exists():  # return None
        if not os.access(actual_path, os.R_OK):
            return None
        if actual_path.name.startswith("."):
            return None
        return actual_path

    # ============================================================
    # [LISTING]
    # ============================================================

    def list_items_home(self, this_folder: Path | None = None) -> list[Path]:
        """
        List items inside the base directory.

        Args:
            this_folder: Optional specific folder to list (defaults to base_path)

        Returns:
            List of Path objects inside the base path.
        """
        if not this_folder:
            pasta_atual: Path = self.base_path
        else:
            pasta_atual = Path(this_folder).expanduser().resolve()

        items: list[Path] = []
        for p in pasta_atual.iterdir():
            valid: Path | None = self._validate_path(p)  # Corrigido: sem argumento nomeado
            if valid:
                items.append(valid)

        return items

    # ============================================================
    # [FILTERING]
    # ============================================================

    def filter_by_extension(self, items: list[Path], extension: str) -> list[Path]:
        """
        Filter files by extension.

        Args:
            items: List of Path objects to filter
            extension: File extension (e.g., '.html').

        Returns:
            List of Path objects matching the extension.
        """
        return [p for p in items if p.suffix == extension]


# %%
controller = FileExplorerController(base_path=modelo.home)

# print("\n Todos os itens:", controller.list_items_home())
print("\n Somente pastas:")
pastas_home: list[Path] = controller.list_items_home(this_folder=modelo.home)

if pastas_home and len(pastas_home) > 4:
    pasta_x: Path = pastas_home[4]

    print(controller.list_items_home(this_folder=pasta_x))

    print("\n Somente arquivos:", controller.list_items_home(this_folder=pasta_x))

    # Corrigido: primeiro obtém a lista de itens, depois filtra
    itens_pasta_x: list[Path] = controller.list_items_home(this_folder=pasta_x)
    print("\n Arquivos .html:", controller.filter_by_extension(itens_pasta_x, ".html"))
else:
    print("Não há pastas suficientes na home directory")
