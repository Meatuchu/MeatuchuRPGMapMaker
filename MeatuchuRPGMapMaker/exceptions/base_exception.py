class RPGMapException(Exception):
    def __init__(self, message: str) -> None:
        msg = message or "An Unknown Error has occurred in Meatuchu's RPG Map Maker"
        super().__init__(msg)
