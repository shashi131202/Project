# Supermarket Billing System

## Overview
The **Supermarket Billing System** is a Java-based application that helps manage supermarket purchases, track customer details, and update product inventories. It connects to a MySQL database using JDBC to store and retrieve product and customer data.

## Features
- View available products and their details.
- Purchase products and update stock automatically.
- Generate bills with GST and discount calculations.
- Store customer details and purchase history in the database.

## Technologies Used
- **Java** (JDK 8+)
- **MySQL** (Database)
- **JDBC** (Database Connectivity)
- **Scanner Class** (For user input handling)

## Database Setup
1. **Create the database:**
   ```sql
   CREATE DATABASE super;
   USE super;
   ```
2. **Create tables:**
   ```sql
   CREATE TABLE products (
       Product_ID INT AUTO_INCREMENT PRIMARY KEY,
       Name_of_product VARCHAR(255) NOT NULL,
       Price_Of_Product FLOAT NOT NULL,
       Qunatity_Available INT NOT NULL
   );

   CREATE TABLE customer (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255) NOT NULL,
       phone_no INT NOT NULL,
       bill DOUBLE NOT NULL
   );

   CREATE TABLE purchases (
       id INT,
       product_name VARCHAR(255),
       quantity INT,
       total_cost DOUBLE,
       FOREIGN KEY (id) REFERENCES customer(id)
   );
   ```

## How to Run
1. **Compile the Java Program:**
   ```sh
   javac SuperMarket.java
   ```
2. **Run the Program:**
   ```sh
   java SuperMarket
   ```
3. **Follow On-Screen Instructions:**
   - View available products.
   - Purchase items and generate a bill.
   - Enter customer details.

## Example Usage
- **Viewing Products:**
  - Displays a list of available products.
- **Purchasing Products:**
  - User enters product ID and quantity.
  - Total cost is calculated.
  - Stock is updated in the database.
- **Generating Bill:**
  - GST (20%) and Discount (30%) are applied.
  - Final bill amount is displayed.

## Troubleshooting
- Ensure **MySQL is running** and the database `super` is created.
- Verify **JDBC MySQL driver** is installed and added to the project classpath.
- If `java.sql.SQLException` occurs, check **database credentials** in the code.

# Stock Analysis Bot

## Overview
The **Stock Analysis Bot** is a Streamlit-based chatbot that provides real-time stock market analysis using **Yahoo Finance API** and **Google Gemini AI**. It can fetch stock prices, compute technical indicators, and visualize stock trends.

## Features
- **Fetch Live Stock Prices** (Indian and global stocks)
- **Compute Technical Indicators**
  - Simple Moving Average (SMA)
  - Exponential Moving Average (EMA)
  - Relative Strength Index (RSI)
  - Moving Average Convergence Divergence (MACD)
- **Stock Price Visualization**
- **AI-Powered Chatbot Integration**

## Technologies Used
- **Python** (3.x)
- **Streamlit** (Web UI)
- **Yahoo Finance API (`yfinance`)** (Stock data)
- **Google Generative AI (`google.generativeai`)**
- **Matplotlib** (Data visualization)
- **Joblib & dotenv** (Environment management)

## Installation
### Prerequisites
- Python 3.x installed
- A Google Gemini API key
- Required Python dependencies installed

### Setup
1. **Clone the Repository**
   ```sh
   git clone https://github.com/yourusername/stock-analysis-bot.git
   cd stock-analysis-bot
   ```
2. **Create a Virtual Environment** (Optional but recommended)
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set Up Environment Variables**
   - Create a `.env` file in the project directory.
   - Add your **Google Gemini API key**:
     ```sh
     GOOGLE_API_KEY=your_google_gemini_api_key_here
     ```

## Usage
### Run the Stock Analysis Bot
```sh
streamlit run stock_analysis_bot.py
```

### Example Commands
- **Get stock price**: "What is the stock price of AAPL?"
- **Calculate SMA**: "Calculate 50-day SMA for TESLA"
- **Plot stock price**: "Show me the stock price graph of MSFT or Microsoft"
- "If Indian Stocks type .NS after Stock ticker"

## Troubleshooting
- Ensure your **Google API key or Gemini API key** is correctly set in the `.env` file.
- If dependencies are missing, try running:
  ```sh
  pip install --upgrade -r requirements.txt
  ```
- Check if **Yahoo Finance API (`yfinance`)** is correctly fetching stock data.

