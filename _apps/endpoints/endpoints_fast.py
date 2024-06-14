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
    statistics, vacancy_updated = await refresh_prof_by_AI(vacancies)
    return {
        'vacancy_updated': vacancy_updated,
        'statistics': statistics
    }

@app.get("/get_filtered_by_ai")
async def get_filtered_by_ai():
    vacancies1 = await get_vacancies_with_AI()
    vacancies2 = await get_vacancies_with_AI(table_name='vacancies')
    return {'vacancies': vacancies1 + vacancies2}


def start():
    uvicorn.run(app, host="127.0.0.1", port=5000)

if __name__ == "__main__":
    start()