# 🃏 Belote Cards Vision

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red)
![YOLO](https://img.shields.io/badge/YOLO-Ultralytics-green)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)
![License](https://img.shields.io/badge/license-MIT-orange.svg?style=flat)
![GitHub last commit](https://img.shields.io/github/last-commit/[Heenok93/belote-cards-vision](https://github.com/Heenok93/belote-cards-vision))

Automatic Belote card recognition and scoring application based on **Deep Learning** and **Software Engineering** principles.

The application analyses a photo of a Belote hand, detects the cards using a fine-tuned YOLO model, computes the score according to official Belote rules, allows manual corrections and stores game results in a local SQLite database.

---

# ✨ Features

- 🔐 User authentication
- 📷 Image upload
- 🔍 Automatic image quality assessment
- 🎨 Optional image preprocessing
- 🤖 Automatic card detection using YOLO
- ♠ Belote score computation
- ✏ Manual card correction
- 🏆 Game score management
- 💾 SQLite persistence
- 📱 Responsive interface (desktop & mobile)
- 🐳 Docker deployment

---

# 📸 Application Workflow

```text
Upload image
      │
      ▼
Image quality diagnosis
      │
      ▼
Optional preprocessing
      │
      ▼
YOLO detection
      │
      ▼
Manual correction
      │
      ▼
Belote scoring engine
      │
      ▼
SQLite database
```

---

# 🏗 Project Architecture

```text
belote-cards-vision
│
├── config/
├── models/
│
├── src/
│   ├── assets/
│   ├── database/
│   ├── game/
│   ├── services/
│   └── views/
│
├── Dockerfile
├── docker-compose.yml
├── docker-compose.dev.yml
├── main.py
├── requirements.txt
└── README.md
```

---

# ⚙ Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| Streamlit | User Interface |
| Ultralytics YOLO | Card Detection |
| OpenCV | Image preprocessing |
| SQLite | Local database |
| Pandas | Data manipulation |
| Docker | Deployment |

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/Heenok93/belote-cards-vision.git

cd belote-cards-vision
```

Build and run with Docker

```bash
docker compose up
```

Open the application

```text
http://localhost:8501
```

---

# 📖 Usage

1. Login
2. Upload a Belote hand image
3. Check image quality
4. Apply preprocessing if recommended
5. Launch AI analysis
6. Correct detected cards if necessary
7. Save the score
8. View cumulative scores

---

# 🧠 Artificial Intelligence

The application uses a custom fine-tuned **Ultralytics YOLO** model trained specifically for French Belote cards.

Main characteristics:

- 32 Belote card classes
- Real-world dataset
- Fine-tuning on custom images
- Automatic confidence threshold adjustment
- Manual correction workflow

---

# ♠ Belote Scoring Engine

The scoring engine implements official Belote rules:

- Classic mode
- All Trump
- No Trump
- Dix de Der
- Belote / Rebelote
- Automatic score computation

---

# 🗄 Database

Game results are stored locally using SQLite.

Current features:

- Game creation
- Round history
- Running score
- Score correction
- New game management

---

# 📱 Responsive Design

The interface has been designed for both desktop and mobile devices.

Supported workflows include:

- Smartphone image upload
- Mobile correction interface
- Desktop advanced editor
- Responsive navigation

---

# 📂 Screenshots

### Home

*(Insert screenshot here)*

---

### AI Detection

*(Insert screenshot here)*

---

### Manual Correction

*(Insert screenshot here)*

---

### Score Management

*(Insert screenshot here)*

---

### Mobile Interface

*(Insert screenshot here)*

---

# 🔮 Future Improvements

- Tarot support
- PDF score reports
- Multi-user support
- Cloud deployment
- Automatic game history export

---

# 👨‍💻 Software Engineering

This project was developed following Software Engineering best practices:

- Modular architecture
- Separation of concerns
- Service-oriented design
- Responsive UI
- Docker containerization
- SQLite persistence
- Maintainable codebase

---

# 📜 License

This project is distributed under the MIT License.

---

# 👤 Author

**Thomas Roederer**

Deep Learning & Software Engineering Project

GitHub:

https://github.com/Heenok93

