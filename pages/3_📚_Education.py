import streamlit as st
from streamlit_extras.buy_me_a_coffee import button
import plotly.express as px
from functions import *

st.set_page_config(
    page_icon="📚",
    page_title="Education",
    initial_sidebar_state="expanded",
    )


st.header('Education data')

GENERAL_TAB, PRIMARY_TAB, SECONDARY_TAB, TERTIARY_TAB = st.tabs(["General", "Primary", "Secondary", "Tertiary"])

with GENERAL_TAB:
  df_gov_edu_gdp = get_edu_general_data()
  gov_edu_exp_fig = px.line(df_gov_edu_gdp,
            x="Year",
            y="gov_exp_edu_(%gdp)",
            title="Government expenditure on education (% of GDP)",
            labels={"gov_exp_edu_(%gdp)": "% of GDP"},
            markers=True,
            line_shape="spline"
          )
  gov_edu_exp_fig.update_traces(hovertemplate=" Value: %{y: .3}%")
  gov_edu_exp_fig.update_layout(hovermode="x")
  
  st.plotly_chart(gov_edu_exp_fig, use_container_width=True)

  df_literacy_rate = get_literacy_data()
  literacy_adult_fig = px.line(df_literacy_rate,
              x="Year",
              y=["literacy rate adult", "literacy rate male", "literacy rate female"],
              title="Literacy Rate, Adults (ages 15+)",
              labels={"value": "% of people ages 15+"},
              markers=True
            )
  literacy_adult_fig.data[0].name = "Total"
  literacy_adult_fig.data[0].marker = dict(symbol="x")
  literacy_adult_fig.data[1].name = "Male"
  literacy_adult_fig.data[2].name = "Female"
  literacy_adult_fig.data[2].marker = dict(symbol="square")
  literacy_adult_fig.update_traces(hovertemplate="%{y: .3}%")
  literacy_adult_fig.update_layout(hovermode="x",
                    legend=dict(
                      orientation="h",
                      yanchor="bottom",
                      y = 1.02,
                      xanchor="right",
                      x=1
                    )
                  )
  st.plotly_chart(literacy_adult_fig, use_container_width=True)

  literacy_youth_fig = px.line(df_literacy_rate,
              x = "Year",
              y = ["literacy rate youth total", "literacy rate youth male", "literacy rate youth female"],
              title = "Literacy rate, Youth (ages 15-24)",
              labels={"value": "% of people ages 15-24"},
              markers = True,
            )
  literacy_youth_fig.data[0].name = "Total"
  literacy_youth_fig.data[0].marker = dict(symbol="x")
  literacy_youth_fig.data[1].name = "Male"
  literacy_youth_fig.data[2].name = "Female"
  literacy_youth_fig.update_traces(hovertemplate="%{y: .3}%")
  literacy_youth_fig.update_layout(hovermode="x",
                    legend=dict(
                      orientation="h",
                      yanchor="bottom",
                      y = 1.02,
                      xanchor="right",
                      x=1
                    )
                  )
  st.plotly_chart(literacy_youth_fig, use_container_width=True)

  with st.expander("Source"):
    st.caption("""
      [World Bank - Gov expenditure on education (%GDP)](https://data.worldbank.org/indicator/SE.XPD.TOTL.GD.ZS?locations=MA) \n
      [World Bank - Literacy Rate - Adult](https://data.worldbank.org/indicator/SE.ADT.LITR.ZS?locations=MA) \n
      [World bank - Literacy Rate - Youth](https://data.worldbank.org/indicator/SE.ADT.1524.LT.ZS?locations=MA)
    """)

with PRIMARY_TAB:
  df_primary_teachers, df_primary_duration, df_primary_pupils, df_outOf_school_primary, df_primary_start_age, df_primary_ratio = get_primary_edu_data()
  
  primary_teachers_fig = px.line(df_primary_teachers,
            x="Year",
            y=["primary_total_teachers", "primary_male_teachers", "primary_female_teachers"],
            title="Primary education teachers",
            labels={"value": "Thousands"},
            line_shape="spline",
            markers=True
          )
  primary_teachers_fig.data[0].name = "Total teachers"
  primary_teachers_fig.data[1].name = "Male teachers"
  primary_teachers_fig.data[2].name = "Female teachers"
  primary_teachers_fig.update_traces(hovertemplate=" <b>Value:</b> %{y}")
  primary_teachers_fig.update_layout(hovermode="x",
                    legend=dict(
                      orientation="h",
                      yanchor="bottom",
                      y=1.02,
                      xanchor="right",
                      x=1
                    )
                  )
  st.plotly_chart(primary_teachers_fig, use_container_width=True)

  primary_pupils_fig = px.line(df_primary_pupils,
              x="Year",
              y=["primary_total_pupils", "primary_male_pupils", "primary_female_pupils"],
              title="Primary pupils",
              labels={"value": "Millions"},
              markers=True,
              line_shape="spline",
              custom_data=["primary_total_pupils_r", "primary_male_pupils_r", "primary_female_pupils_r"]
            )
  primary_pupils_fig.data[0].name = "Total pupils"
  primary_pupils_fig.data[0].hovertemplate = " Total pupils: %{customdata[0]} <extra></extra>"
  primary_pupils_fig.data[1].name = "Male pupils"
  primary_pupils_fig.data[1].hovertemplate = " Male pupils: %{customdata[1]} <extra></extra>"
  primary_pupils_fig.data[2].name = "Female pupils"
  primary_pupils_fig.data[2].hovertemplate = " Female pupils: %{customdata[2]} <extra></extra>"

  primary_pupils_fig.update_layout(hovermode="x", 
                    legend=dict(
                      orientation="h",
                      yanchor="bottom",
                      y=1.02,
                      xanchor="right",
                      x=1
                    ))
  st.plotly_chart(primary_pupils_fig, use_container_width=True)

  primary_ratio = px.line(df_primary_ratio,
              x="Year",
              y="primary_pupil_teacher_ratio",
              title="Pupil - teacher ratio",
              labels={"primary_pupil_teacher_ratio": "Pupils"},
              markers=True,
            )
  primary_ratio.update_traces(hovertemplate="%{y: .3} pupils per teacher")
  primary_ratio.update_layout(hovermode="x")
  st.plotly_chart(primary_ratio, use_container_width=True)

  outOfSchool_primary_fig = px.line(df_outOf_school_primary,
              x="Year",
              y=["outOf_school_primary_total", "outOf_school_primary_male", "outOf_school_primary_female"],
              title="Children out of school, primary",
              labels={"value": "Millions"},
              markers=True
            )
  outOfSchool_primary_fig.data[0].name = "Total"
  outOfSchool_primary_fig.data[0].hovertemplate = "%{y}"
  outOfSchool_primary_fig.data[1].name = "Male"
  outOfSchool_primary_fig.data[1].hovertemplate = "%{y}"
  outOfSchool_primary_fig.data[2].name = "Female"
  outOfSchool_primary_fig.data[2].hovertemplate = "%{y}"
  outOfSchool_primary_fig.update_layout(hovermode="x unified", legend=dict(
                      orientation="h",
                      yanchor="bottom",
                      y=1.02,
                      xanchor="right",
                      x=1
                    ))
  st.plotly_chart(outOfSchool_primary_fig, use_container_width=True)

  primary_edu_duration_fig = px.line(df_primary_duration,
              x="Year",
              y="primary_duration",
              title="Primary education duarion",
              labels={"primary_duration": " Duration in years"},
              markers=True,
            )
  primary_edu_duration_fig.update_traces(hovertemplate="%{y} years")
  primary_edu_duration_fig.update_layout(hovermode="x")
  st.plotly_chart(primary_edu_duration_fig, use_container_width=True)

  primary_start_age_fig = px.line(df_primary_start_age,
              x="Year",
              y="primary_school_startAge",
              title="Primary school start Age",
              labels={"primary_school_startAge": "Age"},
              markers=True
            )
  primary_start_age_fig.update_traces(hovertemplate="%{y} years")
  primary_start_age_fig.update_layout(hovermode="x")
  st.plotly_chart(primary_start_age_fig, use_container_width=True)

  with st.expander('Sources'):
    st.caption("""
      [Primary education teachers](https://data.worldbank.org/indicator/SE.PRM.TCHR?locations=MA) \n
      [Primary education pupils](https://data.worldbank.org/indicator/SE.PRM.ENRL?locations=MA) \n
      [Pupil-teacher ratio](https://data.worldbank.org/indicator/SE.PRM.ENRL.TC.ZS?locations=MA) \n
      [Children out of school](https://data.worldbank.org/indicator/SE.PRM.UNER?locations=MA)
    """)

with SECONDARY_TAB:
  df_secondary_teachers, df_secondary_pupils, df_secondary_ratio, df_ouOf_school_secondary, df_secondary_duration = get_secondary_edu_data()

  secondary_teachers_fig = px.line(df_secondary_teachers,
              x="Year",
              y=["secondary_total_teachers", "secondary_male_teachers", "secondary_female_teachers"],
              title="Secondary education teachers",
              labels={"value": "Thousands"},
              markers=True,
            )
  secondary_teachers_fig.data[0].name="Total"
  secondary_teachers_fig.data[1].name="Male"
  secondary_teachers_fig.data[2].name="Female"
  secondary_teachers_fig.update_traces(hovertemplate="%{y}")
  secondary_teachers_fig.update_layout(hovermode="x unified",
                    legend=dict(
                      orientation="h",
                      yanchor="bottom",
                      y=1.02,
                      xanchor="right",
                      x=1
                    )
                  )
  
  st.plotly_chart(secondary_teachers_fig, use_container_width=True)

  secondary_pupils_fig = px.line(df_secondary_pupils,
              x="Year",
              y=["secondary_total_pupils", "secondary_male_pupils", "secondary_female_pupils"],
              title="Secondary pupils",
              labels={"value": "Millions"},
              markers=True
            )
  secondary_pupils_fig.data[0].name="Total"
  secondary_pupils_fig.data[1].name="Male"
  secondary_pupils_fig.data[2].name="Female"
  secondary_pupils_fig.update_traces(hovertemplate="%{y}")
  secondary_pupils_fig.update_layout(hovermode="x unified",
                    legend=dict(
                      orientation="h",
                      yanchor="bottom",
                      y=1.02,
                      xanchor="right",
                      x=1
                    )
                  )
  st.plotly_chart(secondary_pupils_fig, use_container_width=True)

  secondary_ratio = px.line(df_secondary_ratio,
              x="Year",
              y="secondary_pupil_teacher_ratio",
              title="Pupil - teacher ratio",
              markers=True,
            )
  secondary_ratio.update_traces(hovertemplate="%{y: .3} pupils per teacher")
  secondary_ratio.update_layout(hovermode="x")
  st.plotly_chart(secondary_ratio, use_container_width=True)

  secondary_outOf_school_fig = px.line(df_ouOf_school_secondary,
              x="Year",
              y=["outOf_school_lowerSecondary_total", "outOf_school_lowerSecondary_male", "outOf_school_lowerSecondary_female"],
              title="Adolescents out of school (% of lower secondary school age)",
              labels={"value": "% of lower secondary school age"},
              markers=True
            )
  secondary_outOf_school_fig.data[0].name="total"
  secondary_outOf_school_fig.data[1].name="Male"
  secondary_outOf_school_fig.data[2].name="Female"
  secondary_outOf_school_fig.update_traces(hovertemplate='%{y: .3}%')
  secondary_outOf_school_fig.update_layout(hovermode="x unified",
                      legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                      )
                    )
  st.plotly_chart(secondary_outOf_school_fig, use_container_width=True)

  secondary_duration_fig = px.line(df_secondary_duration,
              x="Year",
              y="secondary_duration",
              title="Secondary education duration",
              labels={"secondary_duration": "Duration in years"},
              markers=True,
            )
  secondary_duration_fig.update_traces(hovertemplate="%{y} years")
  secondary_duration_fig.update_layout(hovermode="x")
  st.plotly_chart(secondary_duration_fig, use_container_width=True)

  with st.expander("Source"):
    st.caption("""
      [World Bank - Primary Teachers - total](https://data.worldbank.org/indicator/SE.PRM.TCHR?locations=MA) - [female](https://data.worldbank.org/indicator/SE.PRM.TCHR.FE.ZS?locations=MA) \n
      [World Bank - Primary pupils - total](https://data.worldbank.org/indicator/SE.PRM.ENRL?locations=MA) - [female](https://data.worldbank.org/indicator/SE.PRM.ENRL.FE.ZS?locations=MA)\n
      [World Bank - Primary pupil-teacher ratio](https://data.worldbank.org/indicator/SE.PRM.ENRL.TC.ZS?locations=MA)\n
      [World Bank - Adolescents out of school (% of lower secondary school age)](https://data.worldbank.org/indicator/SE.SEC.UNER.LO.ZS?locations=MA)
    """)

with TERTIARY_TAB:
  df_tertiary_enroll, df_tertiary_pupil_teacher_ratio = get_tertiary_edu_data()

  tertiary_enroll_fig = px.line(df_tertiary_enroll,
              x="Year",
              y=["tertiary_enroll_female(%gross)", "tertiary_enroll_male(%gross)"],
              title="Tertiary enrollement (% gross)",
              labels={"value": "% Gross"},
              markers=True,
            )
  tertiary_enroll_fig.data[0].name="Female"
  tertiary_enroll_fig.data[1].name="Male"
  tertiary_enroll_fig.update_traces(hovertemplate="%{y: .3}%")
  tertiary_enroll_fig.update_layout(hovermode="x unified")
  st.plotly_chart(tertiary_enroll_fig, use_container_width=True)

  tertiary_ratio_fig = px.line(df_tertiary_pupil_teacher_ratio,
                x="Year",
                y="tertiary_pupil_teacher_ratio",
                title="Pupil - teacher ratio",
                labels={"tertiary_pupil_teacher_ratio": "pupils"},
                markers=True
              )
  tertiary_ratio_fig.update_traces(hovertemplate="%{y: .3} pupil per teacher")
  tertiary_ratio_fig.update_layout(hovermode="x")
  st.plotly_chart(tertiary_ratio_fig, use_container_width=True)

  with st.expander("Sources"):
    st.caption("""
      [World Bank - Tetiary enrollement (%gross) - Female](https://data.worldbank.org/indicator/SE.TER.ENRR.FE) \n
      [World Bank - pupil-teacher ratio](https://data.worldbank.org/indicator/SE.TER.ENRL.TC.ZS?locations=MA)
    """)


hide = """
  <style>
  footer { visibility: hidden; }
  </style>
"""
st.markdown(hide, unsafe_allow_html=True)