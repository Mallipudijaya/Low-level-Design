from abc import ABC, abstractmethod

# Card class representing a playing card
class Card:
    def __init__(self, letter, number):
        self.letter = letter  # Suit (e.g., 'Hearts', 'Diamonds')
        self.number = number  # Rank (e.g., '2', '3', ..., 'King', 'Ace')

# Hand class representing a collection of cards
class Hand:
    def __init__(self, cards):
        self.cards = cards

    def get_cards(self):
        return self.cards

# Rule interface equivalent
class Rule(ABC):
    @abstractmethod
    def get_priority(self):
        pass

    @abstractmethod
    def validate(self, hand):
        pass

# PairRule class to validate a pair in the hand
class PairRule(Rule):
    def __init__(self, priority):
        self.priority = priority

    def get_priority(self):
        return self.priority

    def validate(self, hand):
        nums = {}
        for card in hand.get_cards():
            nums[card.number] = nums.get(card.number, 0) + 1

        # At least one pair
        return any(count >= 2 for count in nums.values())

# FlushRule class to validate a flush in the hand
class FlushRule(Rule):
    def __init__(self, priority):
        self.priority = priority

    def get_priority(self):
        return self.priority

    def validate(self, hand):
        suits = set()
        for card in hand.get_cards():
            suits.add(card.letter)

        # All cards of the same suit
        return len(suits) == 1

# Poker class to manage poker hands and rules
class Poker:
    def __init__(self, hands, rules):
        self.hands = hands
        self.rules = rules

    def get_winning_hand(self):
        best_hand = None
        highest_priority = -1

        for hand in self.hands:
            for rule in self.rules:
                if rule.validate(hand):
                    if rule.get_priority() > highest_priority:
                        highest_priority = rule.get_priority()
                        best_hand = hand
        
        return best_hand

# Main PokerGame equivalent
if __name__ == "__main__":
    # Create sample cards
    cards1 = [Card('Hearts', '2'), Card('Hearts', '3'), Card('Hearts', '4'), Card('Hearts', '5'), Card('Hearts', '6')]
    cards2 = [Card('Diamonds', '2'), Card('Diamonds', '2'), Card('Diamonds', '3'), Card('Diamonds', '4'), Card('Diamonds', '5')]
    
    hand1 = Hand(cards1)  # Flush
    hand2 = Hand(cards2)  # Pair

    # Define the rules with priorities
    rules = [FlushRule(2), PairRule(1)]

    # Create a poker game with the hands and rules
    poker_game = Poker([hand1, hand2], rules)

    # Get the winning hand based on the rules
    winning_hand = poker_game.get_winning_hand()

    # Output results
    if winning_hand:
        print("Winning hand contains the following cards:")
        for card in winning_hand.get_cards():
            print(f"{card.number} of {card.letter}")
    else:
        print("No winning hand found.")
