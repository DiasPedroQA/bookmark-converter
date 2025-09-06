# """
# folder_utils.py
# ----------------

# Funções utilitárias de manipulação de pastas e arquivos:
# - Filtragem por tipo, nome, extensão e tamanho
# - Montagem de árvore hierárquica
# - Leitura e escrita de arquivos de texto
# - Geração de slugs
# """

# import re
# from pathlib import Path

# from .global_tools import (
#     buscar_apenas_arquivos,
#     buscar_apenas_pastas,
#     buscar_conteudo_pasta,
#     check_valid_path,
# )

# # ============================================================
# # [ARQUIVOS]
# # ============================================================


# def gerar_slug(texto: str) -> str:
#     """
#     Converte texto em slug (URL-friendly).

#     Args:
#         texto: Texto para converter em slug

#     Returns:
#         str: Slug gerado a partir do texto
#     """
#     # Remove caracteres especiais, converte para minúsculas e substitui espaços por hífens
#     slug: str = re.sub(r"[^a-zA-Z0-9\s]", "", texto)
#     slug = slug.lower().strip()
#     slug = re.sub(r"\s+", "-", slug)
#     return re.sub(r"-+", "-", slug).strip("-")


# def ler_conteudo_texto(caminho_arquivo: str | Path, codificacao: str = "utf-8") -> str:
#     """
#     Lê conteúdo de um arquivo de texto.

#     Args:
#         caminho_arquivo: Caminho do arquivo para ler
#         codificacao: Codificação do arquivo (padrão: utf-8)

#     Returns:
#         str: Conteúdo do arquivo

#     Raises:
#         FileNotFoundError: Se o arquivo não for encontrado
#         ValueError: Se o caminho não for um arquivo válido
#         IOError: Se ocorrer erro na leitura
#     """
#     arquivo_validado: Path = check_valid_path(caminho_generico=caminho_arquivo)
#     if not arquivo_validado.is_file():
#         raise ValueError(f"Não é um arquivo válido: {arquivo_validado}")

#     try:
#         return arquivo_validado.read_text(encoding=codificacao)
#     except (IOError, OSError, UnicodeDecodeError) as erro:
#         raise IOError(f"Erro ao ler arquivo {arquivo_validado}: {erro}")


# def escrever_conteudo_texto(
#     caminho_arquivo: str | Path, conteudo: str, codificacao: str = "utf-8", modo: str = "w"
# ) -> None:
#     """
#     Escreve conteúdo em um arquivo de texto.

#     Args:
#         caminho_arquivo: Caminho do arquivo para escrever
#         conteudo: Conteúdo a ser escrito
#         codificacao: Codificação do arquivo (padrão: utf-8)
#         modo: Modo de escrita ('w' para write, 'a' para append)

#     Raises:
#         IOError: Se ocorrer erro na escrita
#     """
#     caminho = Path(caminho_arquivo)

#     try:
#         with open(caminho, modo, encoding=codificacao) as arquivo:
#             arquivo.write(conteudo)
#     except (IOError, OSError) as erro:
#         raise IOError(f"Erro ao escrever arquivo {caminho}: {erro}")


# # ============================================================
# # [PASTAS] - Funções de filtragem
# # ============================================================


# def buscar_apenas_pastas(itens: list[Path]) -> list[Path]:
#     """
#     Filtra apenas pastas de uma lista de itens.

#     Args:
#         itens: Lista de caminhos para filtrar

#     Returns:
#         list[Path]: Lista contendo apenas pastas
#     """
#     return [item for item in itens if item.is_dir()]


# def buscar_apenas_arquivos(itens: list[Path]) -> list[Path]:
#     """
#     Filtra apenas arquivos de uma lista de itens.

#     Args:
#         itens: Lista de caminhos para filtrar

#     Returns:
#         list[Path]: Lista contendo apenas arquivos
#     """
#     return [item for item in itens if item.is_file()]


# def buscar_por_nome(
#     pasta_base: str | Path,
#     prefixo: Optional[str] = None,
#     sufixo: Optional[str] = None,
#     case_sensitive: bool = False,
#     recursivo: bool = False,
# ) -> list[Path]:
#     """
#     Busca itens pelo prefixo ou sufixo do nome.

#     Args:
#         pasta_base: Pasta base para busca
#         prefixo: Prefixo do nome para filtrar
#         sufixo: Sufixo do nome para filtrar
#         case_sensitive: Se a busca deve ser case sensitive
#         recursivo: Se deve buscar recursivamente

#     Returns:
#         list[Path]: Lista de itens que correspondem aos critérios
#     """
#     pasta_validada: Path = check_valid_path(pasta_base)

#     if not pasta_validada.is_dir():
#         raise ValueError(f"Caminho não é uma pasta: {pasta_validada}")

#     resultados: list[Path] = []
#     itens = buscar_conteudo_pasta(pasta_validada, recursivo)

#     for item in itens:
#         nome = item.name
#         if not case_sensitive:
#             nome = nome.lower()
#             prefixo = prefixo.lower() if prefixo else None
#             sufixo = sufixo.lower() if sufixo else None

#         corresponde_prefixo = prefixo is None or nome.startswith(prefixo)
#         corresponde_sufixo = sufixo is None or nome.endswith(sufixo)

#         if corresponde_prefixo and corresponde_sufixo:
#             resultados.append(item)

#     return resultados


# def buscar_por_extensoes(pasta_base: str | Path, extensoes: list[str], recursivo: bool = False) -> list[Path]:
#     """
#     Busca arquivos por extensões específicas.

#     Args:
#         pasta_base: Pasta base para busca
#         extensoes: Lista de extensões para filtrar
#         recursivo: Se deve buscar recursivamente

#     Returns:
#         list[Path]: Lista de arquivos com as extensões especificadas
#     """
#     pasta_validada: Path = check_valid_path(pasta_base)

#     if not pasta_validada.is_dir():
#         raise ValueError(f"Caminho não é uma pasta: {pasta_validada}")

#     # Normalizar extensões (remover ponto inicial e converter para minúsculas)
#     exts = {ext.lower().lstrip(".") for ext in extensoes}

#     arquivos = global_buscar_apenas_arquivos(pasta_validada, recursivo)
#     return [arquivo for arquivo in arquivos if arquivo.suffix.lower().lstrip(".") in exts]


# def buscar_por_tamanho(
#     pasta_base: str | Path, tamanho_min: int = 0, tamanho_max: Optional[int] = None, recursivo: bool = False
# ) -> list[Path]:
#     """
#     Busca arquivos por intervalo de tamanho.

#     Args:
#         pasta_base: Pasta base para busca
#         tamanho_min: Tamanho mínimo em bytes
#         tamanho_max: Tamanho máximo em bytes (None para sem limite)
#         recursivo: Se deve buscar recursivamente

#     Returns:
#         list[Path]: Lista de arquivos dentro do intervalo de tamanho
#     """
#     pasta_validada: Path = check_valid_path(pasta_base)

#     if not pasta_validada.is_dir():
#         raise ValueError(f"Caminho não é uma pasta: {pasta_validada}")

#     if tamanho_min < 0:
#         raise ValueError("tamanho_min não pode ser negativo")

#     if tamanho_max is not None and tamanho_max < tamanho_min:
#         raise ValueError("tamanho_max não pode ser menor que tamanho_min")

#     arquivos = global_buscar_apenas_arquivos(pasta_validada, recursivo)
#     resultados: list[Path] = []

#     for arquivo in arquivos:
#         try:
#             tamanho = arquivo.stat().st_size
#             if tamanho >= tamanho_min and (tamanho_max is None or tamanho <= tamanho_max):
#                 resultados.append(arquivo)
#         except (OSError, IOError):
#             # Ignorar arquivos inacessíveis
#             continue

#     return resultados


# # ============================================================
# # [ÁRVORE DE PASTAS]
# # ============================================================


# def montar_arvore(
#     pasta_base: str | Path,
#     profundidade_maxima: int = 10,
#     limite_itens: int = 1000,
# ) -> dict[str, Any]:
#     """
#     Gera representação hierárquica de pasta em dicionário.

#     Args:
#         pasta_base: Pasta base para montar a árvore
#         profundidade_maxima: Profundidade máxima de recursão
#         limite_itens: Número máximo de itens a processar

#     Returns:
#         dict[str, Any]: Estrutura hierárquica da árvore de diretórios
#     """
#     pasta_validada: Path = check_valid_path(pasta_base)

#     if not pasta_validada.is_dir():
#         raise ValueError(f"Caminho não é uma pasta: {pasta_validada}")

#     contador: dict[str, int] = {"itens_processados": 0}

#     return {
#         "nome": pasta_validada.name,
#         "caminho": str(pasta_validada),
#         "tipo": "pasta",
#         "filhos": _explorar_diretorio(
#             pasta=pasta_validada,
#             profundidade_maxima=profundidade_maxima,
#             limite_itens=limite_itens,
#             nivel_atual=0,
#             contador=contador,
#         ),
#     }


# def _explorar_diretorio(
#     pasta: Path, profundidade_maxima: int, limite_itens: int, nivel_atual: int, contador: dict[str, int]
# ) -> list[dict[str, Any]]:
#     """
#     Função recursiva interna para montar árvore.

#     Args:
#         pasta: Pasta atual para explorar
#         profundidade_maxima: Profundidade máxima de recursão
#         limite_itens: Número máximo de itens a processar
#         nivel_atual: Nível atual de recursão
#         contador: Contador de itens processados

#     Returns:
#         list[dict[str, Any]]: Lista de filhos do diretório
#     """
#     filhos: list[dict[str, Any]] = []

#     # Verificar limites
#     if nivel_atual >= profundidade_maxima or contador["itens_processados"] >= limite_itens:
#         return filhos

#     try:
#         for item in pasta.iterdir():
#             if contador["itens_processados"] >= limite_itens:
#                 break

#             contador["itens_processados"] += 1

#             if item.is_dir():
#                 filhos.append(
#                     {
#                         "nome": item.name,
#                         "caminho": str(item),
#                         "tipo": "pasta",
#                         "filhos": _explorar_diretorio(
#                             pasta=item,
#                             profundidade_maxima=profundidade_maxima,
#                             limite_itens=limite_itens,
#                             nivel_atual=nivel_atual + 1,
#                             contador=contador,
#                         ),
#                     }
#                 )
#             elif item.is_file():
#                 try:
#                     tamanho = item.stat().st_size
#                     filhos.append(
#                         {
#                             "nome": item.name,
#                             "caminho": str(item),
#                             "tipo": "arquivo",
#                             "tamanho": tamanho,
#                             "extensao": item.suffix,
#                             "filhos": [],
#                         }
#                     )
#                 except (OSError, IOError):
#                     # Arquivo inacessível
#                     filhos.append(
#                         {
#                             "nome": item.name,
#                             "caminho": str(item),
#                             "tipo": "arquivo_erro",
#                             "erro": "acesso_negado",
#                             "filhos": [],
#                         }
#                     )

#     except PermissionError:
#         filhos.append(
#             {
#                 "nome": f"acesso_negado_{pasta.name}",
#                 "caminho": str(pasta),
#                 "tipo": "erro",
#                 "erro": "permissao_negada",
#                 "filhos": [],
#             }
#         )

#     return filhos


# # ============================================================
# # Funções de compatibilidade (aliases)
# # ============================================================

# # Aliases para compatibilidade com código existente
# ler_conteudo_arquivo = ler_conteudo_texto
# escrever_conteudo_arquivo = escrever_conteudo_texto


# if __name__ == "__main__":
#     """Exemplo de uso das funções utilitárias."""
#     try:
#         # Exemplo de uso
#         import tempfile

#         # Criar diretório temporário para teste
#         with tempfile.TemporaryDirectory() as temp_dir:
#             temp_path = Path(temp_dir)

#             # Criar alguns arquivos e pastas de teste
#             (temp_path / "arquivo1.txt").write_text("Conteúdo do arquivo 1")
#             (temp_path / "arquivo2.py").write_text("print('Hello')")
#             (temp_path / "subpasta").mkdir()
#             (temp_path / "subpasta" / "arquivo3.txt").write_text("Conteúdo do arquivo 3")

#             # Testar funções
#             print("Arquivos txt encontrados:")
#             for arquivo in buscar_por_extensoes(temp_path, ["txt"]):
#                 print(f"  - {arquivo.name}")

#             print("\nÁrvore do diretório:")
#             arvore = montar_arvore(temp_path, profundidade_maxima=2)
#             print(f"Pasta: {arvore['nome']}")
#             print(f"Total de filhos: {len(arvore['filhos'])}")

#     except Exception as e:
#         print(f"Erro no exemplo: {e}")
