from user_interfaces.InputValidation import InputValidation


class GenericUI:

    @staticmethod
    def not_implemented():
        print('Not implemented')

    @staticmethod
    def continuar() -> bool:
        return InputValidation.continuar()

    @staticmethod
    def get_string(text_to_show: str) -> str:
        return str(input(text_to_show))
