from flask import Flask, render_template, request
from iris_data import predict_iris
import numpy as np
import psycopg2


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', prediction=None)


@app.route('/predict', methods=['POST'])
def predict():
    sepal_length = float(request.form['sepal_length'])
    sepal_width = float(request.form['sepal_width'])
    petal_length = float(request.form['petal_length'])
    petal_width = float(request.form['petal_width'])

    features = [sepal_length, sepal_width, petal_length, petal_width]
    prediction = predict_iris(features)

    conn = psycopg2.connect(host='localhost', port='5432', user='postgres', password='admin', database='iris')
    cur = conn.cursor()
    #cur.execute('CREATE TABLE allresult (sepal_length float, sepal_width float, petal_length float, petal_width float, prediction varchar);')
    cur.execute('INSERT INTO allresult (sepal_length, sepal_width, petal_length, petal_width, prediction) values (%s, %s, %s, %s, %s)', (sepal_length, sepal_width, petal_length, petal_width, prediction))
    conn.commit()
    cur.close()
    conn.close()
    return render_template('prediction.html', prediction=prediction)

@app.route('/all_result', methods=['GET'])
def all_result():
    conn = psycopg2.connect(host='localhost', port='5432', user='postgres', password='admin', database='iris')
    cur = conn.cursor()
    cur.execute("SELECT * FROM public.allresult")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('all_result.html', rows=rows)


if __name__ == '__main__':
    app.run(debug=True)