from otree.api import Currency as c, currency_range
from otree.models import player, group

from random_termination import models
from ._builtin import Page, WaitPage
from .models import Constants, Player
import numpy as np
#Global variables to integrate into oTree

number_of_students = 40
number_of_rounds = 100
matrix = [[0 for x0 in range(number_of_rounds)] for y0 in range(number_of_students)]
matrix_beliefs = [[0 for x1 in range(number_of_rounds)] for y1 in range(number_of_students)]
matrix_toString = [[0 for x2 in range(number_of_rounds)] for y2 in range(number_of_students)]
matrix_beliefs_toString = [[0 for x3 in range(number_of_rounds)] for y3 in range(number_of_students)]

#Additional functions
def get_payoff_p1(sent_amount, sent_back_amount):
    if sent_amount == 'Exert restrain':
        return 2
    if sent_amount == 'Be assertive' and sent_back_amount == 'Do not challenge':
        return 4
    if sent_amount == 'Be assertive' and sent_back_amount == 'Challenge':
        return -2

def get_belief_payoff_p1(sent_belief, sent_back_amount):
    # Random binomial
    # numpy.random.binomial(n, p, size=None)
    # where n is the number of trials, p is the probability of success, and N is the number of successes.
    # https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.random.binomial.html

    if sent_back_amount == 'Challenge': # at 100 percent
        prob = sent_belief/100
        p_tilda = ((1-pow((1-prob),2)))
        p = np.random.binomial(1, p_tilda, 1)
        if p == 0:
            return 0.05
        else:
            return 0.15

    if sent_back_amount == 'Do not challenge': # at 0 percent
        prob = sent_belief/100
        p_tilda = (1-pow(prob,2))
        p = np.random.binomial(1, p_tilda, 1)
        if p == 0:
            return 0.05
        else:
            return 0.15

def get_belief_payoff_p2(sent_back_belief, sent_amount):

    if sent_amount == "Exert restrain": # at 0 percent
        prob = sent_back_belief/100
        p_tilda = (1-pow(prob,2))
        p = np.random.binomial(1, p_tilda, 1)
        if p == 0:
            return 0.05
        else:
            return 0.15

    if sent_amount == "Be assertive": # at 100 percent
        prob = sent_back_belief/100
        p_tilda = (1-pow(1-prob,2))
        p = np.random.binomial(1, p_tilda, 1)
        if p == 0:
            return 0.05
        else:
            return 0.15






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

class Eliciting_Beliefs_P1(Page):

    form_model = 'group'
    form_fields = ['sent_belief']

    def is_displayed(self):
        return self.player.id_in_group == 1


class SendBack(Page):

    form_model = 'group'
    form_fields = ['sent_back_amount']

    def is_displayed(self):
        return self.player.id_in_group == 2

class Eliciting_Beliefs_P2(Page):

    form_model = 'group'
    form_fields = ['sent_back_belief']

    def is_displayed(self):
        return self.player.id_in_group == 2

class Results1(Page):
    def is_displayed(self):
        return self.round_number < 4
    def vars_for_template(self):
        i = 2 * self.group.id_in_subsession - 2
        return {
            'matrix_p1': np.add(matrix[i],matrix_beliefs[i]),
            'matrix_p2': np.add(matrix[i+1],matrix_beliefs[i+1]),
            'concat_p': zip(np.add(matrix[i], matrix_beliefs[i]), np.add(matrix[i + 1], matrix_beliefs[i + 1]),matrix_toString[i],matrix_toString[i + 1],matrix_beliefs_toString[i],matrix_beliefs_toString[i + 1]),
            'matrix_strategy_p1': matrix_toString[i],
            'matrix_strategy_p2': matrix_toString[i + 1],
            'matrix_belief_p1': matrix_beliefs_toString[i],
            'matrix_belief_p2': matrix_beliefs_toString[i + 1],
            'round': self.round_number,
            'rt': Constants.rt[self.group.id_in_subsession-1]
        }



class Results(Page):

    def is_displayed(self):
        return self.round_number == 4
    def vars_for_template(self):
        i = 2*self.group.id_in_subsession-2
        p1_tot = c(sum(matrix[i]))/4 + c(sum(matrix_beliefs[i]))
        p2_tot = c(sum(matrix[i+1]))/4 + c(sum(matrix_beliefs[i+1]))
        return {
            'player1_total': p1_tot,
            'player2_total': p2_tot,
            'matrix_p1': np.add(matrix[i],matrix_beliefs[i]),
            'matrix_p2': np.add(matrix[i+1],matrix_beliefs[i+1]),
            'concat_p': zip(np.add(matrix[i], matrix_beliefs[i]), np.add(matrix[i + 1], matrix_beliefs[i + 1]),matrix_toString[i],matrix_toString[i + 1],matrix_beliefs_toString[i],matrix_beliefs_toString[i + 1]),
            'matrix_strategy_p1': matrix_toString[i],
            'matrix_strategy_p2': matrix_toString[i+1],
            'matrix_belief_p1': matrix_beliefs_toString[i],
            'matrix_belief_p2': matrix_beliefs_toString[i+1],
            'round': self.round_number,
        }



class WaitForP1(WaitPage):
    pass
class IntermediaryResults(Page):
    pass


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        if self.round_number != 4:
            group = self.group
            p1 = group.get_player_by_id(1)
            p2 = group.get_player_by_id(2)
            p1.payoff = get_payoff_p1(group.sent_amount, group.sent_back_amount)
            p2.payoff = get_payoff_p2(group.sent_amount, group.sent_back_amount)

            i = (2 * self.group.id_in_subsession) - 2
            j = self.round_number - 1

            matrix[i][j] = p1.payoff
            matrix_beliefs[i][j] = get_belief_payoff_p1(group.sent_belief, group.sent_back_amount)
            matrix_toString [i][j] = group.sent_amount
            if group.sent_belief >= 50:
                matrix_beliefs_toString [i][j] = "Assertive: " + str(group.sent_belief)
            else:
                matrix_beliefs_toString [i][j] = "Exert restraint: " + str(group.sent_belief)

            matrix[i + 1][j] = p2.payoff
            matrix_beliefs[i + 1][j] = get_belief_payoff_p2(group.sent_back_belief, group.sent_amount)
            matrix_toString[i + 1][j] = group.sent_back_amount
            if group.sent_back_belief >= 50:
                matrix_beliefs_toString[i + 1][j] = "Challenge: " + str(group.sent_back_belief)
            else:
                matrix_beliefs_toString[i + 1][j] = "Do not challenge: " + str(group.sent_back_belief)

        if self.round_number == 4:
            group = self.group
            p1 = group.get_player_by_id(1)
            p2 = group.get_player_by_id(2)
            p1.payoff = get_payoff_p1(group.sent_amount, group.sent_back_amount)
            p2.payoff = get_payoff_p2(group.sent_amount, group.sent_back_amount)

            i = (2 * self.group.id_in_subsession) - 2
            j = self.round_number-1

            matrix[i][j] = p1.payoff
            matrix_beliefs[i][j] = get_belief_payoff_p1(group.sent_belief, group.sent_back_amount)
            matrix_toString [i][j] = group.sent_amount
            if group.sent_belief >= 50:
                matrix_beliefs_toString [i][j] = "Assertive: " + str(group.sent_belief)
            else:
                matrix_beliefs_toString [i][j] = "Exert restraint: " + str(group.sent_belief)

            matrix[i + 1][j] = p2.payoff
            matrix_beliefs[i + 1][j] = get_belief_payoff_p2(group.sent_back_belief, group.sent_amount)
            matrix_toString[i + 1][j] = group.sent_back_amount
            if group.sent_back_belief >= 50:
                matrix_beliefs_toString[i + 1][j] = "Challenge: " + str(group.sent_back_belief)
            else:
                matrix_beliefs_toString[i + 1][j] = "Do not challenge: " + str(group.sent_back_belief)

class AllGroupsWaitPage(WaitPage):
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number == 4

class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 4

page_sequence = [
    Eliciting_Beliefs_P2,
    Send,
    Eliciting_Beliefs_P1,
    WaitForP1,
    SendBack,
    ResultsWaitPage,
    Results1,
    Results,
    AllGroupsWaitPage,
    Instructions,
]
