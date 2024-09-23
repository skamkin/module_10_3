import threading
from time import sleep
from random import randint

class Bank:

    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()

    def deposit(self):
        for _ in range(100):
            value = randint(50, 500)
            self.balance += value
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            sleep(0.001)
            print(f'Пополнение: {value:.2f} RUR. Ваш баланс: {self.balance:.2f} RUR.')

    def withdrawal(self):
        for _ in range(100):
            value = randint(50, 500)
            print(f'Запрос на снятие: {value} RUR')
            if self.balance < value:
                print(f'>> Запрос отклонен: недостаточно средств. <<')
                self.lock.acquire()
            else:
                self.balance -= value
                sleep(0.001)
                print(f'Снятие: {-value:.2f} RUR. Ваш баланс: {self.balance:.2f} RUR.')

def main():
    bk = Bank()
    # Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
    th1 = threading.Thread(target=Bank.deposit, args=(bk,))
    th2 = threading.Thread(target=Bank.withdrawal, args=(bk,))

    th1.start()
    th2.start()
    th1.join()
    th2.join()

    print(f'Итоговый баланс: {bk.balance}')

if __name__ == '__main__':
    main()
