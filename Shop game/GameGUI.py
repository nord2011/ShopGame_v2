from itertools import product
from tkinter import *
from tkinter.messagebox import showerror, showinfo, showwarning
from tkinter.ttk import Progressbar
from token import NEWLINE
import shop
from random import *
from json import *

global boost
boost = 1

player = shop.Player(name="Игрок", initial_balance=1000, max_storage=500)

apple = shop.Product(name="Яблоко", purchase_price=50, sell_price=30, quantity=2, stak=True)
Arbyz = shop.Product(name="Арбуз", purchase_price=100, sell_price=80, quantity=5, stak=True)
Sword = shop.Product(name="Меч Хуже", purchase_price=200, sell_price=160, stak=False)

Shop = shop.Shop(name="Магазин")

player.inventory.append(apple)
player.inventory.append(Arbyz)
player.inventory.append(Sword)

def update_balance():
    balance.config(text=f"${player.balance:.1f}")

def update_inventory():
    inventory_list.delete(0, END)


    for product in player.inventory:
        inventory_list.insert(END, f"{product.name} // Стоимость продажи: {product.sell_price} // Количество: {product.quantity} // Прибыль: {product.income}")



def update_Shop_list():
    buy_list.delete(0, END)

    for shop in player.shop.shop_list:
        buy_list.insert(END,f"{shop.name} // Стоимость покупки: {shop.purchase_price}// Стоимость продажи: {shop.sell_price} // Количество: {shop.quantity} // Прибыль: {shop.income}")



def more_button_click():
    buy_button.pack_forget()
    sell_button.pack_forget()
    exit_button.pack_forget()
    more_button.pack_forget()

    back_button.pack(side="bottom", fill="x", padx=0, pady=0)
    add_button.pack(side="bottom", fill="x", padx=0, pady=20)
    del_button.pack(side="bottom", fill="x", padx=0, pady=0)

def sell_button_click():
    del_prod = inventory_list.curselection()
    try:
        del_prod_idx = del_prod[0]
    except IndexError:
        print("Выберите товар для продажи")
        showinfo(title="Подсказка", message="Выберите товар для продажи! (нажать на товар в списке инвентаря)")
        return
    player.sell(del_prod_idx)



    update_balance()
    update_inventory()
    update_Shop_list()
    update_progress()

def buy_button_click():
    add_prod = buy_list.curselection()
    try:
        add_prod_idx = add_prod[0]
    except IndexError:
        print("Выберите товар для покупки")
        showinfo(title="Подсказка", message="Выберите товар для покупки! (нажать на товар в списке магазина)" )
        return

    player.buy(add_prod_idx, quantity_to_buy=1)

    update_balance()
    update_inventory()
    update_Shop_list()
    update_progress()



def add_button_click():
    add_window = Toplevel(window)
    add_window.title("Добавление товара (предмета)")
    add_window.geometry("430x330")
    add_window.resizable(False, False)
    add_window.configure(bg="black")

    name_var = StringVar()
    purchase_var = StringVar()
    sell_var = StringVar()
    quantity_var = StringVar()
    stackable_var = StringVar()
    income_var = StringVar()

    Label(add_window,text=f"Название: ",bg="black",fg="white").pack(pady=5,anchor="w")
    name_entry = Entry(add_window, textvariable=name_var)
    name_entry.place(x=10,y=25, width=80)



    Label(add_window, text=f"Стоимость покупки: ", bg="black", fg="white").pack(pady=15, anchor="w")
    purchase_entry = Entry(add_window, textvariable=purchase_var)
    purchase_entry.place(x=10,y=67, width=80)

    Label(add_window, text=f"Стоимость продажи: ", bg="black", fg="white").pack(pady=5, anchor="w")
    sell_entry =  Entry(add_window, textvariable=sell_var)
    sell_entry.place(x=10, y=109, width=80)

    Label(add_window, text=f"Количество: ", bg="black", fg="white").pack(pady=15, anchor="w")
    quantity_entry = Entry(add_window, textvariable=quantity_var)
    quantity_entry.place(x=10, y=151, width=80)

    Label(add_window, text=f"Стакается: ", bg="black", fg="white").pack(pady=7, anchor="w")
    stackable_entry = BooleanVar()
    stackable_entry.set(True)
    stak_checkbox = Checkbutton(
        add_window,
        variable=stackable_var,
        bg="black",
        fg="white",
        activebackground="black",
        activeforeground="white",
        selectcolor="grey")
    stak_checkbox.place(x=10, y=193, width=80)

    Label(add_window, text="Прибыль: ", bg="black", fg="white").pack(pady=15, anchor="w")
    income_entry = Entry(add_window, textvariable=income_var)
    income_entry.place(x=10,y=240, width=80)

    def add_item_click():
        name = name_var.get().strip()
        purchase = purchase_var.get().strip()
        sell = sell_var.get().strip()
        quantity = quantity_var.get().strip()
        stackable = stackable_var.get()
        income = income_var.get().strip()

        if name == "" or purchase == "" or sell == "" or quantity == "" or income == "":
            showwarning(message="Нужно всё заполнить!", title="Подсказка")
            return
        elif stackable == "":
            stackable = 1
        try:
            purchase = int(purchase)
            sell = int(sell)
            quantity = int(quantity)
            stackable = int(stackable)
            income = int(income)
        except ValueError:
            showwarning(message="`Стоимость покупки`/`Стоимость продажи`/`Количество`/`Прибыль` нужно указать в цифрах!",
                        title="Подсказка")
            return
        ##if purchase != int or sell != int or quantity != int:
            ##showwarning(message="`Стоимость покупки`/`Стоимость продажи`/`Количество` нужно указать в цифрах!", title="Подсказка")
            ##return
        if stackable == 0 and quantity > 1:
            quantity = 1
            showwarning(message="Количество этого товара не может превышать больше 1 так как не стакается", title="Подсказка")

        new_product = shop.Product(name=name, purchase_price=purchase, sell_price=sell, quantity=quantity, stak=True, income=income)
        player.shop.shop_list.append(new_product)
        update_Shop_list()
        update_progress()

        add_window.destroy()

    def cancel():
        add_window.destroy()

    save_button = Button(add_window, text="Добавить товар", bg="black", fg="white", command=add_item_click)
    save_button.pack(anchor="se", padx=10, pady=5)

    cancel_button = Button(add_window, text="Вернуться назад", bg="black", fg="white", command=cancel)
    cancel_button.pack(anchor="se", padx=10, pady=5)

def auto_income():

    total_income = 0

    for product in player.inventory:
        if product.stak:
            total_income += product.income * product.quantity
        else:
            total_income += product.income

    player.balance += total_income * boost
    update_balance()


    window.after(1000, auto_income)

def update_progress():
    global progress_value
    global boost

    total_item = 0
    target_progress_bar = 10 * boost

    for product in player.inventory:
        if product.stak:
            total_item += product.quantity
        else:
            total_item += 1

    progress_value = total_item / target_progress_bar * 100
    progress_bar["value"] = progress_value

    if progress_value >= 100:
        reset_button.pack(side="bottom", fill="x", padx=0, pady=10)
    else:
        reset_button.pack_forget()

def reset_button_click():
    global boost
    player.shop.shop_list.clear()
    for product in player.inventory:
        player.shop.shop_list.append(product)
    player.inventory.clear()
    update_inventory()

    update_Shop_list()
    player.balance = 100 * boost
    boost += 0.5 * boost
    update_balance()
    update_progress()


def del_button_click():
    ## Доделать проверки #
    if len(inventory_list.curselection()) > 0:
        player.del_product_inventory(inventory_list.curselection()[0])
    elif len(buy_list.curselection()) > 0:
        player.del_product_shop(buy_list.curselection()[0])
    else:
        showinfo(title="Подсказка", message="Выберите предмет из инвентаря или магазина!")

    update_inventory()
    update_Shop_list()

def back_button_click():
    back_button.pack_forget()
    add_button.pack_forget()
    del_button.pack_forget()

    exit_button.pack(side="bottom",fill="x", padx=0, pady=0)
    buy_button.pack(side="bottom", fill="x", padx=0, pady=20)
    sell_button.pack(side="bottom", fill="x", padx=0, pady=20)
    more_button.pack(side="bottom", fill="x", padx=0, pady=20)


window = Tk()
window.title("Game")
window.geometry("730x640")
window.configure(bg="orange")

more_button_image = PhotoImage(file="more_button.png")
buy_button_image = PhotoImage(file="buy_button.png")
sell_button_image = PhotoImage(file="sell_button.png")
exit_button_image = PhotoImage(file="exit_button.png")

right_panel = Frame(window, bg="black", width=200, bd=6)
right_panel.pack(side="right", fill="y")

balance = Label(
    right_panel,
    text=f"$0",
    bg="black",
    fg="green",
    font=("Comic Sans MS", 20, "bold"),
    bd=6
)
balance.pack(pady=8, padx=5)

exit_button = Button(right_panel,
                     text="Exit",
                     bg="black",
                     fg="white",
                     font=("Comic Sans MS", 20, "bold"),
                     bd=6,
                     command=window.quit,
                     image=exit_button_image,
                     compound="right"
                    )
exit_button.pack(side="bottom",fill="x", padx=0, pady=0)

buy_button = Button(right_panel,
                    text="Buy",
                    bg="black",
                    fg="green",
                    font=("Comic Sans MS", 20, "bold"),
                    bd=6,
                    image=buy_button_image,
                    compound="right",
                    command=buy_button_click
                    )
buy_button.pack(side="bottom", fill="x", padx=0, pady=20)

sell_button = Button(right_panel,
                     text="Sell",
                     bg="black",
                     fg="red",
                     font=("Comic Sans MS", 20, "bold"),
                     bd=6,
                     image=sell_button_image,
                    compound="right",
                     command=sell_button_click)
sell_button.pack(side="bottom", fill="x", padx=0, pady=20)


more_button = Button(right_panel,
                     text="More",
                     bg="black",
                     fg="purple",
                     font=("Comic Sans MS", 20, "bold"),
                     bd=6,
                     image=more_button_image,
                     compound="right",
                     command=more_button_click
                     )
more_button.pack(side="bottom", fill="x", padx=0, pady=20)

progress_bar = Progressbar(
    right_panel,
    orient="horizontal",
    length=150,
    mode="determinate",
)

progress_bar.pack(side="bottom", fill="x", padx=0, pady=10)

reset_button = Button(
    right_panel,
    text="Сброс",
    bg="black",
    fg="yellow",
    font=("Comic Sans MS", 14, "bold"),
    bd=6,
    command=reset_button_click,
    compound="right"
)

add_button = Button(right_panel,
                    text="Add",
                    bg="black",
                    fg="green",
                    font=("Comic Sans MS", 20, "bold"),
                    bd=6,
                    command=add_button_click)

del_button = Button(right_panel,
                    text="Del",
                    bg="black",
                    fg="red",
                    font=("Comic Sans MS", 20, "bold"),
                    bd=6,
                    command=del_button_click)

back_button = Button(right_panel,
                     text="Back",
                     bg="black",
                     fg="white",
                     font=("Comic Sans MS", 20, "bold"),
                     bd=6,
                     command=back_button_click)

main_area = Frame(window, bg="yellow")
main_area.pack(expand=True, fill="both")

bottom_area = Frame(main_area, bg="black", bd=6, height=170)
bottom_area.pack(fill="x", side="bottom")

list_frame = Frame(main_area,
                   bg="black",)
list_frame.pack(fill="x")

inventory_label = Label(list_frame,
                        text="Инвентарь",
                        bg="black",
                        fg="white",
                        font=("Comic Sans MS", 20, "bold"))
inventory_label.pack()

inventory_list = Listbox(list_frame,
                         height=5,
                         bg="black",
                         fg="white")
inventory_list.pack(fill="x")

buy_list_label = Label(bottom_area,
                       text="Купить:",
                       bg="black",
                       fg="white",
                       font=("Comic Sans MS", 20, "bold"))
buy_list_label.pack(fill="x", side="top")

buy_list = Listbox(bottom_area,
                         height=5,
                         bg="black",
                         fg="white")
buy_list.pack(fill="x", side="bottom")





update_balance()
update_inventory()
update_Shop_list()
update_progress()

auto_income()

window.mainloop()