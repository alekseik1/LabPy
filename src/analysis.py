from pylatex import Document, NoEscape, Table, UnsafeCommand
import os
from sympy import *
import pandas as pd


def insert_raw_tex(doc: Document, code: str=""):
    """
    Вставляет сырой LaTeX-код в документ.

    :param doc: Объект *Document*, куда вставлять код
    :param code: Строка с кодом, которую нужно вставить
    :return: Объект *Document* с внесенными изменениями
    """
    doc.append(NoEscape(code))
    return doc


def insert_table_from_file(doc: Document,
                           caption: str='Название',
                           path: str="table1.csv",
                           wrap_table: bool=False,
                           **kwargs):
    """
    Вставляет таблицу в документ.

    Заметьте, что *kwargs* будет передан в *df.to_latex()*

    :param doc: Объект *Document*, куда вставлять таблицу
    :param caption: Название таблицы
    :param path: Путь до файла с таблицей
    :param wrap_table: Обтекать таблицу текстом или нет
    :return:
    """
    is_relative_path = not os.path.isabs(path)
    if is_relative_path:
        filename = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), path)
    else:
        filename = path
    df = pd.read_csv(filename)
    insert_dataframe(doc, df, caption, wrap_table, **kwargs)
    return doc


def insert_dataframe(doc: Document, df: pd.DataFrame=None, caption: str="", wrap_table: bool=False, **kwargs):
    """
    Вставляет датафрейм как *таблицу* в документ

    :param doc: Объект *Document*, куда вставлять таблицу
    :param df: Объект *DataFrame*, который вставлять
    :param caption: Название таблицы
    :param wrap_table: Обтекать таблицу текстом или нет
    :return: Объект *Document* с внесенными изменениями
    """

    kwargs.update({'index': False,   # По-умолчанию нумерация строк отключена
                   'column_format': '|c'*(len(df.keys())+1)+'|'}     # Выравнивание по центру с || между columns
                  )

    if not wrap_table:
        with doc.create(Table(position='htbp')):
            doc.append(UnsafeCommand('centering'))
            doc.append(UnsafeCommand('caption', NoEscape(caption)))
            doc.append(NoEscape(df.to_latex(**kwargs).replace(r'\\', r'\\ \hline')
                                )
                       )
    else:
        # FIXME: реализуй добавление обтекаемой таблицы
        doc.append(None)
    return doc
