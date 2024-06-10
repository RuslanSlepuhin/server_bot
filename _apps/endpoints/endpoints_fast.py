from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn

from parsers.check_vacancies_without_AI import refresh_prof_by_AI

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
def start():
    uvicorn.run(app, host="127.0.0.1", port=5000)

if __name__ == "__main__":
    start()