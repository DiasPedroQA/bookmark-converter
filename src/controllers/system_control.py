"""
Controladores para orquestrar a coleta de dados do sistema operacional do
usuário logado, com validação de caminho, permissões, formatação de dados
e construção do objeto `SistemaOperacional`.

Dependências:
    - models.sistema_operacional_model
    - utils.system_info
"""

import json
from json import JSONDecodeError
from pathlib import Path

from models.sistema_operacional_model import SistemaOperacional
from utils.system_info import (
    bytes_para_legivel,
    filtrar_arquivos_e_pastas,
    formatar_data,
    listar_subcaminhos,
    obter_pasta_raiz_usuario,
    tem_permissao_leitura,
    verificar_caminho_so,
)


def controller_validar_so() -> Path | None:
    """
    Verifica se a pasta raiz do usuário logado é acessível para leitura.

    Returns:
        Path | None: Caminho da pasta se for legível, ou None caso contrário.
    """
    caminho_pasta_usuario: Path = obter_pasta_raiz_usuario()
    return caminho_pasta_usuario if tem_permissao_leitura(caminho_pasta_usuario) else None


def controller_gerar_json_so() -> str | None:
    """
    Monta um objeto `SistemaOperacional` com dados extraídos do ambiente
    e o serializa como JSON.

    Returns:
        str | None: Representação JSON do objeto ou None se falhar.
    """
    caminho_validado: Path | None = controller_validar_so()
    if not caminho_validado:
        return None

    validacao_so: dict[str, bool] = verificar_caminho_so(caminho_validado)
    if not (validacao_so["formato_valido"] and validacao_so["padrao_reconhecido"]):
        return None

    sistema_identificado = SistemaOperacional(
        usuario_logado=caminho_validado.name,
        caminho_pasta_usuario=caminho_validado,
        filhos_pasta_home=listar_subcaminhos(caminho_validado),
        caminho_valido=validacao_so,
        permissao_leitura=True,
        data_acesso=formatar_data(caminho_validado.stat().st_atime),
        data_criacao=formatar_data(caminho_validado.stat().st_ctime),
        data_modificacao=formatar_data(caminho_validado.stat().st_mtime),
        tamanho_caminho=bytes_para_legivel(caminho_validado.stat().st_size),
    )
    return sistema_identificado.model_dump_json(indent=4)


def controller_listar_filhos_home() -> tuple[list[Path], list[Path]] | None:
    """
    Retorna as subpastas e arquivos contidos na pasta home do usuário.

    Returns:
        tuple[list[Path], list[Path]] | None: Listas separadas por tipo de item, ou None se falhar.
    """
    json_data: str | None = controller_gerar_json_so()
    if not json_data:
        return None

    try:
        dados = json.loads(json_data)
        filhos_raw = dados.get("filhos_pasta_home", [])
        if isinstance(filhos_raw, list) and all(isinstance(item, str) for item in filhos_raw):
            caminhos: list[Path] = [Path(p).expanduser().resolve() for p in filhos_raw]
            return filtrar_arquivos_e_pastas(itens=caminhos)
    except (JSONDecodeError, TypeError, KeyError):
        return None
