import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import streamlit as st
import  streamlit_vertical_slider  as svs
from streamlit_extras.buy_me_a_coffee import button
from functions import *

st.set_page_config(
    page_icon="🧮",
    page_title="Demographics",
    initial_sidebar_state="expanded",
    )


st.header("Demographics Data")

POP_TAB, POP_TYPE_TAB, LIFE_TAB, DEATH_TAB = st.tabs(["Population", "Urban / Rural", "Life", "Death"])

with POP_TAB:
    pyramid_data, py_slider = st.columns([5, 1])
    with py_slider:
      #  year = st.selectbox("Select a year", np.arange(1960, 2021))
      year = svs.vertical_slider(
                    default_value=1960, 
                    step=1, 
                    min_value=1960, 
                    max_value=2021,
                    slider_color= '#37a8ff', #optional
                    track_color='#83C9FF', #optional
                    thumb_color = '#FF2B2B' #optional
                    )
      if not year : # without this the year returns none on load
         year = 1960 

    with pyramid_data:
      # --------- population pyramid ----------
      x_M, x_F, x_F_negative, y_age = get_pop_pyramid_data(year)
      pyra_fig = go.Figure()
      pyra_fig.add_trace(go.Bar(y = y_age, x=x_M,
                          name="Male", orientation="h",
                          hovertemplate='%{x} Thousand',
                          marker=dict(
                            color="#83C9FF" # lightblue
                          ))
                    )
      pyra_fig.add_trace(go.Bar(y = y_age, x=x_F_negative,
                          name="Female", orientation="h",
                          customdata=np.stack([x_F], axis=-1),
                          hovertemplate='%{customdata[0]} Thousand',
                          marker=dict(
                            color="#FF2B2B" # red
                          ))
                    )
      pyra_fig.update_layout(title = f'Population Pyramid in {year}',
                        title_font_size = 22, barmode = 'relative',
                        bargap = 0.1, 
                        bargroupgap = 0,
                        xaxis = dict(tickvals = [-1500, -1000, -500, -150,
                                                  0, 150, 500, 1000, 1500],
                                      ticktext = ['1.5M', '1M', '500K', '150k', '0', 
                                                  '150K', '500K', '1M', '1.5M'], 
                                      title = 'Population in thousands',
                                      title_font_size = 14),
                        hovermode="y unified",
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                          )
                      )
      st.plotly_chart(pyra_fig, use_container_width=True)
      
    df = get_pop_data()
    df["total_pop_r"] = df["pop"].apply(lambda x: human_format(x))
    df["male_pop_r"] = df["pop_male"].apply(lambda x: human_format(x))
    df["female_pop_r"] = df["pop_female"].apply(lambda x: human_format(x))
    pop_fig = px.line(df,
                  x="year",
                  y="pop",
                  title="Population of Morocco",
                  labels={"pop": "Population", "year": "Year"},
                  markers=True,
                  custom_data=['total_pop_r']
                )
    pop_fig.add_bar(x=df['year'],
                y=df["pop_male"],
                name="Male population",
                customdata=df[['male_pop_r']],
                hovertemplate=" %{customdata[0]}"
              )
    pop_fig.add_bar(x=df['year'],
                y=df["pop_female"],
                name="Female population",
                customdata=df[['female_pop_r']],
                hovertemplate=" %{customdata[0]}" 
              )
    pop_fig.data[0].hovertemplate = "Total population: %{customdata[0]}"
    pop_fig.update_layout(hovermode="x unified", barmode="stack", legend=dict(
                          orientation="h",
                          yanchor="bottom",
                          y=1.02,
                          xanchor="right",
                          x=1
                        ))
    st.plotly_chart(pop_fig, use_container_width=True)

    pop_growth_fig = px.line(df,
              x="year",
              y="pop_growth_%",
              title="Population growth (annual %)",
              labels={"pop_growth_%": "Growth %"},
              markers=True,
              line_shape="spline",
              custom_data=['pop_growth']
            )
    pop_growth_fig.data[0].hovertemplate = " Year: %{x} <br> Growth %: %{y: .3}% <br> pop: +%{customdata[0]}"
    st.plotly_chart(pop_growth_fig, use_container_width=True)

    with st.expander("Source"):
      st.caption("""
        [United Nations - population pyramid](https://population.un.org/wpp/Download/Standard/Population/)\n
        [World Bank - Population, total](https://data.worldbank.org/indicator/SP.POP.TOTL?locations=MA) - [Male](https://data.worldbank.org/indicator/SP.POP.TOTL.MA.IN?locations=MA) - [Female](https://data.worldbank.org/indicator/SP.POP.TOTL.FE.IN?locations=MA)\n
        [World Bank - Population Growth](https://data.worldbank.org/indicator/SP.POP.GROW?locations=MA)
      """)

with POP_TYPE_TAB:
    df = get_urbanRural_data()

    ur_fig = px.line(df,
              x="year",
              y=["urban_pop", "rural_pop"],
              title="Urban / Rural populations",
              labels={"value": "Pupulation"},
              markers=True,
              line_shape="spline"
            )
    ur_fig.data[0].name = "Urban"
    ur_fig.data[0].hovertemplate = " %{y}"
    ur_fig.data[1].name = "Rural"
    ur_fig.data[1].hovertemplate = " %{y}"
    ur_fig.update_layout(hovermode="x unified", 
                        yaxis=dict(tickformat=".4s"), 
                        legend_title_text="Type",
                        legend=dict(
                          orientation="h",
                          yanchor="bottom",
                          y=1.02,
                          xanchor="right",
                          x=1
                        ))
    st.plotly_chart(ur_fig, use_container_width=True)

    ur_growth_fig = px.line(df,
              x="year",
              y=["urban_pop_growth_%", "rural_pop_growth_%"],
              labels={"value": "Growth in %"},
              title="Urban / Rural Growth (annual %)",
              markers=True,
              line_shape="spline"
            )
    ur_growth_fig.data[0].name = "Urban"
    ur_growth_fig.data[0].hovertemplate = " %{y:.3}%"
    ur_growth_fig.data[1].name = "Rural"
    ur_growth_fig.data[1].hovertemplate = " %{y:.3}%"
    ur_growth_fig.update_layout(
        hovermode="x unified", 
        legend=dict(
          orientation="h",
          yanchor="bottom",
          y=1.02,
          xanchor="right",
          x=1
      )
    )
    st.plotly_chart(ur_growth_fig, use_container_width=True)

    with st.expander("Source"):
      st.caption("""
        [World bank - Urban population](https://data.worldbank.org/indicator/SP.URB.TOTL?locations=MA) - [Rural Growth](https://data.worldbank.org/indicator/SP.URB.GROW?locations=MA)\n
        [World Bank - Rural population](https://data.worldbank.org/indicator/SP.RUR.TOTL?locations=MA) - [Rural Growth](https://data.worldbank.org/indicator/SP.RUR.TOTL.ZG?locations=MA)
      """)

with LIFE_TAB:
  df = get_life_data()
  life_exp_fig = px.line(df,
            x="year",
            y=['life_exp_total', 'life_exp_male', 'life_exp_female'],
            labels={"value": "Age"},
            title="Life expentancy at birth",
          )
  life_exp_fig.data[0].name = "Average"
  life_exp_fig.data[0].hovertemplate = " %{y:.2} years"
  life_exp_fig.data[0].line = dict(dash='dot')
  life_exp_fig.data[1].name = "Male"
  life_exp_fig.data[1].hovertemplate = " %{y:.2} years"
  life_exp_fig.data[2].name = "Female"
  life_exp_fig.data[2].hovertemplate = " %{y:.2} years"
  life_exp_fig.update_layout(hovermode="x unified",
                              legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1
                              )
                            )
  st.plotly_chart(life_exp_fig, use_container_width=True)

  fertility_fig = px.line(df,
              x="year",
              y="fertility_rate",
              title='Fertility rate (births per woman)',
              labels={"fertility_rate": "Births per woman"},
            )
  fertility_fig.data[0].line = dict(dash="dash")
  fertility_fig.data[0].hovertemplate = "Year: %{x} <br> births: %{y}"
  fertility_fig.update_layout(hovermode="x")
  st.plotly_chart(fertility_fig, use_container_width=True)

  with st.expander("Source"):
    st.caption("""
      [World Bank - Life expentancy  at birth - total](https://data.worldbank.org/indicator/SP.DYN.LE00.IN?locations=MA) - [male](https://data.worldbank.org/indicator/SP.DYN.LE00.MA.IN?locations=MA) - [female](https://data.worldbank.org/indicator/SP.DYN.LE00.FE.IN?locations=MA)\n
      [world Bank - Fertility rate](https://data.worldbank.org/indicator/SP.DYN.TFRT.IN?locations=MA)
    """)

with DEATH_TAB:
  df_suicides, df_deaths = get_death_data()
  suicide_fig = px.line(df_suicides,
            x='year',
            y=["suicide_rate(per100k)", "suicide_rate_M(per100k)", "suicide_rate_F(per100k)"],
            title="Suicide Rate per 100.000" ,
            labels={"value": "Deaths"},
            markers=True,
            line_shape='spline',
          )
  suicide_fig.data[0].name = "Average"
  suicide_fig.data[0].hovertemplate = " %{y} per 100K"
  suicide_fig.data[0].line = dict(dash='dot')
  suicide_fig.data[1].name = "Male"
  suicide_fig.data[1].hovertemplate = " %{y} per 100K"
  suicide_fig.data[2].name = "Female"
  suicide_fig.data[2].hovertemplate = " %{y} per 100K"
  suicide_fig.update_layout(hovermode="x unified",
                            legend=dict(
                              orientation="h",
                              yanchor="bottom",
                              y=1.02,
                              xanchor="right",
                              x=1
                            )
                          )

  st.plotly_chart(suicide_fig, use_container_width=True)
  
  deaths_fig = px.line(df_deaths,
                x="year",
                y=["deaths_5-9", "deaths_10-14", "deaths_15-19", "deaths_20-24"],
                title="Deaths by age group",
                labels={"value": "Number of deaths"},
                markers=True
            )
  deaths_fig.data[0].name = "5-9"
  deaths_fig.data[0].hovertemplate = " %{y}"
  deaths_fig.data[0].marker = dict(symbol="x")
  deaths_fig.data[1].name = "10-14"
  deaths_fig.data[1].hovertemplate = " %{y}"
  deaths_fig.data[2].name = "15-19"
  deaths_fig.data[2].hovertemplate = " %{y}"
  deaths_fig.data[3].name = "20-24"
  deaths_fig.data[3].hovertemplate = " %{y}"
  deaths_fig.update_layout(hovermode="x unified",
                           legend=dict(
                              orientation="h",
                              yanchor="bottom",
                              y=1.02,
                              xanchor="right",
                              x=1
                            ))

  st.plotly_chart(deaths_fig, use_container_width=True)

  with st.expander("Source"):
    st.caption("""
      [World Bank - Suicide rate](https://data.worldbank.org/indicator/SH.STA.SUIC.P5?locations=MA) - [male](https://data.worldbank.org/indicator/SH.STA.SUIC.MA.P5?locations=MA) - [female](https://data.worldbank.org/indicator/SH.STA.SUIC.FE.P5?locations=MA)\n
      [World Bank - Deaths by age group - 5-9](https://data.worldbank.org/indicator/SH.DTH.0509?locations=MA) - [10-14](https://data.worldbank.org/indicator/SH.DTH.1014?locations=MA) - [15-19](https://data.worldbank.org/indicator/SH.DTH.1519?locations=MA) - [20-24](https://data.worldbank.org/indicator/SH.DTH.2024?locations=MA)
    """)


hide = """
  <style>
  footer { visibility: hidden; }
  </style>
"""
st.markdown(hide, unsafe_allow_html=True)