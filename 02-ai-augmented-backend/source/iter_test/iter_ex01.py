# for a in [1, 2, 3]:
#     print(a)

a = [1,2,3]
ia = iter(a)
for i in ia:
     print(i)

# print(next(ia))
# print(next(ia))
# print(next(ia))
try:
    print(next(ia))
except:
    print('더 이상 꺼낼 수 없습니다.')

for i in ia:
    print(i)