
class Singleton():
    """
    Define an Instance operation that lets clients access its unique
    instance.
    """

    def __init__(cls):
        super().__init__()
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
