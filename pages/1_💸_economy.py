import plotly.express as px
import streamlit as st
from functions import *

st.set_page_config(
    page_icon="💸",
    page_title="Economy",
    initial_sidebar_state="expanded",
    )


st.header("Economy Data")

GDP_TAB, TRADE_TAB, INFLATION_TAB, LABOR_TAB = st.tabs(
    ["GDP", "Trade", "Inflation", "Labor Force"])

with GDP_TAB:
    df_gdp = get_gdp_data()

    gdp, gdpPC = st.columns(2)
    with gdp:
        gdp_fig = px.line(df_gdp, 
                        x="year", 
                        y="GDP",
                        title='GDP (current US$)',
                        markers=True,
                        line_shape='spline',
                        hover_data=["GDP_r"]
                        )
        gdp_fig.update_traces(hovertemplate="GDP: %{customdata[0]}")
        gdp_fig.update_layout(hovermode="x")
        
        st.plotly_chart(gdp_fig, use_container_width=True)
       
    with gdpPC:
        GDP_capita_fig = px.line(df_gdp,
              x="year",
              y="GDP per capita",
              title='GDP per capita (current US$)',
              markers=True,
              line_shape='spline',
            )
        GDP_capita_fig.update_traces(hovertemplate="GDP per capita: %{y}")
        GDP_capita_fig.update_layout(hovermode="x")
        st.plotly_chart(GDP_capita_fig, use_container_width=True)
    
    gdp_growth, gdpPC_growth = st.columns(2)

    with gdp_growth:
        GDP_growth_fig = px.line(df_gdp,
                x='year',
                y="GDP growth (annual %)",
                title='GDP growth (annual %)',
                markers=True,
                line_shape='spline',
                custom_data=['year', "GDP growth in %"],
                )
        GDP_growth_fig.update_traces(hovertemplate="  GDP growth: %{customdata[1]}")
        GDP_growth_fig.update_layout(hovermode="x")
        st.plotly_chart(GDP_growth_fig, use_container_width=True)
        
    with gdpPC_growth:
        gdpPC_growth_fig = px.line(df_gdp,
              x='year',
              y="GDP per capita growth(annual%)",
              title='GDP per capita growth (annual%)',
              markers=True,
              line_shape='spline',
              custom_data=['year', "GDP per capita growth in %"]
            )
        gdpPC_growth_fig.update_traces(hovertemplate=" GDP per capita growth: %{customdata[1]}")
        gdpPC_growth_fig.update_layout(hovermode="x")
        st.plotly_chart(gdpPC_growth_fig, use_container_width=True)

    with st.expander("Sources "):
        st.caption("""
        [Data World bank GDP (current US$)](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD?locations=MA) -
        [Data World Bank GDP Growth](https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG?locations=MA) \n
        [Data World Bank GDP per capita (current US$)](https://data.worldbank.org/indicator/NY.GDP.PCAP.CD?locations=MA) - 
        [Data World Bank GDP per capita growth](https://data.worldbank.org/indicator/NY.GDP.PCAP.KD.ZG?locations=MA) 
        """)

with TRADE_TAB:
    # EXPORT / IMPORT BY PARTNER
    df_export = eco_load_and_transform("./Morocco export to by partner in 2020_.csv",
                                       'Gross Export', 'GE')
    df_import = eco_load_and_transform("./Morocco import from by partner in 2020_.csv",
                                       'Gross Import', "GI")

    # Radio btns
    Type = st.radio(
        "Select exports or imports",
        ('Exports', 'Imports'),
        label_visibility="collapsed",
        horizontal=True,
        key='Type'
    )
    # Variables change depending on radio value
    if Type == 'Exports':
        partnersInfo = get_partner_variables('Exports', df_export)
    elif Type == 'Imports':
        partnersInfo = get_partner_variables("Imports", df_import)


    # populate the select dynamicly
    options = st.multiselect(
        'Countries',
        partnersInfo["partners_list"],
        partnersInfo["top_10_partners"],
        key='options',
        label_visibility='collapsed',
        max_selections=15)

    # create chart if select has at least one value
    if options:
        # filtered dataframe by countries in the options
        df_ex_partners = df_export[df_export['Country'].isin(
            options)]
        df_im_partners = df_import[df_import['Country'].isin(
            options)]

        fig = px.bar(df_ex_partners if Type == 'Exports' else df_im_partners,
                     x=partnersInfo["x"],
                     y='Country',
                     orientation='h',
                     title=f"Where does Morocco {partnersInfo['title']} 2020 (${partnersInfo['total']})",
                     color='Country',
                     color_discrete_sequence=px.colors.qualitative.Plotly,
                     opacity=0.9,
                     text=partnersInfo["tip_txt"],
                     hover_name='Country',
                     hover_data=partnersInfo["hoverData"],
                     labels=dict({
                         "Country": "",
                     })
                     )

        fig.update_layout(title_font_size=20,
                          uniformtext_minsize=12)
        st.plotly_chart(fig, theme='streamlit', use_container_width=True)

    else:
        st.info('Choose One country or more 👆')

    # --------------- BY PRODUCT ------------------#

    df_export_product = eco_load_and_transform("./Morocco export by product in 2020_.csv",
                                               "Gross Export", "GE")
    df_import_product = eco_load_and_transform(
        "././Morocco import by product in 2020_.csv", "Gross Import", "GI")

    if Type == "Exports":
        productsInfo = get_product_variables(Type, df_export_product)
    else:
        productsInfo = get_product_variables(Type, df_import_product)

    fig1 = px.treemap(productsInfo["df"],
                      path=[px.Constant("all"), 'Sector', 'Name'],
                      values=productsInfo['values'],
                      title=productsInfo['title'],
                      hover_data=productsInfo['hover_data'],
                      height=500
                      )
    fig1.update_traces(
        root_color="lightgrey",
        textinfo='label+percent entry',
        insidetextfont=dict(size=25),
        tiling=dict(pad=3),
        hovertemplate=' <b>%{label}</b><br> Category: %{parent}<br>' +
        ' Gross Export: %{customdata[0]}<br>' +
        ' Share : %{customdata[1]}'
    )

    fig1.update_layout(title_font_size=20 ,margin=dict(t=50, l=25, r=25, b=25))
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

    with st.expander("Sources "):
        st.caption("""
        [Atlas of economic complexity exports and imports](https://atlas.cid.harvard.edu/explore?country=134&queryLevel=location&product=undefined&year=2020&productClass=HS&target=Product&partner=undefined&startYear=1995)
        """)

with INFLATION_TAB:
    
    df_inflation = get_inflation_data()

    st.subheader('Inflation Calculator:')
    left, right = st.columns(2)
    with left:
        amount = st.number_input("Original amount in dirhams:", min_value=0, value=1000)
        start = st.selectbox('Start Year:', options=df_inflation['year'], index=0)
        end = st.selectbox('End year', options=df_inflation['year'], index=61)

    result = df_inflation[df_inflation["year"] == end]["consumer_price_index"].values[0] / df_inflation[df_inflation["year"] == start]["consumer_price_index"].values[0] * amount
    result = "{:.2f}".format(result)
    with right:
        st.write(f'**{amount}** dirhams in {start} corresponds to **{result}** dirhams at the begining of {end} due to inflation')
        with st.expander('Formula'):
            st.write('CPI end year / CPI start year * Amount')

    
    inflation_fig = px.line(df_inflation,
              x="year",
              y=['inflation of consumer prices', "inflation_world"],
              
              title="Inflation rate of consumer prices",
              markers=True,
              line_shape="spline",
              custom_data=['year', "inflation_world %",'inflation %']
            )
    inflation_fig.update_traces(hovertemplate= "%{y: .2}%", hoverinfo="y+x")
    inflation_fig.update_layout(hovermode="x unified",
                                legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=1.02,
                                    xanchor="right",
                                    x=1
                                ))
    st.plotly_chart(inflation_fig, use_container_width=True)
    
    CPI_fig = px.line(df_inflation,
              x="year",
              y="consumer_price_index",
              title="Consumer price index (2010 = 100)",
              markers=True,
              line_shape='spline',
              
            )
    CPI_fig.update_traces(yhoverformat='.1f', hovertemplate=" Year: %{x} <br> %{y}")
    st.plotly_chart(CPI_fig, use_container_width=True)

    with st.expander("Source"):
        st.caption("""
            [World Bank - Inflation rate of consumer prices - Morocco](https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?locations=MA) \n
            [World Bank - Consumer price index](https://data.worldbank.org/indicator/FP.CPI.TOTL?locations=MA)
        """)
    
with LABOR_TAB:
    # ------------ LABOR FIGURE ------------
    df_labor = get_labor_data()
    labor_fig = px.line(df_labor,
              x="year",
              y=["labor force total", "labor force male", "labor force female"],
              labels={"value": "Million"},
              title="Labor force",
              markers=True,
              line_shape="spline",
              custom_data=['LB_total_readable', 'LB_male_readable', "LB_female_readable", "labor force male %", "labor force female %"]
            )
    labor_fig.data[0].hovertemplate = "%{customdata[0]} "
    labor_fig.data[1].hovertemplate = "%{customdata[1]} <br> Share: %{customdata[3]: .4}%"
    labor_fig.data[2].hovertemplate = "%{customdata[2]} <br> Share: %{customdata[4]: .4}%"
    labor_fig.update_layout(hovermode="x unified",legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=1.02,
                                    xanchor="right",
                                    x=1
                                ))
    st.plotly_chart(labor_fig, use_container_width=True)

    # ------------- UNEMPLOYMENT FIGURE --------------

    df_unemployment = get_unemployment_data()
    unem_fig = px.line(df_unemployment,
              x="year",
              y=["unemployed_total", "unemployed_male", "unemployed_female"],
              title="Unemployment",
              markers=True,
              line_shape="spline",
              custom_data=["unem_total_readable", "unem_male_readable", "unem_female_readable", "unemployment, total (% of total labor force)", "unemployment, male (% of male labor force)", "unemployment, female (% of female labor force)"]
            )
    unem_fig.data[0].hovertemplate = "%{customdata[0]} <br> % of total labor force: %{customdata[3]: .3}%"
    unem_fig.data[0].name = "Total"
    unem_fig.data[1].hovertemplate = "%{customdata[1]} <br> % of male labor force: %{customdata[4]: .3}%"
    unem_fig.data[1].name = "Male"
    unem_fig.data[2].hovertemplate = "%{customdata[2]} <br> % of female lobor force: %{customdata[5]: .3}%"
    unem_fig.data[2].name = "Female"
    unem_fig.update_layout(hovermode="x unified",legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=1.02,
                                    xanchor="right",
                                    x=1
                                ))
    st.plotly_chart(unem_fig, use_container_width=True)

    with st.expander("Sources"):
        st.caption("""
            [World Bank - Labor force, total](https://data.worldbank.org/indicator/SL.TLF.TOTL.IN?locations=MA) - [female](https://data.worldbank.org/indicator/SL.TLF.TOTL.FE.ZS?locations=MA)\n
            [World Bank - Unemployment, total](https://data.worldbank.org/indicator/SL.UEM.TOTL.ZS?locations=MA) - 
            [female](https://data.worldbank.org/indicator/SL.UEM.TOTL.FE.ZS?locations=MA) - [Male](https://data.worldbank.org/indicator/SL.UEM.TOTL.MA.ZS?locations=MA)
        """)
