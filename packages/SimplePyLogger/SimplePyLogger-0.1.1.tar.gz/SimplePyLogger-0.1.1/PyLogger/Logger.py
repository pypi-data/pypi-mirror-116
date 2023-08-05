import inspect
import datetime
from pathlib import Path
from threading import Lock
import colorama


class Logger:
    _instance = None
    _log_path = None
    _mutex = Lock()

    def __new__(cls, path=''):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)

            if not path:
                path = str(cls._get_caller_directory() / Path(cls._get_time_string("%y_%m_%d__%H_%M_%S") + '.log'))

            else:
                if isinstance(path, Path):
                    path = path / Path(cls._get_time_string("%y_%m_%d__%H_%M_%S") + '.log')
                else:
                    path = Path(path) / Path(cls._get_time_string("%y_%m_%d__%H_%M_%S") + '.log')

            cls._log_path = path

            colorama.init()

        return cls._instance

    def info(self, *args, **kwargs):
        if "file" in kwargs.keys():
            del kwargs["file"]

        try:
            self._mutex.acquire()

            print(self._get_time_string("%d/%m/%y %H:%M:%S"), f'[{inspect.stack()[1].function}][I] ', *args, **kwargs)

            with open(self._log_path, 'a') as log_file:
                print(self._get_time_string("%d/%m/%y %H:%M:%S"),
                      f'[{inspect.stack()[1].function}][I] ', *args, **kwargs, file=log_file)
        finally:
            self._mutex.release()

    def warning(self, *args, **kwargs):
        if "file" in kwargs.keys():
            del kwargs["file"]

        try:
            self._mutex.acquire()

            print(colorama.Fore.YELLOW, self._get_time_string("%d/%m/%y %H:%M:%S"),
                  f'[{inspect.stack()[1].function}][W] ', *args, colorama.Style.RESET_ALL, **kwargs)

            with open(self._log_path, 'a') as log_file:
                print(self._get_time_string("%d/%m/%y %H:%M:%S"),
                      f'[{inspect.stack()[1].function}][W] ', *args, **kwargs, file=log_file)
        finally:
            self._mutex.release()

    def error(self, *args, **kwargs):
        if "file" in kwargs.keys():
            del kwargs["file"]

        try:
            self._mutex.acquire()

            print(colorama.Fore.RED, self._get_time_string("%d/%m/%y %H:%M:%S"),
                  f'[{inspect.stack()[1].function}][W] ', *args, colorama.Style.RESET_ALL, **kwargs)

            with open(self._log_path, 'a') as log_file:
                print(self._get_time_string("%d/%m/%y %H:%M:%S"),
                      f'[{inspect.stack()[1].function}][W] ', *args, **kwargs, file=log_file)
        finally:
            self._mutex.release()

    @staticmethod
    def _get_caller_directory():
        return Path(inspect.stack()[2].filename).parent

    @staticmethod
    def _get_time_string(fmt: str = ''):
        return datetime.datetime.now().strftime(fmt)
