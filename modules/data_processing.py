from pathlib import Path
import streamlit as st
import pandas as pd
import altair as alt
import mstarpy
import datetime

import streamlit.components.v1 as components


def process_fund(scheme_unit):
    search_scheme, units = scheme_unit
    response = mstarpy.search_funds(term=search_scheme, field=["Name", "fundShareClassId", "SectorName"], country="in", pageSize=20)
    
    
    if response:
        result = response[0]
        fund_data = mstarpy.Funds(term=result['Name'], country="in")
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=3)
        history = fund_data.nav(start_date=yesterday, end_date=today, frequency="daily")

        if history:
            df_history = pd.DataFrame(history)
            nav = df_history['nav'].iloc[-1]

            return (fund_data, units, nav)
    return None



def add_portfolio_entry(stock_data, stock_price):
    name = stock_data.name
    # category_name = fund_data.allocationMap()['categoryName']

    # Check if session_state.portfolio is empty
    if st.session_state.portfolio.empty:
        st.session_state.portfolio = pd.DataFrame([{"Stock Name": name,"Price": float(stock_price), "stock_data": stock_data, 'Checkbox': True}])
    else:
        # Append the new entry to the existing DataFrame
        st.session_state.portfolio.loc[len(st.session_state.portfolio.index)] = [name, float(stock_price),stock_data, True]


def check_ckbox():

        # print(st.session_state.portfolio)

        input_data = st.session_state.portfolio
        

        for i in range(st.session_state.portfolio.shape[0]):
            checkbox_key = f"checkbox_{i}"
            units_key = f"units_{i}"

            
            stock_name = input_data['Stock Name'].iloc[i]
            
            # Place checkbox and text input side by side using columns layout
            # col1, col2 = st.sidebar.columns([1, 1])

           
            # set checkbox
            input_data['Checkbox'] = st.checkbox(label=f"{stock_name}", key=checkbox_key, value=input_data['Checkbox'].values[0])
            
            
        
        if st.session_state.portfolio.shape[0]>0:

            # Filter out unchecked entries and update the DataFrame
            input_data = input_data.loc[input_data['Checkbox'] == True]

        return input_data
             
@st.cache_data
def swot_chart():
    
    st.subheader("Stock Analysis")

    st.markdown(f'Total number of entries: {st.session_state.portfolio.shape[0]}')

    if st.session_state.portfolio.shape[0] > 0:
    
       
       # Create two columns
        col1, col2 = st.columns(spec=[0.6, 0.5])

        # st.markdown(stock)
        
        # Embed the HTML blockquote for each stock in the chosen column
        with col1:
            ticker='SBICARD'
            components.html(f"""
                        <blockquote class="trendlyne-widgets" data-get-url="https://trendlyne.com/web-widget/swot-widget/Poppins/{ticker}/?posCol=00A25B&primaryCol=006AFF&negCol=EB3B00&neuCol=F7941E" data-theme="light"></blockquote><script async src="https://cdn-static.trendlyne.com/static/js/webwidgets/tl-widgets.js" charset="utf-8"> </script>
                    """, height=400)  # Adjust height as needed