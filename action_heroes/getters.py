from configparser import ConfigParser, ExtendedInterpolation
import pathlib

try:
    # importlib is available only from Python 3.7+
    from importlib import resources
except ImportError:
    # importlib_resources package is available for Python 3.4-3.6
    import importlib_resources as resources

import meta


def get_about():
    """Returns contents of about.ini as a dict"""
    return get_config_as_dict(meta, "about.ini")


def get_readme_contents():
    """Returns contents of file marked readme_filename in about.ini"""
    about = get_about()
    readme_filename = about["PROJECT"]["readme_filename"]
    with open(readme_filename, "r", encoding="utf-8") as f:
        readme_contents = f.read()

    return readme_contents


def get_readme_content_type():
    """Returns content type of file marked readme_filename in about.ini"""
    about = get_about()
    suffix = pathlib.Path(about["PROJECT"]["readme_filename"]).suffix
    ext_and_content_types = {"md": "text/markdown", "rst": "text/x-rst"}
    return ext_and_content_types.get(suffix, "text/plain")


def get_config_as_dict(resource_path, config_filename):
    """Returns contents of a config file

    Args:
        resource_path (module): Represents location to fetch resource from.
        config_filename (str): The ini file to fetch from resource_path

    Returns:
        str: contents of config file as a dict

    """
    with resources.path(resource_path, config_filename) as config_path:
        config = ConfigParser(
            delimiters=("="),
            comment_prefixes=("#"),
            inline_comment_prefixes=("#"),
            interpolation=ExtendedInterpolation(),
        )
        config.read(config_path)
        return dict(config)
