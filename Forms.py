from wtforms import Form, validators, IntegerField, StringField, DateField
import re
from wtforms.validators import DataRequired, Regexp


class EditPackForm(Form):
    pack_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    pack_count = IntegerField('', [validators.NumberRange(min=1, max=150), validators.DataRequired()], default=0)
    pack_price = IntegerField('', [validators.NumberRange(min=1, max=150), validators.DataRequired()], default=0)

class DeliveryAddressForm(Form):
    # city = StringField('City', [validators.DataRequired()])
    city = StringField('City/Region', validators=[DataRequired(), Regexp(r'^[a-zA-Z]+$', message="Name can only contain letters")])
    full_name = StringField('Full Name', [validators.DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Regexp(r'^\d{8}$', message="Phone number must be 8 digits long")])
    # phone_number = IntegerField('Phone Number', [validators.NumberRange(min=10000000, max=99999999, message="you idiot"), validators.DataRequired()])
    zip = StringField('Zip code', validators=[DataRequired(), Regexp(r'^\d{6}$', message="Zip code must be 6 digits long")])
    address = StringField('Address', [validators.DataRequired()], render_kw={"placeholder": "Block number, Street, Unit number"})

class PaymentMethodForm(Form):
    card_number = StringField('Card Number', validators=[DataRequired(), Regexp(r'^\d{16}$', message="Card number must be 16 digits long")])
    card_holder_name = StringField('Card Holder Name', [validators.DataRequired()])
    expiry_date = DateField('Expiry Date', [validators.DataRequired()], format='%Y-%m-%d')
    cvv = StringField('CVV', validators=[DataRequired(), Regexp(r'^\d{3}$', message="CVV code must be 3 or 4 digits long")])
