from fredapi import Fred
import requests
import pandas as pd
import QuantLib as ql
from datetime import date
import plotly.express as px
import plotly.graph_objects as go

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app

fred = Fred(api_key='5619d6a86864657a636434c56a8aab9c')
def origin(ticker):
    return fred.get_series(ticker).tail(1).index.item()
def print_curve(xlist, ylist, precision=3):
    """
    Method to print curve in a nice format
    """
    print("----------------------")
    print("Maturities\tCurve")
    print("----------------------")
    for x,y in zip(xlist, ylist):
        print(x,"\t\t", round(y, precision))
    print("----------------------")
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
def get_FRED_swap_rate(ticker):
    return fred.get_series(ticker).iloc[-1]


app.layout = html.Div([
    html.Button(id='plot', n_clicks=0),
    dcc.Graph(id='yc'),
    dcc.Graph(id='gb'),
    dcc.Graph(id='eur'),
])


@app.callback(Output('yc', 'figure'),
              Input('plot', 'n_clicks'))
def display_zero_curve(ip):

    depo_maturities = [ql.Period(1, ql.Days),
                       ql.Period(1, ql.Weeks),
                       ql.Period(1, ql.Months),
                       ql.Period(2, ql.Months),
                       ql.Period(3, ql.Months),
                       ql.Period(6, ql.Months),
                       ql.Period(12, ql.Months)]

    swap_maturities = [ql.Period(2, ql.Years),
                       ql.Period(3, ql.Years),
                       ql.Period(4, ql.Years),
                       ql.Period(5, ql.Years),
                       ql.Period(7, ql.Years),
                       ql.Period(10, ql.Years),
                       ql.Period(15, ql.Years),
                       ql.Period(30, ql.Years)]


    D1_rate = get_FRED_rate('USDONTD156N')
    W1_rate = get_FRED_rate('USD1WKD156N')
    M1_rate = get_FRED_rate('USD1MTD156N')
    M2_rate = get_FRED_rate('USD2MTD156N')
    M3_rate = get_FRED_rate('USD3MTD156N')
    M6_rate = get_FRED_rate('USD6MTD156N')
    M12_rate = get_FRED_rate('USD12MD156N')

    S2 = get_FRED_swap_rate('ICERATES1100USD2Y')
    S3 = get_FRED_swap_rate('ICERATES1100USD3Y')
    S4 = get_FRED_swap_rate('ICERATES1100USD4Y')
    S5 = get_FRED_swap_rate('ICERATES1100USD5Y')
    S7 = get_FRED_swap_rate('ICERATES1100USD7Y')
    S10 = get_FRED_swap_rate('ICERATES1100USD10Y')
    S15 = get_FRED_swap_rate('ICERATES1100USD15Y')
    S30 = get_FRED_swap_rate('ICERATES1100USD30Y')

    depo_rates = [D1_rate, W1_rate, M1_rate, M2_rate, M3_rate, M6_rate, M12_rate]
    swap_rates = [S2, S3, S4, S5, S7, S10, S15, S30]

    print_curve(depo_maturities+swap_maturities, depo_rates+swap_rates)


    og = origin('ICERATES1100USD2Y')
    print(og.year)
    print(og.day)
    print(og.month)
    calc_date = ql.Date(og.month, og.day, og.year)
    ql.Settings.instance().evaluationDate = calc_date

    calendar = ql.UnitedStates()
    bussiness_convention = ql.Unadjusted
    day_count = ql.Thirty360()
    end_of_month = True
    settlement_days = 0
    face_amount = 100
    coupon_frequency = ql.Period(ql.Semiannual)
    settlement_days = 0

    # create deposit rate helpers from depo_rates
    depo_helpers = [ql.DepositRateHelper(ql.QuoteHandle(ql.SimpleQuote(r/100.0)),
                                         m,
                                         settlement_days,
                                         calendar,
                                         bussiness_convention,
                                         end_of_month,
                                         day_count )
                    for r, m in zip(depo_rates, depo_maturities)]

    swap_helpers = []
    for r, m in zip(swap_rates, swap_maturities):
        termination_date = calc_date + m
        schedule = ql.Schedule(calc_date,
                               termination_date,
                               coupon_frequency,
                               calendar,
                               bussiness_convention,
                               bussiness_convention,
                               ql.DateGeneration.Backward,
                               end_of_month)

        swap_helper = ql.FixedRateBondHelper(ql.QuoteHandle(ql.SimpleQuote(face_amount)),
                                             settlement_days,
                                             face_amount,
                                             schedule,
                                             [r / 100.0],
                                             day_count,
                                             bussiness_convention,
                                             )
        swap_helpers.append(swap_helper)

    rate_helpers = depo_helpers + swap_helpers
    yieldcurve = ql.PiecewiseLogCubicDiscount(calc_date,
                                 rate_helpers,
                                 day_count)

    spots = []
    tenors = []
    for d in yieldcurve.dates():
        yrs = day_count.yearFraction(calc_date, d)
        compounding = ql.Compounded
        freq = ql.Semiannual
        zero_rate = yieldcurve.zeroRate(yrs, compounding, freq)
        tenors.append(yrs)
        eq_rate = zero_rate.equivalentRate(day_count,
                                           compounding,
                                           freq,
                                           calc_date,
                                           d).rate()
        spots.append(100*eq_rate)

    print_curve(tenors, spots)
    df = pd.DataFrame({
        "Term": tenors,
        "Zeros": spots,
    })
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Term"], y=df["Zeros"], line_shape='spline'))
    #     px.scatter(df, x="Term", y="Zeros")
    # fig.update_traces(mode='lines+markers')

    return fig


@app.callback(Output('gb', 'figure'),
              Input('plot', 'n_clicks'))
def display_gbp_curve(ip):

    depo_maturities = [ql.Period(1, ql.Days),
                       ql.Period(1, ql.Weeks),
                       ql.Period(1, ql.Months),
                       ql.Period(2, ql.Months),
                       ql.Period(3, ql.Months),
                       ql.Period(6, ql.Months),
                       ql.Period(12, ql.Months)]

    swap_maturities = [ql.Period(2, ql.Years),
                       ql.Period(3, ql.Years),
                       ql.Period(4, ql.Years),
                       ql.Period(5, ql.Years),
                       ql.Period(7, ql.Years),
                       ql.Period(10, ql.Years),
                       ql.Period(15, ql.Years),
                       ql.Period(30, ql.Years)]


    D1_rate = get_FRED_rate('GBPONTD156N')
    W1_rate = get_FRED_rate('GBP1WKD156N')
    M1_rate = get_FRED_rate('GBP1MTD156N')
    M2_rate = get_FRED_rate('GBP2MTD156N')
    M3_rate = get_FRED_rate('GBP3MTD156N')
    M6_rate = get_FRED_rate('GBP6MTD156N')
    M12_rate = get_FRED_rate('GBP12MD156N')

    S2 = get_FRED_swap_rate('ICERATES1100GBP2Y')
    S3 = get_FRED_swap_rate('ICERATES1100GBP3Y')
    S4 = get_FRED_swap_rate('ICERATES1100GBP4Y')
    S5 = get_FRED_swap_rate('ICERATES1100GBP5Y')
    S7 = get_FRED_swap_rate('ICERATES1100GBP7Y')
    S10 = get_FRED_swap_rate('ICERATES1100GBP10Y')
    S15 = get_FRED_swap_rate('ICERATES1100GBP15Y')
    S30 = get_FRED_swap_rate('ICERATES1100GBP30Y')

    depo_rates = [D1_rate, W1_rate, M1_rate, M2_rate, M3_rate, M6_rate, M12_rate]
    swap_rates = [S2, S3, S4, S5, S7, S10, S15, S30]

    print_curve(depo_maturities+swap_maturities, depo_rates+swap_rates)


    og = origin('ICERATES1100USD2Y')
    print(og.year)
    print(og.day)
    print(og.month)
    calc_date = ql.Date(og.month, og.day, og.year)
    ql.Settings.instance().evaluationDate = calc_date

    calendar = ql.UnitedStates()
    bussiness_convention = ql.Unadjusted
    day_count = ql.Thirty360()
    end_of_month = True
    settlement_days = 0
    face_amount = 100
    coupon_frequency = ql.Period(ql.Semiannual)
    settlement_days = 0

    # create deposit rate helpers from depo_rates
    depo_helpers = [ql.DepositRateHelper(ql.QuoteHandle(ql.SimpleQuote(r/100.0)),
                                         m,
                                         settlement_days,
                                         calendar,
                                         bussiness_convention,
                                         end_of_month,
                                         day_count )
                    for r, m in zip(depo_rates, depo_maturities)]

    swap_helpers = []
    for r, m in zip(swap_rates, swap_maturities):
        termination_date = calc_date + m
        schedule = ql.Schedule(calc_date,
                               termination_date,
                               coupon_frequency,
                               calendar,
                               bussiness_convention,
                               bussiness_convention,
                               ql.DateGeneration.Backward,
                               end_of_month)

        swap_helper = ql.FixedRateBondHelper(ql.QuoteHandle(ql.SimpleQuote(face_amount)),
                                             settlement_days,
                                             face_amount,
                                             schedule,
                                             [r / 100.0],
                                             day_count,
                                             bussiness_convention,
                                             )
        swap_helpers.append(swap_helper)

    rate_helpers = depo_helpers + swap_helpers
    yieldcurve = ql.PiecewiseLogCubicDiscount(calc_date,
                                 rate_helpers,
                                 day_count)

    spots = []
    tenors = []
    for d in yieldcurve.dates():
        yrs = day_count.yearFraction(calc_date, d)
        compounding = ql.Compounded
        freq = ql.Semiannual
        zero_rate = yieldcurve.zeroRate(yrs, compounding, freq)
        tenors.append(yrs)
        eq_rate = zero_rate.equivalentRate(day_count,
                                           compounding,
                                           freq,
                                           calc_date,
                                           d).rate()
        spots.append(100*eq_rate)

    print_curve(tenors, spots)
    df = pd.DataFrame({
        "Term": tenors,
        "Zeros": spots,
    })
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Term"], y=df["Zeros"], line_shape='spline'))
    #     px.scatter(df, x="Term", y="Zeros")
    # fig.update_traces(mode='lines+markers')

    return fig

@app.callback(Output('eur', 'figure'),
              Input('plot', 'n_clicks'))
def display_eur_curve(ip):

    depo_maturities = [ql.Period(1, ql.Days),
                       ql.Period(1, ql.Weeks),
                       ql.Period(1, ql.Months),
                       ql.Period(2, ql.Months),
                       ql.Period(3, ql.Months),
                       ql.Period(6, ql.Months),
                       ql.Period(12, ql.Months)]

    swap_maturities = [ql.Period(2, ql.Years),
                       ql.Period(3, ql.Years),
                       ql.Period(4, ql.Years),
                       ql.Period(5, ql.Years),
                       ql.Period(7, ql.Years),
                       ql.Period(10, ql.Years),
                       ql.Period(15, ql.Years),
                       ql.Period(30, ql.Years)]


    D1_rate = get_FRED_rate('EURONTD156N')
    W1_rate = get_FRED_rate('EUR1WKD156N')
    M1_rate = get_FRED_rate('EUR1MTD156N')
    M2_rate = get_FRED_rate('EUR2MTD156N')
    M3_rate = get_FRED_rate('EUR3MTD156N')
    M6_rate = get_FRED_rate('EUR6MTD156N')
    M12_rate = get_FRED_rate('EUR12MD156N')

    S2 = get_FRED_swap_rate('ICERATES1100EUR2Y')
    S3 = get_FRED_swap_rate('ICERATES1100EUR3Y')
    S4 = get_FRED_swap_rate('ICERATES1100EUR4Y')
    S5 = get_FRED_swap_rate('ICERATES1100EUR5Y')
    S7 = get_FRED_swap_rate('ICERATES1100EUR7Y')
    S10 = get_FRED_swap_rate('ICERATES1100EUR10Y')
    S15 = get_FRED_swap_rate('ICERATES1100EUR15Y')
    S30 = get_FRED_swap_rate('ICERATES1100EUR30Y')

    depo_rates = [D1_rate, W1_rate, M1_rate, M2_rate, M3_rate, M6_rate, M12_rate]
    swap_rates = [S2, S3, S4, S5, S7, S10, S15, S30]

    print_curve(depo_maturities+swap_maturities, depo_rates+swap_rates)


    og = origin('ICERATES1100USD2Y')
    print(og.year)
    print(og.day)
    print(og.month)
    calc_date = ql.Date(og.month, og.day, og.year)
    ql.Settings.instance().evaluationDate = calc_date

    calendar = ql.UnitedStates()
    bussiness_convention = ql.Unadjusted
    day_count = ql.Thirty360()
    end_of_month = True
    settlement_days = 0
    face_amount = 100
    coupon_frequency = ql.Period(ql.Semiannual)
    settlement_days = 0

    # create deposit rate helpers from depo_rates
    depo_helpers = [ql.DepositRateHelper(ql.QuoteHandle(ql.SimpleQuote(r/100.0)),
                                         m,
                                         settlement_days,
                                         calendar,
                                         bussiness_convention,
                                         end_of_month,
                                         day_count )
                    for r, m in zip(depo_rates, depo_maturities)]

    swap_helpers = []
    for r, m in zip(swap_rates, swap_maturities):
        termination_date = calc_date + m
        schedule = ql.Schedule(calc_date,
                               termination_date,
                               coupon_frequency,
                               calendar,
                               bussiness_convention,
                               bussiness_convention,
                               ql.DateGeneration.Backward,
                               end_of_month)

        swap_helper = ql.FixedRateBondHelper(ql.QuoteHandle(ql.SimpleQuote(face_amount)),
                                             settlement_days,
                                             face_amount,
                                             schedule,
                                             [r / 100.0],
                                             day_count,
                                             bussiness_convention,
                                             )
        swap_helpers.append(swap_helper)

    rate_helpers = depo_helpers + swap_helpers
    yieldcurve = ql.PiecewiseLogCubicDiscount(calc_date,
                                 rate_helpers,
                                 day_count)

    spots = []
    tenors = []
    for d in yieldcurve.dates():
        yrs = day_count.yearFraction(calc_date, d)
        compounding = ql.Compounded
        freq = ql.Semiannual
        zero_rate = yieldcurve.zeroRate(yrs, compounding, freq)
        tenors.append(yrs)
        eq_rate = zero_rate.equivalentRate(day_count,
                                           compounding,
                                           freq,
                                           calc_date,
                                           d).rate()
        spots.append(100*eq_rate)

    print_curve(tenors, spots)
    df = pd.DataFrame({
        "Term": tenors,
        "Zeros": spots,
    })
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Term"], y=df["Zeros"], line_shape='spline'))
    #     px.scatter(df, x="Term", y="Zeros")
    # fig.update_traces(mode='lines+markers')

    return fig




if __name__ == '__main__':
    app.run_server(debug=True, port=8157)