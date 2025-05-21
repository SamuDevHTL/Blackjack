from flask import Flask, render_template, request, redirect, url_for, session
from mysql.connector import connect, Error
import random

app = Flask(__name__)
app.secret_key = "change_this_to_a_random_secret"  # Needed for sessions

def connect_db():
    try:
        return connect(
            host="localhost",
            user="samudev",
            password="pac",
            database="gambling"
        )
    except Error as e:
        print(f"Database connection error: {e}")
        return None

# Helper: get user money from DB
def get_user_money(user_id):
    conn = connect_db()
    money = 0
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT money FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        if result:
            money = result[0]
        cursor.close()
        conn.close()
    return money

# Helper: update user money in DB
def update_user_money(user_id, new_money):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET money = %s WHERE id = %s", (new_money, user_id))
        conn.commit()
        cursor.close()
        conn.close()

# Card deck setup
SUITS = ['♠', '♣', '♥', '♦']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

def create_deck():
    deck = [(rank, suit) for suit in SUITS for rank in RANKS]
    random.shuffle(deck)
    return deck

def calculate_hand_value(hand):
    value = 0
    aces = 0
    
    for card in hand:
        rank = card[0]
        if rank in ['J', 'Q', 'K']:
            value += 10
        elif rank == 'A':
            aces += 1
        else:
            value += int(rank)
    
    # Add aces
    for _ in range(aces):
        if value + 11 <= 21:
            value += 11
        else:
            value += 1
            
    return value

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "SELECT id FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                user_id = user[0]
                session['user_id'] = user_id
                return redirect(url_for("blackjack"))
            else:
                message = "Invalid username or password."

    return render_template("login.html", message=message)

@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                message = "Username already taken."
            else:
                try:
                    cursor.execute(
                        "INSERT INTO users (username, password, money) VALUES (%s, %s, %s)",
                        (username, password, 50)
                    )
                    conn.commit()
                    cursor.close()
                    conn.close()
                    return redirect(url_for("login"))
                except Error as e:
                    message = f"Registration failed: {e}"
            cursor.close()
            conn.close()

    return render_template("register.html", message=message)

@app.route("/blackjack")
def blackjack():
    if 'user_id' not in session:
        return redirect(url_for("login"))

    user_id = session['user_id']
    money = get_user_money(user_id)

    if 'deck' not in session:
        session['deck'] = create_deck()
        session.modified = True

    return render_template("blackjack.html",
                         money=money,
                         player_hand=session.get('player_hand', []),
                         dealer_hand=session.get('dealer_hand', []),
                         game_over=session.get('game_over', False),
                         message=session.get('message', ""),
                         calculate_hand_value=calculate_hand_value)

@app.route("/blackjack/new")
def new_game():
    if 'user_id' not in session:
        return redirect(url_for("login"))

    user_id = session['user_id']
    money = get_user_money(user_id)
    bet_amount = 10  # Fixed bet amount

    if money < bet_amount:
        session['message'] = "Not enough money to play!"
        session['game_over'] = True
        session.modified = True
        return redirect(url_for('blackjack'))

    # Initialize a new game
    deck = create_deck()
    
    # Deal initial cards
    player_hand = [deck.pop() for _ in range(2)]
    dealer_hand = [deck.pop() for _ in range(2)]
    
    # Store everything in session
    session['deck'] = deck
    session['player_hand'] = player_hand
    session['dealer_hand'] = dealer_hand
    session['game_over'] = False
    session['message'] = ''
    session.modified = True
    
    # Deduct bet amount
    money -= bet_amount
    update_user_money(user_id, money)
    
    # Check for natural blackjack
    if calculate_hand_value(player_hand) == 21:
        session['message'] = 'Blackjack! You win!'
        session['game_over'] = True
        money += bet_amount * 2.5  # Blackjack pays 3:2
        update_user_money(user_id, money)
        session.modified = True
    
    return redirect(url_for('blackjack'))

@app.route("/blackjack/hit")
def hit():
    if 'user_id' not in session:
        return redirect(url_for("login"))

    if session.get('game_over'):
        return redirect(url_for('blackjack'))
    
    # Get current state
    deck = session['deck']
    player_hand = session['player_hand']
    
    # Deal one card to player
    player_hand.append(deck.pop())
    
    # Update session
    session['deck'] = deck
    session['player_hand'] = player_hand
    session.modified = True
    
    # Check hand value
    player_value = calculate_hand_value(player_hand)
    if player_value > 21:
        session['message'] = 'Bust! You lose!'
        session['game_over'] = True
        session.modified = True
    elif player_value == 21:
        session['message'] = 'You got 21!'
        session.modified = True
        return redirect(url_for('blackjack_stand'))
    
    return redirect(url_for('blackjack'))

@app.route("/blackjack/stand")
def blackjack_stand():
    if 'user_id' not in session:
        return redirect(url_for("login"))

    if session.get('game_over'):
        return redirect(url_for('blackjack'))
    
    user_id = session['user_id']
    money = get_user_money(user_id)
    bet_amount = 10  # Fixed bet amount
    
    # Get current state
    deck = session['deck']
    dealer_hand = session['dealer_hand']
    
    # Dealer's turn
    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(deck.pop())
    
    # Update session
    session['deck'] = deck
    session['dealer_hand'] = dealer_hand
    session.modified = True
    
    # Calculate final values
    player_value = calculate_hand_value(session['player_hand'])
    dealer_value = calculate_hand_value(dealer_hand)
    
    # Determine winner
    if dealer_value > 21:
        session['message'] = 'Dealer busts! You win!'
        money += bet_amount * 2
    elif dealer_value > player_value:
        session['message'] = 'Dealer wins!'
    elif dealer_value < player_value:
        session['message'] = 'You win!'
        money += bet_amount * 2
    else:
        session['message'] = 'Push! It\'s a tie!'
        money += bet_amount
    
    session['game_over'] = True
    session.modified = True
    update_user_money(user_id, money)
    return redirect(url_for('blackjack'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

