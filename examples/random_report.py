from src.main import *
from elizabeth import Text

if __name__ == '__main__':
    ru = Text('ru')
    doc = generate_summary(create_document(), text=ru.text(100))
    doc.generate_pdf('test', clean_tex=False)