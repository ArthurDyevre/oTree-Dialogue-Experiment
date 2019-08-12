from otree.api import Currency as c, currency_range
from . import pages, models
from ._builtin import Bot
from .models import Constants
from otree.api import Submission

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from otree.models import group, player
import numpy as np
import random


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


