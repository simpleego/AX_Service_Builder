# try_finally.py
try:
    f = open('foo1.txt', 'r')
    # 무언가를 수행한다.

    #(... 생략 ...)
except FileNotFoundError as e:
    print(e)
# finally:
#     f.close()  # 중간에 오류가 발생하더라도 무조건 실행된다.

print('반드시 수행됩니다.')
