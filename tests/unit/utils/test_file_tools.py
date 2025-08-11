"""
test_file_tools.py
---------------------
Testes unitários para funções de leitura e escrita
de arquivos texto em file_tools.py.

Valida cenários de sucesso e erros esperados.
"""

from pathlib import Path
from typing import NoReturn

import pytest

from src.utils import file_tools


def test_read_text_content_success(tmp_path: Path) -> None:
    """
    Testa leitura correta do conteúdo de um arquivo texto válido.
    """
    file: Path = tmp_path / "test.txt"
    content = "Hello, world!"
    file_tools.create_text_file(file_path=file, content=content)

    result: str = file_tools.read_text_content(file_path=file)
    assert result == content


def test_read_text_content_file_not_found(tmp_path: Path) -> None:
    """
    Testa se FileNotFoundError é lançado ao tentar ler arquivo inexistente.
    """
    non_exist_file: Path = tmp_path / "nofile.txt"
    with pytest.raises(FileNotFoundError):
        file_tools.read_text_content(file_path=non_exist_file)


def test_read_text_content_not_a_file(tmp_path: Path) -> None:
    """
    Testa se FileNotFoundError é lançado ao tentar ler um diretório.
    """
    dir_path: Path = tmp_path / "not_a_file"
    dir_path.mkdir()
    with pytest.raises(FileNotFoundError):
        file_tools.read_text_content(file_path=dir_path)


def test_read_text_content_permission_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Simula PermissionError ao tentar abrir arquivo para leitura.
    """
    file: Path = tmp_path / "file.txt"
    file_tools.create_text_file(file_path=file, content="new content")

    def fake_open(*args, **kwargs) -> NoReturn:
        raise PermissionError("Sem permissão")

    monkeypatch.setattr(Path, "open", fake_open)

    with pytest.raises(PermissionError):
        file_tools.read_text_content(file_path=file)


def test_read_text_content_unicode_decode_error(tmp_path: Path) -> None:
    """
    Testa se UnicodeDecodeError é lançado para arquivo com bytes inválidos para utf-8.
    """
    file: Path = tmp_path / "file.txt"
    file.write_bytes(b"\xff\xfe\x00\x00")
    with pytest.raises(expected_exception=UnicodeDecodeError):
        file_tools.read_text_content(file_path=file)


def test_write_text_content_success(tmp_path: Path) -> None:
    """
    Testa escrita de conteúdo em arquivo novo.
    """
    file: Path = tmp_path / "write_test.txt"
    content = "Test write"
    file_tools.write_text_content(file_path=file, content=content)

    result: str = file_tools.read_text_content(file_path=file)
    assert result == content


def test_write_text_content_overwrite(tmp_path: Path) -> None:
    """
    Testa sobrescrição do conteúdo em arquivo existente.
    """
    file: Path = tmp_path / "write_test.txt"
    file_tools.create_text_file(file_path=file, content="Old content")

    new_content = "New content"
    file_tools.write_text_content(file_path=file, content=new_content)

    result: str = file_tools.read_text_content(file_path=file)
    assert result == new_content


def test_write_text_content_permission_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Simula PermissionError ao tentar abrir arquivo para escrita.
    """
    file: Path = tmp_path / "write_test.txt"

    def fake_open(*args, **kwargs) -> NoReturn:
        raise PermissionError("Sem permissão")

    monkeypatch.setattr(Path, "open", fake_open)

    with pytest.raises(expected_exception=PermissionError):
        file_tools.write_text_content(file_path=file, content="data")
