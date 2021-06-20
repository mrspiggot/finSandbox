from fredapi import Fred
import requests
import pandas as pd
from datetime import date

def get_FRED_rate(ticker):
    today = date.today()
    str_today = str(today)
    url1 = 'https://fred.stlouisfed.org/graph/fredgraph.xls?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id='
    url2 = '&scale=left&cosd='
    url3 = '&coed='
    url4 = '&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Daily&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date='
    url5 = '&revision_date='
    url6 = '&nd=2001-01-02'

    query_string = url1 + ticker + url2 + str_today + url3 + str_today + url4 + str_today + url5 + str_today + url6
    df2 = pd.read_excel(query_string)

    return df2.iloc[-1]['Unnamed: 1']


def get_FRED_rate_history(ticker):
    today = date.today()
    str_today = str(today)
    url1 = 'https://fred.stlouisfed.org/graph/fredgraph.xls?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id='
    url2 = '&scale=left&cosd='
    url3 = '&coed='
    url4 = '&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Daily&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date='
    url5 = '&revision_date='
    url6 = '&nd=2001-01-02'

    query_string = url1 + ticker + url2 + str_today + url3 + str_today + url4 + str_today + url5 + str_today + url6
    df2 = pd.read_excel(query_string)

    return df2.tail(2500)

fred = Fred(api_key='5619d6a86864657a636434c56a8aab9c')
#data = fred.get_series('USDONTD156N')


D1 = get_FRED_rate('USDONTD156N')
print(D1)

D1_df = get_FRED_rate_history('USDONTD156N')
print(D1_df)