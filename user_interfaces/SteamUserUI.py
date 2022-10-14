from user_interfaces.InputValidation import InputValidation


class SteamUserUI:

    @staticmethod
    def run() -> int:
        print(
            '\nMENU STEAM USERS\n'
            '1 - Ver usuários ativos\n'
            '2 - Carregar usuário padrão\n'
            '3 - Definir usuario para web scraper\n'
            '4 - Adicionar cookies a um usuário\n'
            '0 - Voltar para menu principal'
        )
        return InputValidation.int_within_range(0, 4)

    @staticmethod
    def continuar() -> bool:
        return InputValidation.continuar()

    @staticmethod
    def user_created():
        print('Novo usuário carregado!')
