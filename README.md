# Практическая работа "Параллельные вычисления"

Практическую работу сделал: Крюков Никита Андреевич РИ-230915

В данной практической работе **студент** более наглядно сможет увидеть преимущества параллельных вычислений на примере реального **пэт проекта**.

## Что необходимо для практической работы:
1. Заинтересованность студента
2. Средства запуска Python *(рекомендуется использовать IDE PyCharm Community Edition 2024.1.4)*
3. Подборка видео с YouTube, которые студент хочет сохранить себе на компьютер *(рекомендуется 2-5 коротких видео)*

## Этапы выполнения практической работы:
1. Скачать репозиторий с github на компьютер
2. Установить requirements.txt зависимости проекта. Для этого в проекте нужно открыть терминал и выполнить следующую команду:

```
pip install -r requirements.txt
```

3. Ознакомиться с кодом программы
4. Перейти в метод main() и заполнить картёж youtube_urls строками, которые содержат ссылки на видео, которое студент хочет скачать, например: 

```py
# В рамках практической работы рекомендую использовать видео длительностью около минуты.
# Список коротких видео с котиками (Shots):
youtube_urls = ("https://youtu.be/cS2vYtDq8l4?si=tFQWjb1gXrB0-ici"
                "https://youtu.be/SfmFOvVMc-o?si=GY_OsGJryPTPk54N",
                "https://youtu.be/_gKhXrDDYBM?si=pf4bJJDOiRcoPIyt",
                ...)
```
   
6. Запустить последовательный метод sequential_download() в основном методе main(), передав в него список коротких видео youtube_urls.
Зафиксировать время выполнения программы и потребляемую память. После фиксации данных закомментировать метод sequential_download().
7. Запустить параллельный метод, который работает на процессах parallel_download() в основном методе main(), передав в него список коротких видео youtube_urls.
Зафиксировать время выполнения программы и потребляемую память. После фиксации данных закомментировать метод parallel_download().
8. Самостоятельно реализовать метод parallel_download_thread(), который работает последовательно на потоках.
Зафиксировать время выполнения программы и потребляемую память.
9. Сделать вывод об использовании последовательного и параллельных вычислений в практическом проекте.
