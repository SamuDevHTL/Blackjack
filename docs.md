# FaceId-gambling Documentation

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![macOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)

## 📋 Table of Contents
- [Overview](#-overview)
- [Architecture](#-architecture)
- [Database Schema](#-database-schema)
- [Authentication System](#-authentication-system)
- [Game System](#-game-system)
- [Leaderboard System](#-leaderboard-system)
- [Logging System](#-logging-system)
- [UI/UX Design](#-uiux-design)
- [Getting Started](#-getting-started)

## 📖 Overview
A modern web-based Blackjack game with user authentication, virtual currency system, and a global leaderboard. Built with Flask and MySQL, featuring a sleek, responsive UI with smooth animations and gradients.

## 🏗️ Architecture

### Backend (Flask)
- **Framework**: Flask (Python)
- **Database**: MySQL
- **Authentication**: Session-based
- **Logging**: Multi-level logging system

### Frontend
- **Styling**: Custom CSS with modern design principles
- **Fonts**: Poppins (Google Fonts)
- **UI Components**: Pure CSS, no JavaScript framework
- **Animations**: CSS transitions and transforms

## 💾 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    money DECIMAL(10,2) NOT NULL DEFAULT 50.00
);
```

## 🔐 Authentication System

### Features
- User registration with unique username
- Login/logout functionality
- Session-based authentication
- Starting balance of $50 for new users

### Routes
- `/register` - New user registration
- `/login` - User authentication
- `/logout` - Session termination

## 🎮 Game System

### Blackjack Implementation
- Standard casino rules
- Card values:
  - Number cards (2-10): Face value
  - Face cards (J, Q, K): 10
  - Ace: 1 or 11 (automatically optimized)
- Dealer must hit on 16 and below, stand on 17 and above
- Natural blackjack pays 3:2

### Game Routes
- `/blackjack` - Main game view
- `/blackjack/new` - Start new game
- `/blackjack/hit` - Hit action
- `/blackjack/stand` - Stand action

### Betting System
- Configurable bet amounts
- Real-time balance updates
- Minimum bet: $1
- Maximum bet: Current balance

## 🏆 Leaderboard System

### Features
- Real-time global rankings
- Top 10 players display
- Personal stats section
- Current user highlighting
- Live balance updates

### Implementation
- SQL ranking using `RANK()` window function
- Sorted by player balance
- Updates automatically with game results

## 📊 Logging System

### Log Types
1. **Authentication Log** (`logs/auth.log`)
   - User registrations
   - Login attempts
   - Logout events

2. **Game Log** (`logs/game.log`)
   - Game starts
   - Bet amounts
   - Game outcomes
   - Balance changes

3. **Error Log** (`logs/errors.log`)
   - Database errors
   - Authentication failures
   - Game state errors

## 🎨 UI/UX Design

### Design Principles
- Modern, clean interface
- Responsive layout
- Card-based components
- Consistent color scheme
- Interactive animations

### Color Scheme
- Primary Gradient: `#ff6ec4` to `#7873f5`
- Background: Light with blur effects
- Text: Dark gray (`#4b4b4b`)
- Accents: Gold (`#ffd700`)

### Components
1. **Game Area**
   - Dealer's hand
   - Player's hand
   - Game controls
   - Balance display

2. **Leaderboard**
   - User stats section
   - Rankings table
   - Navigation controls

3. **Cards**
   - Visual card representations
   - Hover animations
   - Hidden/revealed states

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- MySQL 5.7 or higher
- pip (Python package manager)
- Git

### Step-by-Step Setup Guide

<details>
<summary>1. System Setup</summary>

#### For Ubuntu/Debian:
```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv

# Install MySQL
sudo apt install mysql-server

# Start MySQL service
sudo systemctl start mysql
sudo systemctl enable mysql
```

#### For Windows:
1. Download and install Python from [python.org](https://www.python.org/downloads/)
2. Download and install MySQL from [mysql.com](https://dev.mysql.com/downloads/installer/)
3. Add Python and pip to your PATH environment variable
</details>

<details>
<summary>2. Database Setup</summary>

```bash
# Login to MySQL (Windows: use MySQL Command Line Client)
sudo mysql -u root -p

# Create database and user
mysql> CREATE DATABASE gambling;
mysql> CREATE USER 'samudev'@'localhost' IDENTIFIED BY 'your_password';
mysql> GRANT ALL PRIVILEGES ON gambling.* TO 'samudev'@'localhost';
mysql> FLUSH PRIVILEGES;
mysql> USE gambling;

# Create users table
mysql> CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    money DECIMAL(10,2) NOT NULL DEFAULT 50.00
);

mysql> exit;
```
</details>

<details>
<summary>3. Project Setup</summary>

```bash
# Clone the repository
git clone https://github.com/yourusername/FaceId-gambling.git
cd FaceId-gambling

# Create and activate virtual environment
## For Linux/macOS:
python3 -m venv venv
source venv/bin/activate

## For Windows:
python -m venv venv
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```
</details>

<details>
<summary>4. Configuration</summary>

1. Create a `requirements.txt` file if it doesn't exist:
```bash
echo "flask
mysql-connector-python
python-dotenv" > requirements.txt
```

2. Create a `.env` file for environment variables:
```bash
echo "FLASK_APP=app.py
FLASK_ENV=development
DB_HOST=localhost
DB_USER=samudev
DB_PASSWORD=your_password
DB_NAME=gambling
SECRET_KEY=your-secret-key-here" > .env
```

3. Create required directories:
```bash
# Create directories for logs and static files
mkdir -p logs static/cards static/css
```
</details>

<details>
<summary>5. Running the Application</summary>

1. First run setup:
```bash
# Make sure you're in the project directory with venv activated
flask run --debug
```

2. Access the application:
- Open your browser and navigate to `http://localhost:5000`
- Register a new account
- Start playing!
</details>

### Directory Structure
```
FaceId-gambling/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
├── static/            # Static assets
│   ├── css/          # Stylesheets
│   └── cards/        # Card images
├── templates/         # HTML templates
├── logs/             # Application logs
│   ├── auth.log      # Authentication logs
│   ├── game.log      # Game logs
│   └── errors.log    # Error logs
└── venv/             # Virtual environment
```
