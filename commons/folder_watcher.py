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

    def __init__(
        self, folder: Path, pooling_interval: int, callback: typing.Callable
    ) -> None:
        self.__folder = folder
        self.__pooling_interval = pooling_interval
        self.__callback = callback

        self.__stop_needed = False
        self.__known_files = []

        self.__thread = Thread(target=self.__watch)
        self.__thread.start()

    def __del__(self) -> None:
        self.stop()

    def __watch(self) -> None:
        while not self.__stop_needed:
            files = set(os.listdir(self.__folder))

            for new_file in files.difference(self.__known_files):
                self.__callback(new_file)

            self.__known_files = files

            time.sleep(self.__pooling_interval)

    def stop(self) -> None:
        self.__stop_needed = True

        time.sleep(self.__pooling_interval)
