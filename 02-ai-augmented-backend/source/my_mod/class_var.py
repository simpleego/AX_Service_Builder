
class Car:
    # 클래스 변수
    serial_count = 0

    def __init__(self, model, color):
        Car.serial_count += 1

        self.model = model
        self.color = color
        self.serial_number =  f"CAR-{Car.serial_count:04d}"

    def show_info(self):
        print(f"시리얼번호 : {self.serial_number}")
        print(f"모델명     : {self.model}")
        print(f"색상       : {self.color}")
        print("-" * 30)


if __name__ == "__main__":
    print(Car.serial_count)

    car1 = Car("아반떼", "흰색")
    car2 = Car("쏘나타", "검정색")
    car3 = Car("그랜저", "회색")
    print(Car.serial_count)

    car1.show_info()
    car2.show_info()
    car3.show_info()

    print("현재까지 생산된 자동차 수 :", Car.serial_count)
    print("현재까지 생산된 자동차 수 :", car2.serial_count)