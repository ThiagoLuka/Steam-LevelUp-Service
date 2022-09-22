from . import InputValidation


class SteamUserUI:

    @staticmethod
    def run() -> int:
        print(
            '\nMENU STEAM USERS\n'
            '1 - Ver usuários ativos\n'
            '2 - Carregar usuário\n'
            '2 - Definir usuario para web scraper\n'
            '3 - Adicionar cookies a um usuário\n'
            '0 - Voltar para menu principal'
        )
        return InputValidation.int_within_range(0, 3)

    @staticmethod
    def continuar() -> bool:
        return InputValidation.continuar()

    @staticmethod
    def user_created():
        print('Novo usuário carregado!')
