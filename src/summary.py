from pylatex import Document, Section, NoEscape


def generate_summary(doc: Document, text: str=''):
    """
    Прописывает *Заключение* в документ **doc**

    :param doc: Объект типа **Document**
    :param text: Текст, который будет записан в *Заключении*
    :return: Объект *Document* с **добавленным** заключением
    """

    with doc.create(Section(r'Заключение')):
        if text == '':
            doc.append(r'Это текст заключения')
        else:
            doc.append(NoEscape(text))
    return doc