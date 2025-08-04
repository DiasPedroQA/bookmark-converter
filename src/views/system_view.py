"""
Docstring para views.system_view
"""


from pathlib import Path


def exportar_json(json_str: str, caminho_destino: Path) -> None:
    """Exporta a string JSON para um arquivo."""
    caminho_destino.write_text(json_str, encoding="utf-8")
    print(f"✅ Arquivo exportado para: {caminho_destino}")


def exportar_csv(filhos_pastas: list[Path], filhos_arquivos: list[Path], destino: Path) -> None:
    """Exporta pastas e arquivos separados por tipo para CSV simples."""
    linhas: list[str] = ["tipo,nome,caminho"]
    for pasta in filhos_pastas:
        linhas.append(f"PASTA,{pasta.name},{pasta}")
    for arquivo in filhos_arquivos:
        linhas.append(f"ARQUIVO,{arquivo.name},{arquivo}")

    destino.write_text("\n".join(linhas), encoding="utf-8")
    print(f"✅ Arquivo CSV exportado em: {destino}")
