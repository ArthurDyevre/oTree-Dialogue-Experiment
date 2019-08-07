from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from otree.models import group, player
import numpy as np
import random
author = 'Sarah Joseph, Supervised by Dr. Nicolas Lampach'

doc = """
Lottery experiment, risk experiments, and judicial experiment with random termination, K.U.L.
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
    name_in_url = 'eliciting_beliefs_rt_TP12'
    players_per_group = 2

    endowment = c(10)
    multiplication_factor = 3

    p = random.randrange(1, 3, 1)
    x = np.random.negative_binomial(3, 0.5, 10) + np.random.negative_binomial(3, 0.5, 10) + np.random.negative_binomial(3, 0.5, 10)
    rt = np.array(x).tolist()

    num_rounds = 20


class Player(BasePlayer):

    gender = models.StringField(
        choices=['Male', 'Female', 'Other'],
        widget=widgets.RadioSelect
    )

    age = models.IntegerField()

    studies = models.StringField(
        choices=['Social Sciences', 'Hard Sciences'],
        widget=widgets.RadioSelect
    )

    question_4 = models.IntegerField(verbose_name='question_4',
                                      min=0, max=6,
                                      widget=widgets.SliderInput())


    question_5 = models.IntegerField(verbose_name='question_5',
                                      min=0, max=6,
                                      widget=widgets.SliderInput())

    question_6 = models.IntegerField(verbose_name='question_6',
                                      min=0, max=10,
                                      widget=widgets.SliderInput())

    #############################

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

    #############################

    lottery1 = models.StringField(
        choices=['Accept','Reject'],
        widget=widgets.RadioSelect
    )
    lottery2 = models.StringField(
        choices=['Accept','Reject'],
        widget=widgets.RadioSelect
    )
    lottery3 = models.StringField(
        choices=['Accept','Reject'],
        widget=widgets.RadioSelect
    )
    lottery4 = models.StringField(
        choices=['Accept','Reject'],
        widget=widgets.RadioSelect
    )
    lottery5 = models.StringField(
        choices=['Accept','Reject'],
        widget=widgets.RadioSelect
    )
    lottery6 = models.StringField(
        choices=['Accept','Reject'],
        widget=widgets.RadioSelect
    )

    #############################

    risk1 = models.StringField(
        choices=['50% chance gaining 0 € and 50% chance of gaining 10 €.','0'],
        widget=widgets.RadioSelect
    )
    risk2 = models.StringField(
        choices=['50% chance gaining 0 € and 50% chance of gaining 10 €.','1'],
        widget=widgets.RadioSelect
    )
    risk3 = models.StringField(
        choices=['50% chance gaining 0 € and 50% chance of gaining 10 €.','2'],
        widget=widgets.RadioSelect
    )
    risk4 = models.StringField(
        choices=['50% chance gaining 0 € and 50% chance of gaining 10 €.','3'],
        widget=widgets.RadioSelect
    )
    risk5 = models.StringField(
        choices=['50% chance gaining 0 € and 50% chance of gaining 10 €.','4'],
        widget=widgets.RadioSelect
    )
    risk6 = models.StringField(
        choices=['50% chance gaining 0 € and 50% chance of gaining 10 €.','5'],
        widget=widgets.RadioSelect
    )
    risk7 = models.StringField(
        choices=['50% chance gaining 0 € and 50% chance of gaining 10 €.','6'],
        widget=widgets.RadioSelect
    )
    risk8 = models.StringField(
        choices=['50% chance gaining 0 € and 50% chance of gaining 10 €.','7'],
        widget=widgets.RadioSelect
    )
    risk9 = models.StringField(
        choices=['50% chance gaining 0 € and 50% chance of gaining 10 €.','8'],
        widget=widgets.RadioSelect
    )
    risk10 = models.StringField(
        choices=['50% chance gaining 0 € and 50% chance of gaining 10 €.','9'],
        widget=widgets.RadioSelect
    )
    risk11 = models.StringField(
        choices=['50% chance gaining 0 € and 50% chance of gaining 10 €.','10'],
        widget=widgets.RadioSelect
    )

    ############################ test buttons ############################
    test_button1 = models.IntegerField(choices=['1'],widget=widgets.RadioSelect)






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

