import pathlib


def pytest_folder() -> pathlib.Path:
    p = pathlib.Path(__file__).parent.resolve()
    assert p.exists()
    assert p.is_dir()
    return p


def proj_folder(pytest_folder:pathlib.Path=pytest_folder()) -> pathlib.Path:
    p = pytest_folder.parent.resolve()
    assert p.exists()
    assert p.is_dir()
    return p


def script_path(proj_folder:pathlib.Path=proj_folder()) -> pathlib.Path:
    p = proj_folder / "ex01.py"
    assert p.exists()
    assert p.is_file()
    return p
