import time
from functools import wraps

def time_checker(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"[{func.__name__}] 수행 시간: {elapsed_time:.6f} 초")
        return result
    return wrapper

N = 10_000_000

@time_checker
def process_with_list():
    data_list = [x * 2 for x in range(N)]
    return sum(data_list)

@time_checker
def process_with_iterator():
    data_iter = (x * 2 for x in range(N))
    return sum(data_iter)

print("--- 리스트 방식 실행 ---")
res_list = process_with_list()

print("\n--- 이터레이터 방식 실행 ---")
res_iter = process_with_iterator()