"""
test_main_tools.py
------------------
Testes unitários para o módulo main_tools.py.

Cobre validação de caminhos, geração de UUID, obtenção de nome,
cálculo de tamanho, extração de datas, verificação de permissões,
e identificação de arquivos ocultos.
"""

import uuid
from collections.abc import Generator
from datetime import datetime
from pathlib import Path

import pytest

from src.utils import main_tools


@pytest.fixture
def temp_file_fixture(tmp_path: Path) -> Generator[Path, None, None]:
    """
    Fixture que cria um arquivo temporário com conteúdo.

    Args:
        tmp_path (Path): Diretório temporário gerado pelo pytest.

    Yields:
        Path: Caminho para o arquivo temporário criado.
    """
    file: Path = tmp_path / "testfile.txt"
    file.write_text(data="hello world")
    yield file


@pytest.fixture
def temp_hidden_file_fixture(tmp_path: Path) -> Generator[Path, None, None]:
    """
    Fixture que cria um arquivo oculto temporário.

    Args:
        tmp_path (Path): Diretório temporário gerado pelo pytest.

    Yields:
        Path: Caminho para o arquivo oculto criado.
    """
    file: Path = tmp_path / ".hiddenfile"
    file.write_text(data="hidden content")
    yield file


@pytest.fixture
def temp_dir_with_files_fixture(tmp_path: Path) -> Generator[Path, None, None]:
    """
    Fixture que cria um diretório temporário com dois arquivos de texto.

    Args:
        tmp_path (Path): Diretório temporário gerado pelo pytest.

    Yields:
        Path: Caminho para o diretório criado.
    """
    dir_path: Path = tmp_path / "folder"
    dir_path.mkdir()
    (dir_path / "file1.txt").write_text(data="content1")
    (dir_path / "file2.txt").write_text(data="content2")
    yield dir_path


def test_validate_path_existing(tmp_path: Path) -> None:
    """
    Testa se validate_path retorna o caminho absoluto para um arquivo existente.

    Args:
        tmp_path (Path): Diretório temporário gerado pelo pytest.

    Asserts:
        O caminho retornado é igual ao caminho absoluto do arquivo criado.
    """
    p: Path = tmp_path / "exists.txt"
    p.write_text(data="exists")
    result: Path = main_tools.validate_path(path_neutral=str(p))
    assert result == p.resolve()


def test_validate_path_not_existing(tmp_path: Path) -> None:
    """
    Testa se validate_path levanta FileNotFoundError para caminho inexistente.

    Args:
        tmp_path (Path): Diretório temporário gerado pelo pytest.

    Raises:
        FileNotFoundError: Quando o caminho não existe.
    """
    p: Path = tmp_path / "not_exists.txt"
    with pytest.raises(expected_exception=FileNotFoundError):
        main_tools.validate_path(path_neutral=p)


def test_get_id_consistency(temp_file_fixture: Path) -> None:
    """
    Testa se get_id gera UUID consistente para o mesmo arquivo.

    Args:
        temp_file_fixture (Path): Fixture de arquivo temporário.

    Asserts:
        Dois UUIDs gerados são iguais e válidos.
    """
    id1: str = main_tools.get_id(path_neutral=temp_file_fixture)
    id2: str = main_tools.get_id(path_neutral=str(temp_file_fixture.resolve()))
    assert id1 == id2
    assert isinstance(uuid.UUID(id1), uuid.UUID)


def test_get_name(temp_file_fixture: Path, temp_hidden_file_fixture: Path) -> None:
    """
    Testa se get_name retorna o nome correto do arquivo e arquivo oculto.

    Args:
        temp_file_fixture (Path): Fixture de arquivo temporário.
        temp_hidden_file_fixture (Path): Fixture de arquivo oculto temporário.

    Asserts:
        Nome do arquivo normal e oculto estão corretos.
    """
    assert main_tools.get_name(path_neutral=temp_file_fixture) == "testfile.txt"
    assert main_tools.get_name(path_neutral=temp_hidden_file_fixture) == ".hiddenfile"


def test_get_size_file(temp_file_fixture: Path) -> None:
    """
    Testa se get_size retorna o tamanho correto para um arquivo.

    Args:
        temp_file_fixture (Path): Fixture de arquivo temporário.

    Asserts:
        Tamanho retornado bate com o tamanho real do arquivo.
    """
    size: int = main_tools.get_size(path_neutral=temp_file_fixture)
    assert size == temp_file_fixture.stat().st_size


def test_get_size_directory(temp_dir_with_files_fixture: Path) -> None:
    """
    Testa se get_size retorna o tamanho total correto para um diretório.

    Args:
        temp_dir_with_files_fixture (Path): Fixture de diretório com arquivos.

    Asserts:
        Tamanho somado dos arquivos é igual ao tamanho retornado.
    """
    size: int = main_tools.get_size(path_neutral=temp_dir_with_files_fixture)
    expected: int = sum(f.stat().st_size for f in temp_dir_with_files_fixture.iterdir())
    assert size == expected


def test_get_size_nonexistent(tmp_path: Path) -> None:
    """
    Testa se get_size retorna zero para caminho inexistente.

    Args:
        tmp_path (Path): Diretório temporário gerado pelo pytest.

    Asserts:
        Valor retornado é zero.
    """
    p: Path = tmp_path / "nonexistent"
    assert main_tools.get_size(path_neutral=p) == 0


def test_get_dates(temp_file_fixture: Path) -> None:
    """
    Testa se get_dates retorna dicionário com datas válidas.

    Args:
        temp_file_fixture (Path): Fixture de arquivo temporário.

    Asserts:
        Dicionário contém datetime para criação, modificação e acesso.
    """
    dates: dict[str, datetime] = main_tools.get_dates(path_neutral=temp_file_fixture)
    assert isinstance(dates, dict)
    assert all(isinstance(v, datetime) for v in dates.values())


def test_get_permissions(tmp_path: Path) -> None:
    """
    Testa se get_permissions retorna permissões reais do arquivo.

    Args:
        tmp_path (Path): Diretório temporário gerado pelo pytest.

    Asserts:
        Permissões 'read' e 'write' são True para arquivo criado.
        Permissão 'execute' é boolean.
    """
    file: Path = tmp_path / "perm_test.txt"
    file.write_text("test")
    perms: dict[str, bool] = main_tools.get_permissions(path_neutral=file)
    assert perms["read"] is True
    assert perms["write"] is True
    assert isinstance(perms["execute"], bool)


def test_is_hidden_path(temp_file_fixture: Path, temp_hidden_file_fixture: Path) -> None:
    """
    Testa se is_hidden_path identifica arquivos ocultos corretamente.

    Args:
        temp_file_fixture (Path): Fixture de arquivo temporário.
        temp_hidden_file_fixture (Path): Fixture de arquivo oculto temporário.

    Asserts:
        Arquivo normal não é oculto.
        Arquivo oculto é detectado como oculto.
    """
    assert not main_tools.is_hidden_path(path_neutral=temp_file_fixture)
    assert main_tools.is_hidden_path(path_neutral=temp_hidden_file_fixture)
