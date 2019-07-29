from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random

# variables for all templates
# --------------------------------------------------------------------------------------------------------------------
def vars_for_all_templates(self):
    return {
        'lottery_a_lo': c(Constants.lottery_a_lo),
        'lottery_a_hi': c(Constants.lottery_a_hi),
        'lottery_b_lo': c(Constants.lottery_b_lo),
        'lottery_b_hi': c(Constants.lottery_b_hi)
    }


# ******************************************************************************************************************** #
# *** CLASS INSTRUCTIONS *** #
# ******************************************************************************************************************** #
class Instructions(Page):

    # only display instruction in round 1
    # ----------------------------------------------------------------------------------------------------------------
    def is_displayed(self):
        return self.subsession.round_number == 1

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):
        return {
            'num_choices':  len(self.participant.vars['mpl_choices']),
            'choices': self.participant.vars['mpl_choices']

        }


# ******************************************************************************************************************** #
# *** PAGE DECISION *** #
# ******************************************************************************************************************** #
class Decision(Page):

    # form model
    # ----------------------------------------------------------------------------------------------------------------
    form_model = 'player'

    # form fields
    # ----------------------------------------------------------------------------------------------------------------
    def get_form_fields(self):
        count = 1
        pay = 2
        option_b = 0
        option_p1= 'If the coin turns up heads, then you lose € '
        option_p2= '; if the coin turns up tails, you win € 6.'
        for i in range(Constants.num_choices[0]):
            self.player.participant.vars['mpl_choices'][i] = (count, 'choice_'+str(count), '5/10', '10/10', option_p1+str(pay)+option_p2, '€ '+str(option_b))
            count = count + 1
            option_b = option_b + 1
            pay = pay + 1

        # unzip list of form_fields from <mpl_choices> list
        form_fields = [list(t) for t in zip(*self.player.participant.vars['mpl_choices'])][1]
        form_fields = form_fields[:6]
        print(form_fields)


        # provide form field associated with pagination or full list
        if Constants.one_choice_per_page:
            page = self.subsession.round_number
            return [form_fields[page - 1]]
        else:
            return form_fields

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):

        # specify info for progress bar
        total = len(self.participant.vars['mpl_choices'])
        page = self.subsession.round_number
        progress = page / total * 100

        print("participant vars mpl choices: ")
        print(self.player.participant.vars['mpl_choices'])
        print(Constants.num_choices[0])

        self.player.participant.vars['mpl_choices'] = self.player.participant.vars['mpl_choices'][:6]

        # TODO changing the vars mpl_choices to fit into the new game
        count = 1
        pay = 2
        option_b = 0
        option_p1= 'If the coin turns up heads, then you lose € '
        option_p2= '; if the coin turns up tails, you win € 6.'
        for i in range(Constants.num_choices[0]):
            self.player.participant.vars['mpl_choices'][i] = (count, 'choice_'+str(count), '5/10', '10/10', option_p1+str(pay)+option_p2, '€ '+str(option_b))
            count = count + 1
            option_b = option_b + 1
            pay = pay + 1


        # unzip list of form_fields from <mpl_choices> list
        form_fields = [list(t) for t in zip(*self.player.participant.vars['mpl_choices'])][1]




        if Constants.one_choice_per_page:
            return {
                'page':      page,
                'total':     total,
                'progress':  progress,
                'choices':   [self.player.participant.vars['mpl_choices'][page - 1]]
            }
        else:
            return {
                'choices':   self.player.participant.vars['mpl_choices'],
                'half_pie': 10,
            }

    # set player's payoff
    # ----------------------------------------------------------------------------------------------------------------
    def before_next_page(self):



        # unzip indices and form fields from <mpl_choices> list
        round_number = self.subsession.round_number
        form_fields = [list(t) for t in zip(*self.participant.vars['mpl_choices'])][1]
        indices = [list(t) for t in zip(*self.participant.vars['mpl_choices'])][0]
        index = indices[round_number - 1]

        # if choices are displayed in tabular format
        # ------------------------------------------------------------------------------------------------------------
        if not Constants.one_choice_per_page:
            count = 2
            print("Choices were: ")
            # replace choices in <choices_made>
            index = 1
            draw = random.randint(1, 6)
            print("draw of lottery: ", draw)

            for j, choice in zip(indices, form_fields):
                choice_i = getattr(self.player, choice)
                print(choice_i)
                self.participant.vars['mpl_choices_made'][j - 1] = choice_i
                if (choice_i == 'B'):
                    self.participant.vars['lottery_score'] = 0
                    print("current payoff: ")
                    print(self.participant.vars['lottery_score'])
                    print(index)
                    break
                if index == draw:
                    if(choice_i == 'A'):
                        loss = count*(-1)
                        coin_toss = [loss,6]
                        self.participant.vars['lottery_score'] = random.choice(coin_toss)
                    if(choice_i == 'B'):
                        self.participant.vars['lottery_score'] = 0
                    print("current payoff: ")
                    print(self.participant.vars['lottery_score'])
                    print(index)
                    break
                count = count + 1
                index = index + 1


# ******************************************************************************************************************** #
# *** PAGE RESULTS *** #
# ******************************************************************************************************************** #
class Results(Page):

    # skip results until last page
    # ----------------------------------------------------------------------------------------------------------------
    def is_displayed(self):
        if Constants.one_choice_per_page:
            return self.subsession.round_number == Constants.num_rounds[0]
        else:
            return True

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):

        # unzip <mpl_choices> into list of lists
        choices = [list(t) for t in zip(*self.participant.vars['mpl_choices'])]
        indices = choices[0]



        if Constants.one_choice_per_page:
            return {
                'payoff':         self.player.payoff,
                'indices':        indices
            }
        else:
            return {
                'option_to_pay':  self.player.option_to_pay,
                'payoff':         self.player.payoff,
                'indices':        indices

            }


# ******************************************************************************************************************** #
# *** PAGE SEQUENCE *** #
# ******************************************************************************************************************** #
page_sequence = [Instructions,Decision,Results]

