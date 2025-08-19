# import os
# import platform
# import re

# import pytest
# from pydantic import ValidationError



# def validar_id_gerado(texto: str) -> IdentificadorValido | ErroIdentificadorInvalido:
#     """
#     Valida a string de entrada e retorna o modelo de sucesso ou erro.
#     """
#     if not texto or not texto.strip():
#         return ErroIdentificadorInvalido(valor_entrada=texto)

#     id_formatado: str = gerar_id_formatado(texto=texto)
#     return IdentificadorValido(valor_entrada=id_formatado)


# def get_regex_caracteres_proibidos() -> re.Pattern[str]:
#     sistema: str = platform.system().lower()
#     if "windows" in sistema:
#         return re.compile(pattern=r'[<>:"/\\|?*\x00-\x1F]')
#     elif "darwin" in sistema:
#         return re.compile(pattern=r"[:]")
#     else:
#         return re.compile(pattern=r"[/]")

# NOMES_RESERVADOS_WINDOWS: set[str] = {
#     "CON",
#     "PRN",
#     "AUX",
#     "NUL",
#     *{f"COM{i}" for i in range(1, 10)},
#     *{f"LPT{i}" for i in range(1, 10)},
# }


# def validar_nome(teste: str) -> NomeValido | ErroNomeInvalido:
#     if not teste or teste.strip() == "":
#         return ErroNomeInvalido(valor_entrada=teste, mensagem="Nome inválido: vazio ou apenas espaços.")

#     if teste.startswith("."):
#         return ErroNomeInvalido(valor_entrada=teste, mensagem="Nome inválido: não pode começar com ponto '.' ")

#     regex: re.Pattern[str] = get_regex_caracteres_proibidos()
#     if regex.search(string=teste):
#         return ErroNomeInvalido(valor_entrada=teste, mensagem="Nome inválido: contém caracteres proibidos.")

#     if platform.system().lower() == "windows":
#         nome_sem_ext: str = os.path.splitext(teste)[0].upper()
#         if nome_sem_ext in NOMES_RESERVADOS_WINDOWS:
#             return ErroNomeInvalido(
#                 valor_entrada=teste, mensagem=f"Nome inválido: '{nome_sem_ext}' é um nome reservado no Windows."
#             )
#         if teste.endswith(" ") or teste.endswith("."):
#             return ErroNomeInvalido(
#                 valor_entrada=teste, mensagem="Nome inválido: não pode terminar com espaço ou ponto no Windows."
#             )

#     return NomeValido(valor_entrada=teste)


# def test_gerar_id_formatado_formato_correto() -> None:
#     texto = "teste123"
#     id_gerado: str = gerar_id_formatado(texto=texto)

#     # Verifica comprimento
#     assert len(id_gerado) == 36

#     # Regex esperado
#     padrao = r"^[a-f0-9]{6}(-[a-f0-9]{6}){4}$"
#     assert re.match(pattern=padrao, string=id_gerado)


# def test_validar_id_com_entrada_valida() -> None:
#     texto = "usuario_valido"
#     resultado: IdentificadorValido | ErroIdentificadorInvalido = validar_id_gerado(texto=texto)

#     assert isinstance(resultado, IdentificadorValido)
#     assert resultado.status is True
#     assert resultado.mensagem == "Identificador válido."
#     assert len(resultado.valor_entrada) == 36


# def test_validar_id_com_entrada_vazia() -> None:
#     resultado: IdentificadorValido | ErroIdentificadorInvalido = validar_id_gerado(texto="")
#     assert isinstance(resultado, ErroIdentificadorInvalido)
#     assert resultado.status is False
#     assert resultado.valor_entrada == ""
#     assert "inválido" in resultado.mensagem


# def test_validar_id_com_espacos_em_branco() -> None:
#     resultado: IdentificadorValido | ErroIdentificadorInvalido = validar_id_gerado(texto="   ")
#     assert isinstance(resultado, ErroIdentificadorInvalido)
#     assert resultado.status is False
#     assert resultado.valor_entrada == "  "


# def test_validar_id_com_none() -> None:
#     resultado: IdentificadorValido | ErroIdentificadorInvalido = validar_id_gerado(texto="")
#     assert isinstance(resultado, ErroIdentificadorInvalido)
#     assert resultado.status is False
#     assert resultado.valor_entrada is not None
#     assert resultado.valor_entrada == ""


# @pytest.mark.parametrize(argnames="entrada", argvalues=["abc", "senha123", "123456789", "outracoisaqualquer"])
# def test_ids_diferentes_para_dados_diferentes(entrada) -> None:
#     id1: str = gerar_id_formatado(texto=entrada)
#     id2: str = gerar_id_formatado(texto=entrada + "extra")
#     assert id1 != id2


# def test_nome_valido_padrao() -> None:
#     resultado: NomeValido | ErroNomeInvalido = validar_nome(teste="meu_arquivo.txt")
#     assert isinstance(resultado, NomeValido)
#     assert resultado.status is True
#     assert resultado.valor_entrada == "meu_arquivo.txt"
#     assert resultado.mensagem == "Nome válido."


# def test_nome_vazio() -> None:
#     resultado: NomeValido | ErroNomeInvalido = validar_nome(teste="")
#     assert isinstance(resultado, ErroNomeInvalido)
#     assert resultado.status is False
#     assert resultado.valor_entrada == ""
#     assert resultado.mensagem == "Nome inválido: vazio ou apenas espaços."


# def test_nome_com_espacos() -> None:
#     resultado: NomeValido | ErroNomeInvalido = validar_nome(teste="   ")
#     assert isinstance(resultado, ErroNomeInvalido)
#     assert resultado.status is False
#     assert resultado.valor_entrada == "   "
#     assert resultado.mensagem == "Nome inválido: vazio ou apenas espaços."


# def test_nome_comecando_ponto() -> None:
#     resultado: NomeValido | ErroNomeInvalido = validar_nome(teste=".oculto")
#     assert isinstance(resultado, ErroNomeInvalido)
#     assert resultado.status is False
#     assert resultado.valor_entrada == ".oculto"
#     assert resultado.mensagem == "Nome inválido: não pode começar com ponto '.' "


# @pytest.mark.parametrize(
#     argnames="nome", argvalues=["arquivo/", "arq\\log", "a|b", "a:b", "a*.*", "a?b", "<script>", ">out"]
# )
# def test_nome_caracteres_proibidos(nome) -> None:
#     resultado: NomeValido | ErroNomeInvalido = validar_nome(teste=nome)
#     assert isinstance(resultado, ErroNomeInvalido)
#     assert resultado.status is False
#     assert resultado.valor_entrada == nome
#     assert resultado.mensagem == "Nome inválido: contém caracteres proibidos."


# def test_nome_com_255_caracteres() -> None:
#     nome: str = "a" * 255
#     resultado: NomeValido | ErroNomeInvalido = validar_nome(teste=nome)
#     assert isinstance(resultado, NomeValido)
#     assert resultado.status is True
#     assert resultado.valor_entrada == nome


# def test_nome_maior_que_255() -> None:
#     nome: str = "a" * 256
#     with pytest.raises(expected_exception=ValidationError):
#         ErroNomeInvalido(valor_entrada=nome)
