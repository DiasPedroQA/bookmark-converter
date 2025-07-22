"""
Script de pós-configuração para o Makefile do HTMLReader.
"""

# scripts/post_setup.py

from pathlib import Path

# Lista de caminhos esperados
ESTRUTURA_ESPERADA: list[str] = [
    "src/controllers/__init__.py",
    "src/models/__init__.py",
    "src/routes/__init__.py",
    "src/utils/__init__.py",
    "src/views/__init__.py",
    "tests/unit/controllers/__init__.py",
    "tests/unit/models/__init__.py",
    "tests/unit/routes/__init__.py",
    "tests/unit/utils/__init__.py",
    "tests/unit/views/__init__.py",
    "tests/integration/__init__.py",
]


def run() -> None:
    """Valida se a estrutura do projeto foi criada corretamente"""
    print("🔍 Validando estrutura do projeto...")

    base_path: Path = Path(__file__).resolve().parent.parent

    erros: list[str] = []
    for relativo in ESTRUTURA_ESPERADA:
        caminho: Path = base_path / relativo
        if not caminho.exists():
            erros.append(f"❌ Ausente: {relativo}")

    if erros:
        print("\n".join(erros))
        raise RuntimeError("⚠️ Estrutura incompleta. Corrija os problemas acima.")

    print("✅ Estrutura validada com sucesso.")
