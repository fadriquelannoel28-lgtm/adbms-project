from flask import Flask, redirect, render_template


app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/Dashboard')
@app.route('/Dashboard')
def dashboard():
    return render_template('index.html', page_title='Dashboard')

@app.route('/Inventory-Management')
def inventory_management():
    return render_template('minventory.html', page_title='Inventory Management')

@app.route('/Stock-Monitoring')
def stock_monitoring():
    return render_template('smonitoring.html', page_title='Stock Monitoring')

@app.route('/Ordering-System')
def ordering_system():
    return render_template('orderings.html', page_title='Ordering System')

@app.route('/Reports')
def reports():
    return render_template('reports.html', page_title='Reports')

@app.route('/User-Access')
def user_access():
    return render_template('user.html', page_title='User Access')

if __name__ == '__main__':
    app.run(debug=True)