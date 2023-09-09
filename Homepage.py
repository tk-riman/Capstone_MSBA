import streamlit as st
import pandas as pd
import plotly.express as px

import plotly.graph_objects as go

st.set_page_config(
    page_title="Data Analsys",
    page_icon="media/logo.png"
)

st.title('Home Page')
st.sidebar.success("select a page")
logo = st.sidebar.image("media/logo.png", width=300)

df = None
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
# Check if a file has been uploaded
if uploaded_file is not None:
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(uploaded_file, encoding='utf-8')
    st.success("CSV uploaded successfully")

    overall_customers = df['Customer Email'].nunique()

    # Compute total number of unique customers for each country
    customers_per_country = df.groupby('Country')['Customer Email'].nunique()

    # overall_customers, customers_per_country
    # st.plotly_chart(px.histogram(df, x='Shipping Fees'))
    fig = go.Figure()

    # Add a trace for the number of customers
    fig.add_trace(go.Indicator(
        mode="number",
        value=overall_customers,
        title="Total Customers"
    ))

    # Dropdown menu for country selection
    country_options = ["All"] + customers_per_country.index.tolist()


    # Define the update function for dropdown
    def update_country(country):
        if country == "All":
            return overall_customers
        else:
            return customers_per_country[country]


    # Correcting the typo and updating the layout for dropdown
    fig.update_layout(
        updatemenus=[{
            "buttons": [
                {
                    "args": [{"value": [update_country(country)]}],
                    "label": country,
                    "method": "restyle"
                }
                for country in country_options
            ],
            "direction": "down",
            "showactive": True,
            "x": 0.5,
            "xanchor": "center",
            "y": 1.2,
            "yanchor": "top"
        }]
    )
    fig1 = fig
    orders_per_country = df.groupby('Country')['Order ID'].nunique()
    overall_total_orders = df['Order ID'].nunique()

    # orders_per_country, overall_total_orders

    fig = go.Figure()

    # Add the overall total orders to the figure
    fig.add_trace(go.Indicator(
        mode="number",
        value=overall_total_orders,
        title="Total Orders",
        domain={'row': 0, 'column': 0},
        visible=True
    ))

    # Add an Indicator for each country
    for country, orders in orders_per_country.items():
        fig.add_trace(go.Indicator(
            mode="number",
            value=orders,
            title=f"Orders in {country}",
            domain={'row': 0, 'column': 0},
            visible=False
        ))

    # Define the dropdown buttons
    buttons = [
        {
            'args': [{'visible': [True] + [False] * len(orders_per_country)}],
            'label': 'Overall',
            'method': 'restyle'
        }
    ]

    for i, country in enumerate(orders_per_country.index):
        visibility_list = [False] * (len(orders_per_country) + 1)
        visibility_list[i + 1] = True
        buttons.append(
            {
                'args': [{'visible': visibility_list}],
                'label': country,
                'method': 'restyle'
            }
        )

    # Update the layout to include the dropdown menu
    fig.update_layout(
        updatemenus=[{
            'buttons': buttons,
            'direction': 'down',
            'showactive': True,
            'x': 0.5,
            'xanchor': 'center',
            'y': 1.15,
            'yanchor': 'top'
        }]
    )

    # Show the figure
    fig2 = fig

    average_order_value_per_country = df.drop_duplicates(subset='Order ID').groupby('Country')['Grand Total'].mean()
    overall_average_order_value = df.drop_duplicates(subset='Order ID')['Grand Total'].mean()

    # average_order_value_per_country, overall_average_order_value

    fig = go.Figure()

    # Add the overall average order value to the figure
    fig.add_trace(go.Indicator(
        mode="number",
        value=overall_average_order_value,
        title="Average Order Value",
        domain={'row': 0, 'column': 0},
        visible=True
    ))

    # Add an Indicator for each country's average
    for country, avg_value in average_order_value_per_country.items():
        fig.add_trace(go.Indicator(
            mode="number",
            value=avg_value,
            title=f"Average Order Value in {country}",
            domain={'row': 0, 'column': 0},
            visible=False
        ))

    # Define the dropdown buttons for the average order value
    avg_buttons = [
        {
            'args': [{'visible': [True] + [False] * len(average_order_value_per_country)}],
            'label': 'Overall',
            'method': 'restyle'
        }
    ]

    for i, country in enumerate(average_order_value_per_country.index):
        visibility_list = [False] * (len(average_order_value_per_country) + 1)
        visibility_list[i + 1] = True
        avg_buttons.append(
            {
                'args': [{'visible': visibility_list}],
                'label': country,
                'method': 'restyle'
            }
        )

    # Update the layout to include the dropdown menu for average order value
    fig.update_layout(
        updatemenus=[{
            'buttons': avg_buttons,
            'direction': 'down',
            'showactive': True,
            'x': 0.5,
            'xanchor': 'center',
            'y': 1.15,
            'yanchor': 'top'
        }]
    )

    # Show the figure
    fig3 = fig

    col1, col2, col3 = st.columns(3)

    st.plotly_chart(fig1)

    st.plotly_chart(fig2)

    st.plotly_chart(fig3)

    overall_grand_total = df.drop_duplicates(subset='Order ID')['Grand Total'].sum()

    # Compute the contribution of each Category Cut to the overall grand total
    category_contribution = df.groupby('Category Cut')['Grand Total'].sum()

    # Calculate the proportion of each Category Cut's contribution to the overall grand total
    category_proportions = category_contribution / overall_grand_total

    # category_proportions
    category_contribution_country = df.groupby(['Country', 'Category Cut'])['Grand Total'].sum()
    grand_total_per_country = df.drop_duplicates(subset='Order ID').groupby('Country')['Grand Total'].sum()
    category_proportions_country = category_contribution_country / grand_total_per_country

    # Create a new figure
    fig = go.Figure()

    # Overall data (initially visible)
    labels_overall = category_proportions.index
    values_overall = category_proportions.values
    fig.add_trace(
        go.Pie(labels=labels_overall, values=values_overall, hole=.3, textinfo='percent+label', visible=True))

    # Add slices for each country's data to the figure (initially not visible)
    for country in df['Country'].unique():
        labels_country = category_proportions_country[country].index
        values_country = category_proportions_country[country].values
        fig.add_trace(
            go.Pie(labels=labels_country, values=values_country, hole=.3, textinfo='percent+label', visible=False))

    # Define the dropdown buttons for the pie chart
    pie_buttons = [
        {
            'args': [{'visible': [True] + [False] * len(df['Country'].unique())}],
            'label': 'Overall',
            'method': 'update'
        }
    ]

    for i, country in enumerate(df['Country'].unique()):
        visibility_list = [False] * (1 + len(df['Country'].unique()))  # 1 for overall + number of countries
        visibility_list[i + 1] = True
        pie_buttons.append(
            {
                'args': [{'visible': visibility_list}],
                'label': country,
                'method': 'update'
            }
        )

    # Update the layout to include the dropdown menu for the pie chart
    fig.update_layout(
        updatemenus=[{
            'buttons': pie_buttons,
            'direction': 'down',
            'showactive': True,
            'x': 0.5,
            'xanchor': 'center',
            'y': 1.15,
            'yanchor': 'top'
        }],
        showlegend=False
    )
    st.plotly_chart(fig)

    overall_category_frequency = df['Category Cut'].value_counts()

    # Compute the frequency of each Category Cut for each country
    category_frequency_country = df.groupby('Country')['Category Cut'].value_counts()
    fig = go.Figure()

    # Add overall data (initially visible) to the figure
    fig.add_trace(
        go.Bar(y=overall_category_frequency.index, x=overall_category_frequency.values, orientation='h',
               visible=True,
               name='Overall'))

    # Add bars for each country's data to the figure (initially not visible)
    for country in df['Country'].unique():
        y_values = category_frequency_country[country].index
        x_values = category_frequency_country[country].values
        fig.add_trace(go.Bar(y=y_values, x=x_values, orientation='h', visible=False, name=country))

    # Define the dropdown buttons for the bar plot
    bar_buttons = [
        {
            'args': [{'visible': [True] + [False] * len(df['Country'].unique())}],
            'label': 'Overall',
            'method': 'update'
        }
    ]

    for i, country in enumerate(df['Country'].unique()):
        visibility_list = [False] * (1 + len(df['Country'].unique()))  # 1 for overall + number of countries
        visibility_list[i + 1] = True
        bar_buttons.append(
            {
                'args': [{'visible': visibility_list}],
                'label': country,
                'method': 'update'
            }
        )

    # Update the layout to include the dropdown menu for the bar plot
    fig.update_layout(
        updatemenus=[{
            'buttons': bar_buttons,
            'direction': 'down',
            'showactive': True,
            'x': 0.5,
            'xanchor': 'center',
            'y': 1.15,
            'yanchor': 'top'
        }],
        barmode='stack'
    )

    st.plotly_chart(fig)

    overall_item_frequency = df['Item Name'].value_counts().head(10)

    # Compute the frequency of each Item Name for each country and select the top 10
    item_frequency_country = df.groupby('Country')['Item Name'].value_counts().groupby('Country').head(10)

    fig = go.Figure()

    # Add overall data (initially visible) to the figure
    fig.add_trace(
        go.Bar(y=overall_item_frequency.index, x=overall_item_frequency.values, orientation='h', visible=True,
               name='Overall'))

    # Add bars for each country's data to the figure (initially not visible)
    for country in df['Country'].unique():
        items_for_country = item_frequency_country[country]
        y_values = items_for_country.index
        x_values = items_for_country.values
        fig.add_trace(go.Bar(y=y_values, x=x_values, orientation='h', visible=False, name=country))

    # Define the dropdown buttons for the bar plot
    bar_buttons = [
        {
            'args': [{'visible': [True] + [False] * len(df['Country'].unique())}],
            'label': 'Overall',
            'method': 'update'
        }
    ]

    for i, country in enumerate(df['Country'].unique()):
        visibility_list = [False] * (1 + len(df['Country'].unique()))  # 1 for overall + number of countries
        visibility_list[i + 1] = True
        bar_buttons.append(
            {
                'args': [{'visible': visibility_list}],
                'label': country,
                'method': 'update'
            }
        )

    # Update the layout to include the dropdown menu for the bar plot
    fig.update_layout(
        updatemenus=[{
            'buttons': bar_buttons,
            'direction': 'down',
            'showactive': True,
            'x': 0.5,
            'xanchor': 'center',
            'y': 1.15,
            'yanchor': 'top'
        }],
        barmode='stack',
        title='Top 10 Most Popular Items'
    )

    st.plotly_chart(fig)

    custom_scale = [
        [0, 'rgb(247,247,247)'],  # pale color for countries not in the data
        [0.0001, 'rgb(252,187,161)'],  # for values > 70 to 2000
        [0.2, 'rgb(252,146,114)'],  # for values > 2000 to 6000
        [0.6, 'rgb(251,106,74)'],  # for values > 6000 to 10000
        [1, 'rgb(222,45,38)']  # for values > 10000 to 15000
    ]

    # Create a Choropleth map with the modified custom color scale
    # fig = go.Figure(go.Choropleth(
    #     locations=orders_count_per_country.index,
    #     z=orders_count_per_country.values,
    #     locationmode='country names',
    #     colorscale=custom_scale,
    #     text=[country_abbreviations.get(country, '') for country in orders_count_per_country.index],
    #     marker_line_color='darkgray',
    #     marker_line_width=0.5,
    #     colorbar_title='Number of Orders',
    #     showscale=True
    # ))

    # Update the layout
    fig.update_geos(projection_type="mercator", showcoastlines=True, coastlinecolor="Black", showland=True,
                    landcolor="white")
    fig.update_layout(title_text='Number of Orders by Country',
                      geo=dict(showframe=False, showcoastlines=False, projection_type='mercator'))
    st.plotly_chart(fig)

    total_value_per_country = df.drop_duplicates(subset='Order ID').groupby('Country')['Grand Total'].sum()

    fig_adjusted = go.Figure(data=[
        go.Bar(x=total_value_per_country.index,
               y=total_value_per_country.values,
               text=total_value_per_country.apply(lambda x: "${:,.0f}".format(x)),
               textposition='outside')
    ])

    # Update the layout and title
    fig_adjusted.update_layout(title_text="Total Revenue by Country", xaxis_title="Country",
                               yaxis_title="Grand Total",
                               barmode='stack')

    # Show the figure

    # st.plotly_chart(fig_adjusted)

    df['Purchase Date'] = pd.to_datetime(df['Purchase Date'])

    # Extract month and year
    df['Year'] = df['Purchase Date'].dt.year
    df['Month'] = df['Purchase Date'].dt.month

    # Group by year, month, and coupon code and count occurrences
    coupon_usage = df.groupby(['Year', 'Month', 'Coupon Code']).size().reset_index(name='Frequency')

    # Create a plot using Plotly Express
    fig = px.bar(
        coupon_usage,
        x='Month',
        y='Frequency',
        color='Coupon Code',
        facet_col='Year',
        title='Coupon Usage Frequency per Month',
        labels={'Month': 'Month', 'Frequency': 'Coupon Usage Frequency'},
    )

    # st.plotly_chart(fig)
    fig = px.treemap(
        df,
        path=['Category Cut', 'Category', 'Item Name'],
        values='Quantity',  # You can replace 'Quantity' with an appropriate column
        color_continuous_scale='Blues',  # Blue color scheme
        title='Interactive Treemap',
    )
    st.plotly_chart(fig)
