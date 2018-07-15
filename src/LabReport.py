from pylatex import Document, Center, NoEscape, UnsafeCommand, Command, Package, Section, LineBreak, NewPage, Table
from pylatex.basic import Environment
from pylatex.base_classes import Container
from pylatex.utils import bold
from src.utils import *
import pandas as pd


class LabReport(Document):
    """
    Класс отчета лабораторной работы
    """

    class TitlePage(Environment):
        _latex_name = 'titlepage'

    class FlushRight(Environment):
        _latex_name = 'flushright'

    class Abstract(Environment):
        _latex_name = 'abstract'
        _escape = False

    ################################################
    #               Значения по умолчанию          #
    ################################################
    IMAGES_PATH = 'images/'     # Путь до картинок по умолчанию
    UNIVERSITY_NANE = r'Московский физико-технический институт'
    DEPARTMENT_NAME = r'Факультет молекулярной и химической физики'
    ################################################

    def __init__(self, **kwargs):
        # Далее идет инициализация параметров документа по умолчанию
        # Если их явным образом указать, они будут переопределены
        if kwargs.get('fontenc') is None:
            kwargs.update({'fontenc': 'T2A'})
        if kwargs.get('documentclass') is None:
            kwargs.update({'documentclass': 'article'})
        if kwargs.get('document_options') is None:
            kwargs.update({'document_options': ['a4paper', '12pt']})
        if kwargs.get('geometry_options') is None:
            kwargs.update({'geometry_options':
                               {'left': '1.27cm',
                                'right': '1.27cm',
                                'top': '2cm',
                                'bottom': '2cm'}
                           })
        if kwargs.get('lmodern') is None:
            kwargs.update({'lmodern': False})

        # Пустые секции
        self.parts = [
            'title_page',
            'abstract',
            'theor_intro',
            'summary'
        ]
        for part in self.parts:
            setattr(self, 'section_%s' % part, Section(r''))
        super().__init__(**kwargs)

    def set_images_path(self, path: str):
        self.IMAGES_PATH = path

    def set_university_name(self, university_name: str):
        self.UNIVERSITY_NANE = university_name

    def set_department_name(self, department_name: str):
        self.DEPARTMENT_NAME = department_name

    def add_abstract(self, text: str = ""):
        """
        Создает аннотацию для лабораторной работы. Анноптация
        прописывается перед началом текста в центре небольшим
        шрифтом; содержит в себе краткую выжимку происходящего.

        :param text: Текст аннотации, поддерживает синтаксис *LaTeX*
        и *pylatex*
        :return: Объект *LabReport* с внесенными изменениями
        """
        abstract = self.Abstract()
        abstract.append(text)

        self.section_abstract = abstract
        return self

    def add_preamble(self):
        """
        Переопределяет преамбулу.

        :return: Объект *LabReport* с **переопределенной** преамбулой
        """
        # Здесь вы можете дописать/переписать свою преамбулу под документ
        ################################################
        # Обнулим преамбулу
        self.preamble = []
        ################################################
        self.preamble.append('')
        ################################################
        # Пакеты, которые будут подключены в преамбулу #

        # Пакеты без аргументов
        no_args_packages = [
            # Работа с русским языком для pdfLatex
            'cmap',  # поиск в PDF
            'mathtext',  # русские буквы
            'indentfirst',  # отступ 1 абзаца

            # Дополнительная работа с математиикой
            'amsfonts', 'amssymb', 'amsthm', 'mathtools',
            # TODO: разберись, почему extsizes не компилится
            # 'extsizes',     # Возможность сделать 14-й шрифт
            'euscript',  # Шрифт Евклид
            'mathrsfs',  # Красивый матшрифт
            'csquotes',  # ещё одна штука для цитат
            'color',  # подключить пакет color
            'graphicx',  # Для вставки рисунков
            'wrapfig',  # Обтекание рисунков и таблиц текстом
            'multicol',
            # Работа с таблицами
            'array', 'tabularx', 'tabulary', 'booktabs',

            'longtable',  # Длинные таблицы
            'multirow',  # Слиянение строк в таблице
            'indentfirst',  # Красная строка
            'titlesec',
            'bm',  # Жирный греческий шрифт
            'bigstrut'
        ]
        self.preamble.extend([Package(i) for i in no_args_packages])
        # hyperref требует доп. аргументов
        args_packages = {'hyperref': ['unicode', 'colorlinks', 'urlcolor=blue',
                                      'linkcolor=blue', 'pagecolor=blue', 'citecolor=blue'],
                         'babel': ['english', 'russian']
                         }
        for name, args in args_packages.items():
            self.preamble.append(Package(name=name, options=args))
        ################################################
        self.preamble.append('')
        ################################################
        #           Подключение своих команд           #

        self.preamble.append(
            Command('DeclareMathOperator', [NoEscape('\sgn'), Command('mathop', arguments='sgn')]))  # Команда \sgn
        self.preamble.append(
            Command('newcommand', NoEscape('\pd'),
                    extra_arguments=[UnsafeCommand('ensuremath',
                                                   UnsafeCommand('cfrac',
                                                                 arguments=[UnsafeCommand('partial', '#1'),
                                                                            UnsafeCommand('partial', '#2')],
                                                                 ))],
                    options=2)
        )  # Частная производная \pd
        self.preamble.append(
            Command('newcommand', NoEscape(r'\abs'),
                    extra_arguments=UnsafeCommand('ensuremath', NoEscape(r'\left|#1\right')),
                    options=1)
        )  # Модуль \abs
        self.preamble.append(
            Command('renewcommand', UnsafeCommand('phi'),
                    extra_arguments=UnsafeCommand('ensuremath', UnsafeCommand('varphi')))
        )  # Буква phi красивая (по канонам)
        self.preamble.append(
            Command('newcommand', UnsafeCommand('pogk'), options=1,
                    extra_arguments=NoEscape(r'\!\left(\cfrac{\sigma_{#1}}{#1}\right)^{\!\!\!2}\!')
                    )
        )  # для погрешностей
        self.preamble.append(UnsafeCommand('providecommand', ['hm', '']))
        self.preamble.append(
            Command('renewcommand*', UnsafeCommand('hm'), options=1,
                    extra_arguments=UnsafeCommand(r'#1\nobreak\discretionary{}{\hbox{$\mathsurround=0pt #1$}}{}'))
        )  # Перенос знаков в формулах (по Львовскому)
        ################################################
        self.preamble.append('')
        ################################################
        #               Путь для картинок              #
        self.preamble.append(
            Command('graphicspath', NoEscape(r'%s' % self.IMAGES_PATH))
        )  # Путь для картинок
        ################################################
        self.preamble.append('')
        ################################################
        #           Определить цвета                   #
        self.preamble.append(
            Command('definecolor', ['BlueGreen', 'RGB', '49, 152, 255'])
        )
        self.preamble.append(
            Command('definecolor', ['Violet', 'RGB', '120, 80, 120'])
        )  # назначить цвета при подключении RGB
        ################################################
        self.preamble.append('')
        ################################################
        #             Всякая всячина                   #
        self.preamble.append(
            Command(r'setlength\fboxsep', '3pt')
        )  # Отступ рамки \fbox{} от рисунка
        self.preamble.append(
            Command(r'setlength\fboxrule', '1pt')
        )  # Обтекание рисунков и таблиц текстом
        self.preamble.append(
            Command('captionsetup', ['labelsep=period, labelfont=bf'], packages=[Package('caption')])
        )
        self.preamble.append(
            Command('titlelabel', NoEscape(r'\thetitle.\quad'))
        )
        ################################################
        self.preamble.append('')
        ################################################
        #           Работа с теоремами                 #
        self.preamble.append(Command('theoremstyle', 'plain'))  # "Теорема"
        # TODO: Я сделал hard-code здесь, поскольку не нашел, как сделать [] после {}{}
        self.preamble.append(NoEscape(r'\newtheorem{theorem}{Теорема}[section]'))
        self.preamble.append(NoEscape(r'\newtheorem{proposition}[theorem]{Утверждение}'))

        self.preamble.append(Command('theoremstyle', 'definition'))  # "Определение"
        self.preamble.append(NoEscape(r'\newtheorem{definition}{Определение}[section]'))
        self.preamble.append(NoEscape(r'\newtheorem{corollary}{Следствие}[theorem]'))
        self.preamble.append(NoEscape(r'\newtheorem{problem}{Задача}[section]'))

        self.preamble.append(Command('theoremstyle', 'remark'))  # "Примечание"
        self.preamble.append(NoEscape(r'\newtheorem*{nonum}{Решение}'))
        self.preamble.append(NoEscape(r'\newtheorem{zamech}{Замечание}[theorem]'))
        ################################################
        self.preamble.append('')
        ################################################
        #  Правильные мат.символы для русского языка   #
        self.preamble.append(Command('renewcommand', [Command('epsilon'), Command('ensuremath', Command('varepsilon'))]))
        self.preamble.append(Command('renewcommand', [Command('phi'), Command('ensuremath', Command('varphi'))]))
        self.preamble.append(Command('renewcommand', [Command('kappa'), Command('ensuremath', Command('varkappa'))]))
        self.preamble.append(Command('renewcommand', [Command('le'), Command('ensuremath', Command('leslant'))]))
        self.preamble.append(Command('renewcommand', [Command('leq'), Command('ensuremath', Command('leqslant'))]))
        self.preamble.append(Command('renewcommand', [Command('ge'), Command('ensuremath', Command('geslant'))]))
        self.preamble.append(Command('renewcommand', [Command('geq'), Command('ensuremath', Command('geqslant'))]))
        self.preamble.append(
            Command('renewcommand', [Command('emptyset'), Command('ensuremath', Command('varnothing'))]))
        ################################################
        return self

    def add_summary(self, text: str = ''):
        """
        Прописывает *Заключение* в документ **doc**

        :param text: Текст, который будет записан в *Заключении*
        :return: Объект *LabReport* с **добавленным** заключением
        """

        sec = Section(r'Заключение')
        if text == '':
            sec.append(r'Это текст заключения')
        else:
            sec.append(NoEscape(text))
        self.section_summary = sec
        return self

    def add_titlepage(self,
                      lab_title: str = 'Хорошая лаба',
                      lab_number: str = '4.1.3',
                      author: str = 'Хороший автор',
                      group: str = '642',
                      date: str = '',
                      ):
        """
        Генерирует титульник для лабы.

        :param lab_title: Название лабы
        :param lab_number: Номер лабы в лабнике
        :param author: Имя автора (будет отображаться)
        :param group: Номер группы, в которой ты учишься
        :param date: Дата изготовления. Если не укзывается, берется сегодня (\today).
        :return: Объект *LabReport* с внесенными изменениями
        """
        tp = LabReport.TitlePage()
        with tp.create(Center()) as center:
            # Название вуза сверху
            center.append(Command('large'))
            center.append(self.UNIVERSITY_NANE)
            center.append(LineBreak())

            # Название факультета
            center.append(self.DEPARTMENT_NAME)
            center.append(NoEscape(r'\\'))
            center.append(Command('vspace', '7cm'))

            # Название и номер лабы
            center.append(Command('huge'))
            center.append(NoEscape(r'Лабораторная работа №%s\\' % lab_number))
            center.append(bold(Command('Large').dumps() +
                             '<< %s >>' % lab_title,
                             escape=False))
        tp.append(Command('vspace', '7.5cm'))

        # Большая магия. Текст справа с указанием автора
        with tp.create(LabReport.FlushRight()) as fl:
            fl.append(Command('noindent'))
            fl.append(r'Выполнил: ')
            fl.append(LineBreak())
            fl.append(r'%s' % author)
            fl.append(LineBreak())
            fl.append(r'студент группы %s' % group)

        # "Москва <дата>" внизу страницы
        with tp.create(Center()) as center:
            center.append(Command('vfill'))
            center.append(r'Москва ')  # Где сделан документ
            if date == '':
                center.append(Command('today'))  # Когда сделан документ
            else:
                center.append(date)  # Если указать дату явно

        # Перенос строки в конце
        self.append(NewPage())

        self.section_title_page = tp
        return self

    def add_theor_introduction(self, content: str = "", file_path: str = ""):
        """
        Создает теоретическое введение к лабе.

        Делать его тяжело и неприятно, поэтому имеется возможность
        взять эту часть из готового .tex файла

        :param content: Строка, которой будет инициализировано теоретическое введение
        :param file_path: Путь к файлу с теор.введением (*необязательно*)
        :return: Объект *LabReport* с готовыми изменениями
        """
        theor_intro = Section(r'Теоретическое введение')
        if file_path != "":
            add_from_tex_file(theor_intro, file_path)
        else:
            # TODO: поскольку теор. часть достаточно сложна для ввода,
            # TODO: я заставлю вас редактировать исходники метода под каждую лабу.
            # FIXME: Возможно, в будущем я придумаю идею получше.
            theor_intro.append(content)

        self.section_theor_intro = theor_intro
        return self

    @staticmethod
    def add_tex_code(section, code: str = ""):
        """
        Вставляет сырой LaTeX-код в отчет.

        :param section: Секция, куда вставлять
        :param code: Строка с кодом, которую нужно вставить
        :return: Секция *Section* с внесенными изменениями
        """
        return insert_raw_tex(section, code)

    @staticmethod
    def add_tex_file(section, path: str):
        """
        Вставляет содержимое **.tex** файла в отчет

        :param section: Секция, куда вставлять
        :param path: Путь до файла
        :return: Объект *Section* с готовыми изменениями
        """
        return add_from_tex_file(section, path)

    @staticmethod
    def add_table_from_file(section,
                            caption: str = 'Название',
                            path: str = "table1.csv",
                            wrap_table: bool = False,
                            **kwargs):
        """
        Вставляет таблицу в документ.

        Заметьте, что *kwargs* будет передан в *df.to_latex()*

        :param section: Секция, куда вставлять
        :param caption: Название таблицы
        :param path: Путь до файла с таблицей
        :param wrap_table: Обтекать таблицу текстом или нет
        :return: Секция с внесенными изменениями
        """
        is_relative_path = not os.path.isabs(path)
        if is_relative_path:
            filename = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), path)
        else:
            filename = path
        df = pd.read_csv(filename)
        LabReport.insert_dataframe(section, df, caption, wrap_table, **kwargs)
        return section

    @staticmethod
    def insert_dataframe(section, df: pd.DataFrame = None, caption: str = "", wrap_table: bool = False, **kwargs):
        """
        Вставляет датафрейм как *таблицу* в документ

        :param section: Секция, куда вставлять таблицу
        :param df: Объект *DataFrame*, который вставлять
        :param caption: Название таблицы
        :param wrap_table: Обтекать таблицу текстом или нет
        :return: Объект *Document* с внесенными изменениями
        """

        kwargs.update({'index': False,  # По-умолчанию нумерация строк отключена
                       'column_format': '|c' * (len(df.keys()) + 1) + '|'}  # Выравнивание по центру с || между columns
                      )

        if not wrap_table:
            with section.create(Table(position='htbp')):
                section.append(UnsafeCommand('centering'))
                section.append(UnsafeCommand('caption', NoEscape(caption)))
                section.append(NoEscape(df.to_latex(**kwargs).replace(r'\\', r'\\ \hline')))
        else:
            # FIXME: реализуй добавление обтекаемой таблицы
            section.append(None)
        return section

    def generate_pdf(self, filepath=None, *, clean=True, clean_tex=True,
                     compiler=None, compiler_args=None, silent=True):
        # Добавляем все разделы в ПРАВИЛЬНОМ порядке

        for part in self.parts:
            self.append(getattr(self, 'section_%s' % part))
        super().generate_pdf(filepath, clean=clean, clean_tex=clean_tex, compiler=compiler,
                             compiler_args=compiler_args, silent=silent)
