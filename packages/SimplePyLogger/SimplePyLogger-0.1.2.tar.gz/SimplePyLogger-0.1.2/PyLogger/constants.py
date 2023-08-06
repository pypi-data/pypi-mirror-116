import colorama

colorama.init()


class LoggerLevels:
    info = 0
    warning = 1
    error = 2
    level_color = {info: '',
                   warning: colorama.Fore.YELLOW,
                   error: colorama.Fore.RED,
                   'end': colorama.Style.RESET_ALL}
