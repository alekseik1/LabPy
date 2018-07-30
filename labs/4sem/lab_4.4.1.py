from src.LabReport import LabReport

if __name__ == '__main__':
    lab = LabReport()
    lab.add_preamble()  # Делаем преамбулу

    author = 'Кожарин Алексей'
    lab.add_titlepage(
        lab_title="Амплитудная дифракционная решетка",
        lab_number='4.4.1',
        author=author,
        group='642',
    )

    lab.add_abstract(
        r'Целью работы является знакомство с настройкой и работой гониометра, '
        r'определение спектральных характеристик амплитудной решетки.'
    )

    lab.add_equipment(
        r'Гониометр Г5, дифракционная решетка, ртутная лампа.'
    )

    lab.add_theor_introduction(
        file_path='labs/4sem/theor.tex'
    )

    lab.generate_pdf('release')