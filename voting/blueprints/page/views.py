#!/usr/bin/env python

from flask import Blueprint, redirect, url_for, current_app
from voting.blueprints.page.models import ElectorateStats, Voting
from pulp import *
import pandas as pd
import json

page = Blueprint('page', __name__)


def _get_data(model, cols=None):
	df = pd.DataFrame(
		[[ij for ij in i] for i in model],
		columns=cols
	)

	data = [
		dict(i) for i in df.to_dict('records')
	]

	return data


@page.route('/')
def index():
	data = _get_data(ElectorateStats.all(), cols=['state', 'population'])

	return json.dumps(data)


@page.route('/opt1')
def opt1():
	data = _get_data(Voting.get_area_votes(), cols=['state', 'votes'])

	"""
	Allocate two bins of different sizes
	bin[0] will contain all the states that will make a candidate lose
	bin[1] will contain all the states that will make a candidate win
	"""
	bins = [268, 270]
	binsCount = len(bins)

	"""
	Minimization problem
	"""
	problem = LpProblem("US Elections 2020", sense=LpMinimize)

	"""
	What are the possible assignments of states in one of the two bins
	"""
	assignments = {
		(state["state"], binNum): pulp.LpVariable(f'({state}, {binNum})', cat=pulp.LpBinary)
		for state in data
		for binNum in range(binsCount)
	}


	"""
	The two bins as variables
	"""
	the_bins = pulp.LpVariable.dicts("Bin used", range(binsCount), cat=pulp.LpBinary)

	# current_app.logger.debug(f'### {the_bins}')

	# Objective
	problem += lpSum(the_bins[i] for i in range(binsCount)), "Objective: allocate state votes in bins"

	# constraints
	"""
	A vote can only go into one of the two bins
	"""
	for state in data:
		problem += pulp.lpSum([assignments[(state['state'], i)] for i in range(binsCount)]) == 1, f"{state} in one bin"

	"""
	The sum of all electoral votes in one bin cannot be bigger than the size of the bin
	"""
	for i in range(binsCount):
		problem += lpSum(
			[state['votes'] * assignments[(state['state'], i)] for state in data]
		) <= bins[i] * the_bins[i], f'take all {i}'

	# current_app.logger.debug(f'### {problem}')

	# solver = pulp.PULP_CBC_CMD()
	solver = pulp.COIN_CMD()
	# solver = pulp.GLPK()
	# solver = None
	problem.solve(solver)

	"""
	Printing the results
	"""
	result = {}

	# is the problem feasible???
	if problem.status == 1:
		for i, j in assignments.items():
			if pulp.value(j):
				result.setdefault(i[1], []).append(i[0])
		return json.dumps(result)
	else:
		return 'NG'


@page.route('/opt2', defaults={'flag': 0})
@page.route('/opt2/<int:flag>')
def opt2(flag):
	"""
	Except Maine and Nebraska, the other states are winner take all policy
	:param flag:
	:return:
	"""
	if flag == 0:
		split = False
		constraint = 268
	else:
		"""
		We consider that Main & Nebraska went to the losing party
		"""
		split = True
		constraint = 259

	data = _get_data(Voting.get_area_votes_proportions(split=split), cols=['state', 'votes', 'proportions'])

	state = [i['state'] for i in data]
	votes = [i['votes'] for i in data]
	proportions = [i['proportions'] for i in data]

	"""
	Maximization problem
	"""
	problem = LpProblem("US Elections 2020", LpMaximize)

	"""
	Each state as a variable
	"""
	states = pulp.LpVariable.dicts("State", state, cat=pulp.LpBinary)

	"""
	Sum the votes that have a higher proportional representation
	"""
	problem += lpSum(s * p for s, p in zip(states.values(), proportions)), 'Objective'

	"""
	The sum of all electoral votes should be less than the constraint (268 for the losing team)
	"""
	problem += lpSum(s * v for s, v in zip(states.values(), votes)) <= constraint, 'Sum of electoral votes'

	# current_app.logger.debug(f"### {problem}")

	# solver = pulp.PULP_CBC_CMD()
	solver = pulp.COIN_CMD()
	# solver = GLPK()
	# solver = None
	problem.solve(solver)

	result = []

	if problem.status == 1:
		for i, j in states.items():
			if pulp.value(j):
				result.append(i)

		return json.dumps({'0': list(set(state) - set(result)), '1': result})
	else:
		return 'NG'


@page.route('/<state>')
def get_state(state):
	return str(ElectorateStats.search(state))
