import streamlit as st
import pandas as pd
import plotly.express as px
from functions import *

st.set_page_config(
    page_icon="🩺",
    page_title="Health",
    initial_sidebar_state="expanded",
    )


st.header("Health Data")

GENERAL_TAB,  WATER_TAB, DEATH_CAUSES_TAB = st.tabs(["General", "Water Access", "Causes of Death"])

with GENERAL_TAB:
  df_hospital_beds = get_hospital_beds_data()
  hospital_beds_fig = px.line(df_hospital_beds,
                x="Year",
                y=["hospital beds MAR(per 1000 people)", "hospital beds ArabW(per 1000 people)", "hospital beds World(per 1000 people)"],
                title="Hospital beds per 1000 people",
                labels={"value": "Number of beds"},
                markers=True
              )
  hospital_beds_fig.data[0].name="Morocco"
  hospital_beds_fig.data[1].name="Arab world"
  hospital_beds_fig.data[2].name="World"
  hospital_beds_fig.update_traces(hovertemplate=" %{y: .3} Beds per 1000")
  hospital_beds_fig.update_layout(hovermode="x unified",
                    legend=dict(
                      orientation="h",
                      yanchor="bottom",
                      y=1.02,
                      xanchor="right",
                      x=1
                    )  
                  )
  st.plotly_chart(hospital_beds_fig, use_container_width=True)

  df_health_exp = get_health_exp_data()
  health_exp_fig = px.line(df_health_exp,
                x="Year",
                y="current health expenditure % of gdp",
                title="Current health expenditure (% of GDP)",
                labels={"current health expenditure % of gdp": "% of GDP"},
                markers=True 
              )
  health_exp_fig.update_traces(hovertemplate=" %{y}%")
  health_exp_fig.update_layout(hovermode="x")

  st.plotly_chart(health_exp_fig, use_container_width=True)

  df_immunization = get_immunization_data()
  immunization_fig = px.line(df_immunization,
                x="Year",
                y=["Immunization, measles %", "Immunization, Hepatitis B %", "Immunization, DPT %", "Immunization, neonatal tetanus %", "Immunization, Polio %", "Immunization, BCG %"],
                title="Immunisation",
                labels={"value": "%"},
                markers=True
              )
  immunization_fig.data[0].name = "measles"
  immunization_fig.data[1].name = "HepB3"
  immunization_fig.data[2].name = "DPT"
  immunization_fig.data[3].name = "Neonatal tetanus"
  immunization_fig.data[4].name = "Polio"
  immunization_fig.data[5].name = "BCG"
  immunization_fig.update_traces(hovertemplate=" %{y}%")
  immunization_fig.update_layout(hovermode="x unified",
                    legend=dict(
                      orientation = "h",
                      yanchor="bottom",
                      y = 1,
                      xanchor="right",
                      x=1
                    )  
                  )
  st.plotly_chart(immunization_fig, use_container_width=True)

  df_health_personnel = get_health_personnel_data()
  health_personnel_fig = px.line(df_health_personnel,
                x="Year",
                y=["medical doctors per 10 000 people", "nursing and midwifery personnel per 10 000 people", "dentists per 10 000 people"],
                title='Health personnel (per 10 000 people)',
                labels={"value": "Number of personnel"},
                markers=True,
                hover_data=["medical doctors number", "nursing and midwifery personnel number", "nursing number", "midwifery number", "dentists number"]
              )
  health_personnel_fig.data[0].name="Medical Doctors"
  health_personnel_fig.data[0].hovertemplate='<b>Medical doctors:</b> <br> %{y: .3} per 10.000 pop <br> %{customdata[0]} Medical doctors <extra></extra>'
  health_personnel_fig.data[1].name="Nurses and Midwifes"
  health_personnel_fig.data[1].hovertemplate=" <b>Nurses and Midwives:</b> <br> %{y: .3} per 10.000 pop <br> %{customdata[1]} Nurses and midwives: <br> --- %{customdata[2]} Nurses <br> --- %{customdata[3]} Midwives <extra></extra>"
  health_personnel_fig.data[2].name="Dentists"
  health_personnel_fig.data[2].hovertemplate=' <b>Dentists:</b> <br> %{y: .3} per 10.000 ppopulation <br> %{customdata[4]} Dentists <extra></extra>'
  health_personnel_fig.update_layout(hovermode="x",
                                    legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=1.02,
                                        xanchor="right",
                                        x=1
                                      ) 
                                    )

  st.plotly_chart(health_personnel_fig, use_container_width=True)


  df_healty_life = get_healthy_life_data()
  healthy_life_fig = px.line(df_healty_life,
                x="Year",
                y=["healthy life expectancy at birth -both sexes", "healthy life expectancy at birth -Male", "healthy life expectancy at birth -Female"],
                title="Healthy life expectancy at birth",
                labels={"value": "Age"},
                markers=True  
              )
  healthy_life_fig.data[0].name="Both sexes"
  healthy_life_fig.data[1].name="Male"
  healthy_life_fig.data[2].name="Female"
  healthy_life_fig.update_traces(hovertemplate="%{y} healthy years")
  healthy_life_fig.update_layout(hovermode="x unified",
                    legend=dict(
                      orientation="h",
                      yanchor="bottom",
                      y=1.02,
                      xanchor="right",
                      x=1
                    )  
                  )

  st.plotly_chart(healthy_life_fig, use_container_width=True)

  with st.expander('Sources'):
    st.caption("""
      [World Bank - Hospital beds - Morocco](https://data.worldbank.org/indicator/SH.MED.BEDS.ZS?locations=MA) - [Arab World](https://data.worldbank.org/indicator/SH.MED.BEDS.ZS?locations=1A) - [World](https://data.worldbank.org/indicator/SH.MED.BEDS.ZS) \n
      [World Health organization - Current health expenditure (CHE) as percentage of gross domestic product (GDP)(%)](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/current-health-expenditure-(che)-as-percentage-of-gross-domestic-product-(gdp)-(-)) \n
      [World Health organization - Immunization & personnel indicators](https://www.who.int/data/gho/data/indicators) \n
      [World Health organization -Healthy life expentancy](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/gho-ghe-hale-healthy-life-expectancy-at-birth)

    """)

with WATER_TAB:
  df_safely_managed_water, df_basic_water = get_water_data()
  safely_managed_water_fig = px.bar(df_safely_managed_water,
              x="Year",
              y=["urban safely managed drinking water services %", "rural safely managed drinking water services %"], 
              title="population using safely managed drinking water services %",
              labels={"value": "%"},
              barmode="group"
            )
  safely_managed_water_fig.data[0].name="Urban"
  safely_managed_water_fig.data[0].hovertemplate=" Year: %{x} <br> %{y}% of Urban population uses safely managed water services <extra></extra>"
  safely_managed_water_fig.data[1].name="Rural"
  safely_managed_water_fig.data[1].hovertemplate=" Year: %{x} <br> %{y}% of Rural population uses safely managed water services <extra></extra>"
  safely_managed_water_fig.update_layout(legend=dict(
      orientation = "h",
      yanchor="bottom",
      y=1.02,
      xanchor = "right",
      x = 1
  ))
  st.plotly_chart(safely_managed_water_fig, use_container_width=True)

  basic_water_fig = px.bar(df_basic_water,
              x="Year",
              y=["urban Basic drinking-water services" , "rural Basic drinking-water services"], 
              title="population using at least basic drinking water services %",
              labels={"value": "%"},
              barmode="group"
            )
  basic_water_fig.data[0].name="Urban"
  basic_water_fig.data[0].hovertemplate=" %{y}% of Urban population uses safely managed water services <extra></extra>"
  basic_water_fig.data[1].name="Rural"
  basic_water_fig.data[1].hovertemplate=" %{y}% of Rural population uses safely managed water services <extra></extra>"
  basic_water_fig.update_layout(legend=dict(
      orientation = "h",
      yanchor="bottom",
      y=1.02,
      xanchor = "right",
      x = 1
  ))
  st.plotly_chart(basic_water_fig, use_container_width=True)

  with st.expander("Sources"):
    st.caption("""
      [World Health Organization - Population using at least basic drinking-water services (%)](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/population-using-at-least-basic-drinking-water-services-(-)) \n
      [World Health Organization - Population using safely managed drinking-water services (%)](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/population-using-safely-managed-drinking-water-services-(-))
    """)

with DEATH_CAUSES_TAB:
  df_death_causes_male = get_male_deaths_causes()
  male_death_causes_fig = px.bar(df_death_causes_male, 
             x="Death rate per 100 000 population", 
             y="Cause",
             orientation="h",
             title="Top 15 causes of death for males - 2019"
            )
  male_death_causes_fig.update_traces(hovertemplate=" %{x} death per 100 000 population")
  st.plotly_chart(male_death_causes_fig, use_container_width=True)

  df_death_causes_female = get_female_death_causes()
  female_death_causes_fig = px.bar(df_death_causes_female, 
             x="Death rate per 100 000 population", 
             y="Cause",
             orientation="h",
             title="Top 15 causes of death for females - 2019"
            )
  female_death_causes_fig.update_traces(hovertemplate=" %{x} death per 100 000 population")
  st.plotly_chart(female_death_causes_fig, use_container_width=True)

  with st.expander("Sources"):
    st.caption("""
      [Global Health Estimates 2020: Deaths by Cause, Age, Sex, by Country and by Region, 2000-2019. Geneva, World Health Organization; 2020.](https://www.who.int/data/gho/data/themes/mortality-and-global-health-estimates/ghe-leading-causes-of-death)
    """)
