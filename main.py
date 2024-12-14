import yt_dlp
import time
import os
import psutil
from multiprocessing import Process
from threading import Thread


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

    # Тут писать код.
    # ...

    print("[ИНФОРМАЦИЯ] Все видео успешно скачаны.")


def main() -> None:
    youtube_urls = ()

    sequential_download()
    # parallel_download()
    # parallel_download_thread()


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
