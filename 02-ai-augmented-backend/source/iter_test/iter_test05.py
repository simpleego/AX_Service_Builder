import time
import tracemalloc
from functools import wraps

def measure_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        start_time = time.perf_counter()
        
        result = func(*args, **kwargs)
        
        end_time = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        elapsed_time = end_time - start_time
        
        print(f"[{func.__name__}]")
        print(f" - 수행 시간: {elapsed_time:.6f} 초")
        print(f" - 최대 메모리 사용량(Peak): {peak / (1024 * 1024):.7f} MB")
        
        return result
    return wrapper

N = 10_000_000

@measure_performance
def process_with_list():
    data_list = [x * 2 for x in range(N)]
    return sum(data_list)

@measure_performance
def process_with_iterator():
    data_iter = (x * 2 for x in range(N))
    return sum(data_iter)

print("--- 1. 리스트 방식 실행 ---")
res_list = process_with_list()

print("\n--- 2. 이터레이터 방식 실행 ---")
res_iter = process_with_iterator()