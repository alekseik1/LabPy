from pylatex import Document, Center, NoEscape, UnsafeCommand
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
        doc.append(UnsafeCommand(
            'vspace',   # Отступ
            ['0.5cm',
             UnsafeCommand(
                 'parbox', ['16cm',  # "Коробочка" посередине
                 UnsafeCommand(
                     'small',
                     UnsafeCommand(
                         'centering',
                         bold('Аннотация') + NoEscape(r'\\') +
                         UnsafeCommand('hspace', '0.6cm').dumps() +
                         text   # Сам текст
                     )
                 )]
             )
             ]
        ))
    return doc
