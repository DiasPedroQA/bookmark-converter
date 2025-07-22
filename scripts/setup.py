# scripts/setup.py

"""
Script de configuração principal para o Makefile do HTMLReader.

Este script instala as dependências do projeto a partir do arquivo requirements.txt.
Pode ser chamado diretamente ou via Makefile.
"""

import scripts.post_setup as post
import scripts.pre_setup as pre


def main() -> None:
    """Função geral do Makefile"""
    print("🔧 Executando etapa de setup do projeto...")
    pre.run()
    post.run()
    print("✅ Setup completo.")


if __name__ == "__main__":
    main()
