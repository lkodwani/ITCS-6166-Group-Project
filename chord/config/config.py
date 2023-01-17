from yaml import safe_load


def build_settings(config_file_path: str, primary_key: str) -> dict:
    """
    Builds the settings dictionary associated with a specific key.

    args:
        config_file_path: the path to the config file (str)
    returns:
        settings: the settings dictionary (dict)
    """

    with open(config_file_path, 'r') as config_file:
        config = safe_load(config_file)

    return config[primary_key]
