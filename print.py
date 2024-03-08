"""Reformat the todo file to something conformat and sensible.
If no output file is given, print the reformatted list to stdout.

Usage:
    print [-f FIELDS] INPUT

Options:
    -f, --fields=FIELDS     Comma-separated list of fields, defaults to all available: complete,priority,completion_date,creation_date,description,projects,contexts,hashtags,tags
"""

from docopt import docopt
import pytodotxt as txt
import re
import sys
from pathlib import Path
from datetime import datetime
from pter.searcher import get_relative_date


def reformat(todo, output_fields):
    tasks = todo.parse()
    today = datetime.now().date()
    FIELDS_INDEX = {
        "complete": 0,
        "priority": 1,
        "completion_date": 2,
        "creation_date": 3,
        "description": 4,
        "projects": 5,
        "contexts": 6,
        "hashtags": 7,
        "tags": 8,
    }
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
            # elif task.attributes["rec"][0].startswith("+"):
            else:
                prev_due_date = task.due_date
                while True:
                    next_due_date = get_relative_date(
                        task.attributes["rec"][0], None, prev_due_date
                    )
                    if not next_due_date or next_due_date > today:
                        break
                    prev_due_date = next_due_date
                if prev_due_date != task.due_date:
                    task.replace_attribute(
                        "due", task.due_date.isoformat(), prev_due_date.isoformat()
                    )

    lines = []
    if output_fields:
        fields = [
            idx
            for name, idx in FIELDS_INDEX.items()
            if name in output_fields.split(",")
        ]
    else:
        fields = FIELDS_INDEX.values()
    selected_fields = [field for idx, field in enumerate(FORMAT) if idx in fields]
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
                " ".join(map(str, [item(task) for item in selected_fields])).strip(" "),
            )
        )
    return lines


def main(input_file, fields=None):
    todo = txt.TodoTxt(input_file)
    lines = reformat(todo, fields)
    text = "\n".join(lines).strip(" \n")
    print(text)


if __name__ == "__main__":
    args = docopt(__doc__)
    input_file = Path(args["INPUT"]).expanduser()
    sys.exit(main(input_file, args.get("--fields")))
