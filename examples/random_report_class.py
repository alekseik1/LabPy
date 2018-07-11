from src.LabReport import LabReport
from elizabeth import Text, Personal
import random
from src.utils import *
# КУЧА пактов pylatex -- ТОЛЬКО для тестов
from pylatex import UnsafeCommand, Section, Math, Alignat, VectorName, Marker, Command, NoEscape, Pageref, Eqref, Center
from pylatex.utils import italic, bold

if __name__ == '__main__':
    # Здесь будет тестирование работы ЛаТеХа
    ################################################
    #       Проверка стиля шрифта                  #
    ru = Text('ru')
    text = [ru.text(40),
            bold(ru.text(40)),
            italic(ru.text(40)),
            ]
    lab = LabReport()
    lab\
        .add_preamble()\
        .add_titlepage(
            author=Personal('ru').full_name(gender='male'),
            group=random.randint(100, 1000),
            lab_number='.'.join([*str(random.randint(100, 999))]),
            lab_title=Text('ru').quote()
        )\
        .add_annotation(r'В этом отчете я сделал кучу дряни, '
                        + italic(r'зато ')
                        + UnsafeCommand('textbf', 'научился ').dumps()
                        + UnsafeCommand('underline', 'выделять текст').dumps())\
        .add_theor_introduction('latex_template/annotation_and_teor.tex')\
        .add_summary(''.join(text))

    ################################################
    ################################################
    #       Проверка математики и ссылок           #
    with lab.create(Section(r'Проверка математики')):
        lab.append(Math(data=['E', '=', 'm', 'c', '^', '2'], escape=False))
        with lab.create(Alignat(escape=False)) as agn:
            agn.append(Command('label', Marker('eq1')))
            agn.extend([VectorName('F'), '=', 'm', VectorName('a'), r'\\'])
            agn.append(Command('label', Marker('eq2')))
            agn.extend(
                [VectorName(NoEscape(r'F_2')), '=', 'G', UnsafeCommand('cfrac', [r'm_1 m_2', r'r^3']), VectorName('r')])
    with lab.create(Section(r'Еще куча всякой дряни')):
        lab.extend(text)
    with lab.create(Section(r'Проверка ссылок')):
        lab.extend([r'Посмотрите на формулу', NoEscape(r'\,'), Eqref(Marker('eq1')), NoEscape(r'\,'),
                    r'и на своего мужа. '])
        lab.extend([r'На страницу', NoEscape(r'\,'), Pageref(Marker('eq2')), NoEscape(r'\,'),
                    r'и на своего мужа. ', r'Да, я на коне.'])
    ################################################
    ################################################
    #       Вставка таблицы из файла               #
    lab.insert_table_from_file('Таблица228', 'examples/data.csv')
    ################################################
    ################################################
    #   Проверка присоединения стороннего файла    #
    with lab.create(Center()):
        lab.append(bold(r'А теперь добавим файл Гоши'))
    add_from_tex_file(lab, 'latex_template/annotation_and_teor.tex')
    ################################################

    lab.generate_pdf('test_class', clean_tex=False)
