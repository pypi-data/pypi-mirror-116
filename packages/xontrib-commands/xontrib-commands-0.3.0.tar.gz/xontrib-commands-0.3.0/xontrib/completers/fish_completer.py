from xonsh.completers import completer
from xonsh.completers.tools import RichCompletion, contextual_command_completer

# from xontrib.commands.utils import run

from xonsh.parsers.completion_context import CommandContext
import subprocess as sp


def create_rich_completion(line: str):
    line = line.strip()
    if "\t" in line:
        cmd, desc = map(str.strip, line.split("\t", maxsplit=1))
    else:
        cmd, desc = line, ""
    return RichCompletion(
        str(cmd),
        description=str(desc),
    )


@contextual_command_completer
def fish_proc_completer(context: CommandContext):
    """Populate completions using fish shell and remove bash-completer"""
    cmd = context.args[-1]
    line = " ".join(cmd) + context.prefix
    output = sp.check_output(["fish", "-c", f"complete -C '{line}'"])
    # print(output, "---")
    for comp in output.decode().strip().splitlines(keepends=False):
        yield create_rich_completion(comp)


completer.add_one_completer("fish", fish_proc_completer, "<bash")
# completer.remove_completer("bash")
