import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('info.db')
cursor = connection.cursor()

# Выбираем всех пользователей
cursor.execute('SELECT * FROM telegram_channels')
users = cursor.fetchall()

# Выводим результаты
for user in users:
  print(user)

# Выбираем всех пользователей
cursor.execute('SELECT * FROM key_words')
users = cursor.fetchall()

# Выводим результаты
for user in users:
  print(user[1])
# Закрываем соединение
connection.close()