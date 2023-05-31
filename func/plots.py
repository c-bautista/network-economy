import matplotlib.pyplot as plt
import numpy as np

def plot_vars(list_to_plot,title):
    """Plot the variables on 'list_to_plot' versus the time and save them as 'title.pdf' '"""
    fig, axs = plt.subplots(len(list_to_plot), figsize=(20,len(list_to_plot)*3))
    # fig.suptitle(title,fontsize=32)
    for i in range(len(list_to_plot)):
        axs[i].tick_params(axis='both', which='major', labelsize=15)
        axs[i].plot(list_to_plot[i][0][10:])
        axs[i].set_ylabel(list_to_plot[i][1],fontsize=22)
    plt.savefig(title+".jpg")
    #plt.show()

#def plot_scan(param_list, models_list, title):
#    """Plot  """
#def net_worth_means(models_list):
#    downstream_net_worth_means=[]
#    upstream_net_worth_means=[]
#    bank_net_worth_means=[]
#    for model in models_list:
#        dd=eval('model.d.'+'A'+'_agg')
#        downstream_net_worth_means.append(np.array(dd).mean()/model.n_agents_d)
#        upstream_net_worth_means.append(np.array(model.u.A_agg).mean()/model.n_agents_u)
#        bank_net_worth_means.append(np.array(model.b.A_agg).mean()/model.n_agents_b)
#    return downstream_net_worth_means, upstream_net_worth_means, bank_net_worth_means

def compute_means(models_list, variable):
    downstream_means=[]
    upstream_means=[]
    bank_means=[]
    result={}

    if variable + '_agg' in dir(models_list[0].d):
        for model in models_list:
            down_agg=eval('model.d.' + variable + '_agg')
            downstream_means.append(np.array(down_agg).mean()/model.n_agents_d)
        result['downstream']=downstream_means

    if variable + '_agg' in dir(models_list[0].u):
        for model in models_list:
            up_agg=eval('model.u.' + variable + '_agg')
            upstream_means.append(np.array(up_agg).mean()/model.n_agents_u)
        result['upstream']=upstream_means

    if variable + '_agg' in dir(models_list[0].b):
        for model in models_list:
            bank_agg=eval('model.b.' + variable + '_agg')
            bank_means.append(np.array(bank_agg).mean()/model.n_agents_b)
        result['bank']=bank_means
    return result


def plot_variation(param_list, result, scale, xlabel, ylabel, name, plotdir):
    plt.clf()
    plt.figure(figsize=(5,3))
    for k, v in result.items():
        if k=='downstream':
            plt.plot(param_list, v, label=k, color=(68/255, 119/255, 170/255))
        if k=='upstream':
            plt.plot(param_list, v, label=k, color='orange')
        if k=='bank':
            plt.plot(param_list, v, label=k, color='green')
    if scale=='log':
        plt.yscale('log')
    else:
        plt.locator_params(axis='y', nbins=5)
    plt.xticks(param_list, fontsize=11)
    plt.yticks(fontsize=11)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(plotdir+name+".jpg")
    plt.clf()
    #plt.show()

#def analysis_net_worth(param_list, models_list, xlabel, ylabel, title):
#    down, up, bank = net_worth_means(models_list)
#    plot_net_worth_variation(param_list, down, up, bank, xlabel, ylabel, title)

def analysis_param(variable, param_list, scale, models_list, xlabel, ylabel, name, plotdir):
    result = compute_means(models_list, variable)
    plot_variation(param_list, result, scale, xlabel, ylabel, name, plotdir)


def plot_net_worth_agg(model, filename):
    plt.figure(figsize=(20,3))
    plt.plot(np.array(model.d.A_agg)/model.d.n_agents, label='downstream', color=(68/255, 119/255, 170/255))
#    plt.plot(np.array(model.u.A_agg)/model.u.n_agents, label='upstream', color='orange')
    plt.plot(np.array(model.b.A_agg)/model.b.n_agents, label='bank', color='green')
    plt.plot(np.array(model.u.A_agg)/model.u.n_agents, label='upstream', color='orange')
    plt.legend(fontsize=14)
    plt.locator_params(axis='y', nbins=5)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    #plt.xlabel('Time', fontsize=20)
    plt.ylabel('Net worth', fontsize=20)
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig(filename)
    plt.clf()

def plot_bankruptcy_agg(model, filename):
    plt.figure(figsize=(20,3))
    plt.plot(np.array(model.d.is_bankrupt_agg)*100/model.d.n_agents, label='downstream', color=(68/255, 119/255, 170/255))
   # plt.plot(np.array(model.u.is_bankrupt_agg)*100/model.u.n_agents, label='upstream', color='orange')
    plt.plot(np.array(model.b.is_bankrupt_agg)*100/model.b.n_agents, label='bank', color='green')
    plt.plot(np.array(model.u.is_bankrupt_agg)*100/model.u.n_agents, label='upstream', color='orange')

    plt.legend(fontsize=14)
    plt.locator_params(axis='y', nbins=5)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlabel('Time', fontsize=20)
    plt.ylabel('Bankruptcies (%)', fontsize=20)
    plt.tight_layout()
    plt.savefig(filename)
    plt.clf()

def plot_credit_agg(model, filename):
    plt.figure(figsize=(20,3))
    plt.plot(np.array(model.d.B_agg), label='downstream', color=(68/255, 119/255, 170/255))
    plt.plot(np.array(model.u.B_agg), label='upstream', color='orange')
    plt.legend(fontsize=14)
    plt.locator_params(axis='y', nbins=5)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    #plt.xlabel('Time', fontsize=20)
    plt.ylabel('Credit', fontsize=20)
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig(filename)
    plt.clf() 
