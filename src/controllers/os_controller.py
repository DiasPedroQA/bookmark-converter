"""
file_explorer_controller.py
---------------------------

Controller avançada para exploração hierárquica de arquivos e pastas,
herdando dados do sistema operacional via OSModel.

Funcionalidades:
- Exploração recursiva (BFS) de arquivos e pastas.
- Filtragem por extensão, tamanho e palavra-chave no nome.
- Ignora arquivos/pastas ocultos.
- Suporte opcional a symlinks.
"""

from __future__ import annotations

import logging
import os
from collections.abc import Iterable
from pathlib import Path


class FileExplorerController:
    """BFS Explorer com validação, filtros e suporte opcional a symlinks."""

    def __init__(
        self,
        base_path: str | Path,
        max_depth: int = 5,
        target_ext: str | None = None,
        follow_symlinks: bool = False,
    ) -> None:
        self.base_path: Path = Path(base_path).expanduser().resolve()
        self.max_depth: int = max(0, int(max_depth))
        self.target_ext: str | None = self._normalize_ext(target_ext)
        self.follow_symlinks: bool = follow_symlinks

        self.files: list[Path] = []
        self.folders: list[Path] = []
        self.invalids: list[Path] = []

        if not self._is_visible(self.base_path) or not self._has_read_permission(self.base_path):
            raise ValueError(f"Base path is not accessible or visible: {self.base_path}")

    # -----------------------
    # Helpers
    # -----------------------
    def _normalize_ext(self, ext: str | None) -> str | None:
        if not ext:
            return None
        return f".{ext.strip().lower().lstrip('.')}"

    def _is_visible(self, path: Path) -> bool:
        try:
            for part in path.parts:
                if part in ("/", "\\") or (len(part) == 2 and part.endswith(":")):
                    continue
                if part.startswith("."):
                    return False
            return True
        except OSError as e:
            logging.warning("Visibility check failed for %s: %s", path, e)
            return False

    def _has_read_permission(self, path: Path) -> bool:
        try:
            return os.access(path, os.R_OK | os.X_OK) if path.is_dir() else os.access(path, os.R_OK)
        except OSError as e:
            logging.warning("Permission check failed for %s: %s", path, e)
            return False

    def _validate_path(self, path: Path) -> Path | None:
        if not self._is_visible(path) or not self._has_read_permission(path):
            self.invalids.append(path)
            return None
        return path

    # -----------------------
    # Listing & separating
    # -----------------------
    def _list_childs(self, folder: Path) -> list[Path]:
        childs: list[Path] = []
        try:
            for child_path in folder.iterdir():
                if not self.follow_symlinks and child_path.is_symlink():
                    continue
                if valid := self._validate_path(child_path):
                    childs.append(valid)
        except (PermissionError, FileNotFoundError, NotADirectoryError, OSError) as e:
            logging.warning("Cannot access folder %s: %s", folder, e)
            self.invalids.append(folder)
        return childs

    def _separate(self, childs: Iterable[Path]) -> tuple[list[Path], list[Path]]:
        files: list[Path] = []
        folders: list[Path] = []
        for child_path in childs:
            try:
                if child_path.is_dir():
                    folders.append(child_path)
                elif child_path.is_file():
                    if self.target_ext is None or child_path.suffix.lower() == self.target_ext:
                        files.append(child_path)
            except OSError as e:
                logging.warning("Failed to check child %s: %s", child_path, e)
                self.invalids.append(child_path)
        return files, folders

    # -----------------------
    # BFS exploration
    # -----------------------
    def _explore_level(self, current_folders: Iterable[Path], level: int) -> list[Path]:
        next_level: list[Path] = []
        current_folders_list: list[Path] = list(current_folders)
        logging.info("Exploring level %d, %d folders in frontier", level, len(current_folders_list))

        for folder_path in current_folders_list:
            childs: list[Path] = self._list_childs(folder_path)
            files, folders = self._separate(childs)

            self.files.extend([f for f in files if f not in self.files])
            self.folders.extend([d for d in folders if d not in self.folders])

            next_level.extend(folders)
        return next_level

    # -----------------------
    # Public API
    # -----------------------
    def explore_folder(self) -> dict[str, list[Path]]:
        """Executa a exploração BFS até max_depth."""
        if self.base_path not in self.folders:
            self.folders.append(self.base_path)

        frontier: list[Path] = [self.base_path]

        for level in range(self.max_depth + 1):
            if not frontier:
                break
            frontier = self._explore_level(frontier, level)

        logging.info(
            "Exploration completed: %d folders, %d files, %d invalid paths",
            len(self.folders),
            len(self.files),
            len(self.invalids),
        )
        return {"folders": self.folders, "files": self.files, "invalids": self.invalids}

    def filter_by_extension(self, childs: Iterable[Path], extension: str | None = None) -> list[Path]:
        """Filtra childs por extensão e prefixo (favoritos_ ou bookmarks)."""
        ext: str | None = self._normalize_ext(extension)
        prefixes: tuple[str, str] = ("favoritos_", "bookmarks")

        out: list[Path] = []
        for child_path in childs:
            try:
                if child_path.is_file():
                    filename: str = child_path.name.lower()
                    if filename.startswith(prefixes) and (ext is None or child_path.suffix.lower() == ext):
                        out.append(child_path)
            except OSError:
                self.invalids.append(child_path)
        return out

    # -----------------------
    # Dunders
    # -----------------------
    def __repr__(self) -> str:
        return (
            f"<FileExplorerController base='{self.base_path}' "
            f"depth={self.max_depth} ext={self.target_ext or '*'} "
            f"follow_symlinks={self.follow_symlinks}>"
        )
