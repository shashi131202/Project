import time
import os
import joblib
import streamlit as st
import google.generativeai as genai
import yfinance as yf
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import json
import re

load_dotenv()
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
if GOOGLE_API_KEY is None:
    st.error("GOOGLE_API_KEY environment variable not set. Please set it.")
    st.stop()  # Stop execution if API key is missing

genai.configure(api_key=GOOGLE_API_KEY)

def is_indian_stock(ticker):
    return ticker.endswith(".NS")

# Define your functions (same as before)
def get_stock_price(ticker):
    try:
        # Check if the ticker is an Indian stock (ends with .NS)
        ticker_data = yf.Ticker(ticker)
        data = ticker_data.history(period='1d')
        price = data['Close'].iloc[-1]
        
        if is_indian_stock(ticker):  # Indian stock prices are already in INR
            return f"The current stock price of {ticker} in INR is ₹{price:.2f}"
        else:  # Global stocks are in USD by default
            return f"The current stock price of {ticker} in USD is ${price:.2f}"
    except Exception as e:
        st.error(f"Error fetching stock price: {e}")
        return None

def calculate_SMA(ticker, window):
    try:
        data = yf.Ticker(ticker).history(period='1y')['Close']
        sma = data.rolling(window=window).mean().iloc[-1]
        if is_indian_stock(ticker):
            return f"The {window}-day Simple Moving Average for {ticker} in INR is ₹{sma:.2f}"
        else:
            return f"The {window}-day Simple Moving Average for {ticker} in USD is ${sma:.2f}"
    except Exception as e:
        st.error(f"Error calculating SMA: {e}")
        return None

def calculate_EMA(ticker, window):
    try:
        data = yf.Ticker(ticker).history(period='1y')['Close']
        ema = data.ewm(span=window, adjust=False).mean().iloc[-1]
        if is_indian_stock(ticker):
            return f"The {window}-day Exponential Moving Average for {ticker} in INR is ₹{ema:.2f}"
        else:
            return f"The {window}-day Exponential Moving Average for {ticker} in USD is ${ema:.2f}"
    except Exception as e:
        st.error(f"Error calculating EMA: {e}")
        return None

def calculate_RSI(ticker):
    try:
        data = yf.Ticker(ticker).history(period='1y').Close
        delta = data.diff()
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)
        ema_up = up.ewm(com=14 - 1, adjust=False).mean()
        ema_down = down.ewm(com=14 - 1, adjust=False).mean()
        rs = ema_up / ema_down
        if is_indian_stock(ticker):
            return f"The  Relative strength index for {ticker} in INR is ₹{str(100 - (100 / (1 + rs)).iloc[-1])}"
        else:
            return f"The  Relative strength index for {ticker} in INR is ${str(100 - (100 / (1 + rs)).iloc[-1])}"
    except Exception as e:
        return f"An error occurred: {e}"


def calculate_MACD(ticker):
    try:
        data = yf.Ticker(ticker).history(period='1y').Close
        short_EMA = data.ewm(span=12, adjust=False).mean()
        long_EMA = data.ewm(span=26, adjust=False).mean()
        MACD = short_EMA - long_EMA
        signal = MACD.ewm(span=9, adjust=False).mean()
        MACD_histogram = MACD - signal
        return f'{MACD[-1]},{signal[-1]}, {MACD_histogram[-1]}'
    except Exception as e:
        return f"An error occurred: {e}"

def plot_stock_price(ticker):
    try:
        data = yf.Ticker(ticker).history(period='1y')
        plt.figure(figsize=(10, 5))
        plt.plot(data.index, data.Close)
        plt.title(f'{ticker} Stock Price Over Last Year')
        plt.xlabel('Date')
        plt.ylabel('Stock Price ($)')
        plt.grid(True)
        plt.savefig('stock.png')
        st.image('stock.png') #Display the plot directly in Streamlit
        plt.close()
        return "Plot displayed above." #Return a message instead of a file path
    except Exception as e:
        return f"An error occurred: {e}"



available_functions = {
    'get_stock_price': get_stock_price,
    'calculate_SMA': calculate_SMA,
    'calculate_EMA': calculate_EMA,
    'calculate_RSI': calculate_RSI,
    'calculate_MACD': calculate_MACD,
    'plot_stock_price': plot_stock_price
}

# PLACE THE FUNCTION DEFINITION HERE
def create_gemini_prompt(user_input, functions):
    # ... (same prompt as before)
    prompt = f"""
    You are a financial analysis assistant. The user will ask a question about stocks.
    Your job is to determine if the user is requesting a specific function call.
    If so, respond calling the function name and arguments.
    If not search the user prompt, respond directly to the user's question (for example who is bill gates,who is tesla's owner).
    
    Available Functions:
    json
    {json.dumps(functions, indent=4)}
    

    User Input: {user_input}

    Respond in one of the following formats:

    1. Function Call:
    json
    {{
        "function_name": "function_name",
        "arguments": {{
            "arg1": "value1",
            "arg2": "value2"
        }}
    }}
    

    2. Direct Response (if no function call is needed):
    [Your direct response to the user's question]
    """
    return prompt

new_chat_id = f'{time.time()}'
MODEL_ROLE = 'ai'
AI_AVATAR_ICON = '✨'
# ... (rest of your Streamlit setup)

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

st.title('Financial Stock Analysis Chatbot')

if 'chat' not in st.session_state:
    st.session_state.model = genai.GenerativeModel('gemini-pro')
    st.session_state.chat = st.session_state.model.start_chat()

user_input = st.text_input('Your Input: ')
st.write("(if indian stock write indian before stock or write .ns after stock)")

if user_input:
    st.session_state['messages'].append({'role': 'user', 'content': f'{user_input}'})

    gemini_prompt = create_gemini_prompt(user_input, functions= [
  {
    'name':'get_stock_price',
    'description':'Gets the latest stock price given the ticker symbol of a company',
    'parameters':{
      'type':'object',
      'properties':{
        'ticker':{
          'type':'string',
          'description':' The stock ticker symbol for a company (For example AAPL for apple. Note FB is renamed to META)'
        }
      },
      'required':['ticker']
    }
    },
  {
    "name":"calculate_SMA",
    "description":"Calculate the simple moving average for a given stock ticker and a window",
    "parameters":{
      "type":"object",
      "properties":{
        "ticker":{
          "type":"string","description":"The stock ticker symbol for a company (For example AAPL for apple. Note FB is renamed to META)"
        },
        "window":{
          'type':"integer",
          "description":"the time frame to consider when calculating SMA"
          
        }
      },
      "required":['ticker','window']
      
    },
    
    
  },
  {
    "name":"calculate_EMA",
    "description":"Calculate the exponential moving average for a given stock ticker and a window",
    "parameters":{
      "type":"object",
        "properties":{
            "ticker":{
              "type":"string","description":"The stock ticker symbol for a company (For example AAPL for apple. Note FB is renamed to META)"
          },
            "window":{
              'type':"integer",
              "description":"the time frame to consider when calculating EMA"
             
          }
        },
        "required":['ticker','window']
       
    },
   
   
  },
  {
    'name':'calculate_RSI',
    'description':'Calculate the RSI for a given stock ticker',
    'parameters':{
      'type':'object',
      'properties':{
        'ticker':{
          'type':'string',
          'description':' The stock ticker symbol for a company (For example AAPL for apple. Note FB is renamed to META)'
        }
      },
      'required':['ticker']
    }
    },
   {
    'name':'calculate_MACD',
    'description':'Calculate the MACD for a given stock ticker',
    'parameters':{
      'type':'object',
      'properties':{
        'ticker':{
          'type':'string',
          'description':' The stock ticker symbol for a company (For example AAPL for apple. Note FB is renamed to META)'
        }
      },
      'required':['ticker']
    }
    }, {
    'name':'plot_stock_price',
    'description':'Plot the stock price for the last year given a stock ticker of a company',
    'parameters':{
      'type':'object',
      'properties':{
        'ticker':{
          'type':'string',
          'description':' The stock ticker symbol for a company (For example AAPL for apple. Note FB is renamed to META)'
        }
      },
      'required':['ticker']
    }
    }
  
])

    response = st.session_state.chat.send_message(
        gemini_prompt,
        stream=False,
    )
    gemini_response = response.text
    print(f"Gemini Response: {gemini_response}") #Print the raw response for debugging

    try:
        try:
            match = re.search(r"\{.*\}", gemini_response, re.DOTALL) # Dotall makes . match newlines
            if match:
                json_string = match.group(0)
                print(f"Extracted JSON: {json_string}")
            function_call = json.loads(json_string)
            
        except:
            if gemini_response.startswith("json\n"):
                cleaned_response = gemini_response[5:].strip()
            else:
                cleaned_response = gemini_response.strip()
            function_call = json.loads(cleaned_response)
        
        match = re.search(r"\{.*\}", gemini_response, re.DOTALL)
        if match:  # Check if a JSON-like string was found
            json_string = match.group(0)
            print(f"Extracted JSON: {json_string}")
            function_call = json.loads(json_string)

        function_name = function_call.get('function_name')
        print(function_name)
        function_args = function_call.get('arguments', {})
        print(function_args)

        if function_name and function_name in available_functions:
            # Correctly retrieve and CALL the function
            function_to_call = available_functions[function_name]
            if isinstance(function_to_call, dict):  # handle the new dict format
                function_to_call = function_to_call["func"]
                
            if function_name in ['calculate_EMA', 'calculate_SMA']:
                function_args['window'] = int(function_args.get('window', 20))

            function_response = function_to_call(**function_args)
            with st.chat_message("assistant"): #Displaying in chat box
                st.markdown(function_response)
            st.session_state['messages'].append({'role': 'assistant', 'content': function_response})
            #st.session_state.gemini_history.append({'role': 'user','parts': [{'text': user_input}]})
            #st.session_state.gemini_history.append({'role': 'model','parts': [{'text': function_response}]})
            #st.session_state.chat = st.session_state.model.start_chat(history = st.session_state.gemini_history)

        else:
            with st.chat_message("assistant"):
                st.markdown("Invalid function call returned by Gemini or function not found.")

    except json.JSONDecodeError as e:
        with st.chat_message("assistant"):
            st.markdown(gemini_response)
        print(f"JSONDecodeError: {e}")
        st.session_state['messages'].append({'role': 'assistant', 'content': gemini_response})
        #st.session_state.gemini_history.append({'role': 'user','parts': [{'text': user_input}]})
        #st.session_state.gemini_history.append({'role': 'model','parts': [{'text': gemini_response}]})
        #st.session_state.chat = st.session_state.model.start_chat(history = st.session_state.gemini_history)

    except Exception as e:
        with st.chat_message("assistant"):
            st.markdown(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")
        st.session_state['messages'].append({'role': 'assistant', 'content': f"An unexpected error occurred: {e}"})
        #st.session_state.gemini_history.append({'role': 'user','parts': [{'text': user_input}]})
        #st.session_state.gemini_history.append({'role': 'model','parts': [{'text': f"An unexpected error occurred: {e}"}]})
        #st.session_state.chat = st.session_state.model.start_chat(history = st.session_state.gemini_history)