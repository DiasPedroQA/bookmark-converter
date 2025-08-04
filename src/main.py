"""
main.py

Ponto de entrada da aplicação. Controla a execução da coleta de dados
do sistema operacional do usuário logado e exibe/expõe os resultados.

Este módulo pode ser usado como script ou importado como lib.
"""

import json
from pathlib import Path

from controllers.system_control import (
    controller_gerar_json_so,
    controller_listar_filhos_home,
)
from views.system_view import exportar_csv, exportar_json


def exibir_json_formatado(json_str: str) -> None:
    """Exibe um JSON formatado no terminal."""
    try:
        objeto = json.loads(json_str)
        print(json.dumps(objeto, indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print("❌ JSON inválido recebido.")


def executar_pipeline_principal(exportar: bool = False) -> None:
    """Executa o pipeline principal do projeto."""
    print("🔍 Coletando dados do sistema operacional...\n")

    json_so: str | None = controller_gerar_json_so()
    if not json_so:
        print("❌ Não foi possível montar o objeto do sistema.")
        return

    exibir_json_formatado(json_str=json_so)

    if exportar:
        exportar_json(json_str=json_so, caminho_destino=Path("dados_sistema.json"))

    filhos: tuple[list[Path], list[Path]] | None = controller_listar_filhos_home()
    if filhos:
        pastas, arquivos = filhos
        print(f"\n📁 Pastas: {len(pastas)} | 📄 Arquivos: {len(arquivos)}")
        exportar_csv(filhos_pastas=pastas, filhos_arquivos=arquivos, destino=Path("filhos_home.csv"))


if __name__ == "__main__":
    # Defina `True` para salvar os dados em JSON e CSV
    executar_pipeline_principal(exportar=True)
