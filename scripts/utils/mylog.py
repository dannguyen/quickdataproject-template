try:
    from rich.console import Console

    MYLOG_CONSOLE = Console()

    def mylog(*args, label=None, color='cyan'):
        labtxt = f"[bold {color} on black]{label}:[/bold {color} on black] " if label else ""
        txt = "\n» ".join([str(a) for a in args])
        if len(args) > 1:
            txt += '\n///'
        MYLOG_CONSOLE.log(f'{labtxt}{txt}')

except ModuleNotFoundError:

    def mylog(*args, label=None, color='cyan'):
        labtxt = f"{label}: " if label else ""
        txt = "\n» ".join([str(a) for a in args])
        if len(args) > 1:
            txt += '\n///'
        print(f'{labtxt}{txt}')
