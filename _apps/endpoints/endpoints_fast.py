from datetime import datetime, timedelta

from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn

from parsers.check_vacancies_without_AI import refresh_prof_by_AI, get_vacancies_with_AI

app = FastAPI()

# Модель данных для входного запроса
class Vacancy(BaseModel):
    id: int
    title: str
    description: str

@app.post("/ai_profession")
async def ai_profession(request: Request):
    vacancies = await request.json()
    statistics, vacancy_updated = await refresh_prof_by_AI(vacancies, to_db=False)
    return {
        'vacancy_updated': vacancy_updated,
        'statistics': statistics
    }

@app.get("/get_filtered_by_ai")
async def get_filtered_by_ai(request: Request):
    session_number = request.query_params['session_number'] if request.query_params.get('session_number') else None
    date_from = request.query_params['date_from'] if request.query_params.get('date_from') else (datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d")
    date_to = request.query_params['date_to'] if request.query_params.get('date_to') else datetime.now().strftime("%Y-%m-%d")

    vacancies1 = await get_vacancies_with_AI(session_number=session_number, date_from=date_from, date_to=date_to)
    vacancies2 = await get_vacancies_with_AI(table_name='vacancies', session_number=session_number, date_from=date_from, date_to=date_to)
    vacancies3 = await get_vacancies_with_AI(table_name='archive', session_number=session_number, date_from=date_from, date_to=date_to)
    return {'amount': len(vacancies1+vacancies2+vacancies3), 'vacancies': vacancies1+vacancies2+vacancies3}


def start():
    uvicorn.run(app, host="127.0.0.1", port=5000)

if __name__ == "__main__":
    start()