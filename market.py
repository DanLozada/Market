#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project 5. In this project, you will apply Object Oriented Programming to 
simulate the market demand/supply model.

Due on: September 30 2020. 11:59 PM

Comment: 6/10 
1. Equilibrium price derived is incorrect. 
2. Plots are defined incorrectly. In standard demand&supply model, y-axis is always 
price and x-axis is always quantity. 
3. Plots do not show consistency with the equilibrium price calculated. 
Note that your equ_price is 200, but there is no such equ_intercpet on your plot. 
4. section 5 is incorrect 

Please check the sample solution 

"""
import random
import uuid
import numpy as np
import matplotlib.pyplot as plt

random.seed(380)
# =============================================================================
# Section 1. Define classes
# =============================================================================
# 1.1. define a class Econ_agent
# attributes: id_number, budget
# methods: introduce_me(self):
# print out agent's id number and budget in sentences.


class Econ_agent:

    def __init__(self, id_number, budget):
        self.id_number = id_number
        self.budget = budget

    def introduce_me(self):
        print(
            f"Hi this econ agent has id {self.id_number}, and a budget {self.budget}")


class Consumer(Econ_agent):

    def __init__(self, id_number, budget, preference):
        super().__init__(id_number, budget)
        self.preference = preference
        self.wtp = self.budget * self.preference

    def buying(self, price):
        if self.wtp > price:
            return 1


class Producer(Econ_agent):

    def __init__(self, id_number, budget, opp_cost):
        super().__init__(id_number, budget)
        self.opp_cost = opp_cost

    def selling(self, price):
        quantity_supplied = self.budget / self.opp_cost

        if price > self.opp_cost:
            return quantity_supplied

    # This method is used on the last portion of the project to simulate a change in demand
    def change_opp_cost(self, percent_of_current_opp_cost):
        self.opp_cost = self.opp_cost * percent_of_current_opp_cost


# =============================================================================
# Section2. generate objects
# =============================================================================
"""
2.1 generate a list of 200 consumer each has a unique id number, budget is determined by a random draw
    from a normal distribution, set the normal distribution mean = 500, s.d. = 100, preference is determined
    by a random draw from a uniform distribution [0,1]
"""

consumers = [Consumer(uuid.uuid4(), random.normalvariate(500, 100), random.randint(0, 1)) for i in range(201)]

"""
2.2 generate a list of 200 producers each has a unique id number budget is determined by a random draw from
 a UNIFORM distribution [10,800], opp_cost is determined by a random draw from uniform distribution [100,200]
"""

producers = [Producer(uuid.uuid4(), np.random.uniform(
    10, 800, None), np.random.uniform(100, 200, None)) for i in range(201)]

# =============================================================================
# Section 3. Simulate the market mechanism, and find the equilibrium
# =============================================================================

"""
See section 4 for the solution to this problem. The last three values returned
by sim_market(start, end) give you the eq_price, eq_demand, eq_supply 
"""

# #=============================================================================
# # Section4. Define the demand curve and supply curve
# #=============================================================================
# # 4.1-4.2: Helper function to simulate demand and supply for a range of prices

# This is a little helper function that adds all of the elements in a list together


def sum_items(my_list):
    sum = 0
    for i in my_list:
        sum += i
    return sum


"""
This function simulates the market and return data for a given price range. 
for example we may want to evaluate our consumers and producers from a start
price to an end price
"""


def sim_market(start, end):
    supply = []
    demand = []
    prices = []

    while start <= end:
        temp_sup = []
        temp_dem = []

        for producer in producers:
            if producer.selling(start) != None:
                temp_sup.append(producer.selling(start))

        for consumer in consumers:
            if consumer.buying(start) != None:
                temp_dem.append(consumer.buying(start))

        prices.append(start)
        q_sup = sum_items(temp_sup)
        q_dem = sum_items(temp_dem)

        supply.append(q_sup)
        demand.append(q_dem)

        if q_dem - q_sup < 5:
            eq_demand = q_dem
            eq_supply = q_sup
            eq_price = start

        start += 1

    return demand, supply, prices, eq_price, eq_demand, eq_supply

sim_demand, sim_supply, sim_prices, eq_price, eq_demand, eq_supply = sim_market(100, 200)

# # 4.3 visualize the demand and supply, see if it makes sense.


def plot_supply_vs_demand(demand, supply, prices):
    plt.style.use('seaborn')

    fig = plt.figure(figsize=(10, 8))

    ax = fig.add_subplot(111)

    ax.plot(prices, supply, 'r', label='Supply')
    ax.plot(prices, demand, 'g', label='Demand')

    ax.set_title('Supply vs Demand')
    ax.set_ylabel('Quantity')
    ax.set_xlabel('Price')
    ax.legend()

    plt.show()


plot_supply_vs_demand(sim_demand, sim_supply, sim_prices)

# #=============================================================================
# # Section 5. Changes in supply
# #=============================================================================
# # imagine there is a technology improvement, reduce the average opp_cost by 5%
# # run a simulation to find the new market equilibrium
# # visualize the change graphically


def change_supply(percent_of_current_opp):
    for i in range(len(producers)):
        producers[i].change_opp_cost(percent_of_current_opp)

    sim_demand, sim_supply, sim_prices, eq_price, eq_demand, eq_supply = sim_market(
        100, 200)

    plot_supply_vs_demand(sim_demand, sim_supply, sim_prices)


change_supply(.95)
