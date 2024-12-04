import threading
import os
import time

def search_keywords_in_file(file_path, keywords, results):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            for word in keywords:
                if word in content:
                    results[word].append(file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

def threaded_search(file_paths, keywords):
    results = {word: [] for word in keywords}
    threads = []

    for file_path in file_paths:
        thread = threading.Thread(target=search_keywords_in_file, args=(file_path, keywords, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results

if __name__ == "__main__":
    # Вхідні дані
    keywords = ["error", "warning", "critical"]
    directory = r"C:\Users\artem\Downloads\text_files"

    file_paths = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.txt')]

    start_time = time.time()
    results = threaded_search(file_paths, keywords)
    end_time = time.time()

    print(f"Results (threading): {results}")
    print(f"Execution time (threading): {end_time - start_time:.2f} seconds")
