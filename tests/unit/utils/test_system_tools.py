"""
test_system_tools.py
---------------------
Testes unitários para o módulo system_tools.py.

Cobre detecção de sistema operacional, regex de caminhos,
validação de caminhos específicos por SO, obtenção de pasta raiz do usuário,
e detecção de sistema de arquivos com psutil.
"""

# import platform
# import re
# from pathlib import Path
# from typing import NoReturn

# import pytest

# from src.utils import system_tools

# current_os: str = platform.system().lower()


# def test_get_os_name_lower() -> None:
#     """Testa se _get_os_name_lower retorna o SO atual em minúsculas."""
#     os_lower: str = system_tools._get_os_name_lower()
#     assert isinstance(os_lower, str)
#     assert os_lower == current_os


# def test_get_regex_for_os_known() -> None:
#     """Testa regex padrão para SOs conhecidos."""
#     for os_name in ["windows", "linux", "darwin"]:
#         regex: re.Pattern = system_tools._get_regex_for_os(os_name_lower=os_name)
#         assert isinstance(regex, re.Pattern)
#         assert regex.pattern != ""


# def test_get_regex_for_os_unknown() -> None:
#     """Testa regex padrão para SO desconhecido (deve usar Linux)."""
#     regex: re.Pattern = system_tools._get_regex_for_os("unknown_os")
#     assert regex.pattern == system_tools._REGEX_PATHS["linux"].pattern


# def test_detect_system() -> None:
#     """Testa se detect_system retorna o nome correto do SO."""
#     detected: str = system_tools.detect_system()
#     assert isinstance(detected, str)
#     assert detected.lower() == current_os


# def test_system_path_regex() -> None:
#     """Testa se system_path_regex retorna regex compatível com SO atual."""
#     regex: re.Pattern = system_tools.system_path_regex()
#     expected_regex: re.Pattern[str] = system_tools._REGEX_PATHS.get(current_os, system_tools._REGEX_PATHS["linux"])
#     assert isinstance(regex, re.Pattern)
#     assert regex.pattern == expected_regex.pattern


# @pytest.mark.parametrize(
#     argnames="path,expected_format,expected_pattern,os_list",
#     argvalues=[
#         # Windows
#         ("C:\\Windows\\System32\\cmd.exe", True, True, ["windows"]),
#         ("C:\\NotAPath\\file.txt", True, False, ["windows"]),
#         ("D:\\Documents\\file.docx", True, True, ["windows"]),
#         ("not/a/valid\\path", False, False, ["windows", "linux", "darwin"]),
#         # Linux
#         ("/usr/bin/bash", True, True, ["linux"]),
#         ("/random/unknown/path", True, False, ["linux"]),
#         ("/etc/passwd", True, True, ["linux"]),
#         # Darwin (Mac)
#         ("/Applications/Safari.app", True, True, ["darwin"]),
#         ("/Users/username/Library/Preferences", True, True, ["darwin"]),
#         ("/System/Library", True, True, ["darwin"]),
#     ],
# )
# def test_validate_os_path(path: str, expected_format: bool, expected_pattern: bool, os_list: list[str]) -> None:
#     """
#     Testa validate_os_path para vários caminhos e SOs.

#     Pula o teste se o SO atual não estiver na lista.
#     """
#     if current_os not in os_list:
#         pytest.skip(reason=f"Teste válido só para SO(s): {os_list}")

#     result: dict[str, bool] = system_tools.validate_os_path(path=path, validate_existence=False)
#     assert result["formato_valido"] is expected_format
#     assert result["padrao_reconhecido"] is expected_pattern


# def test_get_user_root_folder(tmp_path: Path) -> None:
#     """
#     Testa get_user_root_folder com caminho base e padrão.

#     Verifica se retorna caminho resolvido corretamente.
#     """
#     base = str(tmp_path)
#     resolved: Path = system_tools.get_user_root_folder(base_path=base)
#     assert resolved == tmp_path.resolve()

#     home_path: Path = system_tools.get_user_root_folder()
#     assert home_path == Path.home().resolve()


# def test_detect_filesystem_known(tmp_path: Path) -> None:
#     """
#     Testa detect_filesystem com caminho válido.

#     Verifica se o retorno tem as chaves e tipos esperados.
#     """
#     info: dict[str, str] = system_tools.detect_filesystem(path=tmp_path)
#     assert isinstance(info, dict)
#     assert "tipo" in info and isinstance(info["tipo"], str)
#     assert "ponto_montagem" in info and isinstance(info["ponto_montagem"], str)
#     assert "opcoes" in info and isinstance(info["opcoes"], str)


# def test_detect_filesystem_invalid_path() -> None:
#     """Testa detect_filesystem para caminho inválido, deve retornar UNKNOWN."""

#     class BadPath:
#         """Classe para simular caminho inválido que lança exceção ao resolver."""

#         def resolve(self) -> NoReturn:
#             """Simula falha ao tentar resolver o caminho."""
#             raise OSError("Invalid path")

#     bad_path = BadPath()
#     info: dict[str, str] = system_tools.detect_filesystem(path=bad_path)  # type: ignore
#     assert info == {"tipo": "UNKNOWN", "ponto_montagem": "", "opcoes": ""}
