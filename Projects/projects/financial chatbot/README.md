

# 💹 Financial Stock Analysis Chatbot

An **AI-powered financial assistant** built using **Streamlit**, **Google Gemini API**, and **Yahoo Finance (yfinance)**.
This chatbot understands natural language stock-related queries, identifies the required technical indicator (SMA, EMA, RSI, MACD, etc.), and displays results or charts dynamically.

---

## 🚀 Features

✅ **Natural language understanding** using **Gemini Pro**
✅ **Real-time stock price retrieval** (Indian & Global)
✅ **Technical indicators**:

* SMA (Simple Moving Average)
* EMA (Exponential Moving Average)
* RSI (Relative Strength Index)
* MACD (Moving Average Convergence Divergence)
  ✅ **Stock price chart plotting (1 year)**
  ✅ **Support for both INR (Indian stocks)** and **USD (Global stocks)**
  ✅ **Streamlit chat interface** with conversational memory

---

## 🧠 Tech Stack

| Component              | Technology                                    |
| ---------------------- | --------------------------------------------- |
| Frontend               | Streamlit                                     |
| AI Model               | Google Gemini-Pro (via `google.generativeai`) |
| Financial Data         | Yahoo Finance (`yfinance`)                    |
| Data Visualization     | Matplotlib                                    |
| Environment Management | Python Dotenv                                 |
| Serialization          | Joblib, JSON                                  |
| Language               | Python 3.11+                                  |

---

## 🗂️ Project Structure

```
financial_chatbot/
│
├── app.py                        # Main Streamlit app file
├── .env                          # Environment variables (API key)
├── requirements.txt              # Python dependencies
├── stock.png                     # Generated stock chart (temporary)
└── README.md                     # Documentation
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/financial-stock-chatbot.git
cd financial-stock-chatbot
```

### 2️⃣ Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set up environment variables

Create a `.env` file in your project root and add your Gemini API key:

```
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

### 5️⃣ Run the Streamlit app

```bash
streamlit run app.py
```

---

## 💬 How to Use

1. Run the app and open the Streamlit UI in your browser.
2. Enter a query such as:

   * `Get stock price of AAPL`
   * `What is the 50-day EMA of RELIANCE.NS`
   * `Plot the stock price chart of INFY.NS`
   * `Calculate RSI for TSLA`
3. The chatbot will either respond with the result or display a chart.

💡 **Tip:**
For Indian stocks, **add `.NS`** to the symbol (e.g., `TCS.NS`, `INFY.NS`), or just type “Indian stock” before it — Gemini will infer automatically.

---

## 📊 Example Outputs

### 🧾 Example Query 1:

**User:**

> What is the current price of AAPL?

**Response:**

> The current stock price of AAPL in USD is $230.56.

---

### 🧾 Example Query 2:

**User:**

> Plot the 1-year stock chart for RELIANCE.NS

**Response:**

![Stock Chart Example](financialchatbot/stock.png)

> Plot displayed above.

---

## 📈 Supported Functions

| Function                        | Description                              |
| ------------------------------- | ---------------------------------------- |
| `get_stock_price(ticker)`       | Fetches latest closing price             |
| `calculate_SMA(ticker, window)` | Calculates simple moving average         |
| `calculate_EMA(ticker, window)` | Calculates exponential moving average    |
| `calculate_RSI(ticker)`         | Computes relative strength index         |
| `calculate_MACD(ticker)`        | Returns MACD, signal line, and histogram |
| `plot_stock_price(ticker)`      | Displays 1-year stock price chart        |

---

## 🔒 Environment Variables

| Variable         | Description                    |
| ---------------- | ------------------------------ |
| `GOOGLE_API_KEY` | Your Google Gemini Pro API key |

You can get it from [Google AI Studio](https://makersuite.google.com/app/apikey).

---

## 🧩 Dependencies

Create a `requirements.txt` with the following content:

```
streamlit
yfinance
matplotlib
google-generativeai
python-dotenv
joblib
```

---

## ⚠️ Error Handling

* If `GOOGLE_API_KEY` is missing → Streamlit will display an error and stop execution.
* Invalid ticker symbols → Error message displayed using `st.error()`.
* JSON decoding or Gemini misinterpretation → Handled gracefully with fallback response.

---

