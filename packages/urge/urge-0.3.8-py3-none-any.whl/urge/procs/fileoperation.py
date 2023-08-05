from path import Path
import typing as t


def patho(p) -> Path:
    result: Path
    if type(p) == str:
        result = Path(p)

    elif type(p) == Path:
        result = p
    else:
        raise Exception("Must be a str")
    return result


def list_all(path: str, pattern: str = None, **kwd):
    return patho(path).listdir(pattern)


def find(path: str, pattern: str, **kwd):
    return list_all(path, pattern)


def create(path: str, **kwd):
    # return Path(path).touch()
    return patho(path).touch()


def delete(files: t.Union[t.List[Path], str], **kwd):
    if type(files) == list:
        for f in files:
            f = patho(f)
            if f.isdir():
                print(f)
                continue
            f.remove()
        return

    file = patho(files)
    if not file.isdir():
        file.remove()
    # file.remove()


def rename(files: t.Union[str, t.List[Path]]):
    ...


def create_folder(path: t.Any, **kwd) -> str:

    t = type(path)
    is_str = t == str
    is_path = t == Path
    if t not in [str, Path]:
        raise Exception("The argument path must be str or a Path obj")

    patho(path).mkdir()
    assert isinstance(path, str)
    return path


def move(files: t.Union[t.List[Path], str], dst: str, **kwd):

    if type(files) == list:
        # Concidering use mvtree
        # No, because sometimes just want move muiltple files into a new folder.
        for f in files:
            file = patho(f)
            file.move(dst)
        return
    # NOTE To note that when files is not a Paht obj
    # you need to use full path(I guess?)
    # Meh ,no need to worry, Path obj will handle this case with pure LOVE.
    file = patho(files)
    file.move(dst)


def happy():
    return 'Happy'
