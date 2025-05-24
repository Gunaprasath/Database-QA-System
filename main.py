import streamlit as st
from analysis import fetch_data_from_db, plot_brand_cost_analysis
from langchain_helper import process_question  # Assuming this is already defined elsewhere

# Set page configuration
st.set_page_config(
    page_title="Inventory Management Using LLM",
    layout="wide",
    initial_sidebar_state="collapsed"  # Sidebar collapsed by default
)

# Custom CSS for background, navigation, and patterns
st.markdown(
    """
    <style>
        body {
            background: url('https://via.placeholder.com/1500x1000') no-repeat center center fixed;
            background-size: cover;
        }
        .header-container {
            text-align: center;
            padding: 20px;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            margin: auto;
            width: 70%;
        }
        .header-container h1 {
            font-size: 3rem;
            color: #333;
            margin-bottom: 0.5rem;
        }
        .header-container p {
            font-size: 1.2rem;
            color: #666;
        }
        .sidebar-nav ul {
            list-style-type: none;
            padding: 0;
        }
        .sidebar-nav ul li {
            margin: 10px 0;
        }
        .answer-container, .error-container {
            padding: 15px;
            border-radius: 5px;
            background: #f9f9f9;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state for toggling views
if "show_sales_analysis_page" not in st.session_state:
    st.session_state.show_sales_analysis_page = False

# Handle "Sales Analysis" button click
if st.sidebar.button("Sales Analysis"):
    st.session_state.show_sales_analysis_page = True

# Handle "Back to Home" button click
if st.session_state.show_sales_analysis_page and st.button("Back to Home"):
    st.session_state.show_sales_analysis_page = False
    st.rerun()

# Show Sales Analysis Page
if st.session_state.show_sales_analysis_page:
    df = fetch_data_from_db()
    if df is not None:
        st.markdown("### Brand vs Price Analysis")
        fig = plot_brand_cost_analysis(df)
        st.pyplot(fig)
else:
    # App Header
    st.markdown(
        """
        <div class="header-container">
            <h1>Inventory Management using LLM</h1>
        """,
        unsafe_allow_html=True
    )

    # Display the local image below the header
    st.image("welcome.jpg", use_container_width=True)

    st.markdown(
        """
        <div class="header-container">
            <p>A Database Interaction System</p>
            <p>Get instant answers to your database questions!</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Main Question Input Section
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

    # Sidebar with colorful pattern for navigation section
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

# Footer
st.markdown(
    """
    <hr style="margin-top: 30px; border-top: 1px solid #ddd;" />
    <div style="text-align: center; font-size: 0.9rem; color: #888;">
        © 2024 AtliQ T-Shirts | Powered by LangChain & Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
