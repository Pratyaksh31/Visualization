import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# Streamlit title and header
st.title("Data Visualization: Imports and Exports")

# Load the dataset
import_export = pd.read_csv(r"Imports_Exports_Dataset.csv")

# Sample 3001 rows from the dataset
my_data = import_export.sample(n=3001, replace=False, random_state=55031)

# Sidebar filters
st.sidebar.subheader("Filters")

# Multi-select slicer for Import/Export
import_export_filter = st.sidebar.multiselect("Select Import/Export", options=my_data['Import_Export'].unique(), default=my_data['Import_Export'].unique())

# Multi-select slicer for Category
category_filter = st.sidebar.multiselect("Select Category", options=my_data['Category'].unique(), default=my_data['Category'].unique())

# Button to reset filters
if st.sidebar.button("Reset Filters"):
    import_export_filter = my_data['Import_Export'].unique()
    category_filter = my_data['Category'].unique()

# Filter the data based on the selected options
filtered_data = my_data[(my_data['Import_Export'].isin(import_export_filter)) & 
                        (my_data['Category'].isin(category_filter))]

# Convert 'Date' column to datetime for the filtered dataset
filtered_data['Date'] = pd.to_datetime(filtered_data['Date'], format='%d-%m-%Y')

# --------------------------- First Chart: Top 10 Countries by Transaction Value --------------------------- #
# Group by Country and get the sum of 'Value' for the top 10 countries
top_countries = filtered_data.groupby('Country')['Value'].sum().nlargest(10)

# Set up the plotting area using Matplotlib
fig1, ax1 = plt.subplots(figsize=(7, 5))
top_countries.plot(kind='barh', color='green', ax=ax1)  # Horizontal bar chart
ax1.set_title('Top 10 Countries by Transaction Value')
ax1.set_xlabel('Total Value (in USD)')
ax1.set_ylabel('Country')
ax1.grid(axis='x')  # Add gridlines for better readability

# --------------------------- Second Chart: Product Category Pie Chart --------------------------- #
# Set up the pie chart for product category distribution
fig2, ax2 = plt.subplots(figsize=(7, 5))
category_distribution = filtered_data['Category'].value_counts()
category_distribution.plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette('pastel'),
                           startangle=90, wedgeprops={'edgecolor': 'black'}, ax=ax2)
ax2.set_title('Product Category Distribution')
ax2.set_ylabel('')  # Remove y-label for aesthetics

# --------------------------- Third Chart: Total Import vs Export Value --------------------------- #
# Set up the plotting area for Donut Chart
fig3, ax3 = plt.subplots(figsize=(7, 5))
import_export_value = filtered_data.groupby('Import_Export')['Value'].sum()
ax3.pie(import_export_value, labels=import_export_value.index, autopct='%1.1f%%', startangle=90,
         colors=['#1f77b4', '#ff7f0e'])
centre_circle = plt.Circle((0, 0), 0.70, color='white', fc='white')
fig3.gca().add_artist(centre_circle)
ax3.set_title('Total Import vs Export Value')
plt.axis('equal')

# --------------------------- Fourth Chart: Shipping Methods Bar Chart --------------------------- #
# Set up the plotting area for Shipping Methods Bar Chart
fig4, ax4 = plt.subplots(figsize=(7, 5))
shipping_method_count = filtered_data['Shipping_Method'].value_counts()
shipping_method_count.plot(kind='bar', color='purple', ax=ax4)
ax4.set_title('Number of Transactions by Shipping Method')
ax4.set_ylabel('Number of Transactions')
ax4.set_xticklabels(shipping_method_count.index, rotation=45)

# --------------------------- Displaying Charts Side by Side --------------------------- #
# Create a layout for 2 columns for the first row
col1, col2 = st.columns(2)

# Plot 1: Top 10 Countries
with col1:
    st.subheader("Top 10 Countries by Transaction Value")
    st.pyplot(fig1)  # Display Top 10 Countries by Transaction Value

# Plot 2: Product Category Distribution
with col2:
    st.subheader("Product Category Distribution")
    st.pyplot(fig2)  # Display Product Category Distribution

# Create a layout for another 2 columns for the second row
col3, col4 = st.columns(2)

# Plot 3: Total Import vs Export Value
with col3:
    st.subheader("Total Import vs Export Value")
    st.pyplot(fig3)  # Display Total Import vs Export Value

# Plot 4: Shipping Methods Bar Chart
with col4:
    st.subheader("Number of Transactions by Shipping Method")
    st.pyplot(fig4)  # Display Number of Transactions by Shipping Method

# --------------------------- Display the Map Chart --------------------------- #
st.subheader("Total Import and Export Values by Country")
country_values = filtered_data.groupby(['Country', 'Import_Export'])['Value'].sum().reset_index()
country_values_pivot = country_values.pivot(index='Country', columns='Import_Export', values='Value').fillna(0)
country_values_pivot['Total'] = country_values_pivot.sum(axis=1)
fig7 = px.choropleth(country_values_pivot,
                      locations=country_values_pivot.index,
                      locationmode='country names',
                      color='Total',
                      hover_name=country_values_pivot.index,
                      title='Total Import and Export Values by Country',
                      color_continuous_scale=px.colors.sequential.Plasma,
                      labels={'Total': 'Total Value (in USD)'})
fig7.update_layout(width=1100, height=700)
st.plotly_chart(fig7)  # Display the map chart in Streamlit
