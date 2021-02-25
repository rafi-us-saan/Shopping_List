from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shoppinglist.db'
db = SQLAlchemy(app)


class shoppinglist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pName = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(20), nullable=True)
    price = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return '<Item %r>' % self.id




@app.route('/')
@app.route('/app')
def MainView():
    list = shoppinglist.query.order_by(shoppinglist.id).all()
    return render_template('mainview.html', items=list)


@app.route('/newitem')
def NewItem():
    return render_template('newitem.html')


@app.route('/pushitem', methods=['POST','GET'])
def PushItem():
    if request.method == 'POST':
        itemName = request.form['pname']
        itemQuantity = request.form['quantity']
        itemPrice = request.form['price']
        newShoppinglist = shoppinglist(
            pName = itemName,
            quantity = itemQuantity,
            price=itemPrice)
        try:
            db.session.add(newShoppinglist)
            db.session.commit()
            return redirect('/')
        except:
            return "something went wrong"
    else:
        render_template('newitem.html')


@app.route('/delete/<int:id>')
def delete(id):
    itemDelete = shoppinglist.query.get_or_404(id)

    try:
        db.session.delete(itemDelete)
        db.session.commit()
        return redirect('/app')
    except:
        return "something went wrong"


@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    item = shoppinglist.query.get_or_404(id)

    if request.method == 'POST':
        item.pname = request.form['pname']
        item.quantity = request.form['quantity']
        item.price = request.form['price']
    
        try:
            db.session.commit()
            return redirect('/app')
        except:
            return "something went wrong"
    else:
        return render_template('update.html', item=item)


if __name__=="__main__":
    app.run()
