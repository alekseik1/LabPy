from src.main import *
from elizabeth import Text
from pylatex.utils import bold, italic
from pylatex import Math, Alignat, VectorName, Matrix, Eqref, Marker, Pageref
from pylatex.basic import Environment

if __name__ == '__main__':
    # Здесь будет тестирование работы ЛаТеХа
    ################################################
    #       Проверка стиля шрифта                  #
    ru = Text('ru')
    text = [ru.text(40),
            bold(ru.text(40)),
            italic(ru.text(40)),
            ]
    doc = generate_summary(create_document(), text=''.join(text))
    ################################################
    ################################################
    #       Проверка математики и ссылок           #
    with doc.create(Section(r'Проверка математики')):
        doc.append(Math(data=['E', '=', 'm', 'c', '^', '2'], escape=False))
        with doc.create(Alignat(escape=False)) as agn:
            agn.append(Command('label', Marker('eq1')))
            agn.extend([VectorName('F'), '=', 'm', VectorName('a'), r'\\'])
            agn.append(Command('label', Marker('eq2')))
            agn.extend([VectorName(NoEscape(r'F_2')), '=', 'G', UnsafeCommand('cfrac', [r'm_1 m_2', r'r^3']), VectorName('r')])
    with doc.create(Section(r'Еще куча всякой дряни')):
        doc.extend(text)
    with doc.create(Section(r'Проверка ссылок')):
        doc.extend([r'Посмотрите на формулу', NoEscape(r'\,'), Eqref(Marker('eq1')), NoEscape(r'\,'),
                    r'и на своего мужа. '])
        doc.extend([r'На страницу', NoEscape(r'\,'), Pageref(Marker('eq2')), NoEscape(r'\,'),
                    r'и на своего мужа. ', r'Да, я на коне.'])
    doc.generate_pdf('test', clean_tex=False)
