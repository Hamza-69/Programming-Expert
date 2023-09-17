
import random
class Deck:
    value = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    suit = [u"\u2666" , u"\u2665", u"\u2663" , u"\u2660"]
    card_list = []
    for i in suit:
        for j in value:
            card_list.append(f'{j}{i}')
    card_dict = {}
    for i in card_list:
        if i[0] in ['T', 'J', 'Q', 'K', 'A']:
            card_dict[i] = 10
        elif i[0] == 'A':
            card_dict[i] = 1,11
        else:
            card_dict[i] = int(i[0])
    def __init__(self):
        self.cards = Deck.card_list.copy()
    def shuffle(self):
        random.shuffle(self.cards)
    def deal(self):
        x = self.cards[-1]
        self.cards.remove(self.cards[-1])
        return x
    def new(self):
        self.cards = Deck.card_list.copy()
class char:
    def __init__(self):
        self.hand = []
        self.value = 0
class player(char):
    def __init__(self):
        self.balance = 500
        self.bet = 0
        self.hand = []
        self.value = 0
    def __str__(self):
        return 'You are dealt: '
    def __repr__(self):
        return 'You now have: '
class dealer(char):
    def __init__(self):
        self.hand = []
        self.value = 0
    def __str__(self):
        return 'The dealer hits and is dealt: '
    def __repr__(self):
        return 'The dealer has: '
class game:
    n = 0
    gamedeck = Deck()
    player = player()
    dealer = dealer()
    def value(self, item):
        x = []
        for i in item.hand:
            if i[0] == "A":
                x.append(1)
            else:
                item.value += Deck.card_dict[i]
        if len(x) > 0:
            while True:
                if item.value < 10 and len(x) > 1:
                    item.value += 1
                    x.pop()
                    continue
                elif item.value >= 10 and len(x) > 1:
                    item.value += len(x)
                    break
                elif item.value > 10 and len(x) == 1:
                    item.value += 1
                    break
                elif item.value <= 10 and len(x) == 1:
                    item.value += 11
                    break
    def reset(self):
        game.gamedeck = Deck()
        game.gamedeck.shuffle()
        game.player.hand = []
        game.player.value = 0
        game.player.bet = 0
        game.dealer.hand = []
        game.dealer.value = 0
    def start(self):
        self.reset()
        while True:
            bet = float(input("Place your bet: "))
            if bet > game.player.balance:
                print("You do not have sufficient funds.")
            elif bet < 1:
                print("The minimum bet is $1.")
            else:
                game.player.bet = bet
                break
        game.player.hand.append(game.gamedeck.deal())
        game.player.hand.append(game.gamedeck.deal())
        game.dealer.hand.append(game.gamedeck.deal())
        game.dealer.hand.append(game.gamedeck.deal())
        print(f"You are dealt: {game.player.hand[0]}, {game.player.hand[1]}")
        print(f"The dealer has: {game.dealer.hand[0]}, Unknown")
        self.value(game.player)
        self.value(game.dealer)
    def hit(self, item):
        item.hand.append(game.gamedeck.deal())
        item.value = 0
        print(f"{str(item)}{item.hand[-1]}")
        st = ""
        for i in item.hand:
            st += f"{i}, "
        print(f"{repr(item)}{st}")
        self.value(item)
    def play(self):
        x = input(f"You are starting with {game.player.balance}. Would you like to play a hand? ")
        if x != "yes":
            game.n = 1
            return 
        self.start()
        if game.player.value == 21:
            print(f"The dealer has: {game.dealer.hand[0]}, {game.dealer.hand[1]}")
            if game.dealer.value != 21:
                print(f"Blackjack! You win {game.player.bet * 1.5} :)")
                game.player.balance += game.player.bet * 1.5
                return 
        else:
            while True:
                x = input("Would you like to hit or stay? ")
                if x == "hit":
                    self.hit(game.player)
                    if game.player.value > 21:
                        print(f"Your hand value is over 21 and you lose {game.player.bet} :(")
                        game.player.balance -= game.player.bet  
                        return 
                elif x == "stay":
                    break
                else:
                    print("That is not a valid option.")
            print(f"The dealer has: {game.dealer.hand[0]}, {game.dealer.hand[1]}")
            while game.dealer.value < 17:
                self.hit(game.dealer)
                if game.dealer.value > 21:
                    print(f"The dealer busts, you win {game.player.bet} :)")
                    game.player.balance += game.player.bet  
                    return 
            print("The dealer stays.")
            if game.player.value > game.dealer.value:
                print(f'You win {game.player.bet}!')
                game.player.balance += game.player.bet
            elif game.player.value == game.dealer.value:
                print(f'You tie. Your bet has been returned.')
            else:
                print(f"The dealer wins, you lose {game.player.bet} :(")
                game.player.balance -= game.player.bet

print("Welcome to Blackjack!")
blackjack = game()

while game.player.balance >= 1:
    if game.n == 1:
        break
    blackjack.play()
else:
    print("You've ran out of money. Please restart this program to try again. Goodbye.")