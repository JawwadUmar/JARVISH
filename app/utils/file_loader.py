def read_file(filepath, default=""):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return default


def get_resume():
    return read_file("data/resume.txt", "")


def get_prompt():
    return read_file(
        "data/system_prompt.txt",
        "Resume: {resume}\nOptions: {options}\nQuestion: {question}"
    )