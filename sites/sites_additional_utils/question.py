

def compose_question(question, text):
    read = "Прочитай текст вакансии и ответь"
    vacancy_text = f"Текст вакансии: '{text}'. "
    questions = {
        "Is vacancy?":
            f"Прочитай текст и ответь является ли этот текст предложением работы? "
            f"Текст: '{text}'. "
            f"Ответь да или нет.",
        "Is IT?":
            f"{read} связана ли эта вакансия с работой в сфере информационных технологий? "
            f"{vacancy_text}"
            f"Ответь да или нет.",
        "What experience?":
            f"{read} какой опыт в ней требуется? "
            f"{vacancy_text}"
            f"Ответь кратко.",
        "What level?":
            f"{read} какая квалификация IT специалиста в ней требуется? "
            f"{vacancy_text}"
            f"Answer the question in English. Answer options: junior, middle, senior, junior-middle, middle-senior",
        "What salary?":
            f"{read} какую зарплату предлагают в вакансии? "
            f"{vacancy_text}"
            f"Ответь '...' если не достаточно даннных для ответа.",
        "What contacts?":
            f"{read} есть ли в нем контактные данные работодателя или HR? "
            f"{vacancy_text}"
            f"Найди номера телефонов или email. "
            f"Если данные не найдены, ответь: 'нет данных'.",
        "What English?":
            f"{read} какой требуемый уровень знания Английского языка в не указан? "
            f"{vacancy_text}"
            f"Ответь кратко.",
        "What format?":
            f"{read} какой характер работы в ней подразумевается? "
            f"{vacancy_text}"
            f"Ответь словосочетанием из ряда: "
            f"'удаленная работа', "
            f"'полный рабочий день', "
            f"'неполный рабочий день', "
            f"'гибкий график', "
            f"'разовая работа', ",
        "What company?":
            f"{read} название компании, предлагающей эту работу? "
            f"{vacancy_text}",
        "What city?":
            f"{read} название города, в котором предлагают эту работу? "
            f"{vacancy_text}"
            f"Назови страну, город.",
    }
    prompt = questions.get(question)
    return prompt
