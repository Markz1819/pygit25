from __future__ import annotations
import random
import time
# from typing_extensions import override

faces = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
suits = ["♠", "♥", "♣", "♦"]
player_chips: int = 1000  # Initial amount of chips the player has
MAX_CHIPS = 10000

player_hands: list[Hand] = []
dealer: Hand
deck: Hand
insurance_bet: int = 0
was_split: bool = False


# Class representing a playing card
class Card:
    def __init__(self, face: str, suit: str):
        self.face: str = face
        self.suit: str = suit

    def get_value(self) -> int:
        if self.face == "A":
            return 11
        elif self.face in ["J", "Q", "K"]:
            return 10
        else:
            return int(self.face)

    # @override
    def __str__(self) -> str:
        return f"{self.suit}{self.face}"


# Class representing a hand of cards
class Hand:
    def __init__(self, bet: int = 0, is_split: bool = False):
        self.cards: list[Card] = []  # Stores all cards in the hand
        self.value: int = 0  # Total value of the hand
        self.bet: int = bet  # Total bet placed on the hand
        self.busted: bool = False  # Whether or not this hand has busted
        self.stood: bool = False  # Whether or not this hand has stood
        self.is_split: bool = is_split  # Whether this hand came from a split

    # Returns the card at the specified index
    def get_card(self, index: int) -> Card:
        return self.cards[index]

    # Returns and removes the card at the specified index
    def remove_card(self, index: int) -> Card:
        temp = self.cards.pop(index)
        self.calculate_value()
        return temp

    # Adds a card to the hand
    def add_card(self, card: Card):
        self.cards.append(card)
        self.calculate_value()

    # Draws a random card from the deck and adds it to the hand
    def draw_card(self):
        drawn_card = deck.get_card(0)
        self.add_card(drawn_card)
        deck.cards.remove(drawn_card)
        self.calculate_value()

    # Stores and returns the value of the hand
    def calculate_value(self):
        value = 0
        aces = 0
        for card in self.cards:
            if card.face == "A":
                aces += 1
                value += 11
            elif card.face in ["J", "Q", "K"]:
                value += 10
            else:
                value += int(card.face)
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        self.value = value

    def is_blackjack(self) -> bool:
        # Blackjack only counts if it's the original two cards (not from a split)
        return len(self.cards) == 2 and self.value == 21 and not self.is_split

    # Returns a list of cards in the hand
    # @override
    def __str__(self) -> str:
        return ", ".join(str(card) for card in self.cards)


# -------------
# INITIAL SETUP
# -------------


# Setup initial hands
def setup():
    global deck, player_hands, dealer, insurance_bet, was_split
    deck = Hand()  # Initialize the deck
    deck.cards.clear()

    # Fill the deck with cards
    for face in faces:
        for suit in suits:
            deck.add_card(Card(face, suit))
    random.shuffle(deck.cards)

    # Init variables
    player_hands = []
    player_hands.append(Hand())
    dealer = Hand()
    insurance_bet = 0
    was_split = False

    # Deal initial cards
    player_hands[0].draw_card()
    player_hands[0].draw_card()
    dealer.draw_card()
    dealer.draw_card()


# Prompt players for their initial bet
def initial_bet():
    global player_chips

    while True:
        try:
            time.sleep(0.2)
            bet = int(input("Place your bet: "))
            if bet > player_chips:
                print("You don't have enough chips!")
            elif bet <= 0:
                print("Invalid bet! Please enter a positive integer.")
                time.sleep(1)
            else:
                player_chips -= bet
                player_hands[0].bet = bet
                print(f"You bet {bet} chips.")
                time.sleep(0.2)
                break
        except ValueError:
            print("Invalid bet! Please enter a positive integer.")
            time.sleep(1)


# Display initial hands
def show_initial_hands():
    print("----------------------------------------------")
    time.sleep(0.2)
    print(f"Your hand: {player_hands[0]} ({player_hands[0].value})")
    time.sleep(0.2)
    print(f"Dealer's hand: {dealer.get_card(0)}, ??")
    time.sleep(0.2)
    print("----------------------------------------------")
    time.sleep(0.5)


# -------------------
# BLACKJACK BEHAVIOUR
# -------------------


# Check if insurance can be offered, and process it
def offer_insurance():
    global player_chips, insurance_bet
    if dealer.get_card(0).face != "A":
        return

    max_insurance = player_hands[0].bet // 2
    print(f"Would you like insurance? Enter 0 if no. (Max: {max_insurance} chips)")
    time.sleep(0.2)

    while True:
        try:
            amount = int(input(f"Insurance amount (max {max_insurance}): "))
            if amount > player_chips:
                print("Not enough chips!")
                time.sleep(0.2)
            elif amount > max_insurance:
                print(f"Insurance can't exceed {max_insurance} chips!")
            elif amount == 0:
                print("Insurance declined.")
                time.sleep(0.2)
                return
            elif amount < 0:
                print("Invalid amount!")
                time.sleep(1)
            else:
                insurance_bet = amount
                player_chips -= amount
                print(f"Insurance bet placed: {amount} chips")
                time.sleep(0.2)
                break
        except ValueError:
            print("Please enter a valid number!")
            time.sleep(0.2)


# Resolve all potential blackjacks
def resolve_blackjacks():
    global player_chips, insurance_bet

    dealer_bj = dealer.is_blackjack()
    player_bj = player_hands[0].is_blackjack() and len(player_hands) == 1

    time.sleep(0.2)
    if player_bj and dealer_bj:
        print("Both have blackjack!")
        player_chips += player_hands[0].bet  # Return bet
        time.sleep(0.5)
        return True
    elif player_bj:
        print("Blackjack! You win!")
        player_chips += int(player_hands[0].bet * 2.5)  # 3:2 payout
        time.sleep(0.2)
        print(f"[+{int(player_hands[0].bet * 1.5)} chips]")
        time.sleep(0.5)
        return True
    elif dealer_bj:
        print("Dealer blackjack! You lose!")
        time.sleep(0.2)
        print(f"[-{player_hands[0].bet} chips]")

        # Fixed: Insurance pays 3x total (bet + 2x winnings)
        if insurance_bet != 0:
            player_chips += insurance_bet * 3
            print(f"Insurance pays! You win {insurance_bet * 2} chips from insurance!")
            print(f"[+{insurance_bet * 2} chips]")
            time.sleep(0.2)

        time.sleep(0.5)
        return True

    # If no blackjack but insurance was taken, lose it
    if insurance_bet != 0:
        print(f"No dealer blackjack. You lose {insurance_bet} insurance chips.")
        insurance_bet = 0
        time.sleep(0.2)

    return False


# --------------------------
# PLAYER PROMPTING AND LOGIC
# --------------------------


# Player prompting and logic, returns True if at least one hand didn't bust
def player_loop() -> bool:
    global player_hands, was_split

    if was_split:
        hand_num: int = 1
        all_bust = True
        for player_hand in player_hands:
            if player_hand.stood or player_hand.busted:
                hand_num += 1
                continue

            print(f"===Playing Hand {hand_num}===")
            time.sleep(0.2)
            print(f"Your hand: {player_hand} ({player_hand.value})")
            time.sleep(0.2)
            if player_turn(player_hand):
                all_bust = False
            hand_num += 1
        return not all_bust

    return player_turn(player_hands[0])


# Returns True if hand completes without busting, False if busted
def player_turn(hand: Hand) -> bool:
    while not hand.stood and not hand.busted:
        action = input("Hit(H), Bet Options(B), or Stand(S)? \n").lower()

        if action in ["hit", "h"]:
            hit(hand)

        elif action in ["bet", "b"]:
            if betting_options(hand):
                return player_loop()

        elif action in ["stand", "s"]:
            hand.stood = True
            print("You stand.")
            time.sleep(0.2)
            return True
        else:
            print("Invalid input")
            time.sleep(1)

    return not hand.busted


# Functionality for hitting on a hand
def hit(hand: Hand):
    hand.draw_card()

    print("----------------------------------------------")
    time.sleep(0.2)
    print("You drew:", hand.get_card(-1))
    time.sleep(0.2)
    print(f"Your hand: {hand} ({hand.value})")
    time.sleep(0.2)
    print("----------------------------------------------")
    time.sleep(0.2)

    if hand.value > 21:
        hand.busted = True
        print("You busted!")
        time.sleep(0.5)


# Functionality for betting options
def betting_options(hand: Hand):
    prompt = ""
    if can_double_down(hand):
        prompt += "Double Down(D), "
    if can_split(hand) and len(player_hands) < 4:  # Limit splits
        prompt += "Split(S), "

    if prompt == "":
        print("No betting options available.")
        return

    prompt += "or Back(B)?\n"

    action = input(prompt).lower()

    if action in ["double down", "d"] and can_double_down(hand):
        double_down(hand)
    elif action in ["split", "s"] and can_split(hand):
        split_hand(hand)
        return True
    elif action in ["back", "b"]:
        return
    else:
        print("Invalid option!")
        time.sleep(1)
    return False


# Checks if the hand can be doubled down on
def can_double_down(hand: Hand) -> bool:
    global player_chips
    return len(hand.cards) == 2 and player_chips >= hand.bet


# Checks if the hand can be split (same face, not just value)
def can_split(hand: Hand) -> bool:
    global player_chips
    if len(hand.cards) != 2 or player_chips < hand.bet:
        return False

    # Fixed: Must have same face, not just same value
    return hand.cards[0].face == hand.cards[1].face


# Doubles the bet and hits once
def double_down(hand: Hand):
    global player_chips

    player_chips -= hand.bet
    hand.bet *= 2
    print(f"Bet doubled to {hand.bet} chips!")
    time.sleep(0.2)

    hit(hand)

    hand.stood = True


# Splits the hand into two hands
def split_hand(hand: Hand):
    global player_chips, was_split

    player_chips -= hand.bet
    print(f"Split! Additional bet of {hand.bet} chips placed.")
    time.sleep(0.2)

    was_split = True

    # Create new hand with one card from original
    new_hand = Hand(hand.bet, is_split=True)
    new_hand.add_card(hand.remove_card(1))

    # Mark both hands as split
    hand.is_split = True

    # Draw one card to each hand
    hand.draw_card()
    new_hand.draw_card()

    print(f"Drawn: {hand.cards[-1]}")
    time.sleep(0.2)
    print(f"Drawn: {new_hand.cards[-1]}")
    time.sleep(0.2)

    # Fixed: If splitting Aces, only one card each (standard rule)
    if hand.cards[0].face == "A":
        hand.stood = True
        new_hand.stood = True
        print("Split Aces receive only one card each.")
        time.sleep(0.2)

    player_hands.append(new_hand)

    print_player_hands()


# Print every hand the player has
def print_player_hands():
    time.sleep(0.5)
    print("Player's hands:")
    time.sleep(0.5)
    hand_num = 1
    for player_hand in player_hands:
        if player_hand.busted:
            status = "BUST"
        else:
            status = str(player_hand.value)

        print(f"Hand {hand_num}: {player_hand} ({status})")
        time.sleep(0.2)
        hand_num += 1


# ------------
# DEALER LOGIC
# ------------


def dealer_loop():
    print("----------------------------------------------")
    print(f"Dealer's hand: {dealer} ({dealer.value})")
    time.sleep(0.5)

    while dealer.value < 17:
        dealer.draw_card()
        time.sleep(0.2)
        print(f"Dealer drew: {dealer.get_card(-1)}")
        time.sleep(0.2)
        print(f"Dealer's hand: {dealer} ({dealer.value})")
        print("----------------------------------------------")
        time.sleep(0.2)

        if dealer.value > 21:
            print("Dealer busts!")
            time.sleep(0.2)
            print("----------------------------------------------")
            time.sleep(0.5)
            return

    print("Dealer stands")
    time.sleep(0.2)
    print("----------------------------------------------")
    time.sleep(0.5)
    return


# -------------------------------
# DISPLAY RESULT AND CALCULATIONS
# -------------------------------


# Display the final hands of the player and dealer
def show_final_hands():
    global was_split
    print("RESULTS:")
    time.sleep(0.5)
    if was_split:
        print_player_hands()
        time.sleep(0.2)
    else:
        if player_hands[0].busted:
            status = "BUST"
        else:
            status = str(player_hands[0].value)
        print(f"Player's hand: {player_hands[0]} ({status})")
        time.sleep(0.2)

    if dealer.value > 21:
        status = "BUST"
    else:
        status = str(dealer.value)
    print(f"Dealer's hand: {dealer} ({status})")
    time.sleep(0.2)
    print("----------------------------------------------")
    time.sleep(0.5)


# Check the results of the game
def check_all_results():
    hand_num = 1
    for hand in player_hands:
        if was_split:
            print(f"Hand {hand_num}: {resolve_hand(hand)}")
        else:
            print(resolve_hand(hand))
        time.sleep(0.5)
        hand_num += 1


def resolve_hand(hand: Hand):
    global player_chips

    if hand.busted:
        return f"[-{hand.bet} chips]"

    if dealer.value > 21:  # Dealer busts, player wins
        winnings = hand.bet * 2
        player_chips += winnings
        return f"[+{hand.bet} chips]"

    elif hand.value > dealer.value:  # Player wins
        winnings = hand.bet * 2
        player_chips += winnings
        return f"[+{hand.bet} chips]"

    elif hand.value < dealer.value:  # Player loses
        return f"[-{hand.bet} chips]"

    else:  # Push
        player_chips += hand.bet
        return "[+0 chips]"


# --------------
# MAIN FUNCTIONS
# --------------


# Logic of one game
def game_loop():
    # Setup steps
    setup()
    initial_bet()
    show_initial_hands()

    # Blackjack checks
    offer_insurance()
    are_blackjacks = resolve_blackjacks()
    if not are_blackjacks:
        # Fixed: Dealer plays if at least one hand is still alive
        if player_loop():
            dealer_loop()

    show_final_hands()

    if not are_blackjacks:
        check_all_results()


# Shows one of the possible endings that the player might achieve
def show_ending():
    print("\n==============================================")

    if player_chips == 0:
        print("You got the [Casino Sucker] Ending!")
        print(
            "You were another unfortunate victim of the \ncasino, having lost everything."
        )
    elif player_chips < 1000:
        print("You got the [Strategic Retreat] Ending!")
        print(
            "You realized you weren't going to win, \nand wisely quit before it was too late."
        )
    elif player_chips == 1000:
        print("You got the [Casino Tourist] Ending!")
        print("You decided the casino wasn't worth it.")
    elif player_chips < MAX_CHIPS:
        print("You got the [Smart Gambler] Ending!")
        print(
            "You managed to walk away with a profit, \ndeciding to quit while you were ahead."
        )
    else:
        print("You got the [Blacklisted] Ending!")
        print(
            "The casino lost too much, and decided to kick \nyou out before you could win more."
        )

    print(f"Final Score: {player_chips} chips")
    print("==============================================")


def main():
    global player_chips

    print("Hello! Welcome to Blackjack!")
    time.sleep(0.5)
    print("You'll start with 1000 chips.")
    time.sleep(0.5)
    print("Remember, the house always wins. Don't push your luck.")
    time.sleep(0.5)

    start_prompt = input("Start game? (y/n): ").lower()

    while start_prompt not in ["y", "n"]:
        print("Invalid input.")
        start_prompt = input("Start game? (y/n): ").lower()

    while start_prompt == "y":
        game_loop()

        # Check if the player has met an immediate ending condition
        if player_chips == 0 or player_chips >= MAX_CHIPS:
            break

        print(f"\nYou currently have {player_chips} chips.")
        start_prompt = input("Continue(Y) or call it quits(N)? ").lower()

    show_ending()


main()
