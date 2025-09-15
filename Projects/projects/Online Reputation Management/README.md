---
# Online Reputation Management Tool

## 📌 Overview

The Online Reputation Management Tool is a web-based dashboard that helps businesses, content creators, and digital marketers monitor public sentiment across multiple social media platforms. It integrates with **Instagram, Threads, and X (Twitter)** APIs to fetch comments/replies and uses a **RoBERTa-based NLP model** for sentiment analysis.

## ✨ Features

* 🔗 **Multi-Platform Support** – Analyze sentiment from Instagram, Threads, and X in one dashboard.
* 🤖 **AI-Powered Sentiment Analysis** – Uses `cardiffnlp/twitter-roberta-base-sentiment` model to classify comments as **Positive, Neutral, or Negative**.
* 📊 **Interactive Dashboard** – Visualize results using **pie charts, sentiment summary cards, and filters**.
* ⚡ **Real-Time Insights** – Fetch and analyze comments instantly after selecting a post, thread, or tweet.
* 🔐 **Secure API Integration** – API tokens are stored in `.env` files to ensure safe usage.
* 🌐 **Responsive UI** – Built with **Flask, HTML5, Bootstrap, and JavaScript**.

## 🏗️ Architecture

The system consists of:

1. **Frontend (UI Module)** – HTML + Bootstrap + Chart.js for responsive visualization.
2. **Backend (Flask Server)** – Handles API requests and sentiment inference.
3. **NLP Module** – RoBERTa model for sentiment classification.
4. **API Integration Layer** – Connects with Instagram Graph API, Threads API, and Twitter API.

![Architecture Diagram](docs/architecture.png) *(Add image if available)*

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/online-reputation-management.git
cd online-reputation-management
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Create a `.env` file and add:

```ini
INSTAGRAM_ACCESS_TOKEN=your_instagram_token
INSTAGRAM_USER_ID=your_instagram_user_id
THREADS_ACCESS_TOKEN=your_threads_token
X_BEARER_TOKEN=your_twitter_bearer_token
X_USER_ID=your_twitter_user_id
```

### 5. Run the Application

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

## 📂 Project Structure

```
├── app.py                 # Flask backend
├── templates/
│   ├── dashboard.html      # Main dashboard
│   └── platform_page.html  # Individual platform analysis pages
├── requirements.txt       # Python dependencies
├── .env                   # API tokens (not committed to Git)
└── README.md              # Project documentation
```

## 🔮 Future Enhancements

* 📈 Add historical sentiment trend analysis.
* 📢 Real-time alerts for sudden reputation shifts.
* 🌍 Support for multilingual sentiment analysis.
* 🎥 Extend to platforms like YouTube and Reddit.

## 👨‍💻 Contributors

* **M. Shashikanth**
* **M. Yeshwanth Reddy**
* **B. Kevin**
* **T. Yashwanth Raj**

Under the guidance of **Dr. T. V. G. Sridevi**
Department of CSE (AI & ML), KMIT

---
