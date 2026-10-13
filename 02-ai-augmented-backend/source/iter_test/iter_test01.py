import sys

# 데이터 개수 (1000만 개)
N = 10_000_000

# 1. 모든 데이터를 한 번에 메모리에 적재 (리스트 컴프리헨션)
list_data = [x for x in range(N)]

# 2. 데이터를 메모리에 올리지 않고 생성 규칙만 가짐 (제너레이터 표현식 = 이터레이터)
iter_data = (x for x in range(N))

# 메모리 사용량 측정 (Byte 단위)
list_size = sys.getsizeof(list_data)
iter_size = sys.getsizeof(iter_data)

print(f"1. 리스트(한 번에 적재) 메모리: {list_size / (1024 * 1024):.2f} MB")
print(f"2. 이터레이터(지연 생성) 메모리: {iter_size / 1024:.2f} KB")