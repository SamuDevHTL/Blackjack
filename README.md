# FaceId-gambling

Flask web application combining facial recognition with a gambling system, featuring a Blackjack game.

## ✅ Current Features

### Core Systems
- [x] User authentication (register/login/logout)
- [x] MySQL database integration
- [x] Virtual currency with 50 credit starting balance
- [x] Real-time balance & transaction handling
- [x] simple Logs

### Blackjack Implementation
- [x] Complete game logic with standard casino rules
- [x] Card scoring (Face=10, Ace=1/11, Numbers=face value)
- [x] Dealer AI (hits on 16-, stands on 17+)
- [x] Win conditions
  - Natural blackjack (3:2)
  - Regular win (1:1)
  - Push & bust detection
- [X] Configurable bets

### Interface
- [x] Modern, responsive design
- [x] Hidden dealer cards
- [x] Game controls (Hit/Stand/New Game)
- [x] Balance & message display
- [x] Improve looks

## 🛠️ Structure

### Database
```sql
users (
    id: INT PRIMARY KEY
    username: VARCHAR(255)
    password: VARCHAR(255)
    money: DECIMAL(10,2)
)
```

### Routes
```
/                    → Login
/register            → Registration
/blackjack          → Game view
/blackjack/new      → New game
/blackjack/hit      → Hit action
/blackjack/stand    → Stand action
```

## 🚧 Limitations & TODO

### Current Limitations
- Basic security (no password hashing, simple sessions)
- Fixed bet amount (10 credits)
- No advanced game features (split, double down)

### Planned Features
- [ ] Face ID integration

## API Routes

### Authentication
- `GET /` - Login page
- `POST /` - Process login
- `GET /register` - Registration page
- `POST /register` - Process registration
- `GET /logout` - Logout user

### Game
- `GET /blackjack` - Main game view
- `GET /blackjack/new` - Start new game
- `GET /blackjack/hit` - Hit action
- `GET /blackjack/stand` - Stand action

## Security Notes

Current limitations:
   - Plain text password storage (not recommended for production)
   - Basic session management
   - No rate limiting

