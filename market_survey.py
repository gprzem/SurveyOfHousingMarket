from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import statistics

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///formdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

db = SQLAlchemy(app)




class Formdata(db.Model):
    __tablename__ = 'formdata'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    first_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    year_of_study = db.Column(db.Integer)
    district = db.Column(db.Integer)
    searching_time = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    search_amount = db.Column(db.Integer)
    others = db.Column(db.String)

    q1 = db.Column(db.Text)
    q2 = db.Column(db.Integer)
    c1 = db.Column(db.Boolean)
    c2 = db.Column(db.Boolean)
    c3 = db.Column(db.Boolean)
    c4 = db.Column(db.Boolean)
    c5 = db.Column(db.Boolean)
    c6 = db.Column(db.Boolean)
    c7 = db.Column(db.Boolean)
    c8 = db.Column(db.Boolean)
    c9 = db.Column(db.Boolean)
    c10 = db.Column(db.Boolean)

    def __init__(self, first_name, email, year_of_study, district, searching_time, cost, search_amount, others, q1, q2, c1,c2,c3,c4,c5,c6,c7,c8,c9,c10):
        self.first_name = first_name
        self.email = email
        self.year_of_study = year_of_study
        self.district = district
        self.searching_time = searching_time
        self.search_amount = search_amount
        self.cost = cost
        self.others = others
        self.q1 = q1
        self.q2 = q2
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.c4 = c4
        self.c5 = c5
        self.c6 = c6
        self.c7 = c7
        self.c8 = c8
        self.c9 = c9
        self.c10 = c10


db.create_all()


class Districtsdata(db.Model):
    __tablename__ = 'dict_districts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Simpledictionary(db.Model):
    __tablename__ = ''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Difficultiesdata(db.Model):
    __tablename__ = 'dict_difficulties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Infosourcedata(db.Model):
    __tablename__ = 'dict_info_source'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Searchingtimedata(db.Model):
    __tablename__ = 'dict_searching_time'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

class Searchingamount(db.Model):
    __tablename__ = 'dict_searching_amount'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

@app.route("/")
def welcome():
    return render_template('welcome.html')

@app.route("/purpose")
def show_purpose():
    return render_template('purpose.html')

@app.route("/form")
def show_form():
    data1 = db.session.query(Districtsdata)
    data2 = db.session.query(Difficultiesdata)
    data3 = db.session.query(Infosourcedata)
    data4 = db.session.query(Searchingtimedata)
    data5 = db.session.query(Searchingamount)
    return render_template('form.html', districtsdata=data1, difficultiesdata=data2,  infosourcedata=data3,
           searchingtimedata=data4, searchingamount=data5)

@app.route("/raw")
def show_raw():
    fd = db.session.query(Formdata).all()
    data1 = db.session.query(Districtsdata)
    data2 = db.session.query(Difficultiesdata)
    data3 = db.session.query(Infosourcedata)
    data4 = db.session.query(Searchingtimedata)
    data5 = db.session.query(Searchingamount)
    return render_template('raw.html', formdata=fd, districtsdata=data1, difficultiesdata=data2,  infosourcedata=data3,
           searchingtimedata=data4, searchingamount=data5)


@app.route("/result")
def show_result():
    fd_list = db.session.query(Formdata).all()

    # Some simple statistics for sample questions
    satisfaction = []
    q_m = []
    q_w = []
    for el in fd_list:
        if el.q1 == 'M':
            q_m.append(int(el.q2))
        else:
            q_w.append(int(el.q2))

    if len(q_m) > 0:
        mean_q_m = statistics.mean(q_m)
    else:
        mean_q_m = 0

    if len(q_w) > 0:
        mean_q_w = statistics.mean(q_w)
    else:
        mean_q_w = 0

    d = {}
    for year in range(1,6):
        values_for_year = []
        for el_q in fd_list:
            if year == el_q.year_of_study:
                values_for_year.append(el_q.q2)
        if len(values_for_year) > 0:
            mean = statistics.mean(values_for_year)
        else:
            mean = 0
        d[year] = mean


    costs = {}
    for year in range(1,6):
        values_for_year = []
        for el_q in fd_list:
            if year == el_q.year_of_study:
                values_for_year.append(el_q.cost)
        if len(values_for_year) > 0:
            mean = statistics.mean(values_for_year)
        else:
            mean = 0
        costs[year] = mean


    if len(q_m) > 0:
        mean_q_m = statistics.mean(q_m)
    else:
        mean_q_m = 0

    if len(q_w) > 0:
        mean_q_w = statistics.mean(q_w)
    else:
        mean_q_w = 0


    # Prepare data for google charts
    data = [[u'kobiety', mean_q_w],[u'mezczyzni', mean_q_m]]
    data2list = []
    for key in range(1,6):
        data2list.append([str(key), d[key]])
    data3list = []
    for key in range(1,6):
        data3list.append([str(key), costs[key]])
    return render_template('result.html', data=data, data2=data2list, data3=data3list)


@app.route("/save", methods=['POST'])
def save():
    # Get data from FORM
    first_name = request.form['first-name']
    email = request.form['email']
    year_of_study = request.form['year-of-study']
    district = request.form['district']
    searching_time = request.form['searching-time']
    cost = request.form['cost']
    search_amount = request.form['search-amount']
    others = request.form['others']

    q1 = request.form['q1']
    q2 = request.form['q2']
    c1 = request.form['c1']
    c2 = request.form['c2']
    c3 = request.form['c3']
    c4 = request.form['c4']
    c5 = request.form['c5']
    c6 = request.form['c6']
    c7 = request.form['c7']
    c8 = request.form['c8']
    c9 = request.form['c9']
    c10 = request.form['c10']

    # Save the data
    fd = Formdata(first_name, email, year_of_study, district, searching_time, cost, search_amount, others, q1, q2, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)
    db.session.add(fd)
    db.session.commit()

    return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.run()