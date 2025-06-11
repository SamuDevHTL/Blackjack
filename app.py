from flask import Flask, render_template, request, redirect, url_for, session
from mysql.connector import connect, Error
import random
import logging
import os
from datetime import datetime
from decimal import Decimal

app = Flask(__name__)
app.secret_key = "secret-key"  # Needed for sessions

os.makedirs('logs', exist_ok=True)

auth_logger = logging.getLogger('auth')
auth_logger.setLevel(logging.INFO)
auth_handler = logging.FileHandler(os.path.join('logs', 'auth.log'))
auth_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
auth_logger.addHandler(auth_handler)

game_logger = logging.getLogger('game')
game_logger.setLevel(logging.INFO)
game_handler = logging.FileHandler(os.path.join('logs', 'game.log'))
game_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
game_logger.addHandler(game_handler)

error_logger = logging.getLogger('error')
error_logger.setLevel(logging.ERROR)
error_handler = logging.FileHandler(os.path.join('logs', 'errors.log'))
error_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
error_logger.addHandler(error_handler)

def connect_db():
    try:
        return connect(
            host="localhost",
            user="samudev",
            password="pac",
            database="gambling"
        )
    except Error as e:
        error_logger.error(f"Database connection error: {e}")
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

def update_user_money(user_id, new_money):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET money = %s WHERE id = %s", (new_money, user_id))
            conn.commit()
            cursor.close()
            conn.close()
        except Error as e:
            error_logger.error(f"Failed to update money for user {user_id}: {e}")

def get_username(user_id):
    conn = connect_db()
    username = None
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        if result:
            username = result[0]
        cursor.close()
        conn.close()
    return username

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
            cursor = conn.cursor()                      #fix sql-injection
            query = "SELECT id FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                user_id = user[0]
                session['user_id'] = user_id
                auth_logger.info(f"Login: {username}")
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
                auth_logger.info(f"Registration failed - username already taken: {username}")
            else:
                try:
                    cursor.execute(
                        "INSERT INTO users (username, password, money) VALUES (%s, %s, %s)",
                        (username, password, 100)
                    )
                    conn.commit()
                    cursor.close()
                    conn.close()
                    auth_logger.info(f"New user registered: {username}")
                    return redirect(url_for("login"))
                except Error as e:
                    message = f"Registration failed: {e}"
                    error_logger.error(f"Registration error for {username}: {e}")
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
                         current_bet=session.get('current_bet', 10),
                         calculate_hand_value=calculate_hand_value)

@app.route("/blackjack/new", methods=["POST"])
def new_game():
    if 'user_id' not in session:
        return redirect(url_for("login"))

    user_id = session['user_id']
    money = get_user_money(user_id)
    username = get_username(user_id)
    
    try:
        bet_amount = int(request.form.get('bet_amount', 10))
        if bet_amount < 1:
            session['message'] = "Minimum bet is $1!"
            return redirect(url_for('blackjack'))
    except ValueError:
        session['message'] = "Invalid bet amount!"
        return redirect(url_for('blackjack'))

    if money < bet_amount:
        session['message'] = "Not enough money to place that bet!"
        session['game_over'] = True
        session.modified = True
        if username:
            error_logger.error(f"Insufficient funds - User: {username}, Attempted bet: ${bet_amount}, Balance: ${money}")
        return redirect(url_for('blackjack'))

    deck = create_deck()
    
    player_hand = [deck.pop() for _ in range(2)]
    dealer_hand = [deck.pop() for _ in range(2)]
    
    session['deck'] = deck
    session['player_hand'] = player_hand
    session['dealer_hand'] = dealer_hand
    session['game_over'] = False
    session['message'] = ''
    session['current_bet'] = bet_amount
    session.modified = True
    
    money -= bet_amount
    update_user_money(user_id, money)
    
    if username:
        game_logger.info(f"New game: {username} - Bet: ${bet_amount} - Balance: ${money}")
    
    if calculate_hand_value(player_hand) == 21:
        session['message'] = 'Blackjack! You win!'
        session['game_over'] = True
        winnings = Decimal(bet_amount * 2.5)
        money += winnings
        update_user_money(user_id, money)
        session.modified = True
        if username:
            game_logger.info(f"Blackjack win: {username} - Bet: ${bet_amount} - Balance: ${money}")
    
    return redirect(url_for('blackjack'))

@app.route("/blackjack/hit")
def hit():
    if 'user_id' not in session:
        return redirect(url_for("login"))

    if session.get('game_over'):
        return redirect(url_for('blackjack'))
    
    user_id = session['user_id']
    username = get_username(user_id)
    bet_amount = session.get('current_bet', 10)
    
    deck = session['deck']
    player_hand = session['player_hand']
    
    player_hand.append(deck.pop())
    
    session['deck'] = deck
    session['player_hand'] = player_hand
    session.modified = True
    
    player_value = calculate_hand_value(player_hand)
    if player_value > 21:
        session['message'] = 'Bust! You lose!'
        session['game_over'] = True
        session.modified = True
        if username:
            error_logger.info(f"Player Bust - User: {username}, Bet: ${bet_amount}, Final Value: {player_value}")
    elif player_value == 21:
        session['message'] = 'You got 21!'
        session.modified = True
        if username:
            error_logger.info(f"Player got 21 - User: {username}, Bet: ${bet_amount}")
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
    username = get_username(user_id)
    bet_amount = session.get('current_bet', 10)
    
    deck = session['deck']
    dealer_hand = session['dealer_hand']
    
    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(deck.pop())
    
    session['deck'] = deck
    session['dealer_hand'] = dealer_hand
    session.modified = True
    
    player_value = calculate_hand_value(session['player_hand'])
    dealer_value = calculate_hand_value(dealer_hand)
    
    if dealer_value > 21:
        session['message'] = 'Dealer busts! You win!'
        money += bet_amount * 2
        if username:
            game_logger.info(f"Win: {username} - Bet: ${bet_amount} - Balance: ${money}")
    elif dealer_value > player_value:
        session['message'] = 'Dealer wins!'
        if username:
            game_logger.info(f"Loss: {username} - Bet: ${bet_amount} - Balance: ${money}")
    elif dealer_value < player_value:
        session['message'] = 'You win!'
        money += bet_amount * 2
        if username:
            game_logger.info(f"Win: {username} - Bet: ${bet_amount} - Balance: ${money}")
    else:
        session['message'] = 'Push! It\'s a tie!'
        money += bet_amount
        if username:
            game_logger.info(f"Tie: {username} - Bet: ${bet_amount} - Balance: ${money}")
    
    session['game_over'] = True
    session.modified = True
    update_user_money(user_id, money)
    return redirect(url_for('blackjack'))

@app.route("/logout")
def logout():
    if 'user_id' in session:
        username = get_username(session['user_id'])
        if username:
            auth_logger.info(f"Logout: {username}")
    session.clear()
    return redirect(url_for("login"))

@app.route("/leaderboard")
def leaderboard():
    if 'user_id' not in session:
        return redirect(url_for("login"))
    
    conn = connect_db()
    leaderboard_data = []
    if conn:
        try:
            cursor = conn.cursor()
            # Get top 10 players by money
            cursor.execute("""
                SELECT username, money 
                FROM users 
                ORDER BY money DESC 
                LIMIT 10
            """)
            leaderboard_data = cursor.fetchall()
            cursor.close()
            conn.close()
        except Error as e:
            error_logger.error(f"Leaderboard error: {e}")
    
    # Get current user's rank
    user_id = session['user_id']
    user_rank = None
    user_money = get_user_money(user_id)
    username = get_username(user_id)
    
    if conn := connect_db():
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) + 1 
                FROM users 
                WHERE money > (
                    SELECT money 
                    FROM users 
                    WHERE id = %s
                )
            """, (user_id,))
            result = cursor.fetchone()
            if result:
                user_rank = result[0]
            cursor.close()
            conn.close()
        except Error as e:
            error_logger.error(f"User rank error: {e}")
    
    return render_template(
        "leaderboard.html",
        leaderboard=leaderboard_data,
        user_rank=user_rank,
        user_money=user_money,
        username=username
    )

if __name__ == "__main__":
    app.run(debug=True, port=5001)

