from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = "expiry-alert-key"

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)

# Product Model/Table
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    expiry = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50), nullable=False)


# Create DB if not exists
with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        expiry = request.form['expiry']
        category = request.form['category']

        exp_date = datetime.strptime(expiry, "%Y-%m-%d").date()
        new_product = Product(name=name, expiry=exp_date, category=category)

        db.session.add(new_product)
        db.session.commit()
        return redirect('/')

    today = date.today()
    products = Product.query.all()

    # Alert for expired items
    for p in products:
        if p.expiry < today:
            flash(f"⚠ Alert: {p.name} has expired!", "danger")

    return render_template('index.html', products=products, today=today)


# DELETE ROUTE
@app.route('/delete/<int:id>')
def delete(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
