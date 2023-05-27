import random
import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)


# Renders the Main Page
@app.route('/')
def mainPage():
    return render_template('Index.html')


# Changes the Admin password
@app.route('/addExpenses', methods=['POST'])
def addExpenses():
    dateOfExpense = request.form['expenseDate']
    placeOfExpense = request.form['expensePlace']
    itemOfExpense = request.form['expenseItem']
    amountOfExpense = request.form['expenseAmount']

    values = "('" + dateOfExpense + "', '" + placeOfExpense + "', '" + itemOfExpense + "', '" + amountOfExpense + "')"
    connection = sqlite3.connect("DB\\ExpenseTracker.db")
    cur = connection.cursor()
    cur.execute(
        "INSERT INTO EXPENSETRACKER (EXPENSEDATE, EXPENSEPLACE, EXPENSEITEM, EXPENSEAMOUNT) VALUES " + values + ";")
    connection.commit()

    return render_template('Index.html', TemplateBanner="Expense of " + amountOfExpense + " successfully added !!!")


@app.route('/getExpenses', methods=['POST'])
def getExpenses():
    toDateOfExpense = request.form['getFromExpenseDate']
    fromDateOfExpense = request.form['getToExpenseDate']
    colors = ['#F7464A', '#46BFBD', '#FDB45C', '#FEDCBA', '#ABCDEF', '#DDDDDD', '#ABCABC', '#4169E1', '#C71585',
              '#FF4500', '#FEDCBA', '#46BFBD', '#CCFF33', '#81D8D0', '#2E8B57', '#6B8E23', '#08A04B', '#AA6C39']
    typeOfChart = request.form['rangeChartType']

    connection = sqlite3.connect("DB\\ExpenseTracker.db")
    cur = connection.cursor()

    #Begin In Detail Chart Queries
    cur.execute(
        "SELECT EXPENSEAMOUNT FROM EXPENSETRACKER WHERE EXPENSEDATE BETWEEN '" + toDateOfExpense + "' AND '" + fromDateOfExpense + "' ORDER BY EXPENSEDATE ASC;")
    usercheck = cur.fetchall()
    totalamt = []
    for row in usercheck:
        totalamt.append(row[0])

    cur.execute(
        "SELECT EXPENSEDATE FROM EXPENSETRACKER WHERE EXPENSEDATE BETWEEN '" + toDateOfExpense + "' AND '" + fromDateOfExpense + "' ORDER BY EXPENSEDATE ASC;")
    usercheck = cur.fetchall()
    totaldate = []
    for row in usercheck:
        totaldate.append(row[0])

    cur.execute(
        "SELECT EXPENSEPLACE FROM EXPENSETRACKER WHERE EXPENSEDATE BETWEEN '" + toDateOfExpense + "' AND '" + fromDateOfExpense + "' ORDER BY EXPENSEDATE ASC;")
    usercheck = cur.fetchall()
    totalplace = []
    for row in usercheck:
        totalplace.append(row[0])

    cur.execute(
        "SELECT EXPENSEITEM FROM EXPENSETRACKER WHERE EXPENSEDATE BETWEEN '" + toDateOfExpense + "' AND '" + fromDateOfExpense + "' ORDER BY EXPENSEDATE ASC;")
    usercheck = cur.fetchall()
    totalitem = []
    for row in usercheck:
        totalitem.append(row[0])
    #End In Detail Chart Queries

    #Begin Day by Day Details Chart Queries
    cur.execute(
        "SELECT SUM(EXPENSEAMOUNT) FROM EXPENSETRACKER WHERE EXPENSEDATE BETWEEN '" + toDateOfExpense + "' AND '" + fromDateOfExpense + "' GROUP BY EXPENSEDATE;")
    usercheck = cur.fetchall()
    totalamtd2d = []
    for row in usercheck:
        totalamtd2d.append(row[0])

    cur.execute(
        "SELECT EXPENSEDATE FROM EXPENSETRACKER WHERE EXPENSEDATE BETWEEN '" + toDateOfExpense + "' AND '" + fromDateOfExpense + "' GROUP BY EXPENSEDATE;")
    usercheck = cur.fetchall()
    totaldate2d = []
    for row in usercheck:
        totaldate2d.append(row[0])
    #End Day by Day Details Chart Queries

    # Begin Expense by Place
    cur.execute(
        "SELECT EXPENSEPLACE FROM EXPENSETRACKER WHERE EXPENSEDATE BETWEEN '" + toDateOfExpense + "' AND '" + fromDateOfExpense + "' GROUP BY EXPENSEPLACE;")
    usercheck = cur.fetchall()
    customExpnesePlace = []
    for row in usercheck:
        customExpnesePlace.append(row[0])

    cur.execute(
        "SELECT SUM(EXPENSEAMOUNT) FROM EXPENSETRACKER WHERE EXPENSEDATE BETWEEN '" + toDateOfExpense + "' AND '" + fromDateOfExpense + "' GROUP BY EXPENSEPLACE;")
    usercheck = cur.fetchall()
    customExpneseAmount = []
    for row in usercheck:
        customExpneseAmount.append(row[0])

    # End Expense by Place

    TotalAmount = "Total Expense for " + toDateOfExpense + " and " + fromDateOfExpense + " is " + str(
        sum(totalamt)) + " Rupees"

    if (typeOfChart == "Table"):
        return render_template('Table.html', len=len(totalamt), TemplateExpenseDate=totaldate,
                               TemplateExpenseAmount=totalamt, TemplateTotalPlace=totalplace,
                               TemplateTotalItem=totalitem, TemplateTotalAmount=TotalAmount)

    if (typeOfChart == "rangeBar"):
        return render_template('RangeBar.html', TemplateExpenseDate=totaldate, TemplateExpenseAmount=totalamt,
                               TemplateColor=random.choices(colors, k=len(totaldate)),
                               TemplateTitle="Expenses from " + toDateOfExpense + " to " + fromDateOfExpense,
                               TemplateBanner=TotalAmount)

    if (typeOfChart == "rangeBard2d"):
        return render_template('RangeBarD2D.html', TemplateExpenseDate=totaldate2d, TemplateExpenseAmount=totalamtd2d,
                               TemplateColor=random.choices(colors, k=len(totaldate2d)),
                               TemplateTitle="Expenses from " + toDateOfExpense + " to " + fromDateOfExpense,
                               TemplateBanner=TotalAmount)

    if (typeOfChart == "rangePie"):
        return render_template('RangePie.html', TemplateExpenseDate=totaldate, TemplateExpenseAmount=totalamt,
                               TemplateColor=random.choices(colors, k=len(totaldate)),
                               TemplateTitle="Expenses from " + toDateOfExpense + " to " + fromDateOfExpense,
                               TemplateBanner=TotalAmount)

    if (typeOfChart == "rangePied2d"):
        return render_template('RangePieD2D.html', TemplateExpenseDate=totaldate2d, TemplateExpenseAmount=totalamtd2d,
                               TemplateColor=random.choices(colors, k=len(totaldate2d)),
                               TemplateTitle="Expenses from " + toDateOfExpense + " to " + fromDateOfExpense,
                               TemplateBanner=TotalAmount)

    if (typeOfChart == "rangeLine"):
        return render_template('RangeLine.html', TemplateExpenseDate=totaldate, TemplateExpenseAmount=totalamt,
                               TemplateColor=random.choices(colors, k=len(totaldate)),
                               TemplateTitle="Expenses from " + toDateOfExpense + " to " + fromDateOfExpense,
                               TemplateBanner=TotalAmount)

    if (typeOfChart == "rangeLined2d"):
        return render_template('RangeLineD2D.html', TemplateExpenseDate=totaldate2d, TemplateExpenseAmount=totalamtd2d,
                               TemplateColor=random.choices(colors, k=len(totaldate2d)),
                               TemplateTitle="Expenses from " + toDateOfExpense + " to " + fromDateOfExpense,
                               TemplateBanner=TotalAmount)

    if (typeOfChart == "expenseByPlaceBar"):
        return render_template('ExpenseByPlaceBar.html', TemplateExpenseDate=customExpnesePlace, TemplateExpenseAmount=customExpneseAmount,
                               TemplateColor=random.choices(colors, k=len(customExpnesePlace)),
                               TemplateTitle="Expenses from " + toDateOfExpense + " to " + fromDateOfExpense,
                               TemplateBanner=TotalAmount)

    if (typeOfChart == "expenseByPlacePie"):
        return render_template('ExpenseByPlacePie.html', TemplateExpenseDate=customExpnesePlace, TemplateExpenseAmount=customExpneseAmount,
                               TemplateColor=random.choices(colors, k=len(customExpnesePlace)),
                               TemplateTitle="Expenses from " + toDateOfExpense + " to " + fromDateOfExpense,
                               TemplateBanner=TotalAmount)

# Runs the App
if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)
