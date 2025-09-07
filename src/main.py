# """
# main.py

# Controller para exploração BFS de sistema de arquivos com validação de visibilidade
# (evitando segmentos de caminho iniciados por '.') e checagem de permissões de
# leitura/execução. Suporta profundidade máxima e filtro opcional por extensão.

# Componentes:
# - OSModel: informações de sistema
# - FileExplorerController: orquestra exploração por níveis (BFS)
# - FileSystemItemFactory: cria objetos do sistema de arquivos

# Fluxo principal:
# 1) Validar base_path (precisa ter leitura; diretórios precisam de leitura+execução)
# 2) Incluir a própria base_path em `folders` (se válida)
# 3) Para depth em [0..max_depth]:
#    - Para cada pasta do nível atual: listar itens imediatos
#    - Validar cada item (permissão + visibilidade)
#    - Separar em arquivos e pastas
#    - Acumular globalmente
#    - Subpastas válidas alimentam o próximo nível
# 4) Retornar dicionário com listas finais: files, folders, invalids

# Observações:
# - A validação de visibilidade examina *todos* os segmentos do caminho (Path.parts)
# - O filtro de extensão é aplicado apenas a arquivos (case-insensitive) e é opcional
# - Tratamento resiliente para erros de sistema (permissão, inexistência, I/O)
# """

# from __future__ import annotations

# import logging
# from pathlib import Path

# # from controllers.file_explorer_controller import FileExplorerController
# from models.base_system import FileSystemItemFactory
# from models.os_model import OSModel


# def setup_logging() -> None:
#     """Configura o logging para a aplicação"""
#     logging.basicConfig(
#         level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
#     )


# def display_stats(result: dict[str, list[Path]], filter_results: list[Path]) -> None:
#     """Exibe estatísticas dos resultados"""
#     print("\n" + "=" * 60)
#     print("📊 ESTATÍSTICAS DA EXPLORAÇÃO")
#     print("=" * 60)
#     print(f"📁 Pastas encontradas: {len(result['folders'])}")
#     print(f"📄 Arquivos encontrados: {len(result['files'])}")
#     print(f"❌ Caminhos inválidos: {len(result['invalids'])}")
#     print(f"🔍 Arquivos filtrados (.html): {len(filter_results)}")
#     print("=" * 60)


# def display_file_details(filter_results: list[Path], factory: FileSystemItemFactory) -> None:
#     """Exibe detalhes dos arquivos filtrados"""
#     print(f"\n📋 DETALHES DOS ARQUIVOS HTML ({len(filter_results)} encontrados):")
#     print("-" * 80)

#     for i, path in enumerate(filter_results, 1):
#         try:
#             fs_item = factory.moldar_objeto(path_str=str(path))
#             status = "✅" if fs_item.is_valid() else "❌"
#             size_mb = fs_item.raw_size / (1024 * 1024) if fs_item.raw_size > 0 else 0

#             print(f"{i:3d}. {status} {fs_item.name}")
#             print(f"     📍 Caminho: {fs_item.path}")
#             # print(f"     📏 Tamanho: {fs_item.readable_size} ({size_mb:.2f} MB)")
#             print(f"     🕐 Modificado: {fs_item.modified_at.strftime('%Y-%m-%d %H:%M')}")
#             print(f"     🔓 Permissões: {fs_item.permissions}")
#             print(f"     🟢 Acessível: {fs_item.can_access()}")
#             print(f"     🏷️  Extensão: {fs_item.extension}")
#             print("-" * 80)

#         except Exception as e:
#             print(f"{i:3d}. ❌ Erro ao processar {path.name}: {e}")
#             print("-" * 80)


# def explore_directory_structure(controller: FileExplorerController, max_items: int = 10) -> None:
#     """Exibe a estrutura de diretórios encontrada"""
#     print(f"\n🌳 ESTRUTURA DE DIRETÓRIOS (primeiros {max_items}):")
#     print("-" * 60)

#     for i, folder in enumerate(controller.folders[:max_items], 1):
#         print(f"{i:2d}. 📁 {folder}")

#     if len(controller.folders) > max_items:
#         print(f"... e mais {len(controller.folders) - max_items} pastas")


# def main() -> None:
#     """Função principal que demonstra o uso do FileExplorerController"""
#     setup_logging()

#     try:
#         # Inicializar componentes
#         os_model = OSModel()
#         sys_factory = FileSystemItemFactory()

#         print("🚀 INICIANDO EXPLORAÇÃO DO SISTEMA DE ARQUIVOS")
#         print(f"📂 Diretório base: {os_model.home}")

#         # Configurar e executar o controller
#         controller = FileExplorerController(
#             base_path=os_model.home,
#             max_depth=3,  # Reduzido para demonstração
#             target_ext=".html",
#             follow_symlinks=False,
#         )

#         # Executar exploração
#         result = controller.explore_folder()

#         # Filtrar resultados
#         filter_results = controller.filter_by_extension(childs=result["files"], extension=".html")

#         # Exibir resultados
#         display_stats(result, filter_results)
#         display_file_details(filter_results, sys_factory)
#         explore_directory_structure(controller)

#         # Exemplo de informações do sistema
#         print("\n💻 INFORMACÕES DO SISTEMA:")
#         print(f"   Sistema: {os_model.os_name}")
#         print(f"   Usuário: {os_model.username}")
#         print(f"   Home: {os_model.home}")

#     except ValueError as e:
#         logging.error(f"Erro de configuração: {e}")
#         print(f"❌ Erro: {e}")
#     except Exception as e:
#         logging.error(f"Erro inesperado: {e}")
#         print(f"💥 Erro inesperado: {e}")
#     finally:
#         print("\n🎯 Exploração concluída!")


# if __name__ == "__main__":
#     main()
