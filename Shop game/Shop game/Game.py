

player = {
    "name": "NP",
    "level": 1,
    "experience": 0,
    "health": 40,
    "max_health": 100,
    "damage": 10,
    "defense": 0,
    "experience_for_new_level": 100,

}

def add_experience(the_player, experience_up):
    the_player["experience"] += experience_up
    level_up = False

    if experience_up >= the_player["experience_for_new_level"]:
        level_up = True

    while the_player["experience"] >= the_player["experience_for_new_level"]:
        the_player["level"] += 1
        the_player["max_health"] += 5
        the_player["health"] += 5
        the_player["experience"] -= the_player["experience_for_new_level"]
        the_player["experience_for_new_level"] += 20
        print(f"Уровень повышен! Теперь твой уровень {the_player["level"]} ")

    return level_up

def show_player_stats(the_player):
    print("*" * 20)
    print(f"Имя игрока: {the_player["name"]}")
    print(f"Уровень: {the_player["level"]}")
    #print(f"Опыт: {player["experience"]}/{player["experience_for_new_level"]}")
    print(get_exp_progress(the_player))
    print(f"Здоровья: {the_player["health"]}/{the_player["max_health"]}")
    print(f"Урон: {the_player["damage"]}")
    print(f"Защита: {the_player["defense"]}")
    print("*" * 20)


def heal_player(the_player, heal_amount):
    if heal_amount + the_player["health"] >= the_player["max_health"]:


        heal = the_player["max_health"] - the_player["health"]
        if heal == 0:
            print(f"У игрока {the_player['name']} уже максимальное здоровье! ({the_player['health']}/{the_player["max_health"]})")
            return heal

        the_player["health"] = the_player["max_health"]

        print(
            f"Успешно исцелено {heal}! Теперь у игрока `{the_player["name"]}` {the_player["health"]}/{the_player["max_health"]} ")
        return heal


    else:
        the_player["health"] += heal_amount
        print(f"Успешно исцелено {heal_amount}! Теперь у игрока `{the_player["name"]}` {the_player["health"]}/{the_player["max_health"]} ")
        return heal_amount

def get_exp_progress(the_player):
    percentage = (the_player["experience"] / the_player["experience_for_new_level"]) * 100
    bar_length = 10
    filled_length = int(bar_length * percentage / 100)
    empty_length = bar_length - filled_length

    progress_bar = "[" + "=" * filled_length + " " * empty_length + "]"
    progress_string = f"{progress_bar}| {the_player['experience']}/{the_player['experience_for_new_level']} ({percentage:.1f}%)"

    return progress_string


def collect_resources(*resources):
    resources_list = list(resources)
    total_resources = len(resources_list)
    return {
        "total_resources": total_resources,
        "resources_list": resources_list,
        "message": f"Собрано {total_resources} ресурсов"
    }
def create_spell(**spell):

    pass
""""name": "NP",
    "level": 1,
    "experience": 0,
    "health": 40,
    "max_health": 100,
    "damage": 10,
    "defense": 0,
    "experience_for_new_level": 100,"""

def save_game_txt(player_save):
    with open("../Save_player.txt", "w", encoding="utf-8") as file:
        file.write(f"{player_save["name"]}\n")
        file.write(f"{player_save["level"]}\n")
        file.write(f"{player_save["experience"]}\n")
        file.write(f"{player_save["health"]}\n")
        file.write(f"{player_save["max_health"]}\n")
        file.write(f"{player_save["damage"]}\n")
        file.write(f"{player_save["defense"]}\n")
        file.write(f"{player_save["experience_for_new_level"]}\n")

    print("Успешно сохранено!")


def load_game_txt(file_name = "Save_player.txt"):
    with open(file_name, "r", encoding="utf-8") as file:
        lines = file.readlines()

    lines = [line.strip() for line in lines]
    player = {
        "name": lines[0],
        "level": int(lines[1]),
        "experience": int(lines[2]),
        "health": int(lines[3]),
        "max_health": int(lines[4]),
        "damage": int(lines[5]),
        "defense": int(lines[6]),
        "experience_for_new_level": int(lines[7]),
    }
    print("Успешно загружено!")
    return player

exit = False

while exit != True:
    print("*" * 20)
    print("1. Выход")
    print("2. Сохранить игрока")
    print("3. Загрузить игрока")
    print("4. Прибавить опыт")
    print("5. Посмотреть статистику")
    print("6. Исцелить игрока")
    print("7. ")
    print("*" * 20)
    choice = int(input("Выбрать действие: "))

    match choice:
        case 1:
            exit = True
        case 2:
            save_game_txt(player)
        case 3:
            player = load_game_txt("../Save_player.txt")

        case 4:
            add_exp = int(input("Насколько увеличить опыт: "))
            add_experience(player, add_exp)
        case 5:
            show_player_stats(player)
        case 6:
            add_heal = int(input("На сколько прибавить здоровье: "))
            heal_player(player, add_heal)
        ##case 7:


print("Конец программы")


