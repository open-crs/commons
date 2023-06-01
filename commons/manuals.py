"""Module for handling manuals in the operating system."""


import os
import typing


def get_possible_man_locations() -> typing.Generator[str, None, None]:
    for conf_filename in ["/etc/manpath.config", "/etc/man_db.conf"]:
        if os.path.isfile(conf_filename):
            with open(conf_filename, "r", encoding="utf-8") as conf_file:
                content = conf_file.read().split("\n")

                mandatory_lines = [
                    line
                    for line in content
                    if line.startswith("MANDATORY_MANPATH")
                ]
                for line in mandatory_lines:
                    yield line.split()[-1]

                path_maps = [
                    line for line in content if line.startswith("MANPATH_MAP")
                ]
                for line in path_maps:
                    yield line.split()[-1]


def get_manuals_from_location(
    location: str,
) -> typing.Generator[str, None, None]:
    for dirpath, _, filenames in os.walk(location):
        for filename in filenames:
            if filename.endswith(".gz"):
                yield os.path.join(dirpath, filename)


def get_all_manuals() -> typing.Generator[str, None, None]:
    man_locations_iter = get_possible_man_locations()
    for location in man_locations_iter:
        yield from get_manuals_from_location(location)
