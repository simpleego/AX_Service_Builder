def add(self, num):
        self.result += num
        return self.result

class Calculator:
    def __init__(self):
        self.result = 0
        print("생성자 호출됨")

    def add(self, num):
        self.result += num
        return self.result

    def sub(self, num):
        self.result -= num
        return self.result

    def mul(self, num):
            self.result *= num
            return self.result

    def div(self, num):
            if num != 0:
                self.result /= num
            else:
                 return 0
            return self.result
    
    def show_result(self):
         print('result: ',self.result)

calc1 = Calculator()
calc1.add(5)    
print(calc1.show_result())
calc1.sub(3)
print(calc1.show_result())


