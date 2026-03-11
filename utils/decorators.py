import functools
import time

# Shared list to store all timing results
_timing_records = []

def timer_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        duration = end_time - start_time
        _timing_records.append({"name": func.__name__, "duration": duration})

        return result
    return wrapper

def print_timing_summary():
    if not _timing_records:
        return

    print("\n" + "***" * 20)
    print(">>> TIMING SUMMARY <<<")
    print("***" * 20)

    for i, record in enumerate(_timing_records, 1):
        print(f"  {i}. {record['name']:<30} {record['duration']:.4f}s")

    print("-" * 62)
    total = sum(r["duration"] for r in _timing_records)
    slowest = max(_timing_records, key=lambda r: r["duration"])
    print(f"  {'Total time:':<30} {total:.4f}s")
    print(f"  {'Slowest function:':<30} {slowest['name']} ({slowest['duration']:.4f}s)")
    print("***" * 20 + "\n")