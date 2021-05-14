from typing import final
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_, not_
from pprint import pprint
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

db = SQLAlchemy(app)

# Session = sessionmaker(engine)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///expensetracker.db"

app.config['SQLALCHEMY_BINDS'] = {
    'todo': "sqlite:///todo.db"
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Expensetracker(db.Model):

    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    expense_type = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    week = db.Column(db.String, nullable=False)
    value = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f'{self.sno},{self.username},{self.expense_type},{self.date},{self.month},{self.week},{self.value}'


class addtodo(db.Model):

    __bind_key__ = 'todo'
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(255), nullable=False)
    month = db.Column(db.Integer, nullable=False)
    value = db.Column(db.String(255), nullable=False)

    def __repr__(self) -> str:
        return f'{self.sno},{self.username},{self.date},{self.month},{self.value}'


# Home Page Route

@app.route('/', methods=['GET', 'POST'])
def hello_world():

    db.create_all()

    if request.method == 'POST':
        username = request.form.get('name')
        selected = request.form.get('gainexp')
        date = request.form.get('date')
        month = request.form.get('month')
        day = request.form.get('week')
        value = request.form.get('value')

        usernamenotselected = False
        gainexpnotselected = False
        datenotselected = False
        monthnotselected = False
        expensenotspecified = False
        valuenotspecified = False

        if username == "":
            usernamenotselected = True
            return render_template('expenseerror.html', usernamenotselected=usernamenotselected)

        elif selected == None:
            gainexpnotselected = True
            return render_template('expenseerror.html', gainexpnotselected=gainexpnotselected)

        elif date == "":
            datenotselected = True
            return render_template('expenseerror.html', datenotselected=datenotselected)

        elif month == 'None':
            monthnotselected = True
            return render_template('expenseerror.html', monthnotselected=monthnotselected)

        elif day == "":
            expensenotspecified = True
            return render_template('todoerror.html', expensenotspecified=expensenotspecified)

        elif value == "":
            valuenotspecified = True
            return render_template('todoerror.html', valuenotspecified=valuenotspecified)

        else:
            expense = Expensetracker(
                username=username,
                expense_type=selected,
                date=date,
                month=month,
                week=day,
                value=value,
            )
            db.session.add(expense)
            db.session.commit()

    return render_template('index.html')


# Transactions

@app.route('/transactions', methods=['GET', 'POST'])
def transaction():

    value = False
    year_map = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May',
                6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

    if request.method == 'POST':
        fullname = request.form.get('name')
        month = request.form.get('month')
        # print(fullname, month)

        namenotfound = False
        res = db.session.query(Expensetracker).filter(
            Expensetracker.username == fullname).all()

        print(f' Is user present or not : {res}')

        monthnotselected = False
        if month == 'None':
            monthnotselected = True
            return render_template('expenseerror.html', monthnotselected=monthnotselected)

        elif len(res) == 0:
            namenotfound = True
            return render_template('dashboarderror.html', namenotfound=namenotfound)

        else:

            alltransactions = db.session.query(Expensetracker).filter(and_(
                Expensetracker.month == int(month),
                Expensetracker.username == fullname
            )).all()
        # alltransactions = db.session.query(Expensetracker).filter_by(
        #     month=int(month)).all()

            month_topass = year_map[int(month)]

            # print(f' Result array is : {alltransactions}')
            value = True

            return render_template('transaction.html', allTodo=alltransactions, value=value,
                                   month_topass=month_topass)

    # alltransactions = Expensetracker.query.all()

    # print(f' All transactions are : {alltransactions}')

    return render_template('transaction.html')

# AddTodo


@app.route('/addtodo', methods=['GET', 'POST'])
def addtodofunc():

    # Firstly if this does not work at the first time,you have to use the terminal for fixing this
    # so use the terminal and type in python and then type in "from app import db" and then as we wanna
    # use the todo db we have to bind it,so for that type in "db.create_all(bind = ['todo'])",here
    # todo is the database name!
    # db.create_all(bind=['todo'])

    if request.method == 'POST':
        username = request.form.get('todoname')
        date = request.form.get('date')
        month = request.form.get('month')
        todo = request.form.get('value')

        # print(f' Date selected is : {date}')

        month_topass = False
        value = False
        month_pass = False
        datenotselected = False

        if username == "":
            value = True
            return render_template('todoerror.html', value=value)

        elif date == "":
            datenotselected = True
            return render_template('todoerror.html', datenotselected=datenotselected)

        elif month == 'None':
            month_pass = True
            return render_template('todoerror.html', month_pass=month_pass)

        elif todo == "":
            month_topass = True
            return render_template('todoerror.html', month_topass=month_topass)

        else:
            print(f' Date entered is : {date}')

            todos = addtodo(
                username=username,
                date=date,
                month=month,
                value=todo,
            )
            db.session.add(todos)
            db.session.commit()

        alltodos = addtodo.query.all()
        # print(f' All Todos are : {alltodos}')

    return render_template('index.html')


# Display Todos
@app.route('/displaytodo', methods=['GET', 'POST'])
def displaytodofunc():

    value = False
    year_map = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May',
                6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

    if request.method == 'POST':
        fullname = request.form.get('name')
        month = request.form.get('month')

        namenotfound = False
        res = db.session.query(addtodo).filter(
            addtodo.username == fullname).all()

        print(f' Is user present or not : {res}')

        monthnotselected = False
        if month == 'None':
            monthnotselected = True
            return render_template('expenseerror.html', monthnotselected=monthnotselected)

        elif len(res) == 0:
            namenotfound = True
            return render_template('dashboarderror.html', namenotfound=namenotfound)

        else:
            alltransactions = db.session.query(addtodo).filter(and_(
                addtodo.month == int(month),
                addtodo.username == fullname
            )).all()

            month_topass = year_map[int(month)]

            print(f' Result array is : {alltransactions}')
            value = True

            return render_template('todolist.html', allTodo=alltransactions, value=value,
                                   month_topass=month_topass)

    return render_template('todolist.html')


# Dashboard

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    if request.method == 'POST':

        # Extracting the name,as i will be using it later!

        fullname = request.form.get('fullname')
        # print(f' Full Name is : {fullname}')

        # <-------------------------------- This is for Expenses---------------------------------->

        namenotfound = False
        res = db.session.query(Expensetracker).filter(
            Expensetracker.username == fullname).all()

        print(f' Is user present or not : {res}')

        if len(res) == 0:
            namenotfound = True
            return render_template('error.html', namenotfound=namenotfound)

        else:

            expense_dict = {}
            showchart = False
            expense = 1

            for result in db.session.query(Expensetracker).filter(and_(
                Expensetracker.expense_type == 'expenditure',
                Expensetracker.username == fullname
            )).all():

                expense_dict[expense] = result.__dict__
                expense += 1

            expense_week = []
            expense_money = []
            expense_date = []

            for key, value in expense_dict.items():
                for key1, val1 in value.items():
                    if key1 == 'week':
                        expense_week.append(val1)

                    if key1 == 'value':
                        expense_money.append(val1)

                    if key1 == 'date':
                        expense_date.append(val1)

            expense_final = defaultdict(list)
            total_expenses = defaultdict(list)
            year_map = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May',
                        6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
            for string, week, money, date in zip(expense_date, expense_week, expense_money, expense_date):
                string = string.split('-')
                string = string[1]
                if string[0] == '0':
                    string_use = string[1]
                else:
                    string_use = string
                expense_final[string_use].append(({date: money}))

                total_expenses[year_map[int(string_use)]].append(money)

            total_expenses = dict(total_expenses)

        #  <--------------------------Total Expenses end up here------------------------>

        #    <-------------------------This is for gains---------------------------->

            final_dict = {}
            count = 1

            for result in db.session.query(Expensetracker).filter(and_(
                Expensetracker.expense_type == 'gain',
                Expensetracker.username == fullname
            )).all():

                # print(dict(result.__dict__))
                final_dict[count] = result.__dict__

                count += 1

            week_list = []
            money_list = []
            date_list = []
            # pprint(final_dict)

            for key, value in final_dict.items():
                for key1, val1 in value.items():
                    if key1 == 'week':
                        week_list.append(val1)

                    if key1 == 'value':
                        money_list.append(val1)

                    if key1 == 'date':
                        date_list.append(val1)

            final = defaultdict(list)
            total_savings = defaultdict(list)
            months = []
            for string, week, money, date in zip(date_list, week_list, money_list, date_list):
                string = string.split('-')
                string = string[1]

                # Months from Jan->September 1->9 single digit months!
                # print(f' String is : {string}')

                if string[0] == '0':
                    string_use = string[1]

                # Double Digit Months!

                else:
                    string_use = string

                final[string_use].append(({date: money}))
                total_savings[year_map[int(string_use)]].append(money)

            total_savings = dict(total_savings)
            # print(f' Total Savings  : {total_savings}')

            # <---------------------------------Gains End here----------------------------->

            income_date = []
            income_money = []
            expense_date = []
            expense_money = []
            income = 0
            value = False

            showchart = True

            # --------------------------------Year Map------------------------------------------------>

            year_map = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May',
                        6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

            anual_income = request.form.get('income')
            print(anual_income)
            todo = request.form.get('month')

        #    Incomes Value
            income = anual_income
            month_topass = False

            if anual_income == "":
                value = True
                return render_template('error.html', value=value)

            if todo == 'None':
                value = True
                month_topass = True
                return render_template('error.html', value=value, month_topass=month_topass)

            else:

                for value in final[todo]:

                    # print(f' Value is : {value}')
                    for key, val in value.items():
                        income_date.append(key)
                        income_money.append(val)

            #   Expenses value

                for value in expense_final[todo]:

                    for key, val in value.items():
                        expense_date.append(key)
                        expense_money.append(val)

                month = year_map[int(todo)]

                # print(f' Income Date list is : {income_date}')
                # print(f' Income Money list is : {income_money}')
                # print(f' Expenses Date list is : {expense_date}')
                # print(f' Expense Money list is : {expense_money}')
                # print(f' Anual Income is : {anual_income}')
                income_total = sum(income_money)
                expense_total = sum(expense_money)
                montly_income = int(anual_income)//12
                profityaloss = 0

                if expense_total > income_total:
                    plval = abs(expense_total-income_total)
                    paise = abs(montly_income+income_total-expense_total)
                    pl_percent = int(plval//montly_income)*100

                else:
                    plval = abs(income_total-expense_total)
                    paise = abs(montly_income+income_total-expense_total)
                    pl_percent = int(plval//montly_income)*100
                    profityaloss = 1

                # if profityaloss == 1:
                #     # print(f' Profit hai bhai : {plval}')
                #     # print(f' Paise bache : {paise}')
                #     # print(f' Profit % : {pl_percent}')

                # else:
                #     # print(f' Loss hai bhai :( : {plval}')
                #     # print(f' Paise gaye : {paise}')
                #     # print(f' Loss % : {pl_percent}')

                if len(income_money) == 0 and len(expense_money) == 0:
                    return render_template('exception.html', value=value)

                return render_template('dashboard.html', income=income, expense_money=expense_money,
                                       expense_date=expense_date, income_money=income_money, income_date=income_date, expense_final=total_expenses,
                                       saving_final=total_savings, month=month, showchart=showchart,
                                       profityaloss=profityaloss, plval=plval, paise=paise)

    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)
