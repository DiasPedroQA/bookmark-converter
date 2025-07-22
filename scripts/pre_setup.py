"""
Script de pré-configuração para o Makefile do HTMLReader.
"""

# scripts/pre_setup.py

import subprocess
from pathlib import Path


def run() -> None:
    """Executa o script shell que cria a estrutura do projeto"""
    script_path: Path = Path(__file__).resolve().parent.parent / "refatorar_estrutura.sh"
    if not script_path.exists():
        raise FileNotFoundError(f"Script não encontrado: {script_path}")

    print(f"🚀 Executando script de criação de estrutura: {script_path}")
    subprocess.run(args=["bash", str(object=script_path)], check=True)
