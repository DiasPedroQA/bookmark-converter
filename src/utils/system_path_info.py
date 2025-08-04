"""
🔧 Módulo utilitário para extração de metadados de arquivos e diretórios (versão aprimorada).

Inclui:
- Informações básicas e detalhadas
- Estatísticas completas
- Permissões no estilo Unix
- Hashes de segurança
- Detecção de sistema de arquivos
"""

import hashlib
import os
from datetime import datetime

from grp import getgrgid
from pathlib import Path
from pprint import pprint
from pwd import getpwuid
from typing import ClassVar

import psutil


# ========== CLASSE COLETORA ==========


class ColetorDeMetadados:
    """Classe responsável por coletar e processar metadados avançados de arquivos e diretórios.

    Esta classe fornece métodos estáticos e de classe para extrair informações detalhadas sobre
    itens do sistema de arquivos, incluindo:
    - Propriedades básicas (nome, tipo, caminho)
    - Estatísticas (tamanho, datas, profundidade)
    - Permissões detalhadas (Unix-style)
    - Conteúdo de diretórios
    - Informações de segurança (proprietário, hashes)
    - Dados do sistema de arquivos

    Attributes:
        _CACHE (ClassVar[dict]): Cache interno para armazenar resultados
        de cálculos de hash, evitando reprocessamento desnecessário.

    Methods:
        _normalizar_caminho: Normaliza caminhos para forma absoluta
        _determinar_tipo: Identifica o tipo de item (arquivo, pasta, etc.)
        _calcular_hash: Calcula hashes criptográficos de arquivos
        _formatar_tamanho: Formata tamanhos em bytes para leitura humana
        _coletar_permissoes_detalhadas: Extrai permissões no estilo Unix
        _calcular_profundidade: Calcula profundidade máxima de diretórios
        _calcular_tamanho_pasta: Calcula tamanho total e contagem de itens
        _listar_conteudo_aprimorado: Lista conteúdo de diretórios com metadados
        _detectar_sistema_arquivos: Identifica o sistema de arquivos utilizado
        _coletar_datas_aprimoradas: Formata timestamps em múltiplos formatos
        coletar_aprimorado: Método principal que coordena a coleta de todos os metadados

    Example:
        >>> coletor = ColetorDeMetadados()
        >>> metadados = coletor.coletar_aprimorado('/caminho/para/arquivo')
        >>> print(metadados['estatisticas']['tamanho']['legivel'])
        '1.23 MB'
    """

    _CACHE: ClassVar[dict[str, tuple[str, str]]] = {}

    @staticmethod
    def _normalizar_caminho(caminho: str | Path) -> Path:
        """Converte e resolve o caminho para forma absoluta."""
        return Path(caminho).expanduser().resolve()

    @staticmethod
    def _determinar_tipo(caminho: Path) -> str:
        """Identifica se o caminho é arquivo, pasta ou desconhecido."""
        if caminho.is_file():
            return "ARQUIVO"
        if caminho.is_dir():
            return "PASTA"
        if caminho.is_symlink():
            return "LINK"
        return "DESCONHECIDO"

    @classmethod
    def _calcular_hash(cls, caminho: Path) -> tuple[str | int, str | int]:
        """Calcula hashes SHA256 e MD5 para arquivos."""
        if not caminho.is_file():
            return 0, 0

        cache_key: str = f"hash_{caminho}"
        if cache_key in cls._CACHE:
            return cls._CACHE[cache_key]

        sha256 = hashlib.sha256()
        md5 = hashlib.md5()

        try:
            with open(file=caminho, mode="rb") as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
                    md5.update(chunk)
            result: tuple[str, str] = str(sha256.hexdigest()), str(md5.hexdigest())
            cls._CACHE[cache_key] = result
            return result
        except ValueError as e:
            print(f"Erro ao calcular hash para {caminho}: {str(e)}")
            return 0, 0

    @staticmethod
    def _formatar_tamanho(bytesize: float) -> str:
        """Formata tamanho em bytes para string legível."""
        for unit in ["B", "KB", "MB", "GB"]:
            if bytesize < 1024:
                return f"{bytesize:.2f} {unit}"
            bytesize /= 1024
        return f"{bytesize:.2f} TB"

    @classmethod
    def _coletar_permissoes_detalhadas(cls, caminho: Path) -> dict[str, str | bool]:
        """Coleta permissões detalhadas no estilo Unix."""
        stat: os.stat_result = caminho.stat()
        mode: int = stat.st_mode

        def obter_permissoes(mask: int) -> str:
            perms: list[str] = ["r", "w", "x"]
            return "".join([perms[i] if mask & (4 >> i) else "-" for i in range(3)])

        return {
            "usuario": obter_permissoes(mode >> 6),
            "grupo": obter_permissoes(mode >> 3),
            "outros": obter_permissoes(mode),
            "octal": oct(mode & 0o777)[2:],
            "sticky": bool(mode & 0o1000),
            "setuid": bool(mode & 0o4000),
            "setgid": bool(mode & 0o2000),
        }

    @classmethod
    def _calcular_profundidade(cls, caminho: Path) -> int:
        """Calcula a profundidade máxima da estrutura de diretórios."""
        max_depth = 0
        caminho_str = str(caminho)
        for root, _, _ in os.walk(caminho):
            depth: int = root[len(caminho_str) + len(os.path.sep) :].count(os.path.sep)
            if max_depth == max(max_depth, depth):
                max_depth: int = depth
        return max_depth

    @classmethod
    def _calcular_tamanho_pasta(cls, caminho: Path) -> tuple[int, int, bool]:
        """Calcula tamanho total e número de itens em uma pasta."""
        total_tamanho = 0
        total_itens = 0
        limite_atingido = False

        def scan(diretorio: Path, nivel: int) -> None:
            nonlocal total_tamanho, total_itens, limite_atingido
            try:
                for item in diretorio.iterdir():
                    if item.is_file():
                        total_tamanho += item.stat().st_size
                        total_itens += 1
                    elif item.is_dir():
                        total_itens += 1
                        if nivel < 10:  # Limite de profundidade
                            scan(diretorio=item, nivel=nivel + 1)
                        else:
                            limite_atingido = True
            except (PermissionError, OSError) as e:
                print(f"Acesso negado em {diretorio}: {str(e)}")

        scan(diretorio=caminho, nivel=1)
        return total_tamanho, total_itens, limite_atingido

    @classmethod
    def _listar_conteudo_aprimorado(
        cls, caminho: Path
    ) -> dict[str, list[dict[str, str | int | float]] | list[dict[str, str | float | None]] | dict[str, int]]:
        """Lista conteúdo de diretórios com mais detalhes."""
        arquivos: list[dict[str, str | int | float]] = []
        pastas: list[dict[str, str | float | None]] = []
        extensoes: dict[str, int] = {}

        for item in caminho.iterdir():
            try:
                stat: os.stat_result = item.stat()
                if item.is_file():
                    ext: str = item.suffix.lower()
                    item_arquivo: dict[str, str | int | float] = {
                        "nome": item.name,
                        "tamanho": stat.st_size,
                        "modificacao": stat.st_mtime,
                        "extensao": ext,
                    }
                    arquivos.append(item_arquivo)
                    extensoes[ext] = extensoes.get(ext, 0) + 1
                elif item.is_dir():
                    item_pasta: dict[str, str | float | None] = {
                        "nome": item.name,
                        "tamanho": None,
                        "modificacao": stat.st_mtime,
                        "extensao": None,
                    }
                    pastas.append(item_pasta)
            except OSError as e:
                print(f"Erro ao processar {item}: {str(e)}")

        return {
            "arquivos": arquivos,
            "pastas": pastas,
            "resumo": {"total_arquivos": len(arquivos), "total_pastas": len(pastas)},
            "tipos": extensoes,
        }

    @classmethod
    def _detectar_sistema_arquivos(cls, caminho: Path) -> dict[str, str]:
        """Detecta o sistema de arquivos onde o item está armazenado."""
        try:
            caminho = caminho.resolve()
            for part in psutil.disk_partitions():
                try:
                    if caminho.is_relative_to(Path(part.mountpoint)):
                        return {
                            "tipo": str(part.fstype),
                            "ponto_montagem": str(part.mountpoint),
                            "opcoes": str(part.opts),
                        }
                except ValueError:
                    continue
        except ImportError:
            pass
        return {"tipo": "UNKNOWN"}

    @classmethod
    def _coletar_datas_aprimoradas(cls, timestamp: float) -> dict[str, float | str]:
        """Cria objeto DatasAprimoradas a partir de um timestamp."""
        dt: datetime = datetime.fromtimestamp(timestamp=timestamp)
        return {"timestamp": timestamp, "iso": dt.isoformat(), "legivel": dt.strftime(format="%d/%m/%Y %H:%M")}

    @classmethod
    def coletar_aprimorado(cls, caminho: str | Path) -> dict[
        str,
        dict[str, str]
        | dict[str, str | dict[str, str | None]]
        | dict[str, dict[str, int | str] | dict[str, int] | dict[str, dict[str, float | str]] | int]
        | dict[str, str | bool]
        | dict[str, list[dict[str, str | int | float]] | list[dict[str, str | float | None]] | dict[str, int]]
        | dict[str, str | int | None]
        | dict[str, dict[str, float | str] | dict[str, str]]
        | int
        | None,
    ]:
        """Coleta metadados aprimorados de um arquivo ou diretório."""
        caminho = cls._normalizar_caminho(caminho=caminho)
        tipo: str = cls._determinar_tipo(caminho=caminho)
        stat: os.stat_result = caminho.stat()
        total_itens: int = 0
        sha256: str | int | None = None
        md5: str | int | None = None

        # Coletar estatísticas
        if tipo == "ARQUIVO":
            tamanho_bytes: int = stat.st_size
            tamanho_blocos: int = stat.st_blocks
            itens: dict[str, int] = {"total": 1, "arquivos": 1, "pastas": 0}
            profundidade = 0
        else:
            tamanho_bytes, total_itens, _ = cls._calcular_tamanho_pasta(caminho=caminho)
            tamanho_blocos = (tamanho_bytes // 512) + 1 if tamanho_bytes > 0 else 0
            itens = {"total": total_itens, "arquivos": total_itens - 1, "pastas": 1}
            profundidade: int = cls._calcular_profundidade(caminho=caminho)

        estatisticas: dict[str, dict[str, int | str] | dict[str, int] | dict[str, dict[str, float | str]] | int] = {
            "tamanho": {
                "bytes": tamanho_bytes,
                "blocos": tamanho_blocos,
                "legivel": cls._formatar_tamanho(bytesize=tamanho_bytes),
            },
            "itens": itens,
            "datas": {
                "acesso": cls._coletar_datas_aprimoradas(timestamp=stat.st_atime),
                "criacao": cls._coletar_datas_aprimoradas(timestamp=stat.st_ctime),
                "modificacao": cls._coletar_datas_aprimoradas(timestamp=stat.st_mtime),
            },
            "profundidade": profundidade,
        }

        # Coletar informações de proprietário/grupo
        try:
            proprietario: str = getpwuid(stat.st_uid).pw_name
            grupo: str = getgrgid(stat.st_gid).gr_name
        except ImportError:
            proprietario = str(stat.st_uid)
            grupo = str(stat.st_gid)

        # Coletar hashes (apenas para arquivos)
        sha256, md5 = cls._calcular_hash(caminho=caminho) if tipo == "ARQUIVO" else (None, None)

        # Montar o objeto final
        return {
            "cabecalho": {"versao": "2.0", "coletado_em": datetime.now().isoformat()},
            "item": {
                "nome": caminho.name,
                "tipo": tipo,
                "caminho": {
                    "absoluto": str(caminho),
                    "relativo": (
                        str(caminho.relative_to(Path.home())) if str(caminho).startswith(str(Path.home())) else None
                    ),
                },
            },
            "estatisticas": estatisticas,
            "permissoes": cls._coletar_permissoes_detalhadas(caminho=caminho),
            "conteudo": cls._listar_conteudo_aprimorado(caminho=caminho) if tipo == "PASTA" else None,
            "seguranca": {
                "proprietario": proprietario,
                "grupo": grupo,
                "hash_sha256": sha256,
                "hash_md5": md5,
                "selinux": None,
            },
            "sistema": {
                "coletado_em": cls._coletar_datas_aprimoradas(timestamp=stat.st_atime),
                "ferramenta": {"nome": "bookmark-converter", "versao": "1.0.0"},
                "sistema_arquivos": cls._detectar_sistema_arquivos(caminho=caminho),
            },
            "versao_metadados": 2,
        }


# if __name__ == "__main__":
#     print("\n=== Exemplo aprimorado com pasta ===\n")
#     metadados_pasta: dict[
#         str,
#         dict[str, str]
#         | dict[str, str | dict[str, str | None]]
#         | dict[str, dict[str, int | str] | dict[str, int] | dict[str, dict[str, float | str]] | int]
#         | dict[str, str | bool]
#         | dict[str, list[dict[str, str | int | float]] | list[dict[str, str | float | None]] | dict[str, int]]
#         | dict[str, str | int | None]
#         | dict[str, dict[str, float | str] | dict[str, str]]
#         | int
#         | None,
#     ] = ColetorDeMetadados.coletar_aprimorado(caminho="~/Downloads/Firefox/")
#     pprint(metadados_pasta, indent=4)

#     print("\n=== Exemplo aprimorado com arquivo ===\n")
#     metadados_arquivo: dict[
#         str,
#         dict[str, str]
#         | dict[str, str | dict[str, str | None]]
#         | dict[str, dict[str, int | str] | dict[str, int] | dict[str, dict[str, float | str]] | int]
#         | dict[str, str | bool]
#         | dict[str, list[dict[str, str | int | float]] | list[dict[str, str | float | None]] | dict[str, int]]
#         | dict[str, str | int | None]
#         | dict[str, dict[str, float | str] | dict[str, str]]
#         | int
#         | None,
#     ] = ColetorDeMetadados.coletar_aprimorado(caminho="~/Downloads/Firefox/bookmarks.txt")
#     pprint(metadados_arquivo, indent=4)


# === Exemplo aprimorado com pasta ===

# {   'cabecalho': {'coletado_em': '2025-08-01T22:04:42.993268', 'versao': '2.0'},
#     'conteudo': {   'arquivos': [   {   'extensao': '.json',
#                                         'modificacao': 1749095576.6847146,
#                                         'nome': 'bookmarks.json',
#                                         'tamanho': 812238},
#                                     {   'extensao': '.txt',
#                                         'modificacao': 1746588547.7829978,
#                                         'nome': 'favoritos_23_12_2024_raspado.txt',
#                                         'tamanho': 105},
#                                     {   'extensao': '.txt',
#                                         'modificacao': 1750296885.0269866,
#                                         'nome': 'notas.txt',
#                                         'tamanho': 32},
#                                     {   'extensao': '.html',
#                                         'modificacao': 1748331119.7370927,
#                                         'nome': 'bookmarks2.html',
#                                         'tamanho': 31381},
#                                     {   'extensao': '.txt',
#                                         'modificacao': 1750647255.9684284,
#                                         'nome': 'exemplo3.txt',
#                                         'tamanho': 53},
#                                     {   'extensao': '.txt',
#                                         'modificacao': 1746588547.781998,
#                                         'nome': 'favoritos_23_12_2024.txt',
#                                         'tamanho': 91},
#                                     {   'extensao': '.html',
#                                         'modificacao': 1748328701.723424,
#                                         'nome': 'bookmarks.html',
#                                         'tamanho': 732677},
#                                     {   'extensao': '.txt',
#                                         'modificacao': 1750647740.6568348,
#                                         'nome': 'exemplo4.txt',
#                                         'tamanho': 53},
#                                     {   'extensao': '.txt',
#                                         'modificacao': 1746588547.781998,
#                                         'nome': 'bookmarks.txt',
#                                         'tamanho': 86},
#                                     {   'extensao': '.txt',
#                                         'modificacao': 1750469410.29998,
#                                         'nome': 'exemplo2.txt',
#                                         'tamanho': 12},
#                                     {   'extensao': '.txt',
#                                         'modificacao': 1746588547.7829978,
#                                         'nome': 'Histórico.txt',
#                                         'tamanho': 87},
#                                     {   'extensao': '.txt',
#                                         'modificacao': 1750299499.3445137,
#                                         'nome': 'exemplo.txt',
#                                         'tamanho': 18},
#                                     {   'extensao': '.txt',
#                                         'modificacao': 1746588547.781998,
#                                         'nome': 'copy-favoritos_23_12_2024.txt',
#                                         'tamanho': 96}],
#                     'pastas': [   {   'extensao': None,
#                                       'modificacao': 1750391890.2332623,
#                                       'nome': 'Nova Pasta',
#                                       'tamanho': None}],
#                     'resumo': {'total_arquivos': 13, 'total_pastas': 1},
#                     'tipos': {'.html': 2, '.json': 1, '.txt': 10}},
#     'estatisticas': {   'datas': {   'acesso': {   'iso': '2025-08-01T08:19:19.099638',
#                                                    'legivel': '01/08/2025 '
#                                                               '08:19',
#                                                    'timestamp': 1754047159.0996382},
#                                      'criacao': {   'iso': '2025-06-23T00:02:20.656835',
#                                                     'legivel': '23/06/2025 '
#                                                                '00:02',
#                                                     'timestamp': 1750647740.6568348},
#                                      'modificacao': {   'iso': '2025-06-23T00:02:20.656835',
#                                                         'legivel': '23/06/2025 '
#                                                                    '00:02',
#                                                         'timestamp': 1750647740.6568348}},
#                         'itens': {'arquivos': 14, 'pastas': 1, 'total': 15},
#                         'profundidade': 0,
#                         'tamanho': {   'blocos': 3081,
#                                        'bytes': 1577056,
#                                        'legivel': '1.50 MB'}},
#     'item': {   'caminho': {   'absoluto': '/home/pedro-pm-dias/Downloads/Firefox',
#                                'relativo': 'Downloads/Firefox'},
#                 'nome': 'Firefox',
#                 'tipo': 'PASTA'},
#     'permissoes': {   'grupo': 'rwx',
#                       'octal': '775',
#                       'outros': 'r-x',
#                       'setgid': False,
#                       'setuid': False,
#                       'sticky': False,
#                       'usuario': 'rwx'},
#     'seguranca': {   'grupo': 'pedro-pm-dias',
#                      'hash_md5': None,
#                      'hash_sha256': None,
#                      'proprietario': 'pedro-pm-dias',
#                      'selinux': None},
#     'sistema': {   'coletado_em': {   'iso': '2025-08-01T08:19:19.099638',
#                                       'legivel': '01/08/2025 08:19',
#                                       'timestamp': 1754047159.0996382},
#                    'ferramenta': {   'nome': 'bookmark-converter',
#                                      'versao': '1.0.0'},
#                    'sistema_arquivos': {   'opcoes': 'rw,relatime',
#                                            'ponto_montagem': '/',
#                                            'tipo': 'ext4'}},
#     'versao_metadados': 2}
# 
# === Exemplo aprimorado com arquivo ===
# 
# {   'cabecalho': {'coletado_em': '2025-08-01T22:04:42.995848', 'versao': '2.0'},
#     'conteudo': None,
#     'estatisticas': {   'datas': {   'acesso': {   'iso': '2025-08-01T09:19:59.670404',
#                                                    'legivel': '01/08/2025 '
#                                                               '09:19',
#                                                    'timestamp': 1754050799.6704037},
#                                      'criacao': {   'iso': '2025-05-07T00:29:07.781998',
#                                                     'legivel': '07/05/2025 '
#                                                                '00:29',
#                                                     'timestamp': 1746588547.781998},
#                                      'modificacao': {   'iso': '2025-05-07T00:29:07.781998',
#                                                         'legivel': '07/05/2025 '
#                                                                    '00:29',
#                                                         'timestamp': 1746588547.781998}},
#                         'itens': {'arquivos': 1, 'pastas': 0, 'total': 1},
#                         'profundidade': 0,
#                         'tamanho': {   'blocos': 8,
#                                        'bytes': 86,
#                                        'legivel': '86.00 B'}},
#     'item': {   'caminho': {   'absoluto': '/home/pedro-pm-dias/Downloads/Firefox/bookmarks.txt',
#                                'relativo': 'Downloads/Firefox/bookmarks.txt'},
#                 'nome': 'bookmarks.txt',
#                 'tipo': 'ARQUIVO'},
#     'permissoes': {   'grupo': 'rw-',
#                       'octal': '664',
#                       'outros': 'r--',
#                       'setgid': False,
#                       'setuid': False,
#                       'sticky': False,
#                       'usuario': 'rw-'},
#     'seguranca': {   'grupo': 'pedro-pm-dias',
#                      'hash_md5': '098a354d564111b54f47410a6ca67592',
#                      'hash_sha256': '461d216d47340bd84c811e8b5050bacd50e0d24d660816b58484a15a837f9a45',
#                      'proprietario': 'pedro-pm-dias',
#                      'selinux': None},
#     'sistema': {   'coletado_em': {   'iso': '2025-08-01T09:19:59.670404',
#                                       'legivel': '01/08/2025 09:19',
#                                       'timestamp': 1754050799.6704037},
#                    'ferramenta': {   'nome': 'bookmark-converter',
#                                      'versao': '1.0.0'},
#                    'sistema_arquivos': {   'opcoes': 'rw,relatime',
#                                            'ponto_montagem': '/',
#                                            'tipo': 'ext4'}},
#     'versao_metadados': 2}
