# VTB Registry Merge

#### Software development stack ####
- Python 3.5
- PyQt5


#### Описание ####
Программа позволяет объединять реестры на выплату в банк в мультиреестр.
В файле **serializers.py** реализован паттер **Абстрактная Фабрика** что позволяет в будущем масштабировать 
программу, добавляя новые правила сериализации для новых банков.

> Основная особенность (требование при разработке) - отсутствие сторонних библиотек и модулей, не входящих в 
поставку Python и использование устаревшей версии Python 3.5.

#### Структура файлов ####

***forms.py*** - Отрисовка главного окна программы Qt. Кнопки, формы, размеры окон.

***functions.py*** - Основные функции программы. Действия нажатия на кнопку и основная реализация.

***serializers.py*** - Сериализатор. Содержит в себе класс **Абстрактной фабрики** и шаблоны для идентификации банка по 
имени файла реестра, шаблоны для идентификации строк содержимого файла реестра. 
**Содержит функцию слияния, формирующую выходной файл.**
