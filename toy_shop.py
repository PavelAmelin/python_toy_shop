from random import choice
import json
import os


class OurRangeError(Exception):
    pass


class Toy:
    shop_items = {}
    lst_lottery = []
    win_dct = {}

    def __init__(self, id, name, quant, weight):
        self.id = id
        self.name = name
        self.quant = quant
        self.weight = weight

    def add_toy(self):
        self.shop_items.setdefault(self.id, []).extend((self.name, self.quant, self.weight))
        return self.shop_items

    def list_of_weight_for_lottery(self):
        with open('shop_items_rest.json', 'r', encoding='utf-8') as inp:
            self.shop_items = json.load(inp)
            for k in self.shop_items:
                self.lst_lottery.extend((k, self.shop_items[k][0]) for _ in range(self.shop_items[k][1]))
        return len(self.lst_lottery)

    def add_weight(self):
        for k in self.shop_items:
            self.shop_items[k][2] = round(self.shop_items[k][1] / len(self.lst_lottery) * 100, 1)
        return self.shop_items

    def lottery_prize(self, win_num):
        with open('winners_dct.txt', 'a', encoding='utf-8') as file:
            win_toy = choice(self.lst_lottery)
            self.lst_lottery.remove(win_toy)
            self.shop_items[win_toy[0]][1] -= 1
            for k in self.shop_items:
                self.shop_items[k][2] = round(self.shop_items[k][1] / len(self.lst_lottery) * 100, 1)
            file.write(f'Розыгрыш № {win_num} - {win_toy[1]}\n')
        with open('shop_items_rest.json', 'w', encoding='utf-8') as file:
            json.dump(self.shop_items, file, ensure_ascii=False, indent=3)
        return f'Осталось игрушек {len(self.lst_lottery)}', self.shop_items


# Добавьте новые игрушки Toy(ID, название, количесвто, вес=None),
# вес с None будет пересчитан при добавлении веса и розыгрышах
toy1 = Toy(1, 'Плюшевый мишка', 25, None)
toy2 = Toy(2, 'Трансформер', 20, None)
toy3 = Toy(3, 'Конструктор', 8, None)
toy4 = Toy(4, 'Плюшевый заяц', 25, None)
toy5 = Toy(5, 'Паровоз', 18, None)
toy1.add_toy()
toy2.add_toy()
toy3.add_toy()
toy4.add_toy()
print(f'Изначально было: {toy5.add_toy()}')

if os.stat('shop_items_rest.json').st_size == 0:
    with open('shop_items_rest.json', 'w', encoding='utf-8') as file:
        json.dump(Toy.shop_items, file, ensure_ascii=False, indent=3)

print(f'Всего игрушек в магазине осталось: {toy5.list_of_weight_for_lottery()}\n')
print('Перечень оставшихся игрушек')
for k, v in toy5.add_weight().items():
    print(f'ID: {k}, Наименование: {v[0]}, Количесвто: {v[1]}, Вероятность выигрыша в %: {v[2]}')

try:
    cnt = int(input('Введите количество игрушек для розыгрыша (меньше того что осталось в магазине): '))
    if cnt >= len(Toy.lst_lottery):
        raise OurRangeError('Количество, большее или равное всем игрушек в магазине, разыгрываться не может')
    for i in range(1, cnt + 1):
        print(f'Прошел розыгрыш № {i}')
        print(toy5.lottery_prize(i))
    if len(Toy.lst_lottery) == 1:
        print('В магазине осталась одна игрушка, розыгрыш закончен')
except ValueError:
    print('Можно вводить только численные значения')
except OurRangeError as e:
    print(e)

