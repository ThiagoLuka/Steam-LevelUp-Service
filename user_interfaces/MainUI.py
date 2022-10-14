from user_interfaces.InputValidation import InputValidation


class MainUI:

    @staticmethod
    def run() -> int:
        print(
            '\nMENU PRINCIPAL\n'
            '1 - Gerenciar Steam Profiles\n'
            '0 - Sair'
        )
        return InputValidation.int_within_range(0, 1)

    @staticmethod
    def goodbye() -> None:
        print('\nAté mais!\n')
