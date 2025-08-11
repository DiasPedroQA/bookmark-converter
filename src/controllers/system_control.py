# """
# Controller CLI para manipulação e análise de arquivos, pastas e sistema operacional.

# Principais recursos:
# - Exibir informações do sistema
# - Validar caminhos (arquivo ou pasta)
# - Analisar conteúdo de arquivos
# - Analisar conteúdo de pastas com listagem recursiva
# - Filtrar pastas e arquivos na home
# - Buscar arquivos por extensão
# - Listar pastas vazias
# - Listar maiores arquivos
# """

# import re
# import time
# from pathlib import Path

# from models.sistema_operacional_model import SistemaOperacional


# class ModeloDeController:
#     """
#     Docstring para SistemaController
#     """
#     def __init__(self) -> None:
#         """Inicializa o controller com um SistemaOperacional detectado."""
#         self.sistema = SistemaOperacional()

#     # ----------------------
#     #   MÉTODOS PRINCIPAIS
#     # ----------------------

#     def validar_caminho(self, caminho: Path) -> bool:
#         """
#         Valida um caminho (arquivo ou pasta) no contexto do sistema operacional atual.
#         """
#         return self.sistema.validar_caminho(caminho_path=caminho)

#     def listar_pastas_home(self) -> list[Path]:
#         """Lista todas as pastas na home do usuário."""
#         return self.sistema.pastas_publicas

#     def listar_arquivos_home(self) -> list[Path]:
#         """Lista todos os arquivos na home do usuário."""
#         return self.sistema.arquivos_publicos

#     # def buscar_por_extensao(self, extensao: str) -> list[Path]:
#     #     """
#     #     Lista arquivos na home com a extensão especificada.
#     #     Exemplo: buscar_por_extensao('.txt')
#     #     """
#     #     if not extensao.startswith("."):
#     #         extensao = "." + extensao
#     #     return [p for p in self.sistema.arquivos_publicos if p.suffix.lower() == extensao.lower()]

#     def listar_pastas_vazias_home(self) -> list[Path]:
#         """Lista pastas vazias na home do usuário."""
#         return [p for p in self.sistema.pastas_publicas if not any(p.iterdir())]

#     def listar_maiores_arquivos_home(self, qnte_lim_files: int = 5) -> list[Path]:
#         """
#         Lista os maiores arquivos na home.
#         :param qnte_lim_files: Quantos arquivos retornar (default: 5)
#         """
#         arquivos: list[Path] = self.sistema.arquivos_publicos
#         return sorted(arquivos, key=lambda p: p.stat().st_size, reverse=True)[:qnte_lim_files]

#     # ----------------------
#     #   MÉTODOS EXTRA
#     # ----------------------

#     def filtrar_por_regex(self, padrao: str, somente_arquivos: bool = True) -> list[Path]:
#         """
#         Filtra arquivos/pastas na home usando uma regex.
#         :param padrao: Expressão regular para filtrar nomes.
#         :param somente_arquivos: Se True, busca só arquivos. Se False, inclui pastas.
#         """

#         lista: list[Path] = (
#             self.sistema.arquivos_publicos
#             if somente_arquivos
#             else (self.sistema.arquivos_publicos + self.sistema.pastas_publicas)
#         )
#         return [p for p in lista if re.search(pattern=padrao, string=p.name)]

#     def buscar_por_nome(self, nome: str, ignorar_maiusculas: bool = True) -> list[Path]:
#         """
#         Busca arquivos/pastas pelo nome.
#         :param nome: Parte do nome a ser buscada.
#         :param ignorar_maiusculas: Ignora diferenças entre maiúsculas e minúsculas.
#         """
#         termo: str = nome.lower() if ignorar_maiusculas else nome
#         return [
#             p
#             for p in (self.sistema.arquivos_publicos + self.sistema.pastas_publicas)
#             if (p.name.lower() if ignorar_maiusculas else p.name).find(termo) != -1
#         ]

#     def listar_modificados_recentemente(self, dias: int = 7) -> list[Path]:
#         """
#         Lista arquivos modificados nos últimos X dias.
#         """
#         agora: float = time.time()
#         limite_segundos: int = dias * 86400
#         return [p for p in self.sistema.arquivos_publicos if (agora - p.stat().st_mtime) <= limite_segundos]
