DOIT_CONFIG = {
    "default_tasks": [
        "python_dependencies",
        "flake8",
        "black",
        "pydocstyle",
        "mypy",
        "pytest",
    ],
    "cleanforget": True,
    "verbosity": 0,
}

python_directories = ["ayx_blackbird", "tests"]


def task_python_dependencies():
    log_file = ".doit.pip.log"
    return {
        "actions": [f"pip install -r requirements-dev.txt --log {log_file}"],
        "file_dep": ["requirements.txt", "requirements-dev.txt"],
        "targets": [log_file],
        "clean": True,
    }


def task_black():
    for directory in python_directories:
        yield {
            "name": directory,
            "actions": [f"black --check {directory}"],
            "file_dep": list_files(directory),
            "task_dep": ["python_dependencies"],
        }


def task_flake8():
    for directory in python_directories:
        yield {
            "name": directory,
            "actions": [f"flake8 {directory}"],
            "file_dep": list_files(directory),
        }


def task_pydocstyle():
    for directory in python_directories:
        yield {
            "name": directory,
            "actions": [f"pydocstyle --convention=numpy {directory}"],
            "file_dep": list_files(directory),
        }


def task_mypy():
    return {
        "actions": [f"mypy ayx_blackbird"],
        "file_dep": list_files("ayx_blackbird") + ["mypy.ini"],
    }


def task_pytest():
    file_deps = []
    for path in python_directories:
        file_deps += list_files(path)

    return {"actions": [f"pytest tests"], "file_dep": file_deps}


def list_files(directory):
    import os

    fs = []
    for root, directories, files in os.walk(directory):
        for file in files:
            fs.append(os.path.join(root, file))
    return fs