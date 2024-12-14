import yt_dlp
import time
import os
import psutil
from multiprocessing import Process
from threading import Thread


"""

Практическая работа "Параллельные вычисления"

В данной практической работе студент более наглядно сможет увидеть преимущества параллельных вычислений на примере реального пэт проекта.

Что необходимо для практической работы:
1. Интерес
2. Средства запуска Python
3. Подборка видео с YouTube, которые студент хочет сохранить себе на компьютер

Этапы выполнения практической работы:
1. Скачать репозиторий с github
2. Установить зависимости проекта requirements.txt
3. Ознакомиться с кодом
4. Перейти в метод main() и заполнить картёж youtube_urls строками, которые содержат ссылки на видео, которое студент хочет скачать, например: 
    # Список коротких видео с котиками (Shots).
    # В рамках практической работы рекомендую использовать видео длительностью около минуты.
    youtube_urls = ('https://youtu.be/cS2vYtDq8l4?si=tFQWjb1gXrB0-ici'
                    'https://youtu.be/SfmFOvVMc-o?si=GY_OsGJryPTPk54N',
                    'https://youtu.be/_gKhXrDDYBM?si=pf4bJJDOiRcoPIyt',
                    ...)
                    
6. Запустить последовательный метод sequential_download() в основном методе main(), передав в него список коротких видео youtube_urls.
Зафиксировать время выполнения программы и потребляемую память. После фиксации данных закомментировать метод sequential_download().
7. Запустить параллельный метод, который работает на процессах parallel_download() в основном методе main(), передав в него список коротких видео youtube_urls.
Зафиксировать время выполнения программы и потребляемую память. После фиксации данных закомментировать метод parallel_download().
8. Самостоятельно реализовать метод parallel_download_thread(), который работает последовательно на потоках.
Зафиксировать время выполнения программы и потребляемую память.
9. Сделать вывод об использовании последовательного и параллельных вычислений в практическом проекте.
"""


def get_memory_usage() -> float:
    """Получение используемой памяти в мегабайтах."""
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss / (1024 * 1024)


def video_downloader(video_url: str) -> str:
    """Функция для скачивания видео с YouTube."""
    ydl_opts = {"format": "best",
                "outtmpl": "%(title)s.%(ext)s",
                "quiet": True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        file_name = ydl.prepare_filename(info)

    print("[ИНФОРМАЦИЯ] Файл", f'"{file_name}"', "скачан")
    print("=" * 72)
    return file_name


def sequential_download(youtube_urls: tuple) -> None:
    """Последовательное скачивание видео."""
    print("=" * 72)
    for url in youtube_urls:
        print(f"[ИНФОРМАЦИЯ] Скачивание видео с URL: {url}")
        video_downloader(url)


def parallel_download(youtube_urls: tuple) -> None:
    """Параллельное скачивание видео с помощью процессов."""
    print("=" * 72)
    print("[ИНФОРМАЦИЯ] Начинается параллельное скачивание видео с использованием процессов.")

    processes = []

    for url in youtube_urls:
        process = Process(target=video_downloader, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print("[ИНФОРМАЦИЯ] Все видео успешно скачаны.")


def parallel_download_thread(youtube_urls: tuple) -> None:
    """Параллельное скачивание видео с помощью потоков."""
    print("=" * 72)
    print("[ИНФОРМАЦИЯ] Начинается параллельное скачивание видео с использованием потоков.")

    threads = []

    for url in youtube_urls:
        thread = Thread(target=video_downloader, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("[ИНФОРМАЦИЯ] Все видео успешно скачаны.")


def main() -> None:
    youtube_urls = ('https://youtu.be/cS2vYtDq8l4?si=tFQWjb1gXrB0-ici',
                    'https://youtu.be/SfmFOvVMc-o?si=GY_OsGJryPTPk54N',
                    'https://youtu.be/_gKhXrDDYBM?si=pf4bJJDOiRcoPIyt')

    # sequential_download(youtube_urls)
    # parallel_download(youtube_urls)
    parallel_download_thread(youtube_urls)


def app() -> None:
    start_time = time.perf_counter()

    main()

    stop_time = time.perf_counter()

    print("=" * 72)
    print(f"    Время выполнения: {stop_time - start_time:0.5f} секунд.")
    final_memory = get_memory_usage()
    print(f"    Использовано памяти: {final_memory:.2f} Mb.")
    print("=" * 72)


if __name__ == "__main__":
    app()
