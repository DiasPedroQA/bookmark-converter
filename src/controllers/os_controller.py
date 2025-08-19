"""
os_controller.py
----------------

Controller responsável por gerir a OSModel e expor as informações do sistema de forma organizada.
"""

from models.sistema_operacional_model import OSModel

# Tipos auxiliares
FileDict = dict[str, str | int | bool | dict[str, str] | dict[str, bool]]
FolderDict = dict[str, str | bool | int | dict[str, str] | dict[str, bool] | list["FolderDict"] | None]
SearchesDict = dict[str, list[FileDict] | dict[str, str | int]]


class OSController:
    """Controller para orquestrar operações da OSModel."""

    def __init__(self) -> None:
        self.model = OSModel()

    # --------------------------
    # Exibição / Agregação
    # --------------------------

    def show_system_overview(self) -> dict[str, str | int]:
        """Retorna visão geral do sistema operacional."""
        info: dict[str, str | int] = self.model.so_method_obter_info_so()
        print("\n=== INFORMAÇÕES DO SISTEMA ===")
        for k, v in info.items():
            print(f"{k}: {v}")
        return info

    # def explore_user_home(self, recursive: bool = False) -> FolderDict:
    #     """Explora a pasta raiz do usuário logado."""
    #     print(f"\n=== EXPLORANDO HOME: {self.model.user_home} ===")
    #     return self.model.folder_info(path=self.model.user_home, recursive=recursive)

    # def list_root_folders(self) -> list[FolderDict]:
    #     """Lista pastas da raiz do sistema (ex: / ou C:\\)."""
    #     print("\n=== PASTAS NA RAIZ DO SISTEMA ===")
    #     root = Path("/")
    #     folders: list[FolderDict] = []
    #     for item in root.iterdir():
    #         if item.is_dir():
    #             folders.append(self.model.folder_info(path=item, recursive=False))
    #     return folders

    # def search_examples(self) -> SearchesDict:
    #     """Exemplo de buscas e filtros para debug/demonstração."""
    #     base: Path = self.model.user_home
    #     print(f"\n=== BUSCAS NA PASTA: {base} ===")
    #     return {
    #         "arquivos_txt": self.model.search_files(base_path=base, extensions=[".txt"]),
    #         "arquivos_pequenos": self.model.filter_files_by_size(base_path=base),
    #         "resumo_home": self.model.summarize_directory(path=base),
    #     }

    # --------------------------
    # Fluxo completo
    # --------------------------

    def run(self) -> dict[str, dict[str, str | int] | FolderDict | list[FolderDict] | SearchesDict]:
        """Executa fluxo padrão: overview + home + raiz + exemplos."""
        print("\n========== INICIANDO CONTROLLER ==========")
        overview: dict[str, str | int] = self.show_system_overview()
        # home_data: FolderDict = self.explore_user_home(recursive=False)
        # root_data: list[FolderDict] = self.list_root_folders()
        # searches: SearchesDict = self.search_examples()

        return {
            "overview": overview,
            # "home": home_data,
            # "root": root_data,
            # "searches": searches,
        }
