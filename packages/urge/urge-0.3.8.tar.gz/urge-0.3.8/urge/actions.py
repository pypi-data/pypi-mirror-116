import typing as t

from path import Path
from .base import Action, action
from .procs import weather, youdao, browser, memegen, fileoperation
from dataclasses import dataclass


class do(Action):
    procs = []

    def __init__(self, *args) -> None:
        assert isinstance(self.procs, list)
        for f in args:
            self.procs.append(f)


@dataclass
class web_screenshot(Action):
    url: str
    procs = [browser.web_screenshot]


@dataclass
class get_now_temp(Action):
    city: str
    ascii_graphs: bool = True
    procs = [weather.get_weather, weather.ret_weather]


@dataclass
class get_simple_temp(Action):
    city: str
    ascii_graphs: bool = False
    procs = [weather.get_weather, weather.ret_weather]


@dataclass
class translate(Action):
    q: str
    full: bool = False
    procs = [youdao.translate_post, youdao.translate_filter]


@dataclass
class easy_translate(Action):
    q: str
    procs = [youdao.easy_translate]


@dataclass
class easy_ocr(Action):
    path: str
    procs = [youdao.pic2base64, youdao.ocr_post, youdao.ocr_ret]


@dataclass
class meme_gen(Action):
    name: str
    up: t.Optional[str]
    down: str
    procs = [memegen.get_meme]


@dataclass
class list_all(Action):
    path: str
    procs = [fileoperation.list_all]


class work_at:
    def __init__(self, workdir: str) -> None:
        self.workdir = workdir

    def find(self, pattern: str):
        f_list = fileoperation.find(self.workdir, pattern)
        return FShelper(f_list)

    @action([fileoperation.create])
    def create(self, file_name: str) -> Action:  # Just make lsp happy..
        # return dict(file=file)
        path = f'{self.workdir}/{file_name}'
        return locals()

    def create_folder(self):
        ...


class FShelper:
    def __init__(self, files) -> None:
        self.file_list = files
        # print(files)

    @action([fileoperation.delete])
    def delete(self) -> Action:
        files = self.file_list
        # return dict(self=self, files=files)
        return locals()

    def rename(self):
        ...

    def move(self):
        ...

    def zip(self):
        ...

    def unzip(self):
        ...

    def read(self):
        ...

    def write(self):
        ...
