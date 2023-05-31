from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, IntegerField, SelectField, SelectMultipleField

class Form(FlaskForm):
    periods = IntegerField(label='Number  of periods')
    p = FloatField(label="p (Bank's net worth importance in credit rate)")
    q = FloatField(label='q (Leverage importance in credit rate)')
    submit = SubmitField(label='Compute')

class Form_scan(FlaskForm):
    select_param = SelectField(label='Parameter to scan')
    scan_values = StringField(label='List of values')
    submit_scan = SubmitField(label='Compute ')

