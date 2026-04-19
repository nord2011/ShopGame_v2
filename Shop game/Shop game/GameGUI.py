import tkinter
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo, showwarning
from tkinter.ttk import Progressbar
import shop
from PIL import Image, ImageTk
import os
import sys

# ================= ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ =================
global boost
boost = 1
progress_value = 0

player = shop.Player(name="Игрок", initial_balance=100, max_storage=500)
Shop = shop.Shop(name="Магазин")

# Переменные для работы с новым UI (карточки товаров)
selected_inv_index = None
selected_shop_index = None
inv_frames = []
shop_frames = []
inv_canvas = None
shop_canvas = None


# ================= ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =================
def get_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

def create_scroll_container(parent, height=120):
    """Создаёт область с прокруткой для карточек товаров"""
    global inv_canvas, shop_canvas
    canvas = Canvas(parent, bg="black", height=height, highlightthickness=0)
    scrollbar = Scrollbar(parent, orient="vertical", command=canvas.yview)
    scroll_frame = Frame(canvas, bg="black")

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    return scroll_frame, canvas


def update_balance():
    balance.config(text=f"${player.balance:.1f}")


def update_inventory():
    """Перерисовывает список инвентаря с картинками"""
    global selected_inv_index, inv_frames
    for f in inv_frames: f.destroy()
    inv_frames.clear()
    selected_inv_index = None

    for i, product in enumerate(player.inventory):
        frm = Frame(inv_scroll_frame, bg="#222", highlightbackground="#555", highlightthickness=1)
        frm.pack(fill="x", pady=2, padx=5)

        # Путь к картинке: img_яблоко.png, img_меч_хуже.png и т.д.
        img_path = product.image_path
        print(img_path)
        try:
            orig_img = Image.open(img_path)
            resize_img = orig_img.resize((32, 32))
            img = ImageTk.PhotoImage(resize_img)
            img_lbl = Label(frm, image=img, bg="#222")
            img_lbl.image = img  # ВАЖНО: сохраняем ссылку, иначе сборщик мусора удалит картинку
            img_lbl.pack(side="left", padx=5)
        except Exception:
            # Заглушка, если файла картинки нет
            Label(frm, text="📦", font=24, bg="#222").pack(side="left", padx=5)

        txt = f"{product.name} | Прод.: {product.sell_price} | Кол-во: {product.quantity} | Прибыль: {product.income}"
        lbl = Label(frm, text=txt, bg="#222", fg="white", font=("Comic Sans MS", 10), wraplength=500, justify="left")
        lbl.pack(side="left", fill="x", expand=True)

        # Привязка клика к карточке и тексту
        frm.bind("<Button-1>", lambda e, idx=i: select_inv(idx))
        lbl.bind("<Button-1>", lambda e, idx=i: select_inv(idx))
        inv_frames.append(frm)

    if inv_canvas: inv_canvas.update_idletasks()


def update_Shop_list():
    """Перерисовывает список магазина с картинками"""
    global selected_shop_index, shop_frames
    for f in shop_frames: f.destroy()
    shop_frames.clear()
    selected_shop_index = None

    for i, product in enumerate(player.shop.shop_list):
        frm = Frame(shop_scroll_frame, bg="#222", highlightbackground="#555", highlightthickness=1)
        frm.pack(fill="x", pady=2, padx=5)

        img_name = product.name.lower().replace(" ", "_")
        img_path = product.image_path
        print(img_path)
        print(f"Файл существует? {os.path.exists(img_path)}")

        try:
            orig_img = Image.open(img_path)
            resize_img = orig_img.resize((32,32))
            img = ImageTk.PhotoImage(resize_img)
            ##img = PhotoImage(file=img_path)
            img_lbl = Label(frm, image=img, bg="#222")
            img_lbl.image = img
            img_lbl.pack(side="left", padx=5)
        except Exception as e:
            print(f"Ошибка загрузки {img_path}:{e}")
            Label(frm, text="🛒", font=24, bg="#222").pack(side="left", padx=5)

        txt = f"{product.name} | Покупка: {product.purchase_price} | Прод.: {product.sell_price} | Кол-во: {product.quantity} | Прибыль: {product.income}"
        lbl = Label(frm, text=txt, bg="#222", fg="white", font=("Comic Sans MS", 10), wraplength=500, justify="left")
        lbl.pack(side="left", fill="x", expand=True)

        frm.bind("<Button-1>", lambda e, idx=i: select_shop(idx))
        lbl.bind("<Button-1>", lambda e, idx=i: select_shop(idx))
        shop_frames.append(frm)

    if shop_canvas: shop_canvas.update_idletasks()


# ================= ЛОГИКА ВЫБОРА И КНОПОК =================
def select_inv(idx):
    global selected_inv_index, selected_shop_index
    selected_inv_index = idx
    selected_shop_index = None
    # Подсветка выбранного
    for i, frm in enumerate(inv_frames):
        frm.config(highlightbackground="yellow" if i == idx else "#555", highlightthickness=3 if i == idx else 1)
    for frm in shop_frames:
        frm.config(highlightbackground="#555", highlightthickness=1)


def select_shop(idx):
    global selected_shop_index, selected_inv_index
    selected_shop_index = idx
    selected_inv_index = None
    for i, frm in enumerate(shop_frames):
        frm.config(highlightbackground="cyan" if i == idx else "#555", highlightthickness=3 if i == idx else 1)
    for frm in inv_frames:
        frm.config(highlightbackground="#555", highlightthickness=1)


def sell_button_click():
    if selected_inv_index is None:
        showinfo("Подсказка", "Выберите товар в инвентаре!")
        return
    player.sell(selected_inv_index)
    update_balance()
    update_inventory()
    update_Shop_list()
    update_progress()


def buy_button_click():
    if selected_shop_index is None:
        showinfo("Подсказка", "Выберите товар в магазине!")
        return
    player.buy(selected_shop_index, quantity_to_buy=1)
    update_balance()
    update_inventory()
    update_Shop_list()
    update_progress()


def del_button_click():
    if selected_inv_index is not None:
        player.del_product_inventory(selected_inv_index)
        update_inventory()
    elif selected_shop_index is not None:
        player.del_product_shop(selected_shop_index)
        update_Shop_list()
    else:
        showinfo(title="Подсказка", message="Выберите предмет из инвентаря или магазина!")
    update_progress()


def more_button_click():
    buy_button.pack_forget()
    sell_button.pack_forget()
    exit_button.pack_forget()
    more_button.pack_forget()
    progress_bar.pack_forget()
    back_button.pack(side="bottom", fill="x", padx=0, pady=0)
    add_button.pack(side="bottom", fill="x", padx=0, pady=20)
    del_button.pack(side="bottom", fill="x", padx=0, pady=0)


def back_button_click():
    back_button.pack_forget()
    add_button.pack_forget()
    del_button.pack_forget()
    exit_button.pack(side="bottom", fill="x", padx=0, pady=0)
    buy_button.pack(side="bottom", fill="x", padx=0, pady=20)
    sell_button.pack(side="bottom", fill="x", padx=0, pady=20)
    more_button.pack(side="bottom", fill="x", padx=0, pady=20)
    progress_bar.pack(side="bottom", fill="x", padx=0, pady=10)




def add_button_click():
    add_window = Toplevel(window)
    add_window.title("Добавление товара")
    add_window.geometry("430x460")
    add_window.resizable(False, False)
    add_window.configure(bg="black")

    name_var = StringVar()
    purchase_var = StringVar()
    sell_var = StringVar()
    quantity_var = StringVar()
    stackable_var = BooleanVar(value=True)
    income_var = StringVar()
    image_var = StringVar()

    def image_selector():
        file_name = askopenfilename(
            title="Выберите картинку",
            filetypes=[("PNG Images", "*.png"), ("All Files", "*.*")],
            initialdir="/SG Picture"
        )
        if file_name:
            image_var.set(file_name)
            img_label.config(text=os.path.basename(file_name), fg="lime")



    # Простая и надёжная вёрстка через pack
    Label(add_window, text="Название:", bg="black", fg="white").pack(pady=(10, 0), anchor="w", padx=10)
    Entry(add_window, textvariable=name_var).pack(fill="x", padx=10)

    Label(add_window, text="Стоимость покупки:", bg="black", fg="white").pack(pady=(10, 0), anchor="w", padx=10)
    Entry(add_window, textvariable=purchase_var).pack(fill="x", padx=10)

    Label(add_window, text="Стоимость продажи:", bg="black", fg="white").pack(pady=(10, 0), anchor="w", padx=10)
    Entry(add_window, textvariable=sell_var).pack(fill="x", padx=10)

    Label(add_window, text="Количество:", bg="black", fg="white").pack(pady=(10, 0), anchor="w", padx=10)
    Entry(add_window, textvariable=quantity_var).pack(fill="x", padx=10)

    Label(add_window, text="Стакается:", bg="black", fg="white").pack(pady=(10, 0), anchor="w", padx=10)
    Checkbutton(add_window, variable=stackable_var, bg="black", fg="white", selectcolor="grey").pack(anchor="w",
                                                                                                     padx=10)

    Label(add_window, text="Прибыль:", bg="black", fg="white").pack(pady=(10, 0), anchor="w", padx=10)
    Entry(add_window, textvariable=income_var).pack(fill="x", padx=10)

    Button(add_window, text="Добавить картинку", bg="black", fg="white", command=image_selector).pack(pady=(10, 0), anchor="w", padx=10)
    img_label = Label(add_window, textvariable=image_var)
    img_label.pack(pady=(10, 0), anchor="w", padx=10)

    def add_item_click():
        name = name_var.get().strip()
        purchase = purchase_var.get().strip()
        sell = sell_var.get().strip()
        quantity = quantity_var.get().strip()
        stackable = stackable_var.get()
        income = income_var.get().strip()
        image_path = image_var.get().strip()

        if not name or not purchase or not sell or not quantity or not income:
            showwarning(message="Нужно заполнить все поля!", title="Подсказка")
            return
        try:
            purchase = int(purchase)
            sell = int(sell)
            quantity = int(quantity)
            income = int(income)
        except ValueError:
            showwarning(message="Числовые поля должны содержать только цифры!", title="Подсказка")
            return

        if not stackable and quantity > 1:
            quantity = 1
            showwarning(message="Нестакающиеся товары могут быть только в количестве 1", title="Подсказка")

        new_product = shop.Product(name=name, purchase_price=purchase, sell_price=sell,
                                   quantity=quantity, stak=stackable, income=income, image_path=image_path)
        player.shop.shop_list.append(new_product)
        update_Shop_list()
        update_progress()
        add_window.destroy()

    Button(add_window, text="Добавить товар", bg="black", fg="white", command=add_item_click).pack(anchor="se", padx=10,
                                                                                                   pady=10)
    Button(add_window, text="Отмена", bg="black", fg="white", command=add_window.destroy).pack(anchor="se", padx=10,
                                                                                               pady=5)


# ================= АВТО-ДОХОД И ПРОГРЕСС =================
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
    global progress_value, boost
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
    shop_inv = player.shop.shop_list.copy()
    player.shop.shop_list.clear()
    a = [p.name for p in shop_inv]

    for product in player.inventory:
        player.shop.shop_list.append(product)

    # Безопасное объединение количеств
    for orig in shop_inv:
        found = False
        for cur in player.shop.shop_list:
            if cur.name == orig.name:
                cur.quantity += orig.quantity
                found = True
                break
        if not found:
            player.shop.shop_list.append(orig)

    player.inventory.clear()
    update_inventory()
    update_Shop_list()
    player.balance = 100 * boost
    boost += 0.5 * boost
    update_balance()
    update_progress()


# ================= ИНИЦИАЛИЗАЦИЯ ОКНА =================
window = Tk()
window.title("Game")
window.geometry("730x640")
window.configure(bg="orange")

# Загрузка картинок кнопок (с проверкой на наличие файлов)
try:
    more_button_image = PhotoImage(file=get_path("more_button.png"))
    buy_button_image = PhotoImage(file=get_path("buy_button.png"))
    sell_button_image = PhotoImage(file=get_path("sell_button.png"))
    exit_button_image = PhotoImage(file=get_path("exit_button.png"))
except Exception as e:
    print(f"⚠️ Не удалось загрузить картинки кнопок: {e}")

right_panel = Frame(window, bg="black", width=200, bd=6)
right_panel.pack(side="right", fill="y")

balance = Label(right_panel, text="$0", bg="black", fg="green", font=("Comic Sans MS", 20, "bold"), bd=6)
balance.pack(pady=8, padx=5)

# Кнопки с картинками
exit_button = Button(right_panel, text="Exit", bg="black", fg="white", font=("Comic Sans MS", 20, "bold"), bd=6,
                     command=window.quit, compound="right")
try:
    exit_button.config(image=exit_button_image)
except:
    pass
exit_button.pack(side="bottom", fill="x", padx=0, pady=0)

buy_button = Button(right_panel, text="Buy", bg="black", fg="green", font=("Comic Sans MS", 20, "bold"), bd=6,
                    compound="right", command=buy_button_click)
try:
    buy_button.config(image=buy_button_image)
except:
    pass
buy_button.pack(side="bottom", fill="x", padx=0, pady=20)

sell_button = Button(right_panel, text="Sell", bg="black", fg="red", font=("Comic Sans MS", 20, "bold"), bd=6,
                     compound="right", command=sell_button_click)
try:
    sell_button.config(image=sell_button_image)
except:
    pass
sell_button.pack(side="bottom", fill="x", padx=0, pady=20)

more_button = Button(right_panel, text="More", bg="black", fg="purple", font=("Comic Sans MS", 20, "bold"), bd=6,
                     compound="right", command=more_button_click)
try:
    more_button.config(image=more_button_image)
except:
    pass
more_button.pack(side="bottom", fill="x", padx=0, pady=20)

progress_bar = Progressbar(right_panel, orient="horizontal", length=150, mode="determinate")
progress_bar.pack(side="bottom", fill="x", padx=0, pady=10)

reset_button = Button(right_panel, text="Сброс", bg="black", fg="yellow", font=("Comic Sans MS", 14, "bold"), bd=6,
                      command=reset_button_click, compound="right")
add_button = Button(right_panel, text="Add", bg="black", fg="green", font=("Comic Sans MS", 20, "bold"), bd=6,
                    command=add_button_click)
del_button = Button(right_panel, text="Del", bg="black", fg="red", font=("Comic Sans MS", 20, "bold"), bd=6,
                    command=del_button_click)
back_button = Button(right_panel, text="Back", bg="black", fg="white", font=("Comic Sans MS", 20, "bold"), bd=6,
                     command=back_button_click)

main_area = Frame(window, bg="yellow")
main_area.pack(expand=True, fill="both")

bottom_area = Frame(main_area, bg="black", bd=6, height=170)
bottom_area.pack(fill="x", side="bottom")

list_frame = Frame(main_area, bg="black")
list_frame.pack(fill="x")

inventory_label = Label(list_frame, text="Инвентарь", bg="black", fg="white", font=("Comic Sans MS", 20, "bold"))
inventory_label.pack()
# ЗАМЕНА Listbox на прокручиваемый контейнер
inv_scroll_frame, inv_canvas = create_scroll_container(list_frame, height=120)

buy_list_label = Label(bottom_area, text="Купить:", bg="black", fg="white", font=("Comic Sans MS", 20, "bold"))
buy_list_label.pack(fill="x", side="top")
# ЗАМЕНА Listbox на прокручиваемый контейнер
shop_scroll_frame, shop_canvas = create_scroll_container(bottom_area, height=120)

# Инициализация
update_balance()
update_inventory()
update_Shop_list()
update_progress()
auto_income()
window.mainloop()