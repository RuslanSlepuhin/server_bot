import datetime
from datetime import timedelta

from _apps.individual_tg_bot.settings import APP_DEBUG, APP_HOST, APP_PORT
from _apps.individual_tg_bot.text import once_per_day
from flask import Flask, jsonify, request

from service import db

app = Flask(__name__)


@app.route("/user_requests_vacancies", methods=["GET"])
def get_user_requests_vacancies():
    if request.args is not None:
        query_string = list(request.args.keys())[0]
        query_params = query_string.split("&")
        params_dict = {}
        for param in query_params:
            key, value = param.split("=")
            params_dict[key] = value

        selected_direction = params_dict.get("selected_direction")
        selected_specializations = params_dict.get("selected_specializations")[2:-2]
        selected_level = params_dict.get("selected_level")[2:-2]
        selected_location = params_dict.get("selected_location")[2:-2]
        selected_work_format = params_dict.get("selected_work_format")[2:-2]
        keyword = params_dict.get("keyword")
        vacancies = db.receive_vacancy(
            direction=selected_direction,
            specialization=selected_specializations,
            level=selected_level,
            location=selected_location,
            work_format=selected_work_format,
            keyword=keyword,
        )

        return jsonify(vacancies)


@app.route("/user_digest", methods=["GET"])
def get_user_digest():
    if request.args is not None:
        selected_direction = request.args.get("direction")
        selected_specializations = request.args.get("specialization")
        selected_level = request.args.get("level")
        selected_location = request.args.get("location")
        selected_work_format = request.args.get("work_format")
        keyword = request.args.get("keywords")
        interval = datetime.datetime.now() - timedelta(minutes=once_per_day)
        vacancies = db.get_periodical_task_vacancies(
            direction=selected_direction,
            specialization=selected_specializations,
            level=selected_level,
            location=selected_location,
            work_format=selected_work_format,
            keyword=keyword,
            interval=interval,
        )
        return jsonify(vacancies)


if __name__ == "__main__":
    app.run(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)
