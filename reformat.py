import pytodotxt as txt
from pathlib import Path

def reformat(todo):
    tasks = todo.parse()
    FORMAT = [
        lambda x: "x" if x.is_completed else "",
        lambda x: f"({x.priority})" if x.priority else "",
        lambda x: x.completion_date.isoformat() if x.completion_date else "",
        lambda x: x.creation_date.isoformat() if x.creation_date else "",
        lambda x: x.bare_description(),
        lambda x: " ".join([f"#{tag}" for tag in sorted(set(x.hashtags))]),
        lambda x: " ".join([f"+{pro}" for pro in sorted(set(x.projects))]),
        lambda x: " ".join([f"@{con}" for con in sorted(set(x.contexts))]),
        lambda x: " ".join(sorted({f"{att}:{val[0]}" for att, val in x.attributes.items()}),)
    ]
    for task in tasks:
        if "pri" in task.attributes:
            task.priority = task.attributes["pri"][0]
            task.remove_attribute("pri")
    lines = []
    for task in sorted(tasks, key=lambda x: x.priority or "Z"):
        lines.append(" ".join(map(str, [item(task) for item in FORMAT])).replace("  ", " ").strip(" "))
    return lines

def main():
    todo_file = Path("~/Desktop/tmp/todo.txt").expanduser()
    todo = txt.TodoTxt(todo_file)
    lines = reformat(todo)
    text = "\n".join(lines).strip(" \n")
    print(text)
    todo_file.write_text(text)

if __name__ == "__main__":
    main()
