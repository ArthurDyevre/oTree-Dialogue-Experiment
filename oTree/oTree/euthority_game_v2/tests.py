from . import pages
from euthority_game_v2.templates._builtin import Bot
from .models import Constants
from otree.api import Submission

from . import draft3

class PlayerBot(Bot):
    cases = [{'player1': 'Exert restrain', 'player2': 'Do not challenge','p1_payoff': 2, 'p2_payoff': 2},
             {'player1': 'Exert restrain','player2': 'Challenge','p1_payoff': 2, 'p2_payoff': 2},
             {'player1': 'Be assertive', 'player2': 'Do not challenge', 'p1_payoff': 4, 'p2_payoff': 0},
             {'player1': 'Be assertive', 'player2': 'Challenge', 'p1_payoff': -2, 'p2_payoff': -2}]

    def play_round(self):
        case = self.case
        if self.player.id_in_group == 1:
            yield(pages.Send, {"sent_amount": case['player1']})
        if self.player.id_in_group == 2:
            yield(pages.SendBack, {"sent_back_amount": case['player2']})
        if self.round_number < Constants.rt[self.group.id_in_subsession - 1]:
            yield(pages.Results1)
        if self.round_number == Constants.rt[self.group.id_in_subsession - 1]:
            yield Submission(pages.Results,check_html=False)

        if self.player.id_in_group == 1:
            expected_payoff = case['p1_payoff']
        else:
            expected_payoff = case['p2_payoff']

        assert self.player.payoff == expected_payoff

        next = Constants.rt[self.group.id_in_subsession - 1]
        print("amount of round: ",Constants.rt[self.group.id_in_subsession - 1])

        draft3.round_test.append(next)


