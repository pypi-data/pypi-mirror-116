from subprocess import run, PIPE
from .exceptions import SedException


def sed(input_str: str, expression: str) -> str:
    cmd = run(
        ["sed", expression],
        input=bytes(input_str, encoding="utf-8"),
        stdout=PIPE,
        stderr=PIPE,
    )
    if cmd.returncode == 0:
        return str(cmd.stdout, encoding="utf-8")
    else:
        raise SedException(cmd.stderr)
