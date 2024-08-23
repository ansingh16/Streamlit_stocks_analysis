from pathlib import Path
import streamlit as st
import pandas as pd
import altair as alt
import mstarpy
import datetime



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



def add_portfolio_entry(fund_data, units, nav):
    name = fund_data.name
    category_name = fund_data.allocationMap()['categoryName']

    # Check if session_state.portfolio is empty
    if st.session_state.portfolio.empty:
        st.session_state.portfolio = pd.DataFrame([{"Scheme Name": name, "Units": float(units), "NAV": float(nav), "fund_data": fund_data, "Scheme Category": category_name, 'Checkbox': True}])
    else:
        # Append the new entry to the existing DataFrame
        st.session_state.portfolio.loc[len(st.session_state.portfolio.index)] = [name, float(units), float(nav), fund_data, category_name, True]


def check_ckbox():

        # print(st.session_state.portfolio)

        input_data = st.session_state.portfolio
        

        for i in range(st.session_state.portfolio.shape[0]):
            checkbox_key = f"checkbox_{i}"
            units_key = f"units_{i}"

            
            scheme_name = input_data['Scheme Name'].iloc[i]
            
            # Place checkbox and text input side by side using columns layout
            col1, col2 = st.sidebar.columns([1, 1])

           
            # set checkbox
            input_data['Checkbox'] = col1.checkbox(label=f"{scheme_name}", key=checkbox_key, value=input_data['Checkbox'].values[0])
            
            # set units
            input_data['Units'] = col2.text_input(label="Units", key=units_key, value=input_data['Units'].values[0])
        
        if st.session_state.portfolio.shape[0]>0:

            # Filter out unchecked entries and update the DataFrame
            input_data = input_data.loc[input_data['Checkbox'] == True]

        return input_data
             

def stock_plots():
    
    st.subheader("Stock Analysis")

    st.markdown("### Portfolio Value")