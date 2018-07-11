# LabPy
*"Хороша та лаба, что делает себя сама"*

Проект **LabPy** пытается сделать шаблонное оформление лабораторных работ более
простым для конечного пользователя.

### Что это?
Это - набор утилит для автоматической обработки результатов и верстки 
отчета в **LaTeX**.

## Установка
1.(опционально) Создайте виртуальное окружение:
```bash
virtualenv venv
source venv/bin/activate
``` 
2.Установите зависимости:
```bash
pip install -r requirements.txt
```
## Запуск
**WARNING**: *Секция в процессе разработки*

Для генерации отчета по **существующему** шаблону достаточно запусить *.py*-файл
шаблона, заменив все файлы с экспериментальными данными своими.

*Пример*: шаблон лабы 4.1.3 находится в папке **templates/4-1-3** (*ее пока нет*).
Запустите
```bash
python templates/4-1-3/main.py
```
В той же папке будет создан файл **4.1.3.pdf** - затеханная лаба

## Свои шаблоны
При желании и времени вы можете создать свой шаблон для лабы.

За подробностями см. [здесь](OWN_TEMPLATE.md).

## Контрибьюция
Если вы нашли баг или ошибку, пишите в **Issues**, либо исправляйте и
делайте **Pull request**. Буду крайне признателен, если вы поможете в написании
шаблонов.