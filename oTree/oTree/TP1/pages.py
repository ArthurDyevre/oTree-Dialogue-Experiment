from otree.api import Currency as c, currency_range
from otree.models import player, group
from itertools import chain
from ._builtin import Page, WaitPage
from .models import Constants, Player
import time
import numpy as np
import random
import eliciting_beliefs_rt.database

#Global variables to integrate into oTree
# Matrices could be moved to protected enviroment e.g. database or
# Matrices as database work for oTree 2.2.4
number_of_students = 40
number_of_rounds = 100
matrix = [[0 for x0 in range(number_of_rounds)] for y0 in range(number_of_students)]
matrix_nature = [[0 for x0 in range(number_of_rounds)] for y0 in range(number_of_students)]
matrix_beliefs = [[0 for x1 in range(number_of_rounds)] for y1 in range(number_of_students)]
matrix_toString = [[0 for x2 in range(number_of_rounds)] for y2 in range(number_of_students)]
matrix_beliefs_toString = [[0 for x3 in range(number_of_rounds)] for y3 in range(number_of_students)]
matrix_lottery_risks = [[0 for x0 in range(2)] for y0 in range(number_of_students)] # lottery is column 1, risk is column 2
count = 0
matrix_finished = []
matrix_finished.clear()



#Additional functions
def get_payoff_p1(self, sent_amount, sent_back_amount):
    type = random.randrange(1, 3, 1)
    i = (2 * self.group.id_in_subsession) - 2
    j = self.round_number - 1
    if type == 1:
        matrix_nature[i][j] = "hawkish"
    if type == 2:
        matrix_nature[i][j] = "dovish"

    if sent_amount == 'Exert restrain':
        if type == 1: # type = hawkish
            return 4
        if type == 2: # type = dovish
            return 6
    if sent_amount == 'Be assertive' and sent_back_amount == 'Do not challenge':
        return 7
    if sent_amount == 'Be assertive' and sent_back_amount == 'Challenge':
        return -4

def get_payoff_p2(sent_amount, sent_back_amount):
    if sent_amount == 'Exert restrain':
        return 4
    if sent_amount == 'Be assertive' and sent_back_amount == 'Do not challenge':
        return 1
    if sent_amount == 'Be assertive' and sent_back_amount == 'Challenge':
        return -4

def get_belief_payoff_p1(sent_belief, sent_back_amount):
    if sent_back_amount == 'Challenge':
        prob = sent_belief/100
        p_tilda = ((2-pow((1-prob),2)))/2
        p = np.random.binomial(1, p_tilda, 1)
        if p == 0:
            return 0.05
        else:
            return 0.15

    if sent_back_amount == 'Do not challenge':
        prob = sent_belief/100
        p_tilda = (2-pow(prob,2))/2
        p = np.random.binomial(1, p_tilda, 1)
        if p == 0:
            return 0.05
        else:
            return 0.15

def get_belief_payoff_p2(sent_back_belief, sent_amount):
    if sent_amount == "Be assertive":
        prob = sent_back_belief/100
        p_tilda = (2-pow(1-prob,2))/2
        p = np.random.binomial(1, p_tilda, 1)
        if p == 0:
            return 0.05
        else:
            return 0.15

    if sent_amount == "Exert restrain":
        prob = sent_back_belief/100
        p_tilda = (2-pow(prob,2))/2
        p = np.random.binomial(1, p_tilda, 1)
        if p == 0:
            return 0.05
        else:
            return 0.15


class Send(Page):

    form_model = 'group'
    form_fields = ['sent_amount']

    def is_displayed(self):
        return self.player.id_in_group == 1 and  self.round_number <= Constants.rt[self.group.id_in_subsession-1]

class Eliciting_Beliefs_P1(Page):

    form_model = 'group'
    form_fields = ['sent_belief']

    def is_displayed(self):
        return self.player.id_in_group == 1 and  self.round_number <= Constants.rt[self.group.id_in_subsession-1]


class SendBack(Page):

    form_model = 'group'
    form_fields = ['sent_back_amount']

    def is_displayed(self):
        return self.player.id_in_group == 2 and self.round_number <= Constants.rt[self.group.id_in_subsession-1]

class Eliciting_Beliefs_P2(Page):

    form_model = 'group'
    form_fields = ['sent_back_belief']

    def is_displayed(self):
        return self.player.id_in_group == 2 and self.round_number <= Constants.rt[self.group.id_in_subsession-1]

class Results1(Page):
    def is_displayed(self):
        return self.round_number < Constants.rt[self.group.id_in_subsession-1]
    def vars_for_template(self):
        i = 2 * self.group.id_in_subsession - 2
        return {
            'matrix_p1': np.add(matrix[i],matrix_beliefs[i]),
            'matrix_p2': np.add(matrix[i+1],matrix_beliefs[i+1]),
            'concat_p': zip(np.add(matrix[i], matrix_beliefs[i]), np.add(matrix[i + 1], matrix_beliefs[i + 1]),matrix_toString[i],matrix_toString[i + 1],matrix_beliefs_toString[i + 1],matrix_beliefs_toString[i], matrix_nature[i]),
            'matrix_strategy_p1': matrix_toString[i],
            'matrix_strategy_p2': matrix_toString[i + 1],
            'matrix_belief_p1': matrix_beliefs_toString[i],
            'matrix_belief_p2': matrix_beliefs_toString[i + 1],
            'round': self.round_number,
            'rt': Constants.rt[self.group.id_in_subsession-1]
        }



class Results(Page):

    def is_displayed(self):
        return self.round_number == Constants.rt[self.group.id_in_subsession-1]
    def vars_for_template(self):
        i = 2*self.group.id_in_subsession-2
        p1_tot = c(sum(matrix[i]))/Constants.rt[self.group.id_in_subsession-1] + c(sum(matrix_beliefs[i]))
        p2_tot = c(sum(matrix[i+1]))/Constants.rt[self.group.id_in_subsession-1] + c(sum(matrix_beliefs[i+1]))

        return {
            'player1_total': p1_tot,
            'player2_total': p2_tot,
            'matrix_p1': np.add(matrix[i],matrix_beliefs[i]),
            'matrix_p2': np.add(matrix[i+1],matrix_beliefs[i+1]),
            'concat_p': zip(np.add(matrix[i], matrix_beliefs[i]), np.add(matrix[i + 1], matrix_beliefs[i + 1]),matrix_toString[i],matrix_toString[i + 1],matrix_beliefs_toString[i + 1],matrix_beliefs_toString[i], matrix_nature[i]),
            'matrix_strategy_p1': matrix_toString[i],
            'matrix_strategy_p2': matrix_toString[i+1],
            'matrix_belief_p1': matrix_beliefs_toString[i],
            'matrix_belief_p2': matrix_beliefs_toString[i+1],
            'round': self.round_number,
            'count': len(matrix_finished),
            'num_groups': len(self.subsession.get_groups()),
        }



class WaitForP1(WaitPage):
    pass


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        print("update!")
        print(Constants.num_rounds)
        print(self.round_number)

        for i in self.group.get_players():
            if i.id_in_group ==1:
                p = i
        if self.round_number == 1:
            print("group: ", self.group.id_in_subsession)
            print("number of rounds: ",Constants.rt[self.group.id_in_subsession-1])


        if self.round_number != Constants.rt[self.group.id_in_subsession-1]:
            group = self.group
            p1 = group.get_player_by_id(1)
            p2 = group.get_player_by_id(2)
            p1.payoff = get_payoff_p1(p,group.sent_amount, group.sent_back_amount)
            p2.payoff = get_payoff_p2(group.sent_amount, group.sent_back_amount)

            i = (2 * self.group.id_in_subsession) - 2
            j = self.round_number - 1

            matrix[i][j] = p1.payoff
            matrix_beliefs[i][j] = get_belief_payoff_p1(group.sent_belief, group.sent_back_amount)
            matrix_toString [i][j] = group.sent_amount
            if group.sent_belief >= 50:
                matrix_beliefs_toString [i][j] = str(group.sent_belief) + "%"
            else:
                matrix_beliefs_toString [i][j] = str(group.sent_belief) + "%"

            matrix[i + 1][j] = p2.payoff
            matrix_beliefs[i + 1][j] = get_belief_payoff_p2(group.sent_back_belief, group.sent_amount)
            matrix_toString[i + 1][j] = group.sent_back_amount
            if group.sent_back_belief >= 50:
                matrix_beliefs_toString[i + 1][j] = str(group.sent_back_belief)  + "%"
            else:
                matrix_beliefs_toString[i + 1][j] = str(group.sent_back_belief) + "%"

        if self.round_number == Constants.rt[self.group.id_in_subsession-1]:
            group = self.group
            p1 = group.get_player_by_id(1)
            p2 = group.get_player_by_id(2)
            p1.payoff = get_payoff_p1(p,group.sent_amount, group.sent_back_amount)
            p2.payoff = get_payoff_p2(group.sent_amount, group.sent_back_amount)

            i = (2 * self.group.id_in_subsession) - 2
            j = self.round_number-1

            matrix[i][j] = p1.payoff
            matrix_beliefs[i][j] = get_belief_payoff_p1(group.sent_belief, group.sent_back_amount)
            matrix_toString [i][j] = group.sent_amount
            if group.sent_belief >= 50:
                matrix_beliefs_toString [i][j] = str(group.sent_belief) + "%"
            else:
                matrix_beliefs_toString [i][j] = str(group.sent_belief) + "%"

            matrix[i + 1][j] = p2.payoff
            matrix_beliefs[i + 1][j] = get_belief_payoff_p2(group.sent_back_belief, group.sent_amount)
            matrix_toString[i + 1][j] = group.sent_back_amount
            if group.sent_back_belief >= 50:
                matrix_beliefs_toString[i + 1][j] = str(group.sent_back_belief) + "%"
            else:
                matrix_beliefs_toString[i + 1][j] = str(group.sent_back_belief) + "%"

            matrix_finished.append(1)
            print(matrix_finished)


class Summary(Page):

    def vars_for_template(self):
        i = 2*self.group.id_in_subsession-2
        p1_tot_EBRT = c(sum(matrix[i]))/Constants.rt[self.group.id_in_subsession-1] + c(sum(matrix_beliefs[i]))
        p2_tot_EBRT = c(sum(matrix[i+1]))/Constants.rt[self.group.id_in_subsession-1] + c(sum(matrix_beliefs[i+1]))

        classifier = 'none'
        if self.player.id_in_group == 1:
            classifier = 'A'
            EB_score = "Your score is " + str(p1_tot_EBRT) + " and " + "your opponent scored " + str(p2_tot_EBRT)
            t_score = float(self.participant.vars['lottery_score']) + float(self.participant.vars['risk_score']) + float(p1_tot_EBRT)

        if self.player.id_in_group == 2:
            classifier = 'B'
            EB_score = "Your score is " + str(p2_tot_EBRT) + " and " + "your opponent scored " + str(p1_tot_EBRT)
            t_score = float(self.participant.vars['lottery_score']) + float(self.participant.vars['risk_score']) + float(p2_tot_EBRT)

        games = ["Lottery", "Risk", "Elicing Beliefs"]
        scores = [self.participant.vars['lottery_score'], self.participant.vars['risk_score'], EB_score ]


        return {
            'concat_p': zip(games,scores),
            'classifier': classifier,
            'total': t_score
        }
    def is_displayed(self):
        return self.round_number == Constants.rt[self.group.id_in_subsession-1]

class Questionaire(Page):
    form_model = 'player'
    form_fields = ['gender','age','studies','question_4','question_5','question_6']

    def vars_for_template(self):
        return {
            'count': len(matrix_finished),
            'num_groups': len(self.subsession.get_groups()),
        }
    def is_displayed(self):
        return self.round_number == Constants.rt[self.group.id_in_subsession-1]

page_sequence = [
    Eliciting_Beliefs_P2,
    Send,
    Eliciting_Beliefs_P1,
    WaitForP1,
    SendBack,
    ResultsWaitPage,
    Results1,
    Results,
    Questionaire,
    Summary,
]