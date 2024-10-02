from flask import Flask, render_template, request, jsonify
from calculate import transport_forecast
import json

app = Flask(__name__)


@app.route('/')
def index():
    # отправка формы для заполнения
    return render_template('html_content.html')


@app.route('/submit', methods=['POST'])
def submit():
    # Обработка входных данных
    data = request.get_json()
    forecast_result = transport_forecast(data)
    return jsonify(forecast_result)


@app.route('/result', methods=['GET'])
def result():
    # Получаем данные из параметров запроса
    result_str = request.args.get('result')
    input_data_str = request.args.get('input_data')

    # Проверяем, что параметры не равны None
    if result_str is None or input_data_str is None:
        return "Ошибка: отсутствуют необходимые параметры запроса", 400

    # Преобразуем данные из строки JSON в объекты Python
    try:
        result = json.loads(result_str)
        input_data = json.loads(input_data_str)
    except json.JSONDecodeError:
        return "Ошибка: некорректный формат JSON", 400

    return render_template('html_result.html', result=result, input_data=input_data)


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
