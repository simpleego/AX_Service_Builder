# try_finally2.py
try:
    print("나누기 전")
    4 / 2
    print("나누기 후")
except ZeroDivisionError:
    print("오류가 발생했습니다.")
finally:
    print("finally 실행!")
