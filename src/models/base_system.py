"""
Módulo base_system
------------------
Define classes abstratas e utilitárias para representação e manipulação de itens do sistema de arquivos,
incluindo arquivos, diretórios e permissões, além de uma fábrica para criação de instâncias a partir do sistema operacional.
"""

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from models.system_enums import PathValidity, PermissionType, SystemAttribute


@dataclass
class Permissions:
    """Representa permissões simplificadas de arquivo/pasta"""

    can_read: bool = False
    can_write: bool = False

    def has_permission(self, permission_type: PermissionType) -> bool:
        """Verifica se uma permissão específica existe"""
        if permission_type == PermissionType.READ:
            return self.can_read
        if permission_type == PermissionType.WRITE:
            return self.can_write
        return False

    def __str__(self) -> str:
        read: str = "R" if self.can_read else "-"
        write: str = "W" if self.can_write else "-"
        return f"{read} & {write}"


@dataclass
class FileSystemItem(ABC):
    """Classe base abstrata para representar itens do sistema de arquivos"""

    # Propriedades básicas
    path: str
    name: str
    raw_size: int
    created_at: datetime
    modified_at: datetime

    # Validade do caminho
    validity: PathValidity = PathValidity.VALID
    validity_reason: str = ""

    # Permissões simplificadas
    permissions: Permissions = field(default_factory=Permissions)

    # Metadados estendidos
    accessed_at: datetime | None = None
    metadata_changed_at: datetime | None = None
    system_attributes: set[SystemAttribute] = field(default_factory=set)

    # Para navegação
    parent_path: str | None = None

    # Para monitoramento de alterações
    version: int = 1
    change_history: list[dict[str, str]] = field(default_factory=list)

    @property
    @abstractmethod
    def is_file(self) -> bool:
        """Retorna True se for arquivo, False se for pasta"""

    @property
    @abstractmethod
    def item_type(self) -> str:
        """Retorna o tipo do item ('file' ou 'directory')"""

    @property
    def extension(self) -> str | None:
        """Retorna a extensão do arquivo (se aplicável)"""
        if self.is_file:
            return Path(self.path).suffix.lower()
        return None

    @property
    def has_system_attribute(self) -> dict[SystemAttribute, bool]:
        """Retorna um dicionário com o status de cada atributo de sistema"""
        return {attr: attr in self.system_attributes for attr in SystemAttribute}

    def add_to_change_history(self, change_type: str, details: dict[str, str]) -> None:
        """Adiciona uma entrada ao histórico de alterações"""
        self.change_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "version": str(self.version),
                "type": change_type,
                "details": str(details),
            }
        )
        self.version += 1

    def mark_as_invalid(self, reason: str) -> None:
        """Marca o caminho como inválido"""
        self.validity = PathValidity.INVALID
        self.validity_reason = reason

    def mark_as_non_existent(self) -> None:
        """Marca o caminho como não existente"""
        self.validity = PathValidity.NON_EXISTENT
        self.validity_reason = "Path does not exist"

    def mark_as_access_denied(self) -> None:
        """Marca o caminho como acesso negado"""
        self.validity = PathValidity.ACCESS_DENIED
        self.validity_reason = "Access denied"

    def is_valid(self) -> bool:
        """Verifica se o caminho é válido"""
        return self.validity == PathValidity.VALID

    def can_access(self) -> bool:
        """Verifica se o caminho pode ser acessado"""
        return self.validity in {PathValidity.VALID, PathValidity.ACCESS_DENIED}

    def __str__(self) -> str:
        status: str = "✅" if self.is_valid() else "❌"
        item_type: str = "📄" if self.is_file else "📁"
        perms: str = str(self.permissions)
        return f"{status} {item_type} [{perms}] {self.path}"


@dataclass
class File(FileSystemItem):
    """Representa um arquivo"""

    content_html_file: str | None = None

    @property
    def is_file(self) -> bool:
        return True

    @property
    def item_type(self) -> str:
        return "file"

    @property
    def readable_size(self) -> str:
        """Retorna o tamanho em formato legível"""
        sizes: list[str] = ["B", "KB", "MB", "GB"]
        size_val = float(self.raw_size)
        i = 0
        while size_val >= 1024 and size_val < 10 * 1024 and i < len(sizes) - 1:
            size_val /= 1024
            i += 1
        return f"{size_val:.2f} {sizes[i]}"


@dataclass
class Directory(FileSystemItem):
    """Representa um diretório/pasta"""

    item_count: int = 0
    total_size: int = 0

    @property
    def is_file(self) -> bool:
        return False

    @property
    def item_type(self) -> str:
        return "directory"


class FileSystemItemFactory:
    """Factory para criar instâncias de File ou Directory"""

    @staticmethod
    def moldar_objeto(path_str: str) -> FileSystemItem:
        """Cria uma instância baseada no caminho real do sistema"""
        try:
            path = Path(path_str)

            if not path.exists():
                item: FileSystemItem = FileSystemItemFactory._create_nonexistent_item(path_str=str(path_str))
                item.mark_as_non_existent()
                return item

            stats: os.stat_result = path.stat()
            created_at: datetime = datetime.fromtimestamp(stats.st_ctime)
            modified_at: datetime = datetime.fromtimestamp(stats.st_mtime)
            accessed_at: datetime = datetime.fromtimestamp(stats.st_atime)

            system_attributes: set[SystemAttribute] = set()
            if path.name.startswith("."):
                system_attributes.add(SystemAttribute.HIDDEN)

            # Permissões simplificadas
            can_read: bool = path.is_file() and os.access(path, os.R_OK)
            can_write: bool = path.is_file() and os.access(path, os.W_OK)
            permissions = Permissions(can_read=can_read, can_write=can_write)

            if path.is_file():
                return File(
                    path=str(path.absolute()),
                    name=path.name,
                    raw_size=stats.st_size,
                    created_at=created_at,
                    modified_at=modified_at,
                    accessed_at=accessed_at,
                    metadata_changed_at=modified_at,
                    permissions=permissions,
                    system_attributes=system_attributes,
                    content_html_file=None,
                )

            item_count: int = sum(1 for _ in path.iterdir())
            return Directory(
                path=str(path.absolute()),
                name=path.name,
                raw_size=0,
                created_at=created_at,
                modified_at=modified_at,
                accessed_at=accessed_at,
                metadata_changed_at=modified_at,
                permissions=permissions,
                system_attributes=system_attributes,
                item_count=item_count,
                total_size=0,
            )

        except PermissionError:
            item = FileSystemItemFactory._create_nonexistent_item(path_str=path_str)
            item.mark_as_access_denied()
            return item
        except OSError as e:
            item = FileSystemItemFactory._create_nonexistent_item(path_str=path_str)
            item.mark_as_invalid(str(e))
            return item

    @staticmethod
    def _create_nonexistent_item(path_str: str) -> FileSystemItem:
        """Cria um item para caminhos inválidos/não existentes"""
        path = Path(path_str)
        now: datetime = datetime.now()

        # Permissões padrão para itens não existentes
        permissions = Permissions(can_read=False, can_write=False)

        if path.suffix:
            return File(
                path=path_str,
                name=path.name,
                raw_size=0,
                created_at=now,
                modified_at=now,
                permissions=permissions,
                content_html_file=None,
            )
        return Directory(
            path=path_str,
            name=path.name,
            raw_size=0,
            created_at=now,
            modified_at=now,
            permissions=permissions,
            item_count=0,
            total_size=0,
        )
