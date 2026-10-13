# iterator.py
class MyIterator:
    def __init__(self, data):
        self.data = data
        self.position = 0
        print('객체 생성됨')

    def __iter__(self):
        print('반복객체 반환')
        return self

    def __next__(self):
        if self.position >= len(self.data):
            raise StopIteration
        result = self.data[self.position]
        self.position += 1
        print('사용함')
        return result

if __name__ == "__main__":
    i = MyIterator([1,2,3])
    for item in i:
        print(item)
