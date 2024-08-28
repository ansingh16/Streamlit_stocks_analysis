import mstarpy
import pandas as pd
import datetime
import streamlit as st
from modules.data_processing import add_portfolio_entry, process_fund
from multiprocessing import Pool


def search_stock(search_term):

        # search for mutual funds
        response = mstarpy.search_stock(term=search_term, field=["Name","fundShareClassId"], exchange='XNSE', pageSize=100000)
        # convert to dataframe
        response = pd.DataFrame(response)

        # get filtered options
        filtered_options = [option for option in response.Name if search_term.lower() in option.lower()]


        # Display the selectbox with filtered options
        selected_stock = st.selectbox('Select an option', filtered_options)


        
        if selected_stock != ' ':

            # include_units = st.text_input(label="Shares", key=2, value=1)
            if st.button("Add", key="add"):
                    
                    # stockid
                    stockid = response.loc[response['Name'] == selected_stock, 'fundShareClassId'].iloc[0]
                    # add screener
                    stock_data = mstarpy.Stock(term=f"{stockid}", exchange="XNSE")
                    print(stock_data)
                    # today
                    today = datetime.date.today()
                    # yesterday
                    yesterday = today - datetime.timedelta(days=2)

                    #get historical data
                    history = stock_data.historical(start_date=yesterday,end_date=today, frequency="daily")
                    
                    
                    # if history is not empty
                    if len(history) > 0:
                        # with spinner:
                        df_history = pd.DataFrame(history)
                        stock_price = df_history['close'].iloc[-1]

                        
                        add_portfolio_entry(stock_data,stock_price)

        return

def add_portfolio_file(uploaded_file):
      
      if uploaded_file is not None:
            # Read the uploaded file into a pandas DataFrame
            input_portfolio = pd.read_csv(uploaded_file)

            schemes_units = list(zip(input_portfolio['Scheme Name'], input_portfolio['Units']))

            with Pool() as pool:
                results = pool.map(process_fund, schemes_units)

                        
            for result in results:
                if result:
                    fund_data, units, nav = result
                    add_portfolio_entry(fund_data, units, nav)


            return
