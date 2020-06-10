from typing import Callable

from envmanager.utils.helpers import read_plan_and_load_environs_for_apps


def env_loader(config_object: object) -> Callable:
    """
    Decorator function that runs pre-configurations before the main application is run
    @rtype: object
    """
    read_plan_and_load_environs_for_apps(config_object)

    def wrapper(func: Callable) -> Callable:
        return func

    return wrapper