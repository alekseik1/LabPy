from pylatex import Document, Command, Center, LargeText, LineBreak, NoEscape, HugeText, NewPage, UnsafeCommand
from pylatex.basic import Environment
from pylatex.utils import italic, bold

################################################
UNIVERSITY_NANE = r'Московский физико-технический институт'
# TODO: поменяйте на свой факультет
DEPARTMENT_NAME = r'Факультет молекулярной и химической физики'
################################################


class TitlePage(Environment):
    _latex_name = 'titlepage'


class FlushRight(Environment):
    _latex_name = 'flushright'


def generate_titlepage(doc: Document,
                       lab_title: str='Хорошая лаба',
                       lab_number: str='4.1.3',
                       author: str='Хороший автор',
                       group: str='642',
                       date: str='',
                       ):
    """
    Генерирует титульник для лабы.
    :param doc: Объект *Document*, в который будет запись
    :param lab_title: Название лабы
    :param lab_number: Номер лабы в лабнике
    :param author: Имя автора (будет отображаться)
    :param group: Номер группы, в которой ты учишься
    :param date: Дата изготовления. Если не укзывается, берется сегодня (\today).
    :return: Объект *Document* с внесенными изменениями
    """
    with doc.create(TitlePage()):
        with doc.create(Center()):
            # Название вуза сверху
            doc.append(Command('large'))
            doc.append(UNIVERSITY_NANE)
            doc.append(LineBreak())

            # Название факультета
            doc.append(DEPARTMENT_NAME)
            doc.append(NoEscape(r'\\'))
            doc.append(Command('vspace', '7cm'))

            # Название и номер лабы
            doc.append(Command('huge'))
            doc.append(NoEscape(r'Лабораторная работа №%s\\' % lab_number))
            doc.append(bold(Command('Large').dumps() +
                            '<< %s >>' % lab_title,
                            escape=False))
        doc.append(Command('vspace', '7.5cm'))

        # Большая магия. Текст справа с указанием автора
        with doc.create(FlushRight()):
            doc.append(Command('noindent'))
            doc.append(r'Выполнил: ')
            doc.append(LineBreak())
            doc.append(r'%s' % author)
            doc.append(LineBreak())
            doc.append(r'студент группы %s' % group)

        # "Москва <дата>" внизу страницы
        with doc.create(Center()):
            doc.append(Command('vfill'))
            doc.append(r'Москва ')           # Где сделан документ
            if date == '':
                doc.append(Command('today'))    # Когда сделан документ
            else:
                doc.append(date)    # Если указать дату явно

    # Перенос строки в конце
    doc.append(NewPage())

    return doc
