from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from otree.models import group, player
import numpy as np
import random
author = 'Sarah Joseph, Supervised by Nicolas Lampach'
research_group = 'Euthority: Conflict and cooperation in the European Union legal system'

doc = """
Judicial experiment with random termination
"""

class Subsession(BaseSubsession):
    def creating_session(self):
        if Constants.p == 1:
            matrix = self.get_group_matrix()
            t1 = matrix[0][0]
            matrix[0][0] = matrix[0][1]
            matrix[0][1] = t1
            self.set_group_matrix(matrix)


class Constants(BaseConstants):
    name_in_url = 'euthority_game'
    players_per_group = 2

    endowment = c(10)
    multiplication_factor = 3

    p = random.randrange(1, 3, 1)
    rt = [4]*10
    num_rounds = 4

class Player(BasePlayer):


    sent_amount = models.StringField(
        choices=['Exert restrain', 'Be assertive'],
        widget=widgets.RadioSelect
    )
    sent_back_amount = models.StringField(
        choices=['Do not challenge', 'Challenge'],
        widget=widgets.RadioSelect
    )


class Group(BaseGroup):
    def get_payoff_p1(self):
        return self.set_payoff_p1(player.sent_amount, player.sent_back_amount)

    def get_payoff_p2(self):
        return self.set_payoff_p2(self.sent_amount, self.sent_back_amount)

    sent_amount = models.StringField(
        choices=['Exert restrain', 'Be assertive'],
        widget=widgets.RadioSelect
    )

    sent_back_amount = models.StringField(
        choices=['Do not challenge', 'Challenge'],
        widget=widgets.RadioSelect
    )

