import tracemalloc

N = 10_000_000

print("--- 1. 리스트로 전체 데이터 생성 및 처리 ---")
tracemalloc.start()

# 모든 데이터를 리스트에 한 번에 올림
data_list = [x * 2 for x in range(N)]
total_list = sum(data_list)

current, peak_list = tracemalloc.get_traced_memory()
tracemalloc.stop()
tracemalloc.clear_traces()
print('리스트 결과 :', total_list)
print(f"리스트 처리 중 최대 메모리 사용량(Peak): {peak_list / (1024 * 1024):.2f} MB")


print("\n--- 2. 이터레이터(제너레이터)로 데이터 생성 및 처리 ---")
tracemalloc.start()

# 데이터를 미리 만들지 않고, 이터레이터(제너레이터)로 하나씩 생성하며 처리
data_iter = (x * 2 for x in range(N))
total_iter = sum(data_iter)

current, peak_iter = tracemalloc.get_traced_memory()
tracemalloc.stop()
tracemalloc.clear_traces()

print('이터레이터 결과 :', total_iter)
print(f"이터레이터 처리 중 최대 메모리 사용량(Peak): {peak_iter / (1024 * 1024):.6f} MB")