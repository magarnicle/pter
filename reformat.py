"""Reformat the todo file to something conformat and sensible.
If no output file is given, print the reformatted list to stdout.

Usage:
    reformat INPUT [OUTPUT]
"""
from docopt import docopt
import pytodotxt as txt
import re
import sys
from pathlib import Path
from datetime import datetime
from pter.searcher import get_relative_date


def reformat(todo):
    tasks = todo.parse()
    today = datetime.now().date()
    FORMAT = [
        lambda x: "x" if x.is_completed else "",
        lambda x: f"({x.priority})" if x.priority else "",
        lambda x: x.completion_date.isoformat() if x.completion_date else "",
        lambda x: x.creation_date.isoformat() if x.creation_date else "",
        lambda x: x.bare_description(),
        lambda x: " ".join([f"+{pro}" for pro in sorted(set(x.projects))]),
        lambda x: " ".join([f"@{con}" for con in sorted(set(x.contexts))]),
        lambda x: " ".join([f"tag:{tag}" for tag in sorted(set(x.hashtags))]),
        lambda x: " ".join(
            sorted(
                {f"{att}:{val[0]}" for att, val in x._attributes.items()},
                key=lambda x: f"{0 if x.startswith('id:') else 1}{x}",
            )
        ),
    ]
    for task in tasks:
        if "pri" in task.attributes:
            if not task.priority:
                task.priority = task.attributes["pri"][0]
            task.remove_attribute("pri")
        if not task.is_completed and "rec" in task.attributes:
            if not task.due_date:
                task.add_attribute("due", today.isoformat())
            elif not task.attributes["rec"][0].startswith("+"):
                prev_due_date = task.due_date
                while True:
                    next_due_date = get_relative_date(
                        task.attributes["rec"][0], None, prev_due_date
                    )
                    if next_due_date > today:
                        break
                    prev_due_date = next_due_date
                if prev_due_date != task.due_date:
                    task.replace_attribute(
                        "due", task.due_date.isoformat(), prev_due_date.isoformat()
                    )

    lines = []
    for task in sorted(
        tasks,
        key=lambda x: (
            f"{1 if x.is_completed else 0}"
            f'{x.priority or "Z"}'
            f'{x.completion_date.isoformat() if x.completion_date else "9999"}'
            f'{x.due_date.isoformat() if x.due_date else "9999"}'
            f"{x.bare_description()}"
        ),
    ):
        lines.append(
            re.sub(
                " +",
                " ",
                " ".join(map(str, [item(task) for item in FORMAT])).strip(" "),
            )
        )
    return lines


def main(input_file, output_file=None):
    todo = txt.TodoTxt(input_file)
    lines = reformat(todo)
    text = "\n".join(lines).strip(" \n")
    if output_file:
        output_file.write_text(text)
    else:
        print(text)


if __name__ == "__main__":
    args = docopt(__doc__)
    input_file = Path(args["INPUT"]).expanduser()
    output_path = args.get("OUTPUT")
    if output_path:
        output_file = Path(output_path).expanduser()
    else:
        output_file = None
    sys.exit(main(input_file, output_file=output_file))
