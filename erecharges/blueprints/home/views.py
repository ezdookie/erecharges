# -*- coding: utf-8 -*-
from erecharges.blueprints.home.forms import PhoneRechargeForm
from erecharges.providers.claro import do_recharge
from flask import render_template, Blueprint, url_for, request, flash
from werkzeug.utils import redirect

bp_home = Blueprint('home', __name__)

@bp_home.route('/')
def index():
    form_phonerecharge = PhoneRechargeForm()
    return render_template('home/index.html', form_phonerecharge=form_phonerecharge)

@bp_home.route('/confirm/', methods=['POST'])
def confirm():
    form_phonerecharge = PhoneRechargeForm()
    if form_phonerecharge.validate_on_submit():
        form_data = request.form
        response = do_recharge(
            phone_number=form_data.get('phone_number'),
            amount=form_data.get('amount_options'),
        )
        if response: flash('Recarga exitosa al número {} con S/. {} soles'.format(
                form_data.get('phone_number'), form_data.get('amount_options')),
                'text-success bg-success')
        else: flash('No se pudo hacer la recarga al número {}'.format(
            form_data.get('phone_number')), 'text-danger bg-danger')
    return redirect(url_for('home.index'))