import sqlite3

conn = sqlite3.connect('bank.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY,
        full_name TEXT,
        phone_number TEXT,
        balance REAL DEFAULT 0
    )
''')

conn.commit()

def register_client():
    full_name = input("Введите ФИО клиента: ")
    phone_number = input("Введите номер телефона клиента: ")

    cursor.execute('INSERT INTO clients (full_name, phone_number) VALUES (?, ?)', (full_name, phone_number))
    conn.commit()
    print("Клиент успешно зарегистрирован.")

def search_clients_by_name(full_name):
    cursor.execute('SELECT * FROM clients WHERE full_name LIKE ?', ('%' + full_name + '%',))
    return cursor.fetchall()

def search_clients_by_phone(phone_number):
    cursor.execute('SELECT * FROM clients WHERE phone_number = ?', (phone_number,))
    return cursor.fetchall()

def deposit(client_id, amount):
    cursor.execute('UPDATE clients SET balance = balance + ? WHERE id = ?', (amount, client_id))
    conn.commit()
    print("Баланс успешно пополнен.")

def withdraw(client_id, amount):
    cursor.execute('UPDATE clients SET balance = balance - ? WHERE id = ?', (amount, client_id))
    conn.commit()
    print("Деньги успешно сняты.")

def view_balance(client_id):
    cursor.execute('SELECT balance FROM clients WHERE id = ?', (client_id,))
    result = cursor.fetchone()
    if result:
        print("Баланс:", result[0])
    else:
        print("Клиент не найден.")

def calculate_deposit(client_id, months):
    annual_interest_rate = 0.05
    monthly_interest_rate = annual_interest_rate / 12
    initial_balance = view_balance(client_id)

    if initial_balance is None:
        print("Клиент не найден.")
        return

    future_balance = initial_balance * (1 + monthly_interest_rate)**months
    print("Баланс через", months, "месяцев:", future_balance)

while True:
    print("\nВыберите действие:")
    print("1. Регистрация нового клиента")
    print("2. Поиск клиента по ФИО")
    print("3. Поиск клиента по номеру телефона")
    print("4. Пополнение баланса")
    print("5. Снятие денег с баланса")
    print("6. Просмотр баланса")
    print("7. Подсчет вклада на 12-24-36 месяцев")
    print("8. Выйти из программы")

    choice = input("Введите номер действия: ")

    if choice == '1':
        register_client()
    elif choice == '2':
        full_name = input("Введите ФИО для поиска: ")
        clients = search_clients_by_name(full_name)
        print("Результаты поиска:")
        for client in clients:
            print(client)
    elif choice == '3':
        phone_number = input("Введите номер телефона для поиска: ")
        clients = search_clients_by_phone(phone_number)
        print("Результаты поиска:")
        for client in clients:
            print(client)
    elif choice == '4':
        client_id = int(input("Введите ID клиента: "))
        amount = float(input("Введите сумму для пополнения: "))
        deposit(client_id, amount)
    elif choice == '5':
        client_id = int(input("Введите ID клиента: "))
        amount = float(input("Введите сумму для снятия: "))
        withdraw(client_id, amount)
    elif choice == '6':
        client_id = int(input("Введите ID клиента: "))
        view_balance(client_id)
    elif choice == '7':
        client_id = int(input("Введите ID клиента: "))
        months = int(input("Введите количество месяцев для расчета: "))
        calculate_deposit(client_id, months)
    elif choice == '8':
        break
    else:
        print("Неверный выбор. Попробуйте снова.")

conn.close()




