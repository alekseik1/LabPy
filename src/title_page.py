from pylatex import Document, Command, Center, LargeText, NewLine, NoEscape, HugeText
from pylatex.basic import Environment
from pylatex.utils import italic, bold


class TitlePage(Environment):
    _latex_name = 'titlepage'


class FlushRight(Environment):
    _latex_name = 'flushright'


def generate_titlepage(doc: Document,
                       title: str='Хорошееназвание',
                       lab_number: str='4.1.3',
                       author: str='Хорошего автора',
                       group: str='642',
                       date: str='',
                       ):
    """
    Генерирует титульник для лабы.
    :param doc: Объект *Document*, в который будет запись
    :param title: Название лабы
    :param author: Имя автора (будет отображаться)
    :param date: Дата изготовления. Если не укзывается, берется сегодня (\today).
    :return: Объект *Document* с внесенными изменениями
    """
    # TODO: Это хардкор. Может, напишешь нормально титульник?
    doc.extend([
        NoEscape(r'\begin{titlepage}'),
        NoEscape(r'\begin{center} '),
        NoEscape(r'\large Московский физико-технический институт\\'),
        NoEscape(r'Факультет молекулярной и химической физики\\'),
        NoEscape(r'\vspace{7cm}'),
        NoEscape(r'\huge Лабораторная работа №4.1.3\\'),
        NoEscape(r'\textbf{\Large <<Рефрактометр Аббе>>}\\'),
        NoEscape(r'\end{center} '),
        NoEscape(r'\vspace{7.5cm}'),
        NoEscape(r'{\par \raggedleft \large \emph{Выполнил:}\\'
                 r' студент 1 курса\\ '
                 r'642 группы ФМХФ\\'
                 r' Демьянов Георгий\\ '
                 r'Сергеевич \par}'),
        NoEscape(r'\begin{center}'),
        NoEscape(r'\vfill Москва 2018'),
        NoEscape(r'\end{center}'),
        NoEscape(r'\end{titlepage}'),
        NoEscape(r'\newpage'),

    ])
    # TODO: это шаблон из вышки, но он не работает. Думаю, стоит его сделать потом
    '''
    doc.append(Command('thispagestyle', 'empty'))
    with doc.create(Center()):
        doc.append(italic(r'Московский физико-технический институт'))      # Университет
        doc.append(NewLine())
        doc.append(LargeText(r'Факультет молекулярной и химической физики'))  # Факультет
    doc.append(Command('vspace', '13ex'))
    with doc.create(FlushRight()):
        doc.append(Command('noindent'))
        doc.append(italic(author))
        doc.append(NewLine())
        doc.append(r'группы %s' % group)
    with doc.create(Center()):
        doc.append(Command('vspace', '13ex'))
        doc.append(bold(Command('Large', r'<< %s >>' % title).dumps(), escape=False))
        doc.append(NewLine())
        doc.append(bold(LargeText(r'<< %s >>' % title).dumps()))
    '''

    return doc
