import random
import csv
import os


def draw_card():
    card = random.randint(1, 13)
    if card > 10:
        card = 10
    elif card == 1:
        card = 11
    return card

def hand_value(cards):
    value = sum(cards)
    aces = cards.count(11)
    
    while value > 21 and aces > 0:
        value -= 10
        aces -= 1
    
    return value


def play_game():
    # Creating dealer and player cards
    d_cards = [draw_card() for _ in range(2)]
    p_cards = [draw_card() for _ in range(2)]
    player_actions =[]
    split_cards = []
    



    while True:
        try:
            bet_amount = int(input("How much do you want to bet? Max Bet is 1000: "))
            if bet_amount > 1000:
                print("You can't bet this much, all bets must be under 1000")
            elif bet_amount <= 1000:
                print("You have bet", bet_amount, "credits")
                break
            else:
                print("Invalid input. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            
    print("Dealer's face-up card:", d_cards[0])
    print("Your initial cards:", p_cards)

    # Check if dealer has a blackjack
    if hand_value(d_cards) == 21 and len(d_cards) == 2:
        print("Dealer's cards:", d_cards)
        return p_cards, split_cards, d_cards, 'Dealer Wins', -bet_amount, bet_amount, player_actions


    # Player's turn
    while hand_value(p_cards) < 21:
        action_taken = input("Do you want to hit, stay, double down, or split? ").lower()
        player_actions.append(action_taken)
        if action_taken == "hit":
            p_cards.append(random.randint(1, 11))
            print("You now have a total of", hand_value(p_cards), "from these cards:", p_cards)
        elif action_taken == "stay":
            break
        elif action_taken == "double down" and len(p_cards) == 2:
            p_cards.append(random.randint(1, 11))
            print("You now have a total of", hand_value(p_cards), "from these cards:", p_cards)

            bet_amount *= 2
            break
        elif action_taken == "split" and len(p_cards) == 2 and p_cards[0] == p_cards[1]:
            split_cards = [p_cards.pop(), random.randint(1, 11)]
            p_cards.append(random.randint(1, 11))
            print("You split your cards! Your first hand is", p_cards, "and your second hand is", split_cards)
        else:
            print("Invalid action.")

    # Check player's card sum
    if hand_value(p_cards) > 21:
        print("Dealer's cards:", d_cards)
        print("You lost", bet_amount, "credits.")
        return p_cards, split_cards, d_cards, 'Dealer Wins', -bet_amount, bet_amount, player_actions
    elif hand_value(p_cards) == 21:
        print("You won", bet_amount, "credits.")
        return p_cards, split_cards, d_cards, 'Player Wins', bet_amount, bet_amount, player_actions

    # Dealer's turn
    while hand_value(d_cards) < 17:
        d_cards.append(draw_card())
        print("Dealer now has a total of", hand_value(d_cards), "from these cards:", d_cards)

    # Check dealer's card sum
    if hand_value(d_cards) > 21:
        print("You won", bet_amount, "credits.")
        return p_cards, split_cards, d_cards, 'Player Wins', bet_amount, bet_amount, player_actions
    elif hand_value(d_cards) > hand_value(p_cards):
        print("Dealer's cards:", d_cards)
        print("You lost", bet_amount, "credits.")
        return p_cards, split_cards, d_cards, 'Dealer Wins', -bet_amount, bet_amount, player_actions
    elif hand_value(d_cards) == hand_value(p_cards):
        print("Dealer's cards:", d_cards)
        print("It's a tie. You didn't win or lose any credits.")
        return p_cards, split_cards, d_cards, 'Tie', 0, bet_amount, player_actions
    else:
        print("You won", bet_amount, "credits.")
        return p_cards, split_cards, d_cards, 'Player Wins', bet_amount, bet_amount, player_actions
# Create a CSV file to store results
# Function to check if the file is empty
def is_file_empty(file_path):
    return os.path.getsize(file_path) == 0

# Create or append to a CSV file to store results
file_name = 'blackjack_results.csv'
with open(file_name, mode='a', newline='') as csv_file:
    fieldnames = ['player_cards', 'split_cards', 'd_cards', 'actions', 'result', 'bet_amount', 'payout']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the header only if the file is empty
    if is_file_empty(file_name):
        writer.writeheader()

    while True:
        p_cards, split_cards, d_cards, result, payout, bet_amount, player_actions = play_game()
        print(result)

        # Write the results to the CSV file
        writer.writerow({'player_cards': p_cards, 'split_cards': split_cards, 'd_cards': d_cards, 'actions': player_actions, 'result': result, 'bet_amount': bet_amount, 'payout': payout})

        # Ask the player to play again
        play_again = input("Do you want to play again? (yes or no)").lower()
        if play_again != "yes":
            break

