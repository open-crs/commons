import os
import time
import typing
from pathlib import Path
from threading import Thread


class FolderWatcher:
    __callback: typing.Callable
    __folder: Path
    __pooling_interval: int
    __thread: Thread
    __stop_needed: bool
    __known_files: typing.List[str]
    __ignored_files: typing.List[str]

    def __init__(
        self,
        folder: Path,
        pooling_interval: int,
        callback: typing.Callable,
        ignored_files: typing.List[str],
    ) -> None:
        self.__folder = folder
        self.__pooling_interval = pooling_interval
        self.__callback = callback
        self.__ignored_files = ignored_files

        self.__stop_needed = False
        self.__known_files = []

        self.__thread = Thread(target=self.__watch, daemon=True)
        self.__thread.start()

    def __del__(self) -> None:
        try:
            self.stop()
        except Exception:
            pass

    def __watch(self) -> None:
        while not self.__stop_needed:
            try:
                files = set(os.listdir(self.__folder))
            except (FileNotFoundError, OSError):
                files = set()
            files = files.difference(set(self.__ignored_files))

            new_files = files.difference(set(self.__known_files))
            for new_file in new_files:
                try:
                    self.__callback(new_file)
                except Exception:
                    pass

            self.__known_files = list(files)

            time.sleep(self.__pooling_interval)

    def stop(self) -> None:
        self.__stop_needed = True
        try:
            time.sleep(self.__pooling_interval)
        except KeyboardInterrupt:
            pass
