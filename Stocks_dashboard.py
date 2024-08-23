import streamlit as st

st.set_page_config(initial_sidebar_state="expanded")


import pandas as pd
from streamlit.components.v1 import html
from streamlit_navigation_bar import st_navbar
from modules.data_processing import  check_ckbox
from modules.data_processing import  stock_plots
from modules.dashboard import search_fund, add_portfolio_file


 # Initialize session state variables if not already initialized

if 'portfolio' not in st.session_state:
    st.session_state.portfolio = pd.DataFrame()



styles_nav = {
        "nav": {
        "width": "100%",                   # Full width of the container
        "background-color": "teal",        # Background color for the navigation bar
        "display": "flex",                 # Enable flexbox layout
        "justify-content": "center",       # Center the navigation items
        "overflow": "hidden",              # Prevent overflow issues
        "position": "relative",            # Allows better control of positioning
        "left": "0",                       # Aligns the navigation bar to the start
        "right": "0",                      # Aligns the navigation bar to the end
        "margin": "0 auto",                # Center the navbar in its container
        "padding-left": "150px",            # Space between the sidebar and navigation items
    },
        "span": {
            "border-radius": "0.5rem",
            "padding": "0.4375rem 0.625rem",
            "margin": "0 0.125rem",
        },
        "active": {
            "background-color": "rgba(255, 255, 255, 0.25)",
        },
        "hover": {
            "background-color": "rgba(255, 255, 255, 0.35)",
        }
    }



def main():

    
    pages = ["Stock Analysis"]
    
    
    # Add entry to the list of inputs
    with st.sidebar:

        # set App Name
        st.markdown("<h1 style='text-align: center;'>Stock Analysis</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>By Ankit Singh</h3>", unsafe_allow_html=True)
        #add logo at the center
        
        left_co, cent_co,last_co = st.columns(3)
        with cent_co:
            st.image('./images/logo.jpeg', use_column_width=True)
        

        st.markdown('---')

        st.markdown("<h2 style='text-align: center;'>Portfolio Dashboard</h2>", unsafe_allow_html=True)


        # create search bar
        search_term = st.sidebar.text_input(label="Search", key=1)

        if search_term:
            
            search_fund(search_term)
            

        st.header('OR')

                
        st.header("Upload CSV File")
        st.info("Please upload a CSV file with the following columns: 'Scheme Name', 'Units'")

        # add file uploader
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

        # make two columns
        col1, col2 = st.columns(2)

        with col1:
            
            if st.button("Add file", key="add_csv"):            

                with st.spinner("Analyzing..."):
                
                    add_portfolio_file(uploaded_file)
        with col2:

            if st.button("Add sample file", key="add_sample"):            

                with st.spinner("Analyzing..."):
                    
                    uploaded_file = './sample_port.csv'
                    add_portfolio_file(uploaded_file)


        st.markdown('---')
            
        # Display entries with checkboxes in the sidebar
        st.markdown("<h1 style='text-align: center;'>Stock Entries</h1>", unsafe_allow_html=True)
        
        # check which checkboxes are checked
        st.session_state.portfolio = check_ckbox()

        # check if portfolio is not empty
        if st.session_state.portfolio.shape[0] >0:
                    
                    consol_holdings = get_consol_holdings()

                    # set session state for consol_holdings
                    st.session_state["consol_holdings"] = consol_holdings



    # Custom CSS to create a 2-inch spacer
    st.markdown(
        """
        <style>
        .spacer {
            height: 1.95rem;  /* Create a 2-inch space */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

    # Render the navigation bar
    navigation = st_navbar(pages, styles=styles_nav,selected='Stock Analysis')




    # Call the appropriate function based on the selected page
    if navigation == 'Stock Analysis':
        stock_plots()
    

    
        

          

# Call the main function
if __name__ == "__main__":
    main()
