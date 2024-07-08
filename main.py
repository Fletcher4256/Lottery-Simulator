import random, concurrent.futures, threading, os
from tqdm import tqdm

chosenNumbers = [32, 3, 74, 19, 45, 99]
match_counts = [0] * 7
match_values = [0, 0, 0, 30, 140, 1750, 1000000]
plays = 100000000
num_threads = 16
downloads_folder = os.path.expanduser('~/Downloads')

lock = threading.Lock()

def play_lottery(start, end, progress_bar):
    local_match_counts = [0] * 7

    for _ in range(start, end):
        rolledNumbers = [random.randint(1,99) for _ in range(6)]
        matches = sum(1 for cnumber in chosenNumbers if cnumber in rolledNumbers)

        local_match_counts[matches] += 1

        with lock:
            progress_bar.update(1)
    
    return local_match_counts

def update_global_counters(local_counts):
    for i in range(7):
        match_counts[i] += local_counts[i]

def print_results():
    print(f"0 Matches: {match_counts[0]}")
    print(f"1 Match: {match_counts[1]}")
    print(f"2 Matches: {match_counts[2]}")
    print(f"3 Matches: {match_counts[3]} worth {match_values[3] * match_counts[3]} in prize money")
    print(f"4 Matches: {match_counts[4]} worth {match_values[4] * match_counts[4]} in prize money")
    print(f"5 Matches: {match_counts[5]} worth {match_values[5] * match_counts[5]} in prize money")
    print(f"6 Matches: {match_counts[6]}")

    with open(f"{downloads_folder}/lottery_simulation.txt", "w") as file:
        file.write(f"0 Matches: {match_counts[0]}\n1 Match: {match_counts[1]}\n2 Matches: {match_counts[2]}\n3 Matches: {match_counts[3]} worth {match_values[3] * match_counts[3]} in prize money\n4 Matches: {match_counts[4]} worth {match_values[4] * match_counts[4]} in prize money\n5 Matches: {match_counts[5]} worth {match_values[5] * match_counts[5]} in prize money\n6 Matches: {match_counts[6]}")

chunk_size = plays // num_threads
futures = []

with tqdm(total=plays, desc="Playing...") as progress_bar:
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        for i in range(num_threads):
            start = i * chunk_size
            end = (i + 1) * chunk_size if i != num_threads - 1 else plays
            futures.append(executor.submit(play_lottery, start, end, progress_bar))

        for future in concurrent.futures.as_completed(futures):
            update_global_counters(future.result())

print_results()