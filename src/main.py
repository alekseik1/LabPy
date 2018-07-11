from pylatex import Document, UnsafeCommand
import os
from .preamble import generate_preambula
from .summary import generate_summary


def create_document(fill_preamble: bool=True):
    """
    Создает пустой документ и (опционально) заполняет его преамбулой.

    :param fill_preamble: Заполнять преамбулой или нет
    :return: Объект типа *Document* для дальнейшего заполнения
    """
    tmp_doc = Document(fontenc='T2A',
                       documentclass='article',
                       document_options=['a4paper', '12pt'],
                       geometry_options={'left': '1.27cm',
                                         'right': '1.27cm',
                                         'top': '2cm',
                                         'bottom': '2cm'},
                       lmodern=False)
    if fill_preamble:
        tmp_doc = generate_preambula(tmp_doc)
    return tmp_doc


def add_from_tex_file(doc: Document, path: str):
    """
    Добавляет в *doc* весь контент из файла (через \include)

    :param doc: Объект *Document*, в которой добавляем файл
    :param path: Относительный путь до файла (корень начинается с корневой папки **проекта**)
    :return: Измененный объект *doc* типа **Document**
    """
    is_relative_path = not os.path.isabs(path)
    if is_relative_path:
        filename = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), path)
    else:
        filename = path
    doc.append(UnsafeCommand('input', filename))
    return doc

from .title_page import generate_titlepage
from src.theor_introduction import generate_theor_introduction


if __name__ == '__main__':
    doc = create_document()
    generate_preambula(doc)
    generate_summary(doc)
    doc.generate_pdf('main', clean_tex=False)
