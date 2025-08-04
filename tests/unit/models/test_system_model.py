# # pylint: disable=C

# from pathlib import Path

# from models.system_model import ItemDeSistema, PastaBase, SistemaOperacional


# def test_itembase_valido() -> None:
#     item = ItemDeSistema(nome="teste.txt", caminho=Path("/tmp/teste.txt"), tipo="ARQUIVO", tamanho=123)
#     assert item.nome == "teste.txt"
#     assert item.tipo == "ARQUIVO"
#     assert item.tamanho == 123


# # def test_itembase_invalido_tipo() -> None:
# #     with pytest.raises(expected_exception=ValueError, match="Tipo inválido"):
# #         ItemDeSistema(nome="invalido", caminho=Path("/tmp/xyz"), tipo="desconhecido")


# def test_pastabase_sem_itens() -> None:
#     pasta = PastaBase(nome="vazia", caminho=Path("/tmp/vazia"))
#     assert pasta.total_itens() == 0
#     assert pasta.arquivos == []
#     assert pasta.subpastas == []


# def test_pastabase_com_arquivos_e_pastas() -> None:
#     arquivo1 = ItemDeSistema(
# nome="arquivo1.txt", caminho=Path("/tmp/arquivo1.txt"), tipo="ARQUIVO", tamanho=100)
#     pasta1 = ItemDeSistema(nome="pasta1", caminho=Path("/tmp/pasta1"), tipo="PASTA'")

#     pasta_base = PastaBase(
#         nome="base",
#         caminho=Path("/tmp/base"),
#         arquivos=[arquivo1],
#         subpastas=[pasta1],
#     )

#     assert pasta_base.total_itens() == 2
#     assert pasta_base.arquivos[0].nome == "arquivo1.txt"
#     assert pasta_base.subpastas[0].tipo == "PASTA'"


# def test_sistema_operacional(tmp_path: Path) -> None:
#     # Setup: cria estrutura temporária
#     arquivo: Path = tmp_path / "teste.txt"
#     arquivo.write_text(data="conteúdo")

#     subpasta: Path = tmp_path / "docs"
#     subpasta.mkdir()

#     arquivo_item = ItemDeSistema(
# nome=arquivo.name, caminho=arquivo, tipo="ARQUIVO", tamanho=arquivo.stat().st_size)
#     pasta_item = ItemDeSistema(
# nome=subpasta.name, caminho=subpasta, tipo="PASTA'")

#     pasta_base = PastaBase(
# nome=tmp_path.name, caminho=tmp_path, arquivos=[arquivo_item], subpastas=[pasta_item])

#     so = SistemaOperacional(nome="Linux", versao="Ubuntu 22.04", pasta_usuario=pasta_base)

#     estrutura = so.listar_estrutura()

#     assert estrutura["nome"] == "Linux"
#     assert estrutura["versao"] == "Ubuntu 22.04"
#     assert estrutura["total_arquivos"] == 1
#     assert estrutura["total_subpastas"] == 1
