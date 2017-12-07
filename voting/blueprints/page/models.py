#!/usr/bin/env python

from voting.extensions import db
from sqlalchemy import or_


class ElectorateStats(db.Model):
	__bind_key__ = 'sqlite'
	__tablename__ = 'electorate_stats'

	area_name = db.Column('area_name', db.String, primary_key=True)
	total_population = db.Column('total_population', db.Integer)
	voting_rights = db.Column('voting_rights', db.Integer)
	half_voting_rights = db.Column('half_voting_rights', db.Integer)

	def __init__(self, **kwargs):
		super(ElectorateStats, self).__init__(**kwargs)

	def _serialize(self):
		return {
			'area': self.area_name,
			'population': self.total_population,
			'voting': self.voting_rights,
			'half': self.half_voting_rights
		}

	@classmethod
	def all(cls):
		"""
		All the records
		:return:
		"""
		q = db.session.query(
			ElectorateStats.area_name,
			ElectorateStats.half_voting_rights
		).order_by(ElectorateStats.area_name.asc()).all()
		return q

	@classmethod
	def search(cls, state):
		"""
		Return only one state
		:param state:
		:return:
		"""
		q = db.session.query(
			ElectorateStats.area_name,
			ElectorateStats.total_population,
			ElectorateStats.voting_rights,
			ElectorateStats.half_voting_rights
		).filter(ElectorateStats.area_name.is_(state)).first()

		return q


class ElectorateVotes(db.Model):
	__bind_key__ = 'sqlite'
	__tablename__ = 'electorate_votes'

	area_name = db.Column('area_name', db.String, primary_key=True)
	votes = db.Column('votes', db.Integer)

	def __init__(self, **kwargs):
		super(ElectorateVotes, self).__init__(**kwargs)


class Voting(db.Model):
	__bind_key__ = 'sqlite'
	__tablename__ = 'voting'

	area_name = db.Column('area_name', db.String, primary_key=True)
	votes = db.Column('votes', db.Integer)
	proportions = db.Column('proportions', db.Float)

	def __init__(self, **kwargs):
		super(Voting, self).__init__(**kwargs)

	@classmethod
	def get_area_votes(cls):
		q = db.session.query(
			Voting.area_name,
			Voting.votes
		).order_by(Voting.proportions.desc()).all()

		return q

	@classmethod
	def get_area_votes_proportions(cls, split=False):
		q1 = db.session.query(
			Voting.area_name,
			Voting.votes,
			Voting.proportions
		).order_by(Voting.proportions.desc()).all()

		# https://www.270towin.com/content/split-electoral-votes-maine-and-nebraska
		q2 = db.session.query(
			Voting.area_name,
			Voting.votes,
			Voting.proportions
		).filter(or_(
			Voting.area_name.isnot('Main'),
			Voting.area_name.isnot('Nebraska')
		)).all()

		if split:
			return q2
		else:
			return q1

