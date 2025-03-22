def info(message):
    """Prints regular info messages with Blue color."""
    print(f"\033[94mINFO:\t  {message}\033[0m")


def warn(message):
    """Prints warning messages with Yellow color."""
    print(f"\033[93mWARNING:\t  {message}\033[0m")


def err(message):
    """Prints error messages with Red color."""
    print(f"\033[91mERROR:\t  {message}\033[0m")
