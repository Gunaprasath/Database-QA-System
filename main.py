import streamlit as st
from analysis import fetch_data_from_db, plot_brand_cost_analysis
from langchain_helper import process_question  # Assuming this is already defined elsewhere

# Set page configuration
st.set_page_config(
    page_title="AtliQ T-Shirts: Database Q&A 👕",
    page_icon="👕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for background, navigation, and patterns (same as before)
st.markdown(
    """
    <style>
        /* Your CSS code here */
    </style>
    """,
    unsafe_allow_html=True
)

# App Header
st.markdown(
    """
    <div class="header-container">
        <h1>AtliQ T-Shirts </h1>
        <h1>👕</h1>
        <p>A Database Interaction System</p>
        <p>Get instant answers to your database questions!</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Sales Analysis Button in Sidebar
show_sales_analysis = st.sidebar.button("Sales Analysis")

if "show_sales_analysis_page" not in st.session_state:
    st.session_state.show_sales_analysis_page = False

if show_sales_analysis or st.session_state.show_sales_analysis_page:
    st.session_state.show_sales_analysis_page = True
    df = fetch_data_from_db()
    if df is not None:
        st.markdown("### Brand vs Price Analysis")
        fig = plot_brand_cost_analysis(df)
        st.pyplot(fig)

    if st.button("Back to Home"):
        st.session_state.show_sales_analysis_page = False
        st.rerun()

else:
    question = st.text_input("", placeholder="e.g., What are the best-selling T-shirts?")
    if question:
        with st.spinner("Searching the database..."):
            response = process_question(question)
        st.markdown("### Answer:")
        if response:
            st.markdown(
                f"""
                <div class="answer-container">
                    <strong> </strong><br>{response}
                </div>
                """,
                unsafe_allow_html=True
            )
            st.balloons()
        else:
            st.markdown(
                """
                <div class="error-container">
                    <strong>No answer found for this question.</strong><br>
                    Please refine your query and try again.
                </div>
                """,
                unsafe_allow_html=True
            )

# Sidebar with colorful pattern for navigation section (same as before)
st.sidebar.markdown(
    """
    <div class="sidebar-nav">
        <h3>Explore Sales Insights</h3>
        <ul>
            <li><strong>Sales Trends</strong> - Track overall sales</li>
            <li><strong>Best Selling Brands</strong> - Identify top-selling brands</li>
            <li><strong>Customer Insights</strong> - Get detailed customer analysis</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# Footer (same as before)
st.markdown(
    """
    <hr style="margin-top: 30px; border-top: 1px solid #ddd;" />
    <div style="text-align: center; font-size: 0.9rem; color: #888;">
        © 2024 AtliQ T-Shirts | Powered by LangChain & Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
