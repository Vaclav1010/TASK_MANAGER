import json
from datetime import datetime, timedelta, date

# Soubor pro ukládání úkolů
FILE_NAME = "ukoly.json"
DNESNI_DATUM = date.today().strftime("%d/%m/%Y")
FORMAT = "%d/%m/%Y"
CENTER = 70
SEPARATOR = CENTER * "="

# Konstanty pro klíče slovníků
KEY_NAZEV = "NAZEV"
KEY_STAV = "STAV"
KEY_DATUM_PRIDANI = "DATUM_PRIDANI"
KEY_DEADLINE = "DEADLINE"
KEY_POPIS = "POPIS"

# Stav úkolů
STAV_NENI_HOTOVO = "neni hotovo"
STAV_HOTOVO = "hotovo"


# Nacteni ukolu
def load_tasks():  # Načtení úkolů ze souboru
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


ukoly = load_tasks()


def save_tasks(tasks):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)
    print("Úkoly byly uloženy.")


def greet():
    print(SEPARATOR)
    print("WELCOME IN TASK MANAGER".center(CENTER))
    print(SEPARATOR)
    print(f"Nejblizsi 3 deadliny jsou:".center(CENTER).upper())
    print(zobraz_nejblizsi_deadline())
    print(
        "\n1| Nový úkol\n2| Označit jako hotový\n3| Zobrazit úkoly\n4| Ukončit program\n"
    )


def format_task(prvek):
    return (
        f">>> |{prvek[KEY_NAZEV]:<22} |DEADLINE: {prvek[KEY_DEADLINE]:<10} - "
        f"STAV: {prvek[KEY_STAV].upper():<10}"
    )


def get_valid_date(prompt):
    while True:
        try:
            date_str = input(prompt)
            return datetime.strptime(date_str, FORMAT).strftime(FORMAT)
        except ValueError:
            print("Neplatný formát data. Zadejte datum ve formátu DD/MM/YYYY.")


def zobraz_nejblizsi_deadline():
    today = datetime.today()
    threshold = today + timedelta(days=3)

    close_deadlines = [
        (datetime.strptime(prvek[KEY_DEADLINE], FORMAT), format_task(prvek))
        for prvek in ukoly
        if datetime.strptime(prvek[KEY_DEADLINE], FORMAT) <= threshold
    ]

    if not close_deadlines:
        print("Žádné blízké deadliny nebyly nalezeny.")
    else:
        for _, line in sorted(close_deadlines):
            print(line)


def new_task():
    task_name = input("Zadej název úkolu: ")
    popis = input("Zadej popis tasku: ")
    deadline = get_valid_date("Zadejte deadline (ve formátu DD/MM/YYYY): ")

    ukoly.append(
        {
            KEY_NAZEV: task_name,
            KEY_STAV: "neni hotovo",
            KEY_DATUM_PRIDANI: DNESNI_DATUM,
            KEY_DEADLINE: deadline,
            KEY_POPIS: popis,
        }
    )

    print(f"Úkol '{task_name}' byl přidán do seznamu.")


def display_tasks():
    if not ukoly:
        print("Seznam úkolů je prázdný.")
        return

    print(SEPARATOR)
    print("SEZNAM TASKU:".center(CENTER))
    print(SEPARATOR)
    for prvek in ukoly:
        print(format_task(prvek))
        print(SEPARATOR)


def marked_as_done():
    display_tasks()
    found = False
    donne = input("Napiš úkol, který chceš označit jako hotový: ")

    for prvek in ukoly:
        if prvek.get(KEY_NAZEV) == donne:
            prvek.update({KEY_STAV: STAV_HOTOVO})
            print(f"Task'{prvek.get(KEY_NAZEV)}' byl oznacen jako hotovy")
            found = True
            break

    if not found:
        print(f"Task '{donne}' nebyl nalezen v seznamu.")


def exit_program():
    save_tasks(ukoly)
    print("Na shledanou!")


# Hlavní programová smyčka
def main():
    greet()

    while True:
        choice = input("Zvol akci: ")

        if choice == "1":
            new_task()
        elif choice == "2":
            marked_as_done()
        elif choice == "3":
            display_tasks()
        elif choice == "4":
            exit_program()
            break
        else:
            print("Neplatná volba, zkus to znovu.")


main()
