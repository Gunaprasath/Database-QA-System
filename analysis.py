import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to connect to MySQL and fetch data
def fetch_data_from_db():
    try:
        # Connect to the MySQL database
        cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            password="#Guna@80",  # Use your actual database password
            database="new_db"
        )

        # Query to fetch brand and price information
        query = "SELECT brand, price FROM t_shirts"
        df = pd.read_sql(query, cnx)

        # Close the connection
        cnx.close()

        return df

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


# Function to plot the graph (Brand vs Price)
def plot_brand_cost_analysis(df):
    # Group by 'brand' and calculate average price
    brand_price_avg = df.groupby('brand')['price'].mean().sort_values()

    # Set the color palette for the bar chart
    sns.set_palette("husl")

    # Plot the bar chart
    plt.figure(figsize=(12, 8))
    bars = brand_price_avg.plot(kind='bar', color=sns.color_palette("Set2", len(brand_price_avg)))

    # Title and labels with larger, readable font
    plt.title("Average Price per Brand", fontsize=18, fontweight='bold', color='darkblue')
    plt.xlabel("Brand", fontsize=14)
    plt.ylabel("Average Price", fontsize=14)

    # Customizing the x-axis tick labels for better readability
    plt.xticks(rotation=45, ha='right', fontsize=12)

    # Displaying gridlines for better readability
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Adding left-rotated annotations inside the bars (centered vertically)
    for index, value in enumerate(brand_price_avg):
        # Positioning the text inside the bar (slightly adjusted to be vertically centered)
        bars.patches[index].set_edgecolor('black')  # Make the edges black for better visibility
        plt.text(bars.patches[index].get_x() + bars.patches[index].get_width() / 2,
                 bars.patches[index].get_height() / 2,
                 f'Rs.{value:.2f}',
                 ha='center',
                 va='center',
                 fontsize=12,
                 fontweight='bold',
                 color='white',
                 rotation=90)  # Left rotate the text by 90 degrees

    # Show the plot
    plt.tight_layout()

    return plt
