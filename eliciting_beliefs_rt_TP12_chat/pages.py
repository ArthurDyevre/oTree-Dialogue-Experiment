from otree.api import Currency as c, currency_range
from otree.models import player, group
from itertools import chain
from ._builtin import Page, WaitPage
from .models import Constants, Player
import time
import numpy as np
import random
import eliciting_beliefs_rt.database

#Global variables function as the database to integrate into oTree upon deployment, they work for oTree version 2.2.4
#-----------------------------------------------------------------------------------------------------------------------
number_of_students = 40
number_of_rounds = 100
matrix = [[0 for x0 in range(number_of_rounds)] for y0 in range(number_of_students)]
matrix_pi = [[0 for x0 in range(number_of_rounds)] for y0 in range(number_of_students)]
matrix_tau = [[0 for x0 in range(number_of_rounds)] for y0 in range(number_of_students)]

matrix_beliefs = [[0 for x1 in range(number_of_rounds)] for y1 in range(number_of_students)]
matrix_toString = [[0 for x2 in range(number_of_rounds)] for y2 in range(number_of_students)]
matrix_beliefs_toString = [[0 for x3 in range(number_of_rounds)] for y3 in range(number_of_students)]
matrix_lottery_risks = [[0 for x0 in range(2)] for y0 in range(number_of_students)] # proxy is column 1, risk is column 2
matrix_end = [False for y0 in range(number_of_students)]
count = 0
matrix_finished = []
matrix_finished.clear()
#-----------------------------------------------------------------------------------------------------------------------


#Additional functions
#----------------------------------------------------------------------------------
def get_payoff_p1(sent_amount, sent_back_amount,i,j):
    if sent_amount == 'Exert restrain':
        if matrix_pi[i][j] == "hawkish":  # type = hawkish
            return 4
        if matrix_pi[i][j] == "dovish":  # type = dovish
            return 6

    if sent_amount == 'Be assertive' and sent_back_amount == 'Do not challenge':
        return 7

    if sent_amount == 'Be assertive' and sent_back_amount == 'Challenge':
        if matrix_tau[i][j] == "hawkish": # type = hawkish
            return -4
        if matrix_tau[i][j] == "dovish": # type = dovish
            return -6

def get_payoff_p2(sent_amount, sent_back_amount,i,j):

    if sent_amount == 'Exert restrain':
        if matrix_pi[i][j] == "hawkish":
            return 4
        if matrix_pi[i][j] == "dovish":
            return 6

    if sent_amount == 'Be assertive' and sent_back_amount == 'Do not challenge':
        return 1

    if sent_amount == 'Be assertive' and sent_back_amount == 'Challenge':
        if matrix_tau[i][j] == "hawkish": # type = hawkish
            return -4
        if matrix_tau[i][j] == "dovish": # type = dovish
            return -6

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

    else:
        return 0

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



#-----------------------------------------------------------------------------------------

# Class construction of the pages
#-----------------------------------------------------------------------------------------

class Instructions(Page):

    # only display instruction in round 1
    # ----------------------------------------------------------------------------------------------------------------
    def is_displayed(self):
        i = 2 * self.group.id_in_subsession - 2
        return self.subsession.round_number == 1 and matrix_end[i] == False and matrix_end[i+1] == False

class Mid_Questionaire(Page):
    form_model = 'player'
    form_fields = ['mid_question_1','mid_question_2']

    def vars_for_template(self):
        return {
            'count': len(matrix_finished),
            'num_groups': len(self.subsession.get_groups()),
        }
    def is_displayed(self):
        i = 2 * self.group.id_in_subsession - 2
        return self.subsession.round_number == 1 and matrix_end[i] == False and matrix_end[i+1] == False


class Mid_Questionaire_Answers(Page):
    form_model = 'player'
    def vars_for_template(self):
        return {
            'count': len(matrix_finished),
            'num_groups': len(self.subsession.get_groups()),
        }
    def is_displayed(self):
        i = 2 * self.group.id_in_subsession - 2
        return self.subsession.round_number == 1 and matrix_end[i] == False and matrix_end[i+1] == False

class AllGroupsWaitPage(WaitPage):
    wait_for_all_groups = True
    def is_displayed(self):
        i = 2 * self.group.id_in_subsession - 2
        return self.subsession.round_number == 1 and matrix_end[i] == False and matrix_end[i + 1] == False

class Send(Page):

    form_model = 'group'
    form_fields = ['sent_amount']

    def is_displayed(self):
        i = 2 * self.group.id_in_subsession - 2
        return self.player.id_in_group == 1 and  self.round_number <= Constants.rt[self.group.id_in_subsession-1] and matrix_end[i] == False and matrix_end[i+1] == False

    def vars_for_template(self):
        i = 2 * self.group.id_in_subsession - 2
        j = self.round_number - 1

        pi = random.randrange(1, 3, 1)
        if pi == 1:
            matrix_pi[i][j] = "hawkish"
        if pi == 2:
            matrix_pi[i][j] = "dovish"

        return {
            'nature': matrix_pi[i][j]
        }
class Eliciting_Beliefs_P1(Page):

    form_model = 'group'
    form_fields = ['sent_belief']

    def is_displayed(self):
        i = 2 * self.group.id_in_subsession - 2
        return self.player.id_in_group == 1 and  self.round_number <= Constants.rt[self.group.id_in_subsession-1] and matrix_end[i] == False and matrix_end[i+1] == False and self.group.sent_amount != 'Exert restrain'


class SendBack(Page):

    form_model = 'group'
    form_fields = ['sent_back_amount']

    def is_displayed(self):
        i = 2 * self.group.id_in_subsession - 2
        return self.player.id_in_group == 2 and self.round_number <= Constants.rt[self.group.id_in_subsession-1] and matrix_end[i] == False and matrix_end[i+1] == False  and self.group.sent_amount != 'Exert restrain'
    def vars_for_template(self):
        i = 2 * self.group.id_in_subsession - 2
        j = self.round_number - 1
        return {
            'nature': matrix_tau[i][j]
        }
class Eliciting_Beliefs_P2(Page):

    form_model = 'group'
    form_fields = ['sent_back_belief']

    def vars_for_template(self):
        i = 2 * self.group.id_in_subsession - 2
        j = self.round_number - 1
        tau = random.randrange(1, 3, 1)
        if tau == 1:
            matrix_tau[i][j] = "hawkish"
        if tau == 2:
            matrix_tau[i][j] = "dovish"
        return {
            'nature': matrix_tau[i][j]
        }
class Results1(Page):
    def is_displayed(self):
        i = 2 * self.group.id_in_subsession - 2
        return self.round_number < Constants.rt[self.group.id_in_subsession-1] and matrix_end[i] == False and matrix_end[i+1] == False
    def vars_for_template(self):
        i = 2 * self.group.id_in_subsession - 2
        return {
            'matrix_p1': np.add(matrix[i],matrix_beliefs[i]),
            'matrix_p2': np.add(matrix[i+1],matrix_beliefs[i+1]),
            'concat_p': zip(np.add(matrix[i], matrix_beliefs[i]), np.add(matrix[i + 1], matrix_beliefs[i + 1]),matrix_toString[i],matrix_toString[i + 1],matrix_beliefs_toString[i + 1],matrix_beliefs_toString[i],matrix_pi[i],matrix_tau[i]),
            'matrix_strategy_p1': matrix_toString[i],
            'matrix_strategy_p2': matrix_toString[i + 1],
            'matrix_belief_p1': matrix_beliefs_toString[i],
            'matrix_belief_p2': matrix_beliefs_toString[i + 1],
            'round': self.round_number,
            'rt': Constants.rt[self.group.id_in_subsession-1],
            'none': None,
        }



class Results(Page):

    def is_displayed(self):
        i = 2*self.group.id_in_subsession-2
        return self.round_number == Constants.rt[self.group.id_in_subsession-1]
    def vars_for_template(self):
        i = 2*self.group.id_in_subsession-2
        p1_tot = c(sum(matrix[i]))/Constants.rt[self.group.id_in_subsession-1] + c(sum(matrix_beliefs[i]))
        p2_tot = c(sum(matrix[i+1]))/Constants.rt[self.group.id_in_subsession-1] + c(sum(matrix_beliefs[i+1]))
        p1_tot_EBRT = c(sum(matrix[i]))/Constants.rt[self.group.id_in_subsession-1] + c(sum(matrix_beliefs[i]))
        p2_tot_EBRT = c(sum(matrix[i+1]))/Constants.rt[self.group.id_in_subsession-1] + c(sum(matrix_beliefs[i+1]))

        if self.player.id_in_group == 1:
            self.participant.vars['TP12_score'] = p1_tot_EBRT
            self.participant.vars['TP12_score_opponent'] = p2_tot_EBRT
            print('id 1 total TP12: ', self.participant.vars['TP12_score'])
            matrix_end[i] = True
        if self.player.id_in_group == 2:
            self.participant.vars['TP12_score'] = p2_tot_EBRT
            self.participant.vars['TP12_score_opponent'] = p1_tot_EBRT
            print('id 2 total TP12: ', self.participant.vars['TP12_score'])
            matrix_end[i+1] = True

        return {
            'player1_total': p1_tot,
            'player2_total': p2_tot,
            'matrix_p1': np.add(matrix[i],matrix_beliefs[i]),
            'matrix_p2': np.add(matrix[i+1],matrix_beliefs[i+1]),
            'concat_p': zip(np.add(matrix[i], matrix_beliefs[i]), np.add(matrix[i + 1], matrix_beliefs[i + 1]),matrix_toString[i],matrix_toString[i + 1],matrix_beliefs_toString[i + 1],matrix_beliefs_toString[i],matrix_pi[i],matrix_tau[i]),
            'matrix_strategy_p1': matrix_toString[i],
            'matrix_strategy_p2': matrix_toString[i+1],
            'matrix_belief_p1': matrix_beliefs_toString[i],
            'matrix_belief_p2': matrix_beliefs_toString[i+1],
            'round': self.round_number,
            'count': len(matrix_finished),
            'num_groups': len(self.subsession.get_groups()),
            'none': None,
        }



class WaitForP1(WaitPage):
    def is_displayed(self):
        i = 2 * self.group.id_in_subsession - 2
        return self.round_number <= Constants.rt[self.group.id_in_subsession - 1]


class ResultsWaitPage(WaitPage):
    def is_displayed(self):
        i = 2 * self.group.id_in_subsession - 2
        return self.round_number <= Constants.rt[self.group.id_in_subsession-1]

    def after_all_players_arrive(self):
        if self.round_number == 1:
            print("group: ", self.group.id_in_subsession)
            print("number of rounds: ",Constants.rt[self.group.id_in_subsession-1])


        if self.round_number != Constants.rt[self.group.id_in_subsession-1]:
            group = self.group
            p1 = group.get_player_by_id(1)
            p2 = group.get_player_by_id(2)
            i = (2 * self.group.id_in_subsession) - 2
            j = self.round_number - 1
            p1.payoff = get_payoff_p1(group.sent_amount, group.sent_back_amount,i,j)
            p2.payoff = get_payoff_p2(group.sent_amount, group.sent_back_amount,i,j)

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
            i = (2 * self.group.id_in_subsession) - 2
            j = self.round_number-1
            p1.payoff = get_payoff_p1(group.sent_amount, group.sent_back_amount,i,j)
            p2.payoff = get_payoff_p2(group.sent_amount, group.sent_back_amount,i,j)


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

class EBRT_Final_Page(Page):

    # only display instruction in round 1
    # ----------------------------------------------------------------------------------------------------------------
    def is_displayed(self):
        return self.round_number == Constants.rt[self.group.id_in_subsession - 1]

class Summary(Page):

    def vars_for_template(self):
        i = 2*self.group.id_in_subsession-2
        p1_tot_EBRT = c(sum(matrix[i]))/Constants.rt[self.group.id_in_subsession-1] + c(sum(matrix_beliefs[i]))
        p2_tot_EBRT = c(sum(matrix[i+1]))/Constants.rt[self.group.id_in_subsession-1] + c(sum(matrix_beliefs[i+1]))

        classifier = 'none'
        if self.player.id_in_group == 1:
            classifier = 'A'
            EB_score = "Your score as the international court is " + str(round(p1_tot_EBRT,2)) + " and " + "the domestic court scored " + str(round(p2_tot_EBRT,2))
            t_score = float(self.participant.vars['lottery_score']) + float(self.participant.vars['risk_score']) + float(p1_tot_EBRT)

        if self.player.id_in_group == 2:
            classifier = 'B'
            EB_score = "Your score as the domestic court is " + str(round(p2_tot_EBRT,2)) + " and " + "the international court scored " + str(round(p1_tot_EBRT,2))
            t_score = float(self.participant.vars['lottery_score']) + float(self.participant.vars['risk_score']) + float(p2_tot_EBRT)

        games = ["Lottery", "Risk", "Judicial Resources"]
        scores = [round(self.participant.vars['lottery_score'],2), round(self.participant.vars['risk_score'],2), EB_score ]
        matrix_end[i] = True


        return {
            'concat_p': zip(games,scores),
            'classifier': classifier,
            'total': round(t_score,2)
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


#-----------------------------------------------------------------------------------------------------

# Sequence of pages for display
# ---------------------------------------------------------------------------------------------------
page_sequence = [
    Instructions,
    Mid_Questionaire,
    Mid_Questionaire_Answers,
    AllGroupsWaitPage,
    Send,
    Eliciting_Beliefs_P2,
    Eliciting_Beliefs_P1,
    WaitForP1,
    SendBack,
    ResultsWaitPage,
    Results1,
    Results,
    EBRT_Final_Page,
    Questionaire,
    Summary,
]