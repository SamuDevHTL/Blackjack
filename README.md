# FaceId-gambling

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![macOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0)
![iOS](https://img.shields.io/badge/iOS-000000?style=for-the-badge&logo=ios&logoColor=white)![Android](https://img.shields.io/badge/Android-3DDC84?style=for-the-badge&logo=android&logoColor=white)

> A secure Flask web application that combines facial recognition with an engaging gambling system, featuring a Blackjack game implementation.

## 📋 Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [Security Considerations](#security-considerations)
- [Roadmap](#roadmap)

## ✨ Features

### 🔐 Authentication & Security
- User authentication system (register/login/logout)
- Session management
- MySQL database integration
- Virtual currency system with initial 50 credit balance
- Transaction logging and monitoring

### 🎰 Blackjack Game
- Complete game logic following standard casino rules
- Intelligent dealer AI (hits on 16-, stands on 17+)
- Card scoring system:
  - Face cards = 10
  - Ace = 1 or 11 (dynamic)
  - Number cards = face value
- Multiple win conditions:
  - Natural blackjack (3:2 payout)
  - Regular win (1:1 payout)
  - Push and bust detection
- Configurable betting system

### 🎨 User Interface
- Modern, responsive design
- Mobile-friendly layout
- Real-time balance updates
- Interactive game controls
- Strategic dealer card visibility
- Intuitive game messaging system

## 🛠️ Technologies Used
- Python 3.6+
- Flask web framework
- MySQL database
- HTML5/CSS3
- JavaScript
- Docker (coming soon)

## 🏗️ Project Structure

### Database Schema
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    money DECIMAL(10,2) DEFAULT 50.00
);
```

### API Endpoints

#### Authentication Routes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Login page |
| POST | `/` | Process login |
| GET | `/register` | Registration page |
| POST | `/register` | Process registration |
| GET | `/logout` | Logout user |

#### Game Routes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/blackjack` | Main game view |
| GET | `/blackjack/new` | Start new game |
| GET | `/blackjack/hit` | Hit action |
| GET | `/blackjack/stand` | Stand action |

## 🚀 Getting Started

1. Clone the repository
```bash
git clone https://github.com/your-username/FaceId-gambling.git
cd FaceId-gambling
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. Run the application
```bash
python app.py
```

## 🔒 Security Considerations

> ⚠️ **Note**: This is currently a development version. For production deployment, implement:

- Password hashing
- Enhanced session management
- Rate limiting
- SQL injection protection
- CSRF protection
- HTTPS enforcement

## 🗺️ Roadmap

- [ ] Face ID integration