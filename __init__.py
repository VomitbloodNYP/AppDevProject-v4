# clean up import statements and remove unused imports (DO THIS LAST)
import random
from flask import Flask, flash, request, redirect, render_template,Response,url_for,send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary
from flask import Flask, render_template, request, redirect, url_for, Response
from Forms import EditPackForm, DeliveryAddressForm, PaymentMethodForm
import shelve, Pack, io
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary, create_engine
from sqlalchemy.orm import sessionmaker

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Cards.db"
app.config['SECRET_KEY'] = 'be3816ab3ea3b8672fa608a'
db = SQLAlchemy(app)

# make class for card
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(precision=10,scale=2), nullable=False)
    rarity = db.Column(db.String(255), nullable=False)
    booster = db.Column(db.String(255), nullable=False)
    image = db.Column(LargeBinary)
    description = db.Column(db.String(255), nullable=True)

# YX part starts here
# main store page - retrieve from card db
@app.route('/', methods=['GET', 'POST'])
def add_pack():
    print("hello there console snooper")
    data = Card.query.all()
    return render_template('store.html', data=data)

# shopping cart page - retrieve items from basket shelve db
@app.route('/basket')
def basket():
    pack_dict = {}

    db = shelve.open('pack.db', 'r')
    pack_dict = db['Packs']
    db.close()

    pack_list = []
    for key in pack_dict:
        pack = pack_dict.get(key)
        pack_list.append(pack)

    return render_template('basket.html', count=len(pack_list), pack_list=pack_list)

# pack listing page show details of each pack - retrieve and update
@app.route('/packListing/<int:id>/', methods=['GET', 'POST'])
def update_pack_listing(id):
    displayThisCard = Card.query.filter_by(id=id).first()

    # shelve things
    db = shelve.open('basket.db', 'c')

    try:
        basket_dict = db['Basket']
    except:
        print("Error in retrieving Packs from pack.db.")

    # add pack to basket
    if request.method == 'POST':
        return redirect(url_for('success'))

    return render_template('packListing.html', displayThisCard=displayThisCard)

# delete pack from basket - retrieve and delete
@app.route('/deletePack/<int:pack_id>', methods=['POST'])
def delete_pack(pack_id):
    pack_dict = {}

    db = shelve.open('pack.db', 'w')
    pack_dict = db['Packs']

    pack_dict.pop(pack_id)

    db['Packs'] = pack_dict
    db.close()

    return redirect(url_for('shopping_cart'))

# checkout page - create retrieve and update
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    delivery_address_form = DeliveryAddressForm(request.form)
    payment_method_form = PaymentMethodForm(request.form)
    if request.method == 'POST' and delivery_address_form.validate() and payment_method_form.validate():
        return redirect(url_for('success'))
    return render_template('checkout.html', delivery_address_form=delivery_address_form, payment_method_form=payment_method_form)

# very nice
@app.route('/success')
def success():
    return render_template('success.html')

# not very nice
@app.route('/fail')
def fail():
    return render_template('fail.html')
# YX part ends here

# jonath part start
@app.route('/addcard', methods=['GET', 'POST'])
def add_card():
    if request.method == 'POST':

        name = request.form['name']
        type = request.form['type']
        price = request.form['price']
        rarity = request.form['rarity']
        url = request.files['img_file']
        description = request.form['description']
        if description == '':
            description = '<No description>'
        booster=request.form['booster']
        image_data = url.read()
        image_data = bytes(image_data)
        card = Card(name=name, type=type,
                        price=price,booster=booster
                        , rarity=rarity, image=image_data,
                        description=description)
        db.session.add(card)
        db.session.commit()



        return redirect(url_for('data'))
    return render_template('addcard.html')

@app.route('/image/<int:id>')
def image(id):
    card = Card.query.filter_by(id=id).first()
    image = card.image
    if image:
        return Response(image, content_type='image/jpeg')
    else:
        return 'Image Not Found', 404

@app.route('/updateCards/<int:id>')
def update(id):
    return redirect(url_for('update_page', id=id))

@app.route('/updateCards-page/<int:id>')
def update_page(id):
    card = Card.query.filter_by(id=id).first()
    return render_template('updatecards.html', data=card)

@app.route('/Cardsdata')
def data():
    carddata = Card.query.all()
    return render_template("retrievecard.html", data=carddata)

@app.route('/submit-update/<int:id>', methods=['POST'])
def submit_update(id):
    name = request.form['name']
    name=name.capitalize()
    type = request.form['type']
    price = request.form['price']
    rarity = request.form['rarity']
    description = request.form['description']
    if description == '':
        description = '<No description>'
    filecheck = request.form['check']
    booster=request.form['booster']
    card = Card.query.filter_by(id=id).first()
    if card:
        card.name = name
        card.type = type
        card.price = price
        card.rarity = rarity
        card.description = description
        card.booster=booster
        if filecheck != 'failed' and request.method == 'POST':
            url = request.files['img_file']
            image_data = url.read()
            image_data = bytes(image_data)
            card.image=image_data
        db.session.commit()
    # Redirect to the main page
    return redirect(url_for('data'))

@app.route('/filter',methods=['POST'])
def filters():
    rarity = request.form.get('rarefilter')
    filter_name = request.form.get('filter_name')
    if rarity == 'All':
        rarity = 'All'
        filterdata = Card.query.filter(Card.name.contains(filter_name))
        return render_template("retrievecard.html", data=filterdata,rarity=rarity,query=filter_name)
    else:
        filterdata = Card.query.filter((Card.name.contains(filter_name)) & (Card.rarity.contains(rarity))).all()
    return render_template('retrievecard.html', data=filterdata,rarity=rarity,query=filter_name)

@app.route('/resetfilter',methods=['POST'])
def resetfilter():
    rarity = 'All'
    filter_name = ''
    return render_template('retrievecard.html',data=Card.query.all(),rarity=rarity,query=filter_name)
@app.route('/deletecard/<int:id>',methods=['POST'])
def delete(id):
    delete = Card.query.filter_by(id=id).first()
    db.session.delete(delete)
    db.session.commit()
    return redirect(url_for('data'))

#End admin page for jonath
#Start zhengyi code
@app.route('/gachadeletecard/<int:id>',methods=['POST'])
def gachadelete(id):
    gachadelete = Card.query.filter_by(id=id).first()
    db.session.delete(gachadelete)
    db.session.commit()
    return redirect(url_for('gachastore'))

@app.route('/gachastore')
def gachastore():
    return render_template('gachastore.html')

@app.route('/crownzenith')
def crownzenith():
    try:
        data = Card.query.filter_by(booster='Crown Zenith').all()
        temp = []
        for card in data:
            temp.append(card)
        size = len(temp)
        gacharate = random.randint(0, size-1)
        chosenvalue = temp[gacharate]
        return render_template('gachadisplay.html', chosenvalue=chosenvalue)

    except:
        return render_template('gachastock.html')

@app.route('/silvertempest')
def silvertempest():
    try:
        data = Card.query.filter_by(booster='Silver Tempest').all()
        temp = []
        for card in data:
            temp.append(card)
        size = len(temp)
        gacharate = random.randint(0, size-1)
        chosenvalue = temp[gacharate]
        return render_template('gachadisplay.html', chosenvalue=chosenvalue)

    except:
        return render_template('gachastock.html')

@app.route('/lostorigin')
def lostorigin():
    try:
        data = Card.query.filter_by(booster='Lost Origin').all()
        temp = []
        for card in data:
            temp.append(card)
        size = len(temp)
        gacharate = random.randint(0, size-1)
        chosenvalue = temp[gacharate]
        return render_template('gachadisplay.html', chosenvalue=chosenvalue)

    except:
        return render_template('gachastock.html')

@app.route('/astralradiance')
def astralradiance():
    try:
        data = Card.query.filter_by(booster='Astral Radiance').all()
        temp = []
        for card in data:
            temp.append(card)
        size = len(temp)
        gacharate = random.randint(0, size-1)
        chosenvalue = temp[gacharate]
        return render_template('gachadisplay.html', chosenvalue=chosenvalue)

    except:
        return render_template('gachastock.html')

@app.route('/brilliantstars')
def brilliantstars():
    try:
        data = Card.query.filter_by(booster='Brilliant stars').all()
        temp = []
        for card in data:
            temp.append(card)
        size = len(temp)
        gacharate = random.randint(0, size-1)
        chosenvalue = temp[gacharate]
        return render_template('gachadisplay.html', chosenvalue=chosenvalue)

    except:
        return render_template('gachastock.html')

@app.route('/celebrations')
def celebrations():
    try:
        data = Card.query.filter_by(booster='Celebrations').all()
        temp = []
        for card in data:
            temp.append(card)
        size = len(temp)
        gacharate = random.randint(0, size-1)
        chosenvalue = temp[gacharate]
        return render_template('gachadisplay.html', chosenvalue=chosenvalue)

    except:
        return render_template('gachastock.html')

@app.route('/evolvingskies')
def evolvingskies():
    try:
        data = Card.query.filter_by(booster='Evolving skies').all()
        temp = []
        for card in data:
            temp.append(card)
        size = len(temp)
        gacharate = random.randint(0, size-1)
        chosenvalue = temp[gacharate]
        return render_template('gachadisplay.html', chosenvalue=chosenvalue)

    except:
        return render_template('gachastock.html')

@app.route('/vividvoltage')
def vividvoltage():
    try:
        data = Card.query.filter_by(booster='Vivid voltage').all()
        temp = []
        for card in data:
            temp.append(card)
        size = len(temp)
        gacharate = random.randint(0, size-1)
        chosenvalue = temp[gacharate]
        return render_template('gachadisplay.html', chosenvalue=chosenvalue)

    except:
        return render_template('gachastock.html')

@app.route('/sunmoon')
def sunmoon():
    try:
        data = Card.query.filter_by(booster='Sun & moon').all()
        temp = []
        for card in data:
            temp.append(card)
        size = len(temp)
        gacharate = random.randint(0, size-1)
        chosenvalue = temp[gacharate]
        return render_template('gachadisplay.html', chosenvalue=chosenvalue)

    except:
        return render_template('gachastock.html')

#End zhenhyi code

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="127.0.0.69")
