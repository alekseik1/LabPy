from pylatex import Document, NoEscape, UnsafeCommand
import os


def insert_raw_tex(doc: Document, code: str=""):
    """
    Вставляет сырой LaTeX-код в документ.

    :param doc: Объект *Document*, куда вставлять код
    :param code: Строка с кодом, которую нужно вставить
    :return: Объект *Document* с внесенными изменениями
    """
    doc.append(NoEscape(code))
    return doc


def add_from_tex_file(doc: Document, path: str):
    """
    Добавляет в *doc* весь контент из файла (через \include)

    :param doc: Объект *Document*, в которой добавляем файл
    :param path: Относительный путь до файла (корень начинается с корневой папки **проекта**)
    :return: Измененный объект *doc* типа **Document**
    """

    doc.append(UnsafeCommand('input', get_full_path(path)))
    return doc


def get_full_path(path: str):
    """
    Преобразует строку в абсолютный путь до файла

    :param path: Относительный или абсолютный путь
    :return: Абсолютный путь
    """
    is_relative_path = not os.path.isabs(path)
    if is_relative_path:
        filename = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), path)
    else:
        filename = path
    return filename
