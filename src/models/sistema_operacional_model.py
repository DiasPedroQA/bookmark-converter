"""
system_os_model.py
------------------

Modelo avançado para interação com o sistema operacional.
"""

from utils.system_tools import (
    system_method_obter_caminho_usuario,
    system_method_obter_endereco_ip,
    system_method_obter_espaco_disco_livre,
    system_method_obter_info_plataforma,
    system_method_obter_nome_sistema_operacional,
    system_method_obter_nome_usuario,
    system_method_obter_versao_kernel,
)


class OSModel:
    """Modelo para abstrair interações com o sistema operacional e centralizar
    as funcionalidades de arquivos e pastas."""

    def __init__(self) -> None:
        # Propriedades básicas do SO
        self.sys_data_os_name: str = system_method_obter_nome_sistema_operacional()
        self.sys_data_hostname: str = system_method_obter_endereco_ip()
        self.sys_data_user_name: str = system_method_obter_nome_usuario()
        self.sys_data_user_home: str = system_method_obter_caminho_usuario()
        self.sys_data_ip_address: str = system_method_obter_endereco_ip()
        self.sys_data_kernel_version: str = system_method_obter_versao_kernel()
        self.sys_data_platform_info: str = system_method_obter_info_plataforma()

        # Espaço em disco (no root por padrão)
        self.sys_data_disk_free_space: int = system_method_obter_espaco_disco_livre(caminho="/")

        # Sub-modelos
        # self._folder_model = FolderModel(caminho_da_pasta=self.user_home)

    # --------------------------
    # Representação
    # --------------------------

    def __repr__(self) -> str:
        return f"<OSModel os='{self.sys_data_os_name}' username='{self.sys_data_user_name}' ip='{self.sys_data_ip_address}' disk_free_space='{self.sys_data_disk_free_space}'>"

    # --------------------------
    # Informações do sistema
    # --------------------------

    def so_method_obter_info_so(self) -> dict[str, str | int]:
        """Retorna informações detalhadas do sistema."""
        return {
            "os_name": self.sys_data_os_name,
            "hostname": self.sys_data_hostname,
            "username": self.sys_data_user_name,
            "user_home": str(self.sys_data_user_home),
            "ip_address": self.sys_data_ip_address,
            "kernel_version": self.sys_data_kernel_version,
            "platform_info": self.sys_data_platform_info,
            "disk_free_space": self.sys_data_disk_free_space,
            # "disk_free_space_formatado": global_method_formatar_tamanho_caminho(
                # tamanho_bytes=self.sys_data_disk_free_space
            # ),
        }
