import os
import threading
import typing
from pathlib import Path
from threading import Event, Thread


class FolderWatcher:
    __callback: typing.Callable
    __folder: Path
    __pooling_interval: int
    __thread: Thread
    __stop_event: Event
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

        self.__stop_event = Event()
        self.__known_files = []

        self.__thread = Thread(target=self.__watch, daemon=True)
        self.__thread.start()

    def __enter__(self) -> "FolderWatcher":
        return self

    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[typing.Any],
    ) -> None:
        self.stop()

    def close(self) -> None:
        self.stop()

    def __del__(self) -> None:
        try:
            self.stop()
        except Exception:
            pass

    def __watch(self) -> None:
        while not self.__stop_event.is_set():
            try:
                files = set(os.listdir(self.__folder))
            except (FileNotFoundError, OSError):
                files = set()
            files = files.difference(set(self.__ignored_files))

            new_files = files.difference(set(self.__known_files))
            for new_file in new_files:
                self.__callback(new_file)

            self.__known_files = list(files)

            self.__stop_event.wait(self.__pooling_interval)

    def stop(self) -> None:
        self.__stop_event.set()
        if self.__thread.is_alive() and self.__thread is not threading.current_thread():
            self.__thread.join(timeout=self.__pooling_interval)
