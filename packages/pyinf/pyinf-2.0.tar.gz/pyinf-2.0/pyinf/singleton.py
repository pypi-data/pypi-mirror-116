# -*- coding: utf-8 -*-


class _Singleton(type):
    """
    Class that will be used as meta class for Singleton variables
    @cvar _instances: Instances of all the Singletons Created
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Function used when class is called

        """
        if cls not in cls._instances:
            cls._instances[cls] = super(
                _Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(_Singleton('SingletonMeta', (object,), {})):
    pass
