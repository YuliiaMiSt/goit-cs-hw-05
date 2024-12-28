import requests
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import re

def fetch_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return ""

def map_words(text_chunk):
    words = re.findall(r'\b\w+\b', text_chunk.lower())
    return Counter(words)

def reduce_counters(counters):
    total_counter = Counter()
    for counter in counters:
        total_counter.update(counter)
    return total_counter

def split_text(text, num_chunks):
    lines = text.splitlines()
    chunk_size = len(lines) // num_chunks
    return ["\n".join(lines[i * chunk_size:(i + 1) * chunk_size]) for i in range(num_chunks)]

def visualize_top_words(word_freq, top_n=10):
    top_words = word_freq.most_common(top_n)
    words, counts = zip(*top_words)

    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color='skyblue')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title(f'Top {top_n} Words by Frequency')
    plt.xticks(rotation=45)
    plt.show()

def main():
    url = input("Enter the URL of the text: ")
    text = fetch_text(url)

    if not text:
        return

  
    num_threads = 4

  
    text_chunks = split_text(text, num_threads)

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        counters = list(executor.map(map_words, text_chunks))

    word_freq = reduce_counters(counters)

    visualize_top_words(word_freq, top_n=10)

if __name__ == "__main__":
    main()
