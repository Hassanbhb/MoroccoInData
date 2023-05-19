import streamlit as st
import plotly.express as px
from functions import get_map_data
from PIL import Image
from streamlit_extras.buy_me_a_coffee import button

st.set_page_config(
    page_icon="📊",
    page_title="2014 Cencus",
    initial_sidebar_state="expanded",
    )

button(username="hassanbhb", floating=True, width=221)

logo = Image.open('./assets/logo.jpg')
st.image(logo, use_column_width=True)

st.write("""
  Welcome to Morocco in data, \n 
  where you can access consolidated data on Morocco's demographics, economy and more. We've gathered information from multiple sources, ensuring you have a comprehensive view in one convenient place. Explore key indicators, trends, and insights to deepen your understanding of Morocco's progress and challenges across these vital sectors and Gain better understanding of the country's development landscape. \n
  Please consider supporting the project ❤
  ### 2014 Census Data Visualized
""")

regions_map, df = get_map_data()

options = list(df.columns)[4:-1]
data_type = st.selectbox("Select an indicator:", options = options, format_func = lambda x: x.capitalize())

map_fig = px.choropleth_mapbox(data_frame=df, 
              geojson=regions_map, 
              color=data_type,
              title="Data per region",
              locations="id", 
              featureidkey="id",
              mapbox_style="carto-positron",
              center = dict(lat = 29.0, lon = -9.72),
              zoom=4,
              hover_data=["en_name", "ar_name", "am_name", data_type],
              color_discrete_sequence=px.colors.qualitative.Light24,
              opacity=0.8
            )
map_fig.update_geos(fitbounds="locations", visible=False)
map_fig.update_traces(
                  hovertemplate=" <b>%{customdata[0]}</b> <br> Arabic: %{customdata[1]} <br> Amazigh: %{customdata[2]} <br> "+ data_type.capitalize() +": %{customdata[3]} <extra></extra>",
                )
map_fig.update_layout(margin={"r":0,"t":22,"l":0,"b":0})
st.plotly_chart(map_fig, use_container_width=True)


data_fig = px.bar(df,
              x="en_name",
              y=data_type,
              color="en_name",
              title=data_type.capitalize() +" per region",
              labels={"en_name": "Regions"},
              color_discrete_sequence=px.colors.qualitative.Pastel,
            )
data_fig.update_traces(hovertemplate=" <b>%{x}</b> <br> "+ data_type.capitalize() +": %{y:} <extra></extra>")
st.plotly_chart(data_fig, use_container_width=True)

with st.expander("Source"):
    st.caption("2014 Census - Morocco, Haut-commisariat au plan")