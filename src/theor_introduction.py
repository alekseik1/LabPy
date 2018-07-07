from pylatex import Document
from src.main import add_from_tex_file


def generate_theor_introduction(doc: Document, use_file: str=""):
    """
    Создает теоретическое введение к лабе.

    Делать его тяжело и неприятно, поэтому имеется возможность
    взять эту часть из готового .tex файла

    :param doc: Объект *Document*, куда записывать
    :param use_file: Путь к файлу с теор.введением (*необязательно*)
    :return: Объект *Document* с готовыми изменениями
    """
    if use_file != "":
        add_from_tex_file(doc, use_file)
    else:
        # TODO: поскольку теор. часть достаточно сложна для ввода,
        # TODO: я заставлю вас редактировать исходники метода под каждую лабу.
        # FIXME: Возможно, в будущем я придумаю идею получше.
        doc.append(r'Я крутое теоретическое введение. ')
        doc.append(r'Кажется, мой создатель обо мне не позаботился. ')
        doc.append(r'В МФТИ классные лабы! ')
    return doc
