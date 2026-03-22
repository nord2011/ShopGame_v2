from itertools import product
import copy

class Product:
    def __init__(self, name, purchase_price, sell_price, quantity=1, stak=False, income=1):
        self.name = name
        self.purchase_price = purchase_price
        self.sell_price = sell_price
        self.quantity = quantity
        self.stak = stak
        self.income = income

    def str(self):
        return f"{self.name}: {self.quantity} шт. (покупка: {self.purchase_price}, продажа: {self.sell_price})"

    def stak_product(self):
        if self.stak:
            self.quantity = 1





class Player:
    def __init__(self, name, initial_balance=1000, max_storage=50):
        self.name = name
        self.balance = initial_balance
        self.inventory = []  # Список объектов Product
        self.max_storage = max_storage
        self.shop = Shop(name="shop1")

    def get_total_items(self):
        """Получить общее количество товаров на складе"""
        return sum(product.quantity for product in self.inventory)

    def get_free_space(self):
        """Получить свободное место на складе"""
        return self.max_storage - self.get_total_items()

    def find_product(self, product_name):
        """Найти товар в инвентаре по имени"""
        for product in self.inventory:
            if product.name == product_name:
                return product
        return None

    def find_product_buy(self, product_name):
        """  Найти товар в МАГАЗИНЕ  """
        for product in self.shop.shop_list:
            if product.name == product_name:
                return product
        return None

    def buy(self, product_idx, quantity_to_buy):
        product_ = self.shop.shop_list[product_idx]

        if product_ is None:
            print(f"Товар не найден в ассортименте")
            return False

        ####Общая стоимость####

        total_cost = product_.purchase_price * quantity_to_buy


        ####Проверки####
        if self.balance < total_cost:
            print(f"Недостаточно средств! Нужно: {total_cost}, есть: {self.balance}")
            return False

        if self.get_free_space() < quantity_to_buy:
            print(f"Недостаточно места на складе! Нужно: {quantity_to_buy}, свободно: {self.get_free_space()}")
            return False

        if product_.quantity - quantity_to_buy < 0:
            print("В магазине нету столько товара!")
            return False

        new_product = copy.deepcopy(product_)

        self.balance -= total_cost
        """self.inventory.append(new_product)"""

        if not new_product.stak:
            self.inventory.append(new_product)
        elif not self.find_product(new_product.name) is None:
            for idx in range(len(self.inventory)):
                if self.inventory[idx].name == new_product.name:
                    self.inventory[idx].quantity += quantity_to_buy
                    break
        else:
            new_product.quantity = 1
            self.inventory.append(new_product)
            pass




        self.shop.shop_list[product_idx].quantity -= quantity_to_buy
        self.quantity_product(product_)


        print(f"Куплено {quantity_to_buy} шт. товара '{product_.name}' за {total_cost}")
        print(f"Баланс: {self.balance}, на складе: {product_.quantity} шт.")

        return True



        ##self.buy_name_prod(buy_name, product_idx, quantity_to_buy=1)

    def quantity_product(self, product):
        for product_i in self.shop.shop_list:
            if product.name == product_i.name:
                if product_i.quantity <= 0:
                    self.shop.shop_list.remove(product_i)





    """def buy_name_prod(self, product_name, product_idx, quantity_to_buy):

    
        Купить товар

        Проверки:
        1. Хватает ли денег
        2. Хватает ли места на складе
    
        product = self.find_product_buy(product_name)

        if product is None:
            print(f"Товар '{product_name}' не найден в ассортименте")
            return False

        total_cost = product.purchase_price * quantity_to_buy
        required_space = quantity_to_buy

        # Проверка наличия денег
        if self.balance < total_cost:
            print(f"Недостаточно средств! Нужно: {total_cost}, есть: {self.balance}")
            return False

        # Проверка свободного места на складе
        if self.get_free_space() < required_space:
            print(f"Недостаточно места на складе! Нужно: {required_space}, свободно: {self.get_free_space()}")
            return False



        # Совершение покупки
        if product.quantity - quantity_to_buy < 0:
            print("В магазине нету столько товара!")
            return False

        new_product = copy.deepcopy(product)

        self.balance -= total_cost
        self.inventory.append(new_product)


###################### Ошибка ##########################

        self.shop.shop_list[product_idx].quantity -= quantity_to_buy
        self.quantity_product(product)

        print(f"Куплено {quantity_to_buy} шт. товара '{product_name}' за {total_cost}")
        print(f"Баланс: {self.balance}, на складе: {product.quantity} шт.")"""




    def sell_by_product_name(self, product_name, quantity_to_sell):
        """
        Продать товар

        Проверки:
        1. Есть ли товар в инвентаре
        2. Достаточно ли товара для продажи
        """
        product = self.find_product(product_name)

        if product is None:
            print(f"Товар '{product_name}' не найден в инвентаре")
            return False

        # Проверка наличия достаточного количества товара
        if product.quantity < quantity_to_sell:
            print(f"Недостаточно товара! Есть: {product.quantity}, нужно продать: {quantity_to_sell}")
            return False

        # Проверка, что количество не отрицательное
        if quantity_to_sell <= 0:
            print("Количество для продажи должно быть положительным!")
            return False

        # Совершение продажи
        total_income = product.sell_price * quantity_to_sell
        self.balance += total_income
        product.quantity -= quantity_to_sell

        print(f"Продано {quantity_to_sell} шт. товара '{product_name}' за {total_income}")
        print(f"Баланс: {self.balance}, осталось на складе: {product.quantity} шт.")

        # Удаляем товар из инвентаря, если количество стало 0
        if product.quantity == 0:
            self.inventory.remove(product)
            print(f"Товар '{product_name}' удален из инвентаря (закончился)")

        return True

    def sell_by_product(self, product):

        self.sell_by_product_name(product.name, quantity_to_sell=1)

    def sell(self, product_idx):
        prod_name = self.inventory[product_idx].name
        self.sell_by_product_name(prod_name, quantity_to_sell=1)


    def add_product_to_market(self, product):
        """Добавить товар в ассортимент (в инвентарь)"""
        self.inventory.append(product)
        print(f"Товар '{product.name}' добавлен в ассортимент")

    def show_inventory(self):
        """Показать инвентарь игрока"""
        print(f"\n=== ИНВЕНТАРЬ ИГРОКА {self.name} ===")
        print(f"Баланс: {self.balance}")
        print(f"Склад: {self.get_total_items()}/{self.max_storage} (свободно: {self.get_free_space()})")

        if not self.inventory:
            print("Инвентарь пуст")
            return

        for i, product in enumerate(self.inventory, 1):
            print(f"{i}. {[product.name]}")
        print()

    def del_product_inventory(self, product_idx):
        self.inventory.pop(product_idx)

    def del_product_shop(self, product_idx):
        self.shop.shop_list.pop(product_idx)

class Shop:
    def __init__(self, name):
        self.name = name
        self.shop_list = [
            Product(name="Меч", purchase_price=200, sell_price=160, stak=False),
            Product(name="Апельсин", purchase_price=50, sell_price=30, quantity= 10, stak=True),
            Product(name="Лук", purchase_price=350, sell_price=270, stak=False)

        ]

    def delete_product(self, product):
        for product_a in self.shop_list:
            if product.name == product_a.name:
                self.shop_list.remove(product_a)
                return True
        return False

# Демонстрация работы программы
def main():
    # Создаем игрока
    player = Player("Алекс", initial_balance=1500, max_storage=30)

    # Создаем товары
    apple = Product("Яблоки", purchase_price=10, sell_price=15, quantity=0)
    bread = Product("Хлеб", purchase_price=20, sell_price=30, quantity=0)
    milk = Product("Молоко", purchase_price=25, sell_price=35, quantity=0)

    # Добавляем товары в ассортимент
    player.add_product_to_market(apple)
    player.add_product_to_market(bread)
    player.add_product_to_market(milk)

    # Показываем начальное состояние
    player.show_inventory()

    # Тестовые покупки
    print("=== ПОКУПКИ ===")
    player.buy("Яблоки", 5)  # Успешная покупка
    player.buy("Хлеб", 10)  # Успешная покупка
    player.buy("Молоко", 20)  # Должно не хватить места (5+10+20 = 35 > 30)

    player.show_inventory()

    # Продажи
    print("=== ПРОДАЖИ ===")
    player.sell("Яблоки", 3)  # Успешная продажа
    player.sell("Хлеб", 15)  # Должно не хватить товара (есть только 10)
    player.sell("Хлеб", 5)  # Успешная продажа

    player.show_inventory()

    # Пробуем купить снова (теперь есть место)
    print("=== ЕЩЕ ПОКУПКИ ===")
    player.buy("Молоко", 10)  # Теперь должно хватить места

    player.show_inventory()

    # Продаем весь товар
    print("=== ПРОДАЖА ВСЕГО ===")
    player.sell("Яблоки", 2)  # Продаем оставшиеся яблоки (должны удалиться)
    player.sell("Хлеб", 5)  # Продаем оставшийся хлеб (должен удалиться)
    player.sell("Молоко", 10)  # Продаем все молоко (должно удалиться)

    player.show_inventory()

