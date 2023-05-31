from sectors.downstream import DownstreamSector
from sectors.upstream import UpstreamSector
from sectors.bank import BankSector
from func.connections import preferred_partner
from func.plots import plot_vars, plot_net_worth_agg, plot_bankruptcy_agg, plot_credit_agg

import numpy as np
import random
import string

class model():
    def __init__(self, periods=1000, n_agents_d=500, n_agents_u=250, n_agents_b=100, random_connection_probability=0.01,\
            random_sample_size=5, phi=2, beta=0.9, delta_d=0.5, delta_u=1, gamma=0.5, w_d=1, w_u=1, sigma=0.1, theta=0.05, alpha=0.5):
        self.n_agents_d = n_agents_d
        self.n_agents_u = n_agents_u
        self.n_agents_b = n_agents_b
        self.periods = periods
    
        self.random_connection_probability = random_connection_probability
        self.random_sample_size = random_sample_size
        self.phi=phi
        self.beta=beta
        self.delta_d=delta_d
        self.delta_u=delta_u
        self.gamma=gamma
        self.w_d=w_d
        self.w_u=w_u
        self.sigma=sigma
        self.theta=theta
        self.alpha=alpha

        # Initialize the connections' indices randomly
        self.DB_connection = np.random.randint(n_agents_b,size=n_agents_d).astype(int)
        self.DU_connection = np.random.randint(n_agents_u,size=n_agents_d).astype(int)
        self.UB_connection = np.random.randint(n_agents_b,size=n_agents_u).astype(int)

        # Instantiate sectors
        self.d = DownstreamSector(n_agents = self.n_agents_d, phi=self.phi, beta=self.beta, delta_d=self.delta_d, gamma=self.gamma,\
                w_d=self.w_d, sigma=self.sigma, theta=self.theta)
        self.u = UpstreamSector(n_agents = self.n_agents_u, alpha=self.alpha, delta_u=self.delta_u, w_u=self.w_u, sigma=self.sigma,\
                theta=self.theta)
        self.b = BankSector(n_agents = self.n_agents_b)

    def run(self):
        for i in range(self.periods):
            self.d.compute_firm_features()

            self.u.compute_firm_features(D_requested_intermediate_goods = self.d.Q, DU_connection = self.DU_connection)
            self.u.compute_bank_credit(B_net_worth = self.b.A, UB_connection = self.UB_connection)

            self.d.compute_bank_credit(B_net_worth = self.b.A, DB_connection = self.DB_connection)
            self.d.compute_profit(U_price = self.u.u, DU_connection = self.DU_connection)
            self.d.update_net_worth()

            self.u.compute_profit_and_bad_debt(is_bankrupt_D = self.d.is_bankrupt, DU_connection = self.DU_connection,\
                                 D_requested_intermediate_goods = self.d.Q)
            self.u.update_net_worth()

            self.b.compute_profit_and_bad_debt(DB_connection = self.DB_connection, UB_connection = self.UB_connection,\
                        D_bank_interest_rate = self.d.rb, U_bank_interest_rate = self.u.rb, D_bank_credit= self.d.B, \
                        U_bank_credit = self.u.B, is_bankrupt_D = self.d.is_bankrupt, is_bankrupt_U = self.u.is_bankrupt)
            self.b.update_net_worth()

            # If firms are connected to bankrupt agents, connect with another random agent
            self.DU_connection = np.where(self.u.is_bankrupt[self.DU_connection], np.random.randint(self.n_agents_u,size=self.n_agents_d), self.DU_connection)
            self.DB_connection = np.where(self.b.is_bankrupt[self.DB_connection], np.random.randint(self.n_agents_b,size=self.n_agents_d), self.DB_connection)
            self.UB_connection = np.where(self.b.is_bankrupt[self.UB_connection], np.random.randint(self.n_agents_b,size=self.n_agents_u), self.UB_connection)
    
            # Update net_worth(random value in [0,2]) and connections of bankrupt downstream firms
            self.d.A = np.where(self.d.is_bankrupt, 2*np.random.rand(self.n_agents_d), self.d.A)
            self.DU_connection = np.where(self.d.is_bankrupt, np.random.randint(self.n_agents_u,size = self.n_agents_d), self.DU_connection)
            self.DB_connection = np.where(self.d.is_bankrupt, np.random.randint(self.n_agents_b,size = self.n_agents_d), self.DB_connection)
    
            # Update net_worth(random value in [0,2]) and connections of bankrupt upstream firms
            self.u.A = np.where(self.u.is_bankrupt, 2*np.random.rand(self.n_agents_u), self.u.A)
            self.UB_connection = np.where(self.u.is_bankrupt, np.random.randint(self.n_agents_b, size = self.n_agents_u), self.UB_connection)
    
            # Update net_worth(random value in [0,2]) of bankrupt banks
            self.b.A = np.where(self.b.is_bankrupt, 2*np.random.rand(self.n_agents_b), self.b.A)
    
            # Update connections through the preferred-partner algorithm
            self.DU_connection = preferred_partner(self.DU_connection, self.u.A, random_connection_probability = self.random_connection_probability, random_sample_size = self.random_sample_size);
            self.DB_connection = preferred_partner(self.DB_connection, self.b.A, random_connection_probability = self.random_connection_probability, random_sample_size = self.random_sample_size);
            self.UB_connection = preferred_partner(self.UB_connection, self.b.A, random_connection_probability = self.random_connection_probability, random_sample_size = self.random_sample_size);
    
            self.d.append_aggregate_variables()
            self.u.append_aggregate_variables()
            self.b.append_aggregate_variables()

    def plot(self):
        list_to_plot=[[np.array(self.d.A_agg)/self.n_agents_d, 'Net worth - D'],\
                    [np.array(self.u.A_agg)/self.n_agents_u, 'Net worth - U'],\
                    [np.array(self.b.A_agg)/self.n_agents_b, 'Net worth - B'],\
                    [np.array(self.d.profit_agg)/self.n_agents_d, 'Profit - D'],\
                    [np.array(self.u.profit_agg)/self.n_agents_u, 'Profit - U'],\
                    [np.array(self.b.profit_agg)/self.n_agents_b, 'Profit - B'],\
                    [np.array(self.d.B_agg)/self.n_agents_d, 'Bank Cred - D'],\
                    [np.array(self.u.B_agg)/self.n_agents_u, 'Bank Cred - U'],\
                    [np.array(self.u.bad_debt_agg)/self.n_agents_u, 'Bad debt - U'],\
                    [np.array(self.b.bad_debt_agg)/self.n_agents_b, 'Bad debt - B'],\
                    [np.array(self.d.is_bankrupt_agg)/self.n_agents_d, 'Bankrupt - D'],\
                    [np.array(self.u.is_bankrupt_agg)/self.n_agents_u, 'Bankrupt - U'],\
                    [np.array(self.b.is_bankrupt_agg)/self.n_agents_b, 'Bankrupt - B']
                    ]
        random_sufix=''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(20))
        plot_vars(list_to_plot,"static/result_histograms_"+random_sufix)
        plot_net_worth_agg(self, "static/single_run_net_worth_" + random_sufix + ".jpg")
        plot_bankruptcy_agg(self, "static/single_run_bankruptcy_" + random_sufix + ".jpg")
        plot_credit_agg(self,"static/single_run_credit_" + random_sufix + ".jpg")

