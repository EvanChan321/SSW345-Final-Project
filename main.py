import yfinance as yf
from prophet import Prophet
import pandas as pd

class Singleton:
    _instance = None  # Class-level attribute to store the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

    def __init__(self, ticker):
        self.ticker = ticker #gets preprocessed ticker dataframe
        self.model = Prophet()

    def train_model(self):
        self.model.fit(self.ticker)

    def make_prediction(self, periods=5):
        future = self.model.make_future_dataframe(periods=periods)
        forecast = self.model.predict(future)
        prediction = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)
        prediction.rename(columns={'ds': 'Date', 'yhat': 'Predicted value', 'yhat_lower': 'Lower Bound', 'yhat_upper': 'Upper Bound'}, inplace=True)
        return prediction

ticker = ""
print("Type exit to close the program.")
while True: #driver loop
    ticker_symbol = input("Enter a Ticker Symbol for a stock: ").upper().strip()
    if(ticker_symbol == 'EXIT'): break
    ticker = yf.Ticker(ticker_symbol) 
    try:    
        #transforming data to fit the model
        ticker_history = ticker.history(period='1y').reset_index()[['Date','Close']]
        df = pd.DataFrame(ticker_history)
        df.rename(columns={'Date': 'ds', 'Close': 'y'}, inplace=True)
        df['ds'] = pd.to_datetime(df['ds']).dt.tz_localize(None)

        predictor = Singleton(df)
        predictor.train_model()
        prediction = predictor.make_prediction()

        print(f"Current price of {ticker_symbol}: ${ticker.info['currentPrice']}")
        print("Predicted values for the next 5 days: ")
        print(prediction.to_string(index=False))
    except Exception as e:
        print(f"Error checking ticker symbol '{ticker_symbol}': {e}")
        ticker_symbol = input("Enter a Ticker Symbol for a stock: ").upper().strip()
        if(ticker_symbol == 'EXIT'): break
        continue
    

print('program ended')    