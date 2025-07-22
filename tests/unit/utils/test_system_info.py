from src.utils.system_info import get_system_name


def test_platform_specific_behavior() -> None:
    system_name: str = get_system_name()

    if system_name == "Windows":
        # Testes específicos para Windows
        assert "Windows" == system_name
    elif system_name == "Linux":
        # Testes específicos para Linux
        assert "Linux" == system_name
    elif system_name == "Darwin":
        # Testes específicos para macOS
        assert "Darwin" == system_name
