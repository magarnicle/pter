"""Reformat the todo file to something conformat and sensible.
If no output file is given, print the reformatted list to stdout.

Usage:
    reformat [--archive=ARCHIVE] INPUT [OUTPUT]
"""

from docopt import docopt
import pytodotxt as txt
import re
import sys
from pathlib import Path
from datetime import datetime
from pter.searcher import get_relative_date


def parse_date(date_text):
    try:
        parsed_date = datetime.fromisoformat(date_text)
    except ValueError:
        parsed_date = None
        for format in ["%Y-%m-%d"]:
            try:
                parsed_date = datetime.strptime(date_text, format)
            except ValueError:
                continue
        if not parsed_date:
            raise ValueError(f"Could not parse due date format {date_text}")
    return parsed_date


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
        try:
            if "pri" in task.attributes:
                if not task.priority:
                    task.priority = task.attributes["pri"][0]
                task.remove_attribute("pri")
            if not task.is_completed and "rec" in task.attributes:
                if "due" not in task.attributes:
                    task.add_attribute("due", today.isoformat())
                # elif task.attributes["rec"][0].startswith("+"):
                else:
                    due_date_text = task.attributes["due"][0]
                    prev_due_date = parse_date(due_date_text)
                    original_due_date = prev_due_date
                    while True:
                        next_due_date = get_relative_date(
                            task.attributes["rec"][0], None, prev_due_date
                        )
                        if not next_due_date or next_due_date > today:
                            break
                        prev_due_date = next_due_date
                    if prev_due_date != original_due_date:
                        task.replace_attribute(
                            "due",
                            original_due_date.date().isoformat(),
                            prev_due_date.isoformat(),
                        )
        except Exception:
            print(f"Error with task {task}")
            raise

    lines = []
    for task in sorted(
        tasks,
        key=lambda x: (
            f"{1 if x.is_completed else 0}"
            f'{x.priority or "Z"}'
            f'{x.completion_date.isoformat() if x.completion_date else "9999"}'
            f'{parse_date(x.attributes["due"][0]).isoformat() if x.attributes.get("due") else "9999"}'
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
