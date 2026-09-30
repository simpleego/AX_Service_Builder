# try_except.py
a=4
b=0

try:
    c = a / b
except ZeroDivisionError as e:
    c = 0
    print(e)
#c = a / b

print('다음 문장을 수행한다.')