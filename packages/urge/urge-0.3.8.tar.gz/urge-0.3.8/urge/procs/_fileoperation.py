from path import Path
import typing as t


P: t.Optional[Path] = None


def list_all(path: str = None):
    return P.listdir() if P else Path(path).listdir()


def find(path: t.Optional[str], pattern: str):
    return P.listdir(pattern) if P else Path(path).listdir(pattern)


def delete(files: t.Union[str, Path, t.List[Path]]):
    # try file = files[0] looks better
    # I just knew it...
    # Emm... Maybe use if else is also a good choice?

    if isinstance(files, Path):
        files.remove()
    elif isinstance(files, str):
        Path(files).remove()
    elif isinstance(files, list):
        for f in files:
            f.remove()


def create(file: t.Union[str, Path]):
    return file.touch() if isinstance(file, Path) else Path(file).touch()


def rename(file: t.Union[Path, str], to_target: str):
    # It's OK with that
    if isinstance(file, Path):
        file.move(to_target)
    elif isinstance(file, str):
        Path(file)


def easy_sort():
    ...


def create_folder(folder: t.Union[str, Path]):
    return Path(folder).mkdir()


create_folder("/Users/houjue/Desktop/haha")
