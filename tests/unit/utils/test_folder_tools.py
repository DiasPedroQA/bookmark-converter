"""
test_file_tools.py
------------------
Testes unitários para o módulo file_tools.py.

Cobre leitura e escrita de arquivos texto, incluindo
validação de caminhos, manipulação de encoding, e
checagem de erros esperados.
"""

from pathlib import Path
from collections.abc import Generator

import pytest

from src.utils import file_tools


@pytest.fixture
def temp_text_file(tmp_path: Path) -> Generator[Path, None, None]:
    """
    Fixture que cria um arquivo de texto temporário com conteúdo inicial.

    Args:
        tmp_path (Path): Diretório temporário gerado pelo pytest.

    Yields:
        Path: Caminho do arquivo temporário criado.
    """
    file: Path = tmp_path / "sample.txt"
    file.write_text(data="initial content", encoding="utf-8")
    yield file


def test_read_text_content_success(temp_text_file: Path) -> None:
    """
    Testa leitura de conteúdo texto de um arquivo válido.

    Args:
        temp_text_file (Path): Fixture de arquivo temporário.

    Asserts:
        O conteúdo lido é igual ao conteúdo escrito.
    """
    content: str = file_tools.read_text_content(file_path=temp_text_file)
    assert content == "initial content"


def test_read_text_content_file_not_found(tmp_path: Path) -> None:
    """
    Testa se read_text_content lança FileNotFoundError para arquivo inexistente.

    Args:
        tmp_path (Path): Diretório temporário gerado pelo pytest.

    Raises:
        FileNotFoundError: Quando o arquivo não existir.
    """
    non_existent_file: Path = tmp_path / "does_not_exist.txt"
    with pytest.raises(expected_exception=FileNotFoundError):
        file_tools.read_text_content(file_path=non_existent_file)


def test_read_text_content_not_a_file(tmp_path: Path) -> None:
    """
    Testa se read_text_content lança FileNotFoundError para um diretório.

    Args:
        tmp_path (Path): Diretório temporário gerado pelo pytest.

    Raises:
        FileNotFoundError: Quando o caminho for um diretório, não arquivo.
    """
    dir_path: Path = tmp_path / "a_directory"
    dir_path.mkdir()
    with pytest.raises(expected_exception=FileNotFoundError):
        file_tools.read_text_content(file_path=dir_path)


def test_read_text_content_with_different_encoding(tmp_path: Path) -> None:
    """
    Testa leitura de arquivo texto com encoding especificado.

    Args:
        tmp_path (Path): Diretório temporário gerado pelo pytest.

    Asserts:
        O conteúdo é lido corretamente com encoding utf-16.
    """
    file: Path = tmp_path / "utf16file.txt"
    file.write_text(data="texto com acentuação", encoding="utf-16")
    content: str = file_tools.read_text_content(file_path=file, encoding="utf-16")
    assert content == "texto com acentuação"


def test_write_text_content_success(tmp_path: Path) -> None:
    """
    Testa escrita de conteúdo texto em arquivo novo.

    Args:
        tmp_path (Path): Diretório temporário gerado pelo pytest.

    Asserts:
        Conteúdo escrito é lido corretamente.
    """
    file: Path = tmp_path / "write_test.txt"
    file_tools.write_text_content(file, content="novo conteúdo")
    read_back = file.read_text(encoding="utf-8")
    assert read_back == "novo conteúdo"


def test_write_text_content_overwrite(temp_text_file: Path) -> None:
    """
    Testa sobrescrição de conteúdo em arquivo existente.

    Args:
        temp_text_file (Path): Fixture de arquivo temporário.

    Asserts:
        Conteúdo antigo é substituído pelo novo conteúdo.
    """
    file_tools.write_text_content(file_path=temp_text_file, content="conteúdo atualizado")
    content = temp_text_file.read_text(encoding="utf-8")
    assert content == "conteúdo atualizado"
