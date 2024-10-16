import timeit

# Алгоритм Боєра-Мура
def boyer_moore(text, pattern):
    m = len(pattern)
    n = len(text)
    if m == 0:
        return 0

    # Створення таблиці останніх появ символів
    last = {}
    for i in range(m):
        last[pattern[i]] = i

    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return s
        else:
            s += max(1, j - last.get(text[s + j], -1))
    return -1

# Алгоритм Кнута-Морріса-Пратта
def kmp_search(text, pattern):
    m = len(pattern)
    n = len(text)

    # Створення таблиці префіксів
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    i = j = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            return i - j
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

# Алгоритм Рабіна-Карпа
def rabin_karp(text, pattern):
    m = len(pattern)
    n = len(text)
    p = 0
    t = 0
    h = 1
    d = 256
    q = 101

    for i in range(m - 1):
        h = (h * d) % q

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(n - m + 1):
        if p == t:
            if text[i:i + m] == pattern:
                return i
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t = t + q
    return -1


def measure_time(algorithm, text, pattern):
    timer = timeit.timeit(lambda: algorithm(text, pattern), number=1)
    return timer

with open('./стаття 1.txt', 'r', encoding='windows-1251') as f:
    text1 = f.read()

with open('./стаття 2.txt', 'r', encoding='utf-8') as f:
    text2 = f.read()

existing_substring = "алгоритм"
non_existing_substring = "неіснуючийпідрядок"

algorithms = {
    "Boyer-Moore": boyer_moore,
    "Knuth-Morris-Pratt": kmp_search,
    "Rabin-Karp": rabin_karp
}

for text_name, text in [("Article 1", text1), ("Article 2", text2)]:
    print(f"\nТекст: {text_name}")
    for substring_name, substring in [("існуючий", existing_substring), ("вигаданий", non_existing_substring)]:
        print(f"\n  Підрядок: {substring_name}")
        for algorithm_name, algorithm in algorithms.items():
            time_taken = measure_time(algorithm, text, substring)
            print(f"    {algorithm_name}: {time_taken:.6f} seconds")
