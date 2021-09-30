#~~~~~~~~~IMPORTS~~~~~~~~~~#
import requests
import smtplib

#~~~~~~~~~CONSTANTS~~~~~~~~~~#
STOCK = "AAPL"
COMPANY_NAME = "Apple"

API_KEY_ALPHA_V = None
ALPHA_V_ENDPOINT = "https://www.alphavantage.co/query"

API_KEY_NEWSAPI = None
NEWSAPI_ENDPOINT= "https://newsapi.org/v2/everything"

USER_NAME_EMAIL = None
PASSWORD_EMAIL = None

DOWN_EMOJI = "🔻"
UP_EMOJI = "🔺"


#~~~~~~~~~API PARAMS~~~~~~~~~~#
newsapi_params = {
                 "q": f"{COMPANY_NAME}" ,
                "apiKey": API_KEY_NEWSAPI ,
}

alpha_vantage_params = {
        "function":"TIME_SERIES_DAILY",
        "symbol": STOCK,
        "apikey": API_KEY_ALPHA_V,
}

#~~~~~~~~~STOCK API DATA~~~~~~~~~~#
responce = requests.get(url=ALPHA_V_ENDPOINT,params=alpha_vantage_params)
responce.raise_for_status()
stock_prices_data = responce.json()
stock_prices_data = list(stock_prices_data['Time Series (Daily)'].values())
# data_list = [value for (key,value) in data.items()]

yesterday_close = float(stock_prices_data[1]['4. close'])
day_before_yesterday_close = float(stock_prices_data[2]['4. close'])

#~~~~~~~~~Calculate the precentage change ~~~~~~~~~~#
diffrence = abs(yesterday_close-day_before_yesterday_close)
precentage = round((diffrence / yesterday_close)*100)

#~~~~~~~~~GET NEWS API DATA AND FORMAT A MESSAGE TO SEND ~~~~~~~~~~#
if precentage>5:
        responce_news = requests.get(url=NEWSAPI_ENDPOINT, params=newsapi_params)
        responce_news.raise_for_status()
        news_data = responce_news.json()
        news_data = news_data["articles"][:4]
        print(news_data[0]['content'])
        with smtplib.SMTP("smtp.gmail.com") as connection_smtp:
                connection_smtp.starttls()
                connection_smtp.login(user=USER_NAME_EMAIL,password=PASSWORD_EMAIL)
                if yesterday_close > day_before_yesterday_close:
                    msg_body =f"Subject:{COMPANY_NAME}: {STOCK} up by : {precentage}% \n\n" \
                              f"Here is a short summary of articles : \n" \
                            f"Title: {news_data[0]['title']} \n" \
                              f"Content: {news_data[0]['content']} \n" \
                              f"\n" \
                              f"Title: {news_data[1]['title']} \n" \
                              f"Content: {news_data[1]['content']} \n" \
                              f"\n" \
                              f"Title: {news_data[2]['title']} \n" \
                              f"Content: {news_data[2]['content']} \n"
                else:
                    msg_body = f"Subject:{COMPANY_NAME}: {STOCK} down by : {precentage}% \n\n" \
                              f"Here is a short summary of articles : \n" \
                            f"Title: {news_data[0]['title']} \n" \
                              f"Content: {news_data[0]['content']} \n" \
                              f"\n" \
                              f"Title: {news_data[1]['title']} \n" \
                              f"Content: {news_data[1]['content']} \n" \
                              f"\n" \
                              f"Title: {news_data[2]['title']} \n" \
                              f"Content: {news_data[2]['content']} \n"

                msg_body= msg_body.encode("ascii", errors="replace")

                """Send the mail after formatting the message"""
                connection_smtp.sendmail(from_addr=USER_NAME_EMAIL,to_addrs=USER_NAME_EMAIL,msg=msg_body)
                print("Done sending mail")