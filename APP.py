import pandas as pd
import seaborn as sns
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt

# Set Streamlit page config
st.set_page_config(page_title="/Users/pratyakshchauhan/Downloads/Imports_Exports_Dataset.csv", layout="wide")

# Streamlit title and header
st.title("Imports and Exports Dashboard")

# File uploader for dataset input in Streamlit
uploaded_file = st.file_uploader("Upload your Imports_Exports_Dataset.csv", type="csv")

# If a file is uploaded, proceed with analysis
if uploaded_file is not None:
    # Load the dataset
    import_export = pd.read_csv(uploaded_file)

    # Sample 3001 rows from the dataset for visualization
    my_data = import_export.sample(n=3001, replace=False, random_state=55031)

    # --------------------- First Chart: Horizontal Bar Chart --------------------- #
    st.header("1. Top 10 Countries by Transaction Value")
    # Group by Country and get the sum of 'Value' for the top 10 countries
    top_countries = import_export.groupby('Country')['Value'].sum().nlargest(10)

    # Plot horizontal bar chart
    fig1, ax1 = plt.subplots(figsize=(14, 8))
    top_countries.plot(kind='barh', color='green', ax=ax1)
    ax1.set_title('Top 10 Countries by Transaction Value')
    ax1.set_xlabel('Total Value (in USD)')
    ax1.set_ylabel('Country')
    ax1.grid(axis='x')

    # Display chart in Streamlit
    st.pyplot(fig1)

    # --------------------- Second Chart: Product Category Pie Chart --------------------- #
    st.header("2. Product Category Distribution")
    # Pie chart for product category distribution
    fig2, ax2 = plt.subplots(figsize=(14, 8))
    category_distribution = my_data['Category'].value_counts()
    category_distribution.plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette('pastel'),
                               startangle=90, wedgeprops={'edgecolor': 'black'}, ax=ax2)
    ax2.set_title('Product Category Distribution')
    ax2.set_ylabel('')

    # Display chart in Streamlit
    st.pyplot(fig2)

    # --------------------- Third Chart: Donut Chart for Total Import vs Export Value --------------------- #
    st.header("3. Total Import vs Export Value")
    # Convert 'Date' to datetime for analysis
    my_data['Date'] = pd.to_datetime(my_data['Date'], format='%d-%m-%Y')

    # Donut chart for Import vs Export
    fig3, ax3 = plt.subplots(figsize=(14, 8))
    import_export_value = my_data.groupby('Import_Export')['Value'].sum()
    ax3.pie(import_export_value, labels=import_export_value.index, autopct='%1.1f%%',
            startangle=90, colors=['#1f77b4', '#ff7f0e'])
    centre_circle = plt.Circle((0, 0), 0.70, color='white', fc='white')
    fig3.gca().add_artist(centre_circle)
    ax3.set_title('Total Import vs Export Value')
    plt.axis('equal')

    # Display Donut chart in Streamlit
    st.pyplot(fig3)

    # --------------------- Fourth Chart: Shipping Methods Bar Chart --------------------- #
    st.header("4. Number of Transactions by Shipping Method")
    # Shipping Methods Bar Chart
    fig4, ax4 = plt.subplots(figsize=(14, 8))
    shipping_method_count = my_data['Shipping_Method'].value_counts()
    shipping_method_count.plot(kind='bar', color='purple', ax=ax4)
    ax4.set_title('Number of Transactions by Shipping Method')
    ax4.set_ylabel('Number of Transactions')
    ax4.set_xticklabels(shipping_method_count.index, rotation=45)

    # Display chart in Streamlit
    st.pyplot(fig4)

    # --------------------- Fifth Chart: Stacked Bar Chart for Payment Terms by Import/Export --------------------- #
    st.header("5. Payment Terms Distribution by Import/Export")
    fig5, ax5 = plt.subplots(figsize=(20, 14))
    stacked_data = my_data.groupby(['Import_Export', 'Payment_Terms']).size().unstack()
    stacked_data.plot(kind='bar', stacked=True, color=sns.color_palette('Set2'), edgecolor='black', ax=ax5)
    ax5.set_title('Payment Terms Distribution by Import/Export')
    ax5.set_ylabel('Number of Transactions')
    ax5.set_xlabel('Import/Export')
    plt.xticks(rotation=0)

    # Display stacked bar chart in Streamlit
    st.pyplot(fig5)

    # --------------------- Sixth Chart: Average Transaction Value by Month --------------------- #
    st.header("6. Average Value of Transactions by Month")
    my_data['Month'] = my_data['Date'].dt.month
    monthly_avg_value = my_data.groupby('Month')['Value'].mean()
    fig6, ax6 = plt.subplots(figsize=(8, 6))
    ax6.plot(monthly_avg_value.index, monthly_avg_value.values, marker='o', linestyle='-', color='b')
    ax6.set_title('Average Value of Transactions by Month')
    ax6.set_xlabel('Month')
    ax6.set_ylabel('Average Transaction Value')
    ax6.grid(True)

    # Display line chart in Streamlit
    st.pyplot(fig6)

    # --------------------- Seventh Chart: Map for Total Import/Export Values by Country --------------------- #
    st.header("7. Total Import and Export Values by Country")
    country_values = my_data.groupby(['Country', 'Import_Export'])['Value'].sum().reset_index()
    country_values_pivot = country_values.pivot(index='Country', columns='Import_Export', values='Value').fillna(0)
    country_values_pivot['Total'] = country_values_pivot.sum(axis=1)

    # Map Chart using Plotly
    fig7 = px.choropleth(country_values_pivot,
                         locations=country_values_pivot.index,
                         locationmode='country names',
                         color='Total',
                         hover_name=country_values_pivot.index,
                         title='Total Import and Export Values by Country',
                         color_continuous_scale=px.colors.sequential.Plasma,
                         labels={'Total': 'Total Value (in USD)'})
    fig7.update_layout(width=1100, height=700)

    # Display map chart in Streamlit
    st.plotly_chart(fig7)

else:
    st.write("Please upload a CSV file to visualize the data.")
