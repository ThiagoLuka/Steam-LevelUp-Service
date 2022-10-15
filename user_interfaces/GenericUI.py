from user_interfaces.InputValidation import InputValidation


class GenericUI:

    @staticmethod
    def not_implemented():
        print('Not implemented')

    @staticmethod
    def continuar() -> bool:
        return InputValidation.continuar()
