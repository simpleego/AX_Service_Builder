class FourCal:
     def __init__(self, first, second):
         self.first = first
         self.second = second
         self.result = 0

     def setdata(self, first, second):
         self.first = first
         self.second = second

     def showdata(self):
            print('first:',self.first)
            print('second:',self.second)

     def add(self):
         self.result = self.first + self.second
         return self.result
     
     def mul(self):
         result = self.first * self.second
         return result
     def sub(self):
         result = self.first - self.second
         return result
     def div(self):
         result = self.first / self.second
         return result

# cal1 = FourCal(2,5)
# print(cal1.add())

class MoreCalc(FourCal):
    def pow(self):
         result = self.first ** self.second
         return result
    def div(self):
            if self.second != 0:
                  result = self.first / self.second
            else:
                  result = 0
            return result


mcalc1 = MoreCalc(10,20)
print(mcalc1.add())
print(mcalc1.sub())
mcalc1.setdata(5,2)
print(mcalc1.pow())
mcalc1.setdata(5,0)
print(mcalc1.div())