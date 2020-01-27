DOIT_CONFIG = {
    "default_tasks": ["flake8", "black", "pydocstyle", "pytest"],
    "cleanforget": True,
}

python_directories = ["ayx_blackbird", "tests"]


def task_black():
    for directory in python_directories:
        yield {
            "name": directory,
            "actions": [f"black --check {directory}"],
            "file_dep": list_files(directory),
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


def task_pytest():
    file_deps = []
    for path in python_directories:
        file_deps += list_files(path)

    return {
        "actions": [f"pytest tests"],
        "file_dep": file_deps,
    }


def list_files(directory):
    import os

    fs = []
    for root, directories, files in os.walk(directory):
        for file in files:
            fs.append(os.path.join(root, file))
    return fs
