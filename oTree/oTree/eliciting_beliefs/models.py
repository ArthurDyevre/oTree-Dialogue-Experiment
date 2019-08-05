from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from otree.models import group, player
import numpy as np
import random
author = 'Sarah Joseph (Supervised by Nicolas Lampach)'

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
    name_in_url = 'eliciting_beliefs'
    players_per_group = 2

    endowment = c(10)
    multiplication_factor = 3

    p = random.randrange(1, 3, 1)
    x = np.random.binomial(3, 0.5, 10) + np.random.binomial(3, 0.5, 10) + np.random.binomial(3, 0.5, 10)
    rt = np.array(x).tolist()

    num_rounds = 4

class Player(BasePlayer):


    sent_amount = models.StringField(
        choices=['Exert restrain', 'Be assertive'],
        widget=widgets.RadioSelect
    )

    sent_belief = models.IntegerField(verbose_name='sent belief',
                                        min=0, max=100,
                                        initial=50,
                                        widget=widgets.SliderInput())


    sent_back_amount = models.StringField(
        choices=['Do not challenge', 'Challenge'],
        widget=widgets.RadioSelect
    )

    sent_back_belief = models.IntegerField(verbose_name='sent back belief',
                                        min=0, max=100,
                                        initial=50,
                                        widget=widgets.SliderInput())


class Group(BaseGroup):
    def get_payoff_p1(self):
        return self.set_payoff_p1(player.sent_amount, player.sent_back_amount)

    def get_payoff_p2(self):
        return self.set_payoff_p2(self.sent_amount, self.sent_back_amount)

    sent_amount = models.StringField(
        choices=['Exert restrain', 'Be assertive'],
        widget=widgets.RadioSelect
    )

    sent_belief = models.IntegerField(verbose_name='sent belief',
                                        min=0, max=100,
                                        initial=50,
                                        widget=widgets.SliderInput())

    sent_back_amount = models.StringField(
        choices=['Do not challenge', 'Challenge'],
        widget=widgets.RadioSelect
    )

    sent_back_belief = models.IntegerField(verbose_name='sent back belief',
                                        min=0, max=100,
                                        initial=50,
                                        widget=widgets.SliderInput())
