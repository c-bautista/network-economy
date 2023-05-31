import os
from flask import Flask, render_template, redirect, url_for, request
from forms.forms import Form, Form_scan 
from model import model
from main import model_scan 
import random
import string
from func.plots import analysis_param
from flaskext.markdown import Markdown

app = Flask(__name__)
app.config.from_object(__name__)
SECRET_KEY=os.urandom(32)
app.config['SECRET_KEY']=SECRET_KEY
plots_folder=os.path.join('static')

Markdown(app)

@app.route('/test')
def test():
    theta=str(float(request.args['theta'])+1)


@app.route('/results')
def results():
    q=request.args['q']
    periods=request.args['periods']
    p=request.args['p']
    for filename in os.listdir('static/'):
        os.remove('static/' + filename)
    model_instance=model(periods=int(periods), theta=float(q), sigma=float(p))
    model_instance.run()
    model_instance.plot()
    for filename in os.listdir('static/'):
        if "bankruptcy" in filename:
            bankruptcy_image=filename
        if "credit" in filename:
            credit_image=filename
        if  "worth" in filename:
            net_worth_image=filename
    return render_template('results.html', periods=periods, q=q, p=p, bankruptcy_image=bankruptcy_image, credit_image=credit_image, net_worth_image=net_worth_image)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/singlerun', methods=["GET", "POST"])
def single_run():
    form_single=Form()
    if form_single.validate_on_submit():
        periods=form_single.periods.data
        p=form_single.p.data
        q=form_single.q.data
        return redirect(url_for('results', periods=periods, p=p, q=q))
    return render_template('parameters.html', form_single=form_single)

@app.route('/scan', methods=['GET', 'POST'])
def scan():
    form_scan=Form_scan()
    
    form_scan.select_param.choices=["p (Bank's net worth importance)", "q (Leverage importance)"]
    if form_scan.validate_on_submit() and form_scan.scan_values.data!='':
        param_to_scan=form_scan.select_param.data[0]
        values_raw=form_scan.scan_values.data
        return redirect(url_for('scan_results', param=param_to_scan, values_raw=values_raw))
    #parameters=['theta', 'sigma']
    #return render_template('scan.html', parameters=parameters, form_scan=form_scan)
    return render_template('scan.html', form_scan=form_scan)

@app.route('/scan-results')
def scan_results():
    param=request.args['param']
    values_raw=request.args['values_raw']
    values=[]
    for val in values_raw.split(','):
        values.append(float(val))
    for filename in os.listdir('static/'):
        os.remove('static/' + filename)
    param_dict={'p': 'sigma', 'q':'theta'}
    model(param_dict[param])
    models_list=model_scan(param_dict[param], values)
    random_sufix=''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(20))

    analysis_param('N', values, '', models_list, xlabel=param, ylabel='Workers', name='workers_'+random_sufix, plotdir="static/" )
    analysis_param('A', values, '', models_list, xlabel=param, ylabel='Net worth', name='net_worth_'+random_sufix, plotdir="static/")
    analysis_param('B', values, 'log', models_list, xlabel=param, ylabel='Credit', name='credit_'+random_sufix, plotdir="static/")
    analysis_param('is_bankrupt',values, '', models_list, xlabel=param, ylabel='bankruptcies', name='bankruptcies_'+random_sufix, plotdir='static/')
    images=os.listdir('static')

    return render_template('scan_results.html', param=param, param_values=values, images=images)
