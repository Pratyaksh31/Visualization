import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# Streamlit title and header
st.set_page_config(layout="wide", page_title="Imports & Exports Dashboard")
st.title("Data Visualization: Imports and Exports")

# Load the dataset
import_export = pd.read_csv(r"Imports_Exports_Dataset.csv")

# Sample 3001 rows from the dataset
my_data = import_export.sample(n=3001, replace=False, random_state=55031)

# Sidebar filters
st.sidebar.header("Filters")

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

# --------------------- Chart 1: Top 10 Countries by Transaction Value --------------------- #
top_countries = filtered_data.groupby('Country')['Value'].sum().nlargest(10)
fig1 = px.bar(
    top_countries,
    x=top_countries.values,
    y=top_countries.index,
    orientation='h',
    title='Top 10 Countries by Transaction Value',
    labels={'x': 'Total Value (USD)', 'y': 'Country'},
    color=top_countries.values,
    color_continuous_scale=px.colors.sequential.Viridis
)
fig1.update_layout(height=400, title_x=0.5)

# --------------------- Chart 2: Product Category Distribution --------------------- #
category_distribution = filtered_data['Category'].value_counts()
fig2 = px.pie(
    filtered_data, 
    values=category_distribution.values, 
    names=category_distribution.index, 
    title='Product Category Distribution', 
    color_discrete_sequence=px.colors.sequential.RdBu,
    hole=0.4
)
fig2.update_layout(height=400, title_x=0.5)

# --------------------- Chart 3: Total Import vs Export Value --------------------- #
import_export_value = filtered_data.groupby('Import_Export')['Value'].sum()
fig3 = px.pie(
    import_export_value, 
    values=import_export_value.values, 
    names=import_export_value.index, 
    title='Total Import vs Export Value', 
    color_discrete_sequence=px.colors.sequential.Plasma,
    hole=0.6
)
fig3.update_layout(height=400, title_x=0.5)

# --------------------- Chart 4: Number of Transactions by Shipping Method --------------------- #
shipping_method_count = filtered_data['Shipping_Method'].value_counts()
fig4 = px.bar(
    shipping_method_count,
    x=shipping_method_count.index,
    y=shipping_method_count.values,
    title='Number of Transactions by Shipping Method',
    labels={'x': 'Shipping Method', 'y': 'Number of Transactions'},
    color=shipping_method_count.values,
    color_continuous_scale=px.colors.sequential.Tealgrn
)
fig4.update_layout(xaxis_tickangle=-45, height=400, title_x=0.5)

# --------------------- Chart 5: Payment Terms by Import/Export --------------------- #
stacked_data = filtered_data.groupby(['Import_Export', 'Payment_Terms']).size().unstack()
fig5 = px.bar(
    stacked_data,
    title='Payment Terms Distribution by Import/Export',
    labels={'value': 'Number of Transactions'},
    barmode='stack',
    color_discrete_sequence=px.colors.sequential.Aggrnyl
)
fig5.update_layout(height=400, title_x=0.5)

# --------------------- Chart 6: Average Transaction Value by Month --------------------- #
filtered_data['Month'] = filtered_data['Date'].dt.month
monthly_avg_value = filtered_data.groupby('Month')['Value'].mean()
fig6 = px.line(
    monthly_avg_value,
    x=monthly_avg_value.index,
    y=monthly_avg_value.values,
    markers=True,
    title='Average Value of Transactions by Month',
    labels={'x': 'Month', 'y': 'Average Transaction Value (USD)'},
    color_discrete_sequence=['#636EFA']
)
fig6.update_layout(height=400, title_x=0.5)

# --------------------- Chart 7: Total Import/Export Values by Country --------------------- #
country_values = filtered_data.groupby(['Country', 'Import_Export'])['Value'].sum().reset_index()
country_values_pivot = country_values.pivot(index='Country', columns='Import_Export', values='Value').fillna(0)
country_values_pivot['Total'] = country_values_pivot.sum(axis=1)
fig7 = px.choropleth(
    country_values_pivot,
    locations=country_values_pivot.index,
    locationmode='country names',
    color='Total',
    hover_name=country_values_pivot.index,
    title='Total Import and Export Values by Country',
    color_continuous_scale=px.colors.sequential.Plasma,
    labels={'Total': 'Total Value (in USD)'}
)
fig7.update_layout(width=1200, height=700, title_x=0.5)

# --------------------- Displaying the Dashboard --------------------- #
st.write("## Interactive Dashboard")

# First row: Displaying two plots side by side
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)  # Top 10 Countries by Transaction Value

with col2:
    st.plotly_chart(fig2, use_container_width=True)  # Product Category Distribution

# Second row: Two more plots side by side
col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(fig3, use_container_width=True)  # Total Import vs Export Value

with col4:
    st.plotly_chart(fig4, use_container_width=True)  # Number of Transactions by Shipping Method

# Third row: Stacked bar and line charts side by side
col5, col6 = st.columns(2)

with col5:
    st.plotly_chart(fig5, use_container_width=True)  # Payment Terms Distribution

with col6:
    st.plotly_chart(fig6, use_container_width=True)  # Average Value of Transactions by Month

# Final row: Full-width map
st.plotly_chart(fig7, use_container_width=True)  # Map for Total Import/Export Values by Country
