# sql-injections

Practical examples of SQL injections.

Есть веб-сервис с двумя точками входа:
* GET / - возвращает secret-токен пользователя по его логину и паролю;  
* GET /users - возвращает список всех пользователей, если передан secret-токен администратора.

Требуется узнать secret-токен пользователя admin и, используя его, узнать данные для входа в остальные аккаунты и поменять везде пароль на "password". Ван дан только рядовой пользователь с данными аккаунта: *user1*, *password*.

В качестве ответа необходимо предоставить изменненную базу данных и код на Python, который отправляет нужную последовательность запросов к базе.
