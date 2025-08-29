"""XYZ

Controller para exploração BFS de sistema de arquivos com validação de visibilidade
(evitando segmentos de caminho iniciados por '.') e checagem de permissões de
leitura/execução. Suporta profundidade máxima e filtro opcional por extensão.

Componentes:
- OSModel: informações de sistema (mantido do seu código, sem alterações funcionais)
- FileExplorerController: orquestra exploração por níveis (BFS)

Fluxo principal:
1) Validar base_path (precisa ter leitura; diretórios precisam de leitura+execução)
2) Incluir a própria base_path em `folders` (se válida)
3) Para depth em [0..max_depth]:
   - Para cada pasta do nível atual: listar itens imediatos
   - Validar cada item (permissão + visibilidade)
   - Separar em arquivos e pastas
   - Acumular globalmente
   - Subpastas válidas alimentam o próximo nível
4) Retornar dicionário com listas finais: files, folders, invalid

Observações:
- A validação de visibilidade examina *todos* os segmentos do caminho (Path.parts)
- O filtro de extensão é aplicado apenas a arquivos (case-insensitive) e é opcional
- Tratamento resiliente para erros de sistema (permissão, inexistência, I/O)
"""

# %%
from __future__ import annotations

import getpass
import os
import platform
import socket
from pathlib import Path
from typing import Iterable


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
        self._home: Path = Path.home().expanduser()
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


# %%
class FileExplorerController:
    """Controller to explore directories with validation and filtering.

    Regras de validação:
    - Permissão de leitura (e de execução para diretórios)
    - Nenhum segmento do caminho pode começar com '.'

    Estratégia:
    - BFS por níveis (0..max_depth) a partir de base_path
    - Em cada nível, acumula globalmente arquivos e pastas válidos
    - `target_ext` aplica-se apenas a arquivos; se None, aceita todas as extensões
    """

    # ------------------------------------------------------------
    # Construção e representação
    # ------------------------------------------------------------
    def __init__(self, base_path: Path, max_depth: int = 5, target_ext: str | None = None) -> None:
        """Initialize with a base directory, depth limit and optional target extension.

        Args:
            base_path: Path to start exploration.
            max_depth: Maximum depth starting from base_path (0 = somente a raiz).
            target_ext: Extension filter for files (e.g. ".html" or "html"). None = no filter.
        """
        self.base_path: Path = Path(base_path).expanduser().resolve()
        self.max_depth: int = max(0, int(max_depth))
        self.target_ext: str | None = self._normalize_ext(ext=target_ext)

        # Acumuladores globais
        self.files: list[Path] = []
        self.folders: list[Path] = []
        self.invalid: list[Path] = []

        # Validação inicial do base_path (não acumula em invalid: falha é fatal)
        if not self._is_visible(path=self.base_path) or not self._has_read_permission(path=self.base_path):
            raise ValueError(f"Base path is not accessible or visible: {self.base_path}")

    def __repr__(self) -> str:
        return f"<FileExplorerController base='{self.base_path}' depth={self.max_depth} ext={self.target_ext or '*'}>"

    # ------------------------------------------------------------
    # Normalização / Predicados
    # ------------------------------------------------------------
    def _normalize_ext(self, ext: str | None) -> str | None:
        """Normalize extension to lower-case and ensure leading dot.

        Returns:
            e.g. 'HTML' -> '.html'; 'txt' -> '.txt'; None -> None
        """
        if ext is None:
            return None
        e: str = ext.strip().lower()
        if not e:
            return None
        return e if e.startswith(".") else f".{e}"

    def _is_visible(self, path: Path) -> bool:
        """Check that no segment of the path starts with '.' (hidden).

        Notes:
            Path.parts inclui a raiz ('/' em Unix). Apenas segmentos com nome
            iniciando em '.' são considerados ocultos.
        """
        try:
            for part in path.parts:
                # Ignora raiz e drive (e.g. 'C:')
                if part in ("/", "\\") or (len(part) == 2 and part.endswith(":")):
                    continue
                if part.startswith("."):
                    return False
            return True
        except (OSError, PermissionError, ValueError):
            return False

    def _has_read_permission(self, path: Path) -> bool:
        """Check read permissions. For directories, require execute to traverse."""
        try:
            if path.is_dir():
                return os.access(path, os.R_OK | os.X_OK)
            return os.access(path, os.R_OK)
        except (OSError, PermissionError, ValueError):
            return False

    def _validate_path(self, actual_path: Path) -> Path | None:
        """Validate if path is visible and has required permissions.

        Returns:
            The same Path if valid; otherwise None and path is recorded in `invalid`.
        """
        p = Path(actual_path)
        if not self._is_visible(p) or not self._has_read_permission(p):
            self.invalid.append(p)
            return None
        return p

    # ------------------------------------------------------------
    # Listagem e separação
    # ------------------------------------------------------------
    def _list_items(self, folder: Path) -> list[Path]:
        """List immediate children of `folder`, returning only validated paths."""
        items: list[Path] = []
        try:
            for child in Path(folder).iterdir():
                valid: Path | None = self._validate_path(actual_path=child)
                if valid is not None:
                    items.append(valid)
        except (PermissionError, FileNotFoundError, NotADirectoryError, OSError):
            # Pasta inacessível: marca própria pasta como inválida e segue
            self.invalid.append(Path(folder))
        return items

    def _separate(self, items: Iterable[Path]) -> tuple[list[Path], list[Path]]:
        """Separate validated items into (files, folders) applying extension filter to files."""
        files: list[Path] = []
        folders: list[Path] = []
        for p in items:
            try:
                if p.is_dir():
                    folders.append(p)
                elif p.is_file():
                    if self.target_ext is None:
                        files.append(p)
                    else:
                        # Comparação case-insensitive com sufixo normalizado
                        if p.suffix.lower() == self.target_ext:
                            files.append(p)
                # Outros tipos (symlink, socket, etc.) são ignorados silenciosamente
            except OSError:
                self.invalid.append(p)
        return files, folders

    # ------------------------------------------------------------
    # Exploração por nível (BFS)
    # ------------------------------------------------------------
    def _explore_level(self, current_folders: Iterable[Path], depth: int) -> list[Path]:
        """Explore one BFS level: list, validate, separate, accumulate, and return next-level folders."""
        next_level: list[Path] = []

        # Se depth for zero, não faz nada (ponto de parada defensivo)
        if depth <= 0:
            return next_level

        for folder in current_folders:
            items: list[Path] = self._list_items(folder=folder)
            files, folders = self._separate(items=items)
            self.files.extend(files)
            self.folders.extend(folders)
            next_level.extend(folders)

        return next_level

    # ------------------------------------------------------------
    # Orquestração pública
    # ------------------------------------------------------------
    def explore(self) -> dict[str, list[Path]]:
        """Run BFS exploration from base_path up to max_depth.

        Returns:
            Dict with global accumulators: {"files": [...], "folders": [...], "invalid": [...]}.
        """
        # Inclui a própria base_path como pasta válida (se visível & acessível)
        self.folders.append(self.base_path)

        # Nível 0 começa com a raiz
        frontier: list[Path] = [self.base_path]

        # Explora de 0..max_depth
        # Em depth=0, exploramos o conteúdo direto de base_path
        for depth in range(0, self.max_depth + 1):
            frontier = self._explore_level(current_folders=frontier, depth=depth)
            if not frontier:
                break
        return {
            "files": self.files,
            "folders": self.folders,
            "invalid": self.invalid,
        }

    # ------------------------------------------------------------
    # Utilitário opcional
    # ------------------------------------------------------------
    def filter_by_extension(self, items: Iterable[Path], extension: str) -> list[Path]:
        """Public helper to filter arbitrary paths by an extension (case-insensitive)."""
        ext = self._normalize_ext(extension)
        if ext is None:
            return [p for p in items if p.is_file()]
        out: list[Path] = []
        for p in items:
            try:
                if p.is_file() and p.suffix.lower() == ext:
                    out.append(p)
            except OSError:
                self.invalid.append(p)
        return out


# %% Demo de uso (opcional)
if __name__ == "__main__":
    modelo = OSModel()
    controller = FileExplorerController(base_path=modelo.home, max_depth=5, target_ext=".html")
    result: dict[str, list[Path]] = controller.explore()

    print("Folders:", len(result["folders"]))
    print("Files:", len(result["files"]))
    print("Invalid:", len(result["invalid"]))

    # Exemplo de listagem parcial (limitada)
    for p in result["files"][:10]:
        print("file:", p)
