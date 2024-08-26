<h2> Проект REST API интерфейса для добавления заметок </h2>
  <ul>
    <h3>Стек:</h3>
    <li>
      <h4>Бэкенд - FastAPI</h4>
    </li>
    <li>
      <h4>База данных - PostgeSQL</h4>
    </li>
  </ul>
  <h3>Описание проекта:</h3>
  <p>
    Проект предоставляет возможность добавлять и получать список всех созданных заметок. 
    При добавлении заметок происходит валидация орфографических ошибок при помощи сервиса Яндекс.Спеллер.
    Интерфейс поддерживает авторизацию и регистрацию пользователей; доступ к созданнию и получению заметок может только зарегистрирвоанный пользователь.
    Для аутентификации используются куки и JWT-токен.
  </p>
<h3>Запуск на Windows</h3>
<p>Для работы потребуется запущеный Docker Desktop deamon</p>
<code>git clone https://github.com/ElKaloria/Note_project.git
docker-compose -d up --build (для первого запуска)
docker-compose -d up (для последующих)
</code>
<h3>Шаблоны curl запросов для удобного тестирования API:</h3>
<h4>Создание пользователя:</h4>
<code>curl -X 'POST' \
  'http://localhost:8000/auth/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "example@mail.ru",
  "password": "test_pass",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false,
  "username": "test_user"
}'
</code>
<h4>Логин</h4>
<code>curl -X 'POST' \
  'http://localhost:8000/auth/jwt/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=example%40mail.ru&password=string&scope=&client_id=string&client_secret=string'
</code>
<h4>Логаут</h4>
<code>curl -X 'POST' \
  'http://localhost:8000/auth/jwt/logout' \
  -H 'accept: application/json' \
  -d ''
</code>
<h4>Получение списка заметок пользователя</h4>
<code>curl -X 'GET' \
  'http://localhost:8000/notes/?page=1&limit=10' \
  -H 'accept: application/json'
</code>

<h4>Получение заметки по id</h4>
<code>curl -X 'GET' \
  'http://localhost:8000/notes/{note_by_id}?post_id=3' \
  -H 'accept: application/json'
</code>
<h4>Создание заметки</h4>
<code>curl -X 'POST' \
  'http://localhost:8000/notes/create_note' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Your title",
  "text": "Your text"
}'
</code>
<h2>С подробной документацией можно ознакомиться по ссылке http://localhost:8000/docs</h2>
