from user_interfaces.InputValidation import InputValidation


class SteamUserUI:

    @staticmethod
    def run() -> int:
        print(
            '\nMENU STEAM USERS\n'
            '1 - Ver usuários carregados\n'
            '2 - Adicionar usuário\n'
            '3 - Adicionar cookies a um usuário\n'
            '4 - Adicionar headers a um usuário\n'
            '0 - Voltar para menu principal'
        )
        return InputValidation.int_within_range(0, 4)

    @staticmethod
    def continuar() -> bool:
        return InputValidation.continuar()

    @staticmethod
    def user_loaded():
        print('Usuário carregado!')

    @staticmethod
    def no_user():
        print('Nenhum usuário disponível')

    @staticmethod
    def view_users(users: dict) -> list:
        print('Usuários: \n')
        user_options: list = []
        for index, user_name in enumerate(users.keys()):
            print(f'{index} - {user_name}')
            user_options.append(user_name)
        return user_options

    @staticmethod
    def choose_user(qtd_of_users: int):
        print('Digite o número referente ao usuário que deseja: ')
        return InputValidation.int_within_range(0, qtd_of_users - 1)
