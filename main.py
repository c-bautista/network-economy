from model import model
from func.plots import analysis_param# plot_aggregate_vars
import random
import string

#model=model()
#model.run()
#model.plot()

scan_values=[0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]

def model_scan(parameter, values):
    models_list=[]
    for val in values:
        exec('model_ins=model('+parameter+'=val)\nmodel_ins.run()\nmodels_list.append(model_ins)')
    return models_list

#plot_aggregate_vars(model)



#random_sufix=''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(20))
#plot_vars(list_to_plot,"static/result_histograms_"+random_sufix)

#scan('theta', scan_values, r'$\theta$')
#models_list=model_scan('sigma', scan_values)
#analysis_param('N', scan_values, models_list, xlabel=r'$\sigma$', ylabel='Workers', name='Workers'+random_sufix, plotdir="static/" )
#analysis_param('A', scan_values, models_list, xlabel=r'$\sigma$', ylabel='Equity', name='Equity'+random_sufix, plotdir="static/")
#analysis_net_worth([0.2, 0.5], [model1, model2], 'theta', 'Equity', 'Equity')


