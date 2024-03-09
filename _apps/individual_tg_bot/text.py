greet = "Привет, {name},  я ITCoty бот который поможет вам найти работу в IT. Нажмите 'Фильтр вакансий' и выберете желаемые параметры для подбора."
menu = "Меню фильтра вакансий"
info = "Я ITCoty бот который поможет вам найти работу в IT,\nДля прохождения опроса команда /start \n Для вывода меню фильтра вакансий команда /menu."
repeat = "Попробуем ещё раз, нажмите 'Фильтр вакансий' и выберете желаемые параметры для подбора."


get_vacancy = "Поиск вакансий по базе"

# Уведомления о вакансиях
get_notification = "Необходимо выбрать подходящую периодичность"

per_day_notification = "Дайджест за день"
on_getting_notification = "По поступлению вакансий"
cancel_notification = "Отменить получение уведомлений"
chosen_notification = "Выбранная периодичность: {notification}\nХотите изменить?"
confirm_change_notification = "Да, изменить уведомления"
cancel_change_notification = "Нет, вернуться в меню"
success_change_notification = "Уведомления успешно изменены!"
make_vacancy_filter = "Для изменение периодичности необходимо заполнить фильтр вакансий"
# Подходящие вакансии
suit_vacancies = "Подходящая новая вакансии: \n"
# Повтор запроса
new_request = "Хотите сделать новый запрос?"
reset_request = "Сделать новый запрос"
come_back = "Вернуться в главное меню"
user_current_request = "Ваш текущий запрос:\n"
# Интервалы для выбора вакансий
every_thirty_min = 30
once_per_day = 60 * 24

create_table = """CREATE TABLE tg_bot ( user_id bigint ,name varchar(255), email varchar(255),direction varchar(255), specialization varchar(255),location varchar(255),salary_rate varchar(255),work_format varchar(255),keywords varchar(255),CV_url varchar(255)) """
# Фильтр вакансий
direction = "Необходимо выбрать IT направление"
chosen_direction = "Выбранное направление: "
specialization = "Выберите специализацию для направления"
chosen_specialization = "Выбранные специализации:"

level = "Необходимо выбрать уровень владения"
chosen_level = "Выбранный уровень владения:"

location = "Интересующая локация"
chosen_location = "Выбранная локация:"

work_format = "Формат работы"
chosen_format = "Выбранный формат работы:"

add_info = "Ключевое слово:"

# Доп. кнопки
skip_continue = "Пропустить"
accept = "Сохранить и перейти к уровню"
accept_level = "Сохранить и перейти к локации"
accept_location = "Перейти к формату работы"
accept_format = "Перейти к доп. информации"
choose_button = "Выбранная кнопка"
thanks_text = "Спасибо за ответы!"
# Главное меню
vacancy_filter = "Фильтр вакансий"
start_survey = "Пройти опрос"
notification = "Периодичность уведомлений"
user_profile = "Профиль на сайте"
restart = "Прекращение выдачи"
success_restart = "Выдача была успешно удалена, хотите пройти новый запрос"

# Направления
design = "Design"
# Специализации 'Design'
motion = "Motion"
three_d = "3D"
ux_ui = "UX/UI"
illustrator = "Illustrator"
graphic = "Graphic "
designer = "Designer "

backend = "Backend"
# Специализации backend
one_c = "1C"
java = "Java"
python = "Python"
php = "PHP"
c_plus_plus = "C++"
c_sharp = "C#"
dot_net = ".Net"
golang = "Golang"

analyst = "Analyst"
# Специализации analyst
system_analyst = "System Analyst"
ba = "BA"

mobile = "Mobile"
# Специализации mobile
ios = "IOS"
android = "Android"
flutter = "Flutter"

marketing = "Marketing"
# Специализации marketing
seo = "SEO"
copywriter = "Copywriter"
marketer = "Marketer"
content_manager = "Content manager"
media_buyer = "Media buyer"

product_project_manager = "Product & Project manager"
# Специализации Product & Project manager
project_manager = "Project manager"
product_manager = "Product manager"

sales = "Sales"
# Специализации Sales

dev_ops = "DevOps"
# Специализации DevOps

frontend = "Frontend"
# Специализации Frontend
react = "React"
angular = "Angular"
vue = "Vue"

support = "Support"
# Специализации Support

fullstack = "Fullstack"
# Специализации Fullstack

hr = "HR"
# Специализации HR

game_dev = "GameDev"
# Специализации GameDev
unity = "Unity"
game_designer = "Game designer"

qa = "QA"
# Специализации QA
manual = "Manual"
auto = "Auto"

# Уровень по вакансиям
junior = "Junior"
middle = "Middle"
senior = "Senior"
tech_lead = "Lead"

# Формат работы
remote = "remote"
office = "office"
hybrid = "flexible"
any_format = "fulltime"

# Локации
russia = "Россия"
belarus = "Беларусь"
europe = "Европа"
other_location = "Другое"
