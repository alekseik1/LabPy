import pylatex as plx
from pylatex import Document, Package, Command, NoEscape, UnsafeCommand, LineBreak, Section
import os

# Путь для картинок
IMAGES_PATH = 'images/'


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
    doc.preamble.append('')
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
                'indentfirst',  # Красная строка
                'titlesec',
                'bm',           # Жирный греческий шрифт
                'bigstrut'
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
    doc.preamble.append('')
    ################################################
    #           Подключение своих команд           #

    doc.preamble.append(
        Command('DeclareMathOperator', [NoEscape('\sgn'), Command('mathop', arguments='sgn')]))    # Команда \sgn
    doc.preamble.append(
        Command('newcommand', NoEscape('\pd'),
                extra_arguments=[UnsafeCommand('ensuremath',
                                               UnsafeCommand('cfrac',
                                                             arguments=[UnsafeCommand('partial', '#1'),
                                                                        UnsafeCommand('partial', '#2')],
                                                             ))],
                options=2)
    )   # Частная производная \pd
    doc.preamble.append(
        Command('newcommand', NoEscape(r'\abs'),
                extra_arguments=UnsafeCommand('ensuremath', NoEscape(r'\left|#1\right')),
                options=1)
    )   # Модуль \abs
    doc.preamble.append(
        Command('renewcommand', UnsafeCommand('phi'), extra_arguments=UnsafeCommand('ensuremath', UnsafeCommand('varphi')))
    )   # Буква phi красивая (по канонам)
    doc.preamble.append(
        Command('newcommand', UnsafeCommand('pogk'), options=1,
                extra_arguments=NoEscape(r'\!\left(\cfrac{\sigma_{#1}}{#1}\right)^{\!\!\!2}\!')
                )
    )   # для погрешностей
    doc.preamble.append(UnsafeCommand('providecommand', ['hm', '']))
    doc.preamble.append(
        Command('renewcommand*', UnsafeCommand('hm'), options=1,
                extra_arguments=UnsafeCommand(r'#1\nobreak\discretionary{}{\hbox{$\mathsurround=0pt #1$}}{}'))
    )  # Перенос знаков в формулах (по Львовскому)
    ################################################
    doc.preamble.append('')
    ################################################
    #               Путь для картинок              #
    doc.preamble.append(
        Command('graphicspath', NoEscape(r'%s' % IMAGES_PATH))
    )  # Путь для картинок
    ################################################
    doc.preamble.append('')
    ################################################
    #           Определить цвета                   #
    doc.preamble.append(
        Command('definecolor', ['BlueGreen', 'RGB', '49, 152, 255'])
    )
    doc.preamble.append(
        Command('definecolor', ['Violet', 'RGB', '120, 80, 120'])
    )   # назначить цвета при подключении RGB
    ################################################
    doc.preamble.append('')
    ################################################
    #             Всякая всячина                   #
    doc.preamble.append(
        Command(r'setlength\fboxsep', '3pt')
    )   # Отступ рамки \fbox{} от рисунка
    doc.preamble.append(
        Command(r'setlength\fboxrule', '1pt')
    )   # Обтекание рисунков и таблиц текстом
    doc.preamble.append(
        Command('captionsetup', ['labelsep=period, labelfont=bf'], packages=[Package('caption')])
    )
    doc.preamble.append(
        Command('titlelabel', NoEscape(r'\thetitle.\quad'))
    )
    ################################################
    doc.preamble.append('')
    ################################################
    #           Работа с теоремами                 #
    doc.preamble.append(Command('theoremstyle', 'plain'))   # "Теорема"
    # TODO: Я сделал hard-code здесь, поскольку не нашел, как сделать [] после {}{}
    doc.preamble.append(NoEscape(r'\newtheorem{theorem}{Теорема}[section]'))
    doc.preamble.append(NoEscape(r'\newtheorem{proposition}[theorem]{Утверждение}'))

    doc.preamble.append(Command('theoremstyle', 'definition'))  # "Определение"
    doc.preamble.append(NoEscape(r'\newtheorem{definition}{Определение}[section]'))
    doc.preamble.append(NoEscape(r'\newtheorem{corollary}{Следствие}[theorem]'))
    doc.preamble.append(NoEscape(r'\newtheorem{problem}{Задача}[section]'))

    doc.preamble.append(Command('theoremstyle', 'remark'))  # "Примечание"
    doc.preamble.append(NoEscape(r'\newtheorem*{nonum}{Решение}'))
    doc.preamble.append(NoEscape(r'\newtheorem{zamech}{Замечание}[theorem]'))
    ################################################
    doc.preamble.append('')
    ################################################
    #  Правильные мат.символы для русского языка   #
    doc.preamble.append(Command('renewcommand', [Command('epsilon'), Command('ensuremath', Command('varepsilon'))]))
    doc.preamble.append(Command('renewcommand', [Command('phi'), Command('ensuremath', Command('varphi'))]))
    doc.preamble.append(Command('renewcommand', [Command('kappa'), Command('ensuremath', Command('varkappa'))]))
    doc.preamble.append(Command('renewcommand', [Command('le'), Command('ensuremath', Command('leslant'))]))
    doc.preamble.append(Command('renewcommand', [Command('leq'), Command('ensuremath', Command('leqslant'))]))
    doc.preamble.append(Command('renewcommand', [Command('ge'), Command('ensuremath', Command('geslant'))]))
    doc.preamble.append(Command('renewcommand', [Command('geq'), Command('ensuremath', Command('geqslant'))]))
    doc.preamble.append(Command('renewcommand', [Command('emptyset'), Command('ensuremath', Command('varnothing'))]))
    ################################################
    return doc


def generate_summary(doc: Document, text: str=''):
    """
    Прописывает *Заключение* в документ **doc**

    :param doc: Объект типа **Document**
    :return: Объект *Document* с **добавленным** заключением
    """

    with doc.create(Section(r'Заключение')):
        if text == '':
            doc.append(r'Это текст заключения')
        else:
            doc.append(NoEscape(text))
    return doc


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


if __name__ == '__main__':
    doc = create_document()
    generate_preambula(doc)
    generate_summary(doc)
    doc.generate_pdf('main', clean_tex=False)
