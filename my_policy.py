import itertools
from deck import Card
from policy import CribbagePolicy, CompositePolicy, GreedyThrower, GreedyPegger
from scoring import greedy_throw, score
import scoring
import random
class MyPolicy(CribbagePolicy):
    def __init__(self, game):
        self._game = game
        self._policy = CompositePolicy(game, GreedyThrower(game), GreedyPegger(game))
        self._cribTableDealer = {
            (1, 1): 5.50725, (1, 2): 4.589375, (1, 3): 4.757375, (1, 4): 5.402625, (1, 5): 5.552625, (1, 6): 4.034375, 
            (1, 7): 4.052375, (1, 8): 4.09075, (1, 9): 3.68525, (1, 10): 3.734125, (1, 11): 3.961375, (1, 12): 3.6125, 
            (1, 13): 3.565375, 
            (2, 2): 6.04325, (2, 3): 7.119375, (2, 4): 4.949125, (2, 5): 5.646625, (2, 6): 4.2135, (2, 7): 4.285, 
            (2, 8): 4.061625, (2, 9): 4.043625, (2, 10): 3.93175, (2, 11): 4.206875, (2, 12): 3.9155, (2, 13): 3.7655, 
            (3, 3): 6.2365, (3, 4): 5.342125, (3, 5): 6.2645, (3, 6): 4.0475, (3, 7): 4.13525, (3, 8): 4.319875, 
            (3, 9): 4.089375, (3, 10): 3.98, (3, 11): 4.232375, (3, 12): 3.974125, (3, 13): 3.836125, 
            (4, 4): 6.03775, (4, 5): 6.679875, (4, 6): 4.33975, (4, 7): 4.10325, (4, 8): 4.244625, (4, 9): 4.019, 
            (4, 10): 3.880125, (4, 11): 4.0665, (4, 12): 3.760125, (4, 13): 3.719375, 
            (5, 5): 8.756, (5, 6): 6.77, (5, 7): 6.183375, (5, 8): 5.58475, (5, 9): 5.46175, (5, 10): 6.652125, 
            (5, 11): 6.932, (5, 12): 6.58375, (5, 13): 6.496875, 
            (6, 6): 6.07475, (6, 7): 5.31125, (6, 8): 4.868875, (6, 9): 5.224625, (6, 10): 3.392375, (6, 11): 3.55075, 
            (6, 12): 3.312375, (6, 13): 3.23975, 
            (7, 7): 6.203, (7, 8): 6.76225, (7, 9): 4.23425, (7, 10): 3.387625, (7, 11): 3.673375, (7, 12): 3.37575, 
            (7, 13): 3.320625, 
            (8, 8): 5.72525, (8, 9): 4.80025, (8, 10): 4.000625, (8, 11): 3.6425, (8, 12): 3.39825, (8, 13): 3.349875, 
            (9, 9): 5.3285, (9, 10): 4.424625, (9, 11): 4.039, (9, 12): 3.160375, (9, 13): 3.145, 
            (10, 10): 4.986125, (10, 11): 4.621625, (10, 12): 3.600125, (10, 13): 2.992625, 
            (11, 11): 5.45925, (11, 12): 4.594875, (11, 13): 3.838875, 
            (12, 12): 4.7835, (12, 13): 3.552125, 
            (13, 13): 4.622125}
        self._cribTableNon = {
            (1, 1): 5.734625, (1, 2): 4.7425, (1, 3): 4.906125, (1, 4): 5.6315, (1, 5): 5.925875, (1, 6): 4.609375, 
            (1, 7): 4.509125, (1, 8): 4.529875, (1, 9): 4.24575, (1, 10): 4.121, (1, 11): 4.40275, (1, 12): 3.999375,
            (1, 13): 4.013875,
            (2, 2): 6.125875, (2, 3): 7.207375, (2, 4): 5.171125, (2, 5): 5.958875, (2, 6): 4.715875, (2, 7): 4.662875,
            (2, 8): 4.440125, (2, 9): 4.4815, (2, 10): 4.28225, (2, 11): 4.5035, (2, 12): 4.17975, (2, 13): 4.12875,
            (3, 3): 6.48625, (3, 4): 5.618625, (3, 5): 6.56975, (3, 6): 4.645625, (3, 7): 4.641625, (3, 8): 4.649375,
            (3, 9): 4.517625, (3, 10): 4.398625, (3, 11): 4.574625, (3, 12): 4.307125, (3, 13): 4.184625,
            (4, 4): 6.258375, (4, 5): 7.172125, (4, 6): 4.944625, (4, 7): 4.511, (4, 8): 4.568, (4, 9): 4.50825,
            (4, 10): 4.164625, (4, 11): 4.46075, (4, 12): 4.161625, (4, 13): 4.137625, \
            (5, 5): 9.190125, (5, 6): 7.315125, (5, 7): 6.7115, (5, 8): 6.070625, (5, 9): 5.98025, (5, 10): 7.091, 
            (5, 11): 7.357875, (5, 12): 7.100125, (5, 13): 7.02925,
            (6, 6): 6.756625, (6, 7): 5.99575, (6, 8): 5.597, (6, 9): 5.949625, (6, 10): 4.059, (6, 11): 4.263, 
            (6, 12): 3.93225, (6, 13): 3.8065,
            (7, 7): 6.658125, (7, 8): 7.3815, (7, 9): 4.957875, (7, 10): 4.04625, (7, 11): 4.2885, (7, 12): 3.9295, 
            (7, 13): 3.883875,
            (8, 8): 6.234875, (8, 9): 5.50425, (8, 10): 4.653625, (8, 11): 4.2, (8, 12): 3.927875, (8, 13): 3.856875,
            (9, 9): 6.032125, (9, 10): 5.222125, (9, 11): 4.717875, (9, 12): 3.79275, (9, 13): 3.806,
            (10, 10): 5.54125, (10, 11): 5.20325, (10, 12): 4.198, (10, 13): 3.524125,
            (11, 11): 6.038375, (11, 12): 5.188, (11, 13): 4.446, 
            (12, 12): 5.375375, (12, 13): 4.10525,
            (13, 13): 5.173625
        }
        self._cribTable = (self._cribTableDealer, self._cribTableNon)
        self._adjustments = {
            1: 1.12,
            2: 1.18,
            3: 1.21,
            4: 1.21,
            5: 1.66,
            6: 1.2,
            7: 1.18,
            8: 1.16,
            9: 1.13,
            10: 1.12,
            11: 1.17,
            12: 1.08,
            13: 1.03,
        }
    '''
    def generateTable(self, count):
        deck = self._game.deck()._cards
        table = {}
        discard_combos = []
        for rank1, rank2 in itertools.combinations_with_replacement(range(1,14), 2):
            c1 = Card(rank1, "S")
            c2 = Card(rank2, "H")
            c3 = Card(rank1, "S")
            c4 = Card(rank2, "S")
            discard_combos.append(((c1, c2), (c3, c4)))
        num_discarded = 0
        for discard in discard_combos:
            print(f"Discarding: {num_discarded}/{len(discard_combos)}")
            num_discarded += 1
            total_score = 0
            deck2 = [card for card in deck if card not in discard[0]]
            for _ in range(3*count):
                total_score += self.generateTableHelper(deck2, discard[0])
            for _ in range(count):
                total_score += self.generateTableHelper(deck2, discard[1])
            EV = total_score/(4*count)
            ranks = tuple(card.rank() for card in discard[0])
            table[ranks] = EV
        return table
    def generateTableHelper(self, deck, discard):
        opponent_hand = random.sample(deck, 6)
        used_cards = set(discard) | set(opponent_hand)
        remaining_deck = [card for card in deck if card not in used_cards]
        turn_card = random.choice(remaining_deck)
        opponent_keep, opponent_throw, val = scoring.greedy_throw(self._game, opponent_hand, 1)
        crib = list(discard) + list(opponent_throw)        
        return score(self._game, crib, turn_card, True)[0]
    
    def printTable(self, count):
        table = self.generateTable(count)
        for ranks, ev in table.items():
            print(f"{ranks}: {ev}")
    '''

    ''' 
    def calculateWeights(self, count):
        table = {}
        for rank in range(1, 14):
            deck = self._game.deck()._cards
            c = Card(rank, 'S')
            deck2 = [card for card in deck if card != c]
            total_score = 0
            for i in range(count):
                c2 = random.sample(deck2, 3)
                hand = [c] + c2
                turn_card = random.choice([card for card in deck2 if card not in hand])
                total_score += score(self._game, hand, turn_card, False)[0]
            EV = total_score/count
            table[rank] = EV
        for rank in table:
            table[rank] = round(table[rank]/4, 2)
        for rank, EV in table.items():
            print(f"{rank}: {EV},")
    '''

    def keep(self, hand, scores, am_dealer):
        deck = self._game.deck()._cards
        best_keep, best_throw = None, None
        best_score = -1
        for ti in self._game.throw_indices():
            my_keep = [hand[i] for i in range(len(hand)) if i not in ti]
            my_throw = [hand[i] for i in ti]
            deck2 = [card for card in deck if card not in hand]
            
            # calculate hand scores w/ custom adjustments
            hand_score = 0
            for card in deck2:
                hand_score += score(self._game, my_keep, card, False)[0]
            hand_score /= len(deck2)
            thrown = tuple(sorted(card.rank() for card in my_throw))
            if am_dealer:
                hand_score += self._cribTable[0].get(thrown)
            else:
                hand_score -= self._cribTable[1].get(thrown)
            hand_ranks = [card.rank() for card in my_keep]
            for rank in hand_ranks:
                hand_score += self._adjustments[rank]
            if hand_score > best_score:
                best_score = hand_score
                best_keep = my_keep
                best_throw = my_throw

        return best_keep, best_throw

    def peg(self, cards, history, turn, scores, am_dealer):
        best_score = 0
        for card in cards:
            if history.is_legal(self._game, card, 0 if am_dealer else 1):
                score = history.score(self._game, card, 0 if am_dealer else 1)
                if score > best_score:
                    best_card = card
                    best_score = score
        if best_score > 0:
            return best_card

        # try to push them out of legal cards
        for card in cards:
            if history.is_legal(self._game, card, 0 if am_dealer else 1):
                if history.total_points() + self._game.rank_value(card.rank()) >= 28:
                    return card 

        # opening moves
        if history.is_start_round():
            for card in cards:
                if history.is_legal(self._game, card, 0 if am_dealer else 1):
                    # pair trap
                    for card2 in cards:
                        if card != card2 and self._game.rank_value(card.rank()) == self._game.rank_value(card2.rank()) and card.rank() != 5:
                            return card
                    # non-5 15-sum
                    for card2 in cards:
                        if card != card2 and self._game.rank_value(card.rank()) + self._game.rank_value(card2.rank()) == 15:
                            if card.rank() == 5:
                                return card2
                            elif card.rank() > card2.rank():
                                return card
                            else: 
                                return card2
            # prioritize low
            for card in cards:
                if history.is_legal(self._game, card, 0 if am_dealer else 1):
                    if card.rank() <= 4:
                        return card

        # score denial
        for card in cards:
            if history.is_legal(self._game, card, 0 if am_dealer else 1):
                if history.total_points() + card.rank() != 5: # and abs(history._card.rank() - card.rank()) != 1:
                    return card

        # return anything
        for card in cards:
            if history.is_legal(self._game, card, 0 if am_dealer else 1):
                return card
'''
if __name__ == "__main__":
    from cribbage import Game
    import itertools, random

    game = Game()
    print("starting...")
    policy = MyPolicy(game)
    policy.calculateWeights(10000)
    # policy.printTable(2000)
'''