from pylatex import Document, Center, Command, NoEscape
from pylatex.utils import bold


def generate_annotation(doc: Document, text: str=""):
    """
    Создает аннотацию для лабораторной работы. Анноптация
    прописывается перед началом текста в центре небольшим
    шрифтом; содержит в себе краткую выжимку происходящего.

    :param doc: Объект *Document*, куда записывать аннотацию
    :param text: Текст аннотации, поддерживает синтаксис *LaTeX*
    и *pylatex*
    :return: Объект *Document* с внесенными изменениями
    """
    with doc.create(Center()):
        doc.append(Command(
            'vspace',   # Отступ
            ['0.5cm',
             Command(
                 'parbox', '16cm',  # "Коробочка" посередине
                 Command(
                     'small',
                     Command(
                         'centering',
                         bold('Аннотация') + NoEscape(r'\\') +
                         Command('hspace', '0.6cm').dumps() +
                         text   # Сам текст
                     )
                 )
             )
             ]
        ))

