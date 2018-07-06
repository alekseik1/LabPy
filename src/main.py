import pylatex as plx
from pylatex import Document, Package


def generate_preambula(doc: Document):
    """
    Переопределяет преамбулу.

    :param doc: Объект *Document*, в который будет идти запись
    :type doc: :class:`Document` instance
    :return: Объект *Document* с **переопределенной** преамбулой
    """
    # Здесь вы можете дописать/переписать свою преамбулу под документ
    ################################################
    # Обнулим преамбулу
    doc.preamble = []
    ################################################
    ################################################
    # Пакеты, которые будут подключены в преамбулу #
    # Пакеты без аргументов
    no_args_packages = [
                # Работа с русским языком для pdfLatex
                'cmap',         # поиск в PDF
                'mathtext',     # русские буквы
                'indentfirst',  # отступ 1 абзаца

                # Дополнительная работа с математиикой
                'amsfonts', 'amssymb', 'amsthm', 'mathtools',
                # TODO: разберись, почему extsizes не компилится
                #'extsizes',     # Возможность сделать 14-й шрифт
                'euscript',     # Шрифт Евклид
                'mathrsfs',     # Красивый матшрифт
                'csquotes',     # ещё одна штука для цитат
                'color',        # подключить пакет color
                'graphicx',     # Для вставки рисунков
                'wrapfig',      # Обтекание рисунков и таблиц текстом
                'multicol',
                # Работа с таблицами
                'array', 'tabularx', 'tabulary', 'booktabs',

                'longtable',    # Длинные таблицы
                'multirow',     # Слиянение строк в таблице
                # TODO: разберись, что с ним не так
                #'caption',
                'indentfirst',  # Красная строка
                'titlesec',
                'bm',           # Жирный греческий шрифт
                ]
    doc.preamble.extend([Package(i) for i in no_args_packages])
    # hyperref требует доп. аргументов
    args_packages = {'hyperref': ['unicode', 'colorlinks', 'urlcolor=blue',
                                  'linkcolor=blue', 'pagecolor=blue',  'citecolor=blue'],
                     'babel': ['english', 'russian']
                     }
    for name, args in args_packages.items():
        doc.preamble.append(Package(name=name, options=args))
    ################################################


if __name__ == '__main__':
    doc = Document(fontenc='T2A')
    generate_preambula(doc)
    doc.generate_tex()
