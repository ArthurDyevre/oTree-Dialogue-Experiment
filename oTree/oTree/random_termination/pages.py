from otree.api import Currency as c, currency_range
from otree.models import player, group

from random_termination import models
from ._builtin import Page, WaitPage
from .models import Constants, Player
import numpy as np
#Global variables to integrate into oTree
from . import tests
number_of_students = 40
number_of_rounds = 100
matrix = [[0 for x in range(number_of_rounds)] for y in range(number_of_students)]
round_test = []

#Additional functions
def get_payoff_p1(sent_amount, sent_back_amount):
    if sent_amount == 'Exert restrain':
        return 2
    if sent_amount == 'Be assertive' and sent_back_amount == 'Do not challenge':
        return 4
    if sent_amount == 'Be assertive' and sent_back_amount == 'Challenge':
        return -2

def get_payoff_p2(sent_amount, sent_back_amount):
    if sent_amount == 'Exert restrain':
        return 2
    if sent_amount == 'Be assertive' and sent_back_amount == 'Do not challenge':
        return 0
    if sent_amount == 'Be assertive' and sent_back_amount == 'Challenge':
        return -2

class Send(Page):

    form_model = 'group'
    form_fields = ['sent_amount']

    def is_displayed(self):
        return self.player.id_in_group == 1

class SendBack(Page):

    form_model = 'group'
    form_fields = ['sent_back_amount']

    def is_displayed(self):
        return self.player.id_in_group == 2


class Results1(Page):
    def is_displayed(self):
        return self.round_number < Constants.rt[self.group.id_in_subsession-1]
    def vars_for_template(self):
        i = 2 * self.group.id_in_subsession - 2
        return {

            'matrix_p1': matrix[i],
            'matrix_p2': matrix[i+1],
            'round': self.round_number,
            'rt': Constants.rt[self.group.id_in_subsession-1]

        }

class Results(Page):

    def is_displayed(self):
        return self.round_number == Constants.rt[self.group.id_in_subsession-1]
    def vars_for_template(self):
        i = 2*self.group.id_in_subsession-2
        p1_tot = c(sum(matrix[i]))/c(Constants.rt[self.group.id_in_subsession - 1])
        p2_tot = c(sum(matrix[i+1]))/c(Constants.rt[self.group.id_in_subsession-1])
        return {
            'player1_total': p1_tot,
            'player2_total': p2_tot,
            'matrix_p1': matrix[i],
            'matrix_p2': matrix[i+1],
            'round': self.round_number,
        }


class WaitForP1(WaitPage):
    pass
class IntermediaryResults(Page):
    pass


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        if self.round_number != Constants.rt[self.group.id_in_subsession-1]:
            group = self.group
            p1 = group.get_player_by_id(1)
            p2 = group.get_player_by_id(2)
            p1.payoff = get_payoff_p1(group.sent_amount, group.sent_back_amount)
            p2.payoff = get_payoff_p2(group.sent_amount, group.sent_back_amount)

            i = (2 * self.group.id_in_subsession) - 2
            j = self.round_number - 1
            matrix[i][j] = p1.payoff
            matrix[i + 1][j] = p2.payoff

        if self.round_number == Constants.rt[self.group.id_in_subsession-1]:
            group = self.group
            p1 = group.get_player_by_id(1)
            p2 = group.get_player_by_id(2)
            p1.payoff = get_payoff_p1(group.sent_amount, group.sent_back_amount)
            p2.payoff = get_payoff_p2(group.sent_amount, group.sent_back_amount)

            i = (2 * self.group.id_in_subsession) - 2
            j = self.round_number-1
            matrix[i][j] = p1.payoff
            matrix[i + 1][j] = p2.payoff


page_sequence = [
    Send,
    WaitForP1,
    SendBack,
    ResultsWaitPage,
    Results1,
    Results,
]
