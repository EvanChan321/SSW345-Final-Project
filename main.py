import yfinance as yf
from prophet import Prophet
import pandas as pd

ticker = ""

print("Type exit to close the program.")
while True:
    ticker_symbol = input("Enter a Ticker Symbol for a stock: ").upper().strip()
    if(ticker_symbol == 'EXIT'): break
    ticker = yf.Ticker(ticker_symbol) 
    try:    #checking if the symbol exists
        while ticker.history(period="1d").empty:
            print(f"Ticker symbol '{ticker_symbol}' does not exist or has no data. Please try again.")
            ticker_symbol = input("Enter a Ticker Symbol for a stock: ").upper().strip()
            if(ticker_symbol == 'EXIT'): break
            continue
    except Exception as e:
        print(f"Error checking ticker symbol '{ticker_symbol}': {e}")
        ticker_symbol = input("Enter a Ticker Symbol for a stock: ").upper().strip()
        if(ticker_symbol == 'EXIT'): break
        continue
    
    #transforming data to fit the model
    ticker_history = ticker.history(period='1y').reset_index()[['Date','Close']]
    df = pd.DataFrame(ticker_history)
    df.rename(columns={'Date': 'ds', 'Close': 'y'}, inplace=True)
    df['ds'] = pd.to_datetime(df['ds']).dt.tz_localize(None)

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=5)  
    forecast = model.predict(future)

    prediction = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(5)
    prediction.rename(columns={'ds': 'Date', 'yhat': 'Predicted value', "yhat_lower" : "Lower Bound", "yhat_upper" : "Upper Bound"}, inplace=True)

    print(f"Current price of {ticker_symbol}: ${ticker.info['currentPrice']}")
    print("Predicted values for the next 5 days: ")
    print(prediction.to_string(index=False))

print('program ended')    