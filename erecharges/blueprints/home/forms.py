from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, validators

class PhoneRechargeForm(FlaskForm):
    amount_options = RadioField([validators.DataRequired()])
    phone_number = StringField([validators.DataRequired(), validators.Length(min=9, max=9)])

    def __init__(self, *args, **kwargs):
        super(PhoneRechargeForm, self).__init__(*args, **kwargs)
        self.amount_options.choices = [
            ('3', 'S/. 3.00'), ('5', 'S/. 5.00'), ('10', 'S/. 10.00')
        ]