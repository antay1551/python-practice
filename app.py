from flask import Flask, render_template, request
from datetime import datetime
import pygal
import csv

app = Flask(__name__)
number_row_for_length = 1
number_row_for_popularity = 7
number_row_for_subject = 3
available_subject = "Drama"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file uploaded'

        file = request.files['file']

        if file.filename == '':
            return 'No file selected'

        if not file.filename.endswith('.csv'):
            return 'Invalid file format. Please upload a CSV file.'

        file_path = 'tmp.csv'
        file.save(file_path)

        x, y = read_data_from_csv(file_path)
    else:
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]

    chart_svg = create_chart(x, y)

    return render_template('index.html', chart_svg=chart_svg, now=datetime.now(),)

def read_data_from_csv(file_path):
    x = []
    y = []

    with open(file_path, 'r') as file:
        reader = csv.reader(file,delimiter=";")
        next(reader)
        next(reader)
        for row in reader:
            if row[number_row_for_subject] != available_subject:
                continue

            try:
                popularity = int(row[number_row_for_popularity])
                length = int(row[number_row_for_length])
            except ValueError or KeyError:
                continue

            x.append(popularity)
            y.append(length)

    return x, y

def create_chart(x, y):
    line_chart = pygal.Bar(width=4500, x_label_rotation=270)
    line_chart.title = 'Chart'
    line_chart.x_labels = x
    line_chart.add('Length of film', y)

    return line_chart.render().decode().strip()

if __name__ == '__main__':
    app.run()