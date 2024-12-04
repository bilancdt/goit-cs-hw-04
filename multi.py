import multiprocessing
from multiprocessing import Queue
import os
import time

def search_keywords_in_file_mp(file_path, keywords, queue):
    local_results = {word: [] for word in keywords}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            for word in keywords:
                if word in content:
                    local_results[word].append(file_path)
        queue.put(local_results)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

def multiprocess_search(file_paths, keywords):
    results = {word: [] for word in keywords}
    queue = Queue()
    processes = []

    for file_path in file_paths:
        process = multiprocessing.Process(target=search_keywords_in_file_mp, args=(file_path, keywords, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    while not queue.empty():
        local_results = queue.get()
        for word, files in local_results.items():
            results[word].extend(files)

    return results

if __name__ == "__main__":
    # Вхідні дані
    keywords = ["error", "warning", "critical"]
    directory = r"C:\Users\artem\Downloads\text_files"
    file_paths = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.txt')]

    start_time = time.time()
    results = multiprocess_search(file_paths, keywords)
    end_time = time.time()

    print(f"Results (multiprocessing): {results}")
    print(f"Execution time (multiprocessing): {end_time - start_time:.2f} seconds")
