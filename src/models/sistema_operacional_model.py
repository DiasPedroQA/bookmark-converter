# """
# Módulo sistema_operacional_model.py

# Modelo que representa o sistema operacional local, suas informações básicas
# e oferece métodos para listar arquivos, pastas e validar caminhos com base nas regras do SO.

# Utiliza funções utilitárias de:
# - sistema_arquivos (filtros, buscas por extensão)
# - sistema_pastas (filtros, listagem recursiva de pastas vazias)
# - main_tools (normalização de caminhos)
# - utils_so (validação de permissões e formatos de caminho)
# """

# import platform
# from dataclasses import dataclass, field
# from getpass import getuser
# from pathlib import Path

# from utils.file_tools import buscar_por_extensao, filtrar_apenas_arquivos
# from utils.system_tools import tem_permissao_leitura, verificar_caminho_so
# from utils.folder_tools import (
#     filtrar_pastas,
#     listar_pastas_vazias,
# )
# from src.utils.main_tools import (
#     normalizar_caminho,
# )


# @dataclass(frozen=True)
# class ModeloDeOperacional:
#     """
#     Representa o sistema operacional local e fornece métodos para interagir com
#     o sistema de arquivos do usuário logado, incluindo listagens e validações.
#     """

#     nome_so: str = field(default_factory=platform.system)
#     versao: str = field(default_factory=platform.version)
#     usuario_logado: str = field(default_factory=getuser)
#     pasta_usuario: Path = field(default_factory=Path.home)
#     arquitetura: str = field(default_factory=lambda: platform.architecture()[0])

#     @property
#     def arquivos_publicos(self) -> list[Path]:
#         """
#         Retorna lista dos arquivos visíveis (não ocultos) na pasta home do usuário.
#         """
#         return filtrar_apenas_arquivos(self.pasta_usuario.iterdir())

#     @property
#     def pastas_publicas(self) -> list[Path]:
#         """
#         Retorna lista das pastas visíveis (não ocultas) na pasta home do usuário.
#         """
#         return filtrar_pastas(itens=self.pasta_usuario.iterdir())

#     def listar_pastas_vazias_home(self) -> list[Path]:
#         """
#         Retorna todas as pastas vazias dentro da pasta home, recursivamente.
#         """
#         return listar_pastas_vazias(self.pasta_usuario)

#     def listar_maiores_arquivos_home(self, qnte_lim_files: int = 5) -> list[Path]:
#         """
#         Retorna os maiores arquivos da pasta home, limitados por qnte_lim_files.
#         """
#         arquivos: list[Path] = filtrar_apenas_arquivos(paths=self.pasta_usuario.iterdir())
#         return sorted(arquivos, key=lambda p: p.stat().st_size, reverse=True)[:qnte_lim_files]

#     def buscar_por_extensao_home(self, extensao: str) -> list[Path]:
#         """
#         Busca arquivos na pasta home que tenham a extensão passada (ex: '.txt').
#         """
#         return buscar_por_extensao(pasta=self.pasta_usuario, extensao=extensao)

#     def informacoes(self) -> dict:
#         """
#         Retorna um dicionário com informações básicas do SO, usuário e arquivos/pastas públicos.
#         """
#         return {
#             "nome_so": self.nome_so,
#             "versao": self.versao,
#             "usuario_logado": self.usuario_logado,
#             "pasta_usuario": str(self.pasta_usuario),
#             "arquitetura": self.arquitetura,
#             "arquivos_publicos": [str(p) for p in self.arquivos_publicos],
#             "pastas_publicas": [str(p) for p in self.pastas_publicas],
#         }

#     def validar_caminho(self, caminho_path: Path) -> bool:
#         """
#         Valida se o caminho existe, se tem permissão de leitura e se o formato do caminho
#         bate com as regras do sistema operacional atual.

#         Retorna True se válido, False caso contrário.
#         """
#         caminho_normal = normalizar_caminho(caminho_path)

#         if not caminho_normal.exists():
#             print("❌ Caminho não existe.")
#             return False

#         if not tem_permissao_leitura(caminho_normal):
#             print("❌ Sem permissão de leitura.")
#             return False

#         formato_ok = verificar_caminho_so(caminho_normal).get("formato_valido", False)
#         if not formato_ok:
#             print("❌ Caminho inválido para este SO.")
#             return False

#         return True
