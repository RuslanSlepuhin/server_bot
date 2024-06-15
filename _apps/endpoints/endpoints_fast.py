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
    vacancies1 = await get_vacancies_with_AI(session_number=session_number)
    vacancies2 = await get_vacancies_with_AI(table_name='vacancies', session_number=session_number)
    return {'vacancies': vacancies1 + vacancies2}


def start():
    uvicorn.run(app, host="127.0.0.1", port=5000)

if __name__ == "__main__":
    start()