"""
Este módulo define enums relacionados a atributos de sistema para arquivos ou objetos.

Classes:
    SystemAttribute: Enumeração dos possíveis atributos de sistema, como 'compressed', 'encrypted', 'indexed', entre outros.
"""

from enum import Enum


class PermissionType(Enum):
    """
    Enumeração que representa os tipos de permissões que podem ser atribuídas.
    """

    READ = "read"
    WRITE = "write"


class SystemAttribute(Enum):
    """
    Enumeração que representa atributos de sistema que podem ser associados a arquivos ou objetos.
    """

    COMPRESSED = "compressed"
    ENCRYPTED = "encrypted"
    INDEXED = "indexed"
    HIDDEN = "hidden"
    ARCHIVE = "archive"
    SYSTEM = "system"


class PathValidity(Enum):
    """
    Enumeração que representa a validade de um caminho de arquivo ou recurso.
    """

    VALID = "valid"
    INVALID = "invalid"
    NON_EXISTENT = "non_existent"
    ACCESS_DENIED = "access_denied"
    SYSTEM = "system"
