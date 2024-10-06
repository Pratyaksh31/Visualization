import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# Streamlit title and header
st.title("Data Visualization: Imports and Exports")

# File uploader for dataset input in Streamlit
uploaded_file = st.file_uploader("Upload your Imports_Exports_Dataset.csv", type="csv")

# If a file is uploaded, proceed with analysis
if uploaded_file is not None:
    # Load the dataset
    import_export = pd.read_csv(uploaded_file)

    # Sample 3001 rows from the dataset
    my_data = import_export.sample(n=3001, replace=False, random_state=55031)

    # --------------------------- First Chart: Top 10 Countries by Transaction Value --------------------------- #
    st.subheader("Top 10 Countries by Transaction Value")

    # Group by Country and get the sum of 'Value' for the top 10 countries
    top_countries = import_export.groupby('Country')['Value'].sum().nlargest(10)

    # Set up the plotting area using Matplotlib
    fig1, ax1 = plt.subplots(figsize=(7, 5))

    # Plot the horizontal bar chart
    top_countries.plot(kind='barh', color='green', ax=ax1)  # Horizontal bar chart
    ax1.set_title('Top 10 Countries by Transaction Value')
    ax1.set_xlabel('Total Value (in USD)')
    ax1.set_ylabel('Country')
    ax1.grid(axis='x')  # Add gridlines for better readability

    # Display the first plot in Streamlit
    st.pyplot(fig1)

    # --------------------------- Second Chart: Product Category Pie Chart --------------------------- #
    st.subheader("Product Category Distribution")

    # Set up the pie chart for product category distribution
    fig2, ax2 = plt.subplots(figsize=(7, 5))

    # Get category distribution
    category_distribution = my_data['Category'].value_counts()

    # Plot the pie chart
    category_distribution.plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette('pastel'),
                               startangle=90, wedgeprops={'edgecolor': 'black'}, ax=ax2)
    ax2.set_title('Product Category Distribution')
    ax2.set_ylabel('')  # Remove y-label for aesthetics

    # Display the pie chart in Streamlit
    st.pyplot(fig2)

    # --------------------------- Third Chart: Total Import vs Export Value --------------------------- #
    st.subheader("Total Import vs Export Value")

    # Convert 'Date' column to datetime
    my_data['Date'] = pd.to_datetime(my_data['Date'], format='%d-%m-%Y')

    # Set up the plotting area for Donut Chart
    fig3, ax3 = plt.subplots(figsize=(7, 5))

    # Group by Import_Export and sum up the Value column
    import_export_value = my_data.groupby('Import_Export')['Value'].sum()

    # Create a pie chart
    ax3.pie(import_export_value, labels=import_export_value.index, autopct='%1.1f%%', startangle=90, colors=['#1f77b4', '#ff7f0e'])

    # Draw a white circle at the center of the pie chart to make it a donut chart
    centre_circle = plt.Circle((0, 0), 0.70, color='white', fc='white')
    fig3.gca().add_artist(centre_circle)

    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax3.set_title('Total Import vs Export Value')
    plt.axis('equal')

    # Display the Donut Chart in Streamlit
    st.pyplot(fig3)

    # --------------------------- Fourth Chart: Shipping Methods Bar Chart --------------------------- #
    st.subheader("Number of Transactions by Shipping Method")

    # Set up the plotting area for Shipping Methods Bar Chart
    fig4, ax4 = plt.subplots(figsize=(7, 5))

    # Count the number of transactions by shipping method
    shipping_method_count = my_data['Shipping_Method'].value_counts()

    # Plot the bar chart
    shipping_method_count.plot(kind='bar', color='purple', ax=ax4)
    ax4.set_title('Number of Transactions by Shipping Method')
    ax4.set_ylabel('Number of Transactions')
    ax4.set_xticklabels(shipping_method_count.index, rotation=45)

    # Display the bar chart in Streamlit
    st.pyplot(fig4)

    # --------------------------- Fifth Chart: Payment Terms by Import/Export --------------------------- #
    st.subheader("Payment Terms Distribution by Import/Export")

    # Set up the plotting area for Stacked Bar Chart
    fig5, ax5 = plt.subplots(figsize=(7, 5))

    # Group by Import_Export and Payment_Terms to get counts
    stacked_data = my_data.groupby(['Import_Export', 'Payment_Terms']).size().unstack()

    # Plot a stacked bar chart
    stacked_data.plot(kind='bar', stacked=True, color=sns.color_palette('Set2'), edgecolor='black', ax=ax5)

    # Add labels and title
    ax5.set_title('Payment Terms Distribution by Import/Export', fontsize=14, fontweight='bold')
    ax5.set_ylabel('Number of Transactions', fontsize=12)
    ax5.set_xlabel('Import/Export', fontsize=12)
    ax5.set_xticks(rotation=0)

    # Display the stacked bar chart in Streamlit
    st.pyplot(fig5)

    # --------------------------- Sixth Chart: Average Transaction Value by Month --------------------------- #
    st.subheader("Average Value of Transactions by Month")

    # Extract month from the date
    my_data['Month'] = my_data['Date'].dt.month

    # Group by month and calculate the average transaction value
    monthly_avg_value = my_data.groupby('Month')['Value'].mean()

    # Set up the plotting area for line chart
    fig6, ax6 = plt.subplots(figsize=(7, 5))

    # Plot the line graph
    ax6.plot(monthly_avg_value.index, monthly_avg_value.values, marker='o', linestyle='-', color='b')

    # Add labels and title
    ax6.set_title('Average Value of Transactions by Month')
    ax6.set_xlabel('Month')
    ax6.set_ylabel('Average Transaction Value')
    ax6.grid(True)

    # Display the line chart in Streamlit
    st.pyplot(fig6)

    # --------------------------- Seventh Chart: Map for Total Import/Export Values by Country --------------------------- #
    st.subheader("Total Import and Export Values by Country")

    # Group the data by country and import/export status
    country_values = my_data.groupby(['Country', 'Import_Export'])['Value'].sum().reset_index()

    # Pivot the data for plotting
    country_values_pivot = country_values.pivot(index='Country', columns='Import_Export', values='Value').fillna(0)

    # Create a new column for total value
    country_values_pivot['Total'] = country_values_pivot.sum(axis=1)

    # Create a map chart using Plotly
    fig7 = px.choropleth(country_values_pivot,
                          locations=country_values_pivot.index,
                          locationmode='country names',
                          color='Total',
                          hover_name=country_values_pivot.index,
                          title='Total Import and Export Values by Country',
                          color_continuous_scale=px.colors.sequential.Plasma,
                          labels={'Total': 'Total Value (in USD)'})

    # Update layout for larger size
    fig7.update_layout(width=1100, height=700)

    # Display the map chart in Streamlit
    st.plotly_chart(fig7)

else:
    st.write("Please upload a CSV file to visualize the data.")
