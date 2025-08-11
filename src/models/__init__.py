"""
Módulo de agregação de modelos do sistema de arquivos.

Fornece acesso centralizado às classes principais:
- ModeloDeArquivo: manipulação de arquivos individuais.
- ModeloDePasta: gerenciamento de pastas e listagem de conteúdo.
- SistemaOperacional: abstração do sistema operacional com validação de caminhos e permissões.

Importe deste módulo para facilitar o acesso às classes sem precisar referenciar seus caminhos internos.
"""

from .arquivo_model import ModeloDeArquivo
from .pasta_model import ModeloDePasta
from .sistema_operacional_model import SistemaOperacional

__all__: list[str] = [
    "ModeloDePasta",
    "SistemaOperacional",
    "ModeloDeArquivo",
]
