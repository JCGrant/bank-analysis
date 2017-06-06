import csv
import datetime
from collections import OrderedDict
from flask import Flask, render_template, jsonify

DIFFERENCE_COLUMN_NAME = 'Amount'
DATE_COLUMN_NAME = 'Date'
DATE_FORMAT = '%d/%m/%Y'


def dates(start, end, delta=datetime.timedelta(days=1)):
    date = start
    while date <= end:
        yield date
        date += delta

def parse_file(file_name, start_amount=0.0):
    with open(file_name) as f:
        csv_data = list(csv.DictReader(f))

    start_date = datetime.datetime.strptime(csv_data[-1][DATE_COLUMN_NAME], DATE_FORMAT)
    end_date = datetime.datetime.strptime(csv_data[0][DATE_COLUMN_NAME], DATE_FORMAT)

    differences = {}
    for row in csv_data:
        date = datetime.datetime.strptime(row[DATE_COLUMN_NAME], DATE_FORMAT)
        difference = float(row[DIFFERENCE_COLUMN_NAME])
        millis = int(date.timestamp() * 1000)
        try:
            differences[millis] += difference
        except KeyError:
            differences[millis] = difference

    data = []
    amount = start_amount
    for date in dates(start_date, end_date):
        millis = int(date.timestamp() * 1000)
        amount += differences.get(millis, 0)
        data.append({
            'x': millis,
            'y': amount
        })

    return data


app = Flask(__name__)

app.data = []

@app.route('/<file_name>/<float:start_amount>/')
def index(file_name, start_amount):
    if len(app.data) == 0:
        app.data = parse_file(file_name, start_amount)
    return render_template('index.html')

@app.route('/bank_data/')
def bank_data():
    return jsonify({ 'data': app.data })


app.run(debug=True)