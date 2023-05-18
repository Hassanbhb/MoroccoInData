import pandas as pd
import streamlit as st
import json
import geopandas as gpd


def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


st.cache_data
def eco_load_and_transform(url, Gross, g):
    df = pd.read_csv(url)
    df = df.sort_values(by=[Gross], ascending=False)
    df['Share'] = df['Share'].apply(
        lambda x: str(round(x, 2))+"%")
    df[g] = df[Gross].apply(
        lambda x: human_format(x))
    return df

# ------ Getting data ------

st.cache_data
def get_map_data():
    regions = open("./morocco-with-regions_.geojson", encoding="utf-8")
    regions_map = json.loads(regions.read())
    df = pd.read_csv("./Map_data.csv")
    df["population_r"] = df["population"].apply(lambda x: human_format(x))
    return regions_map, df

st.cache_data
def get_eco_data():
    df = pd.read_csv("./Morocco eco data.csv")
    return df

st.cache_data
def get_demographics_data():
    df = pd.read_csv('./demographics data.csv')
    return df

st.cache_data
def get_education_data():
    df = pd.read_csv('./education data.csv')
    return df

# this returns a typle
st.cache_data
def get_Health_data():
    df = pd.read_csv('./health data.csv')
    df_causes_Males = pd.read_csv("./top_10_deaths_causes_males.csv")
    df_causes_females = pd.read_csv("./top_10_deaths_causes_females.csv")
    return df, df_causes_Males, df_causes_females

# ------- economy data -----
def get_gdp_data():
    df = get_eco_data()
    df["GDP_r"] = df["GDP"].apply(lambda x: human_format(x))
    df['GDP growth in %'] = df['GDP growth (annual %)'].apply(lambda x: str(round(x, 2))+"%")
    df['GDP per capita growth in %'] = df['GDP per capita growth(annual%)'].apply(lambda x: str(round(x, 2))+"%")
    return df[["year", "GDP", "GDP_r", "GDP growth (annual %)", "GDP growth in %", "GDP per capita", "GDP per capita growth(annual%)", "GDP per capita growth in %"]]

def get_inflation_data():
    df = get_eco_data()
    df["inflation %"] = df['inflation of consumer prices'].apply(lambda x: str(round(x, 2))+"%")
    df["inflation_world %"] = df['inflation_world'].apply(lambda x: str(round(x, 2))+"%")
    return df[["year","consumer_price_index","inflation of consumer prices", "inflation %", "inflation_world", "inflation_world %"]]

def get_partner_variables(choice, df):
    if choice == "Exports":
        return dict({
            "partners_list": sorted(list(df['Country'])),
            "top_10_partners": list(df['Country'])[:10],
            "x": 'Gross Export',
            "title": 'Export to',
            "hoverData": dict({
                "Country": False,
                "Gross Export": False,
                "GE": False,
                "Share": True
            }),
            "tip_txt": 'GE',
            "total": human_format(df['Gross Export'].sum())
        })
    elif choice == "Imports":
        return dict({
            "partners_list": sorted(list(df['Country'])),
            "top_10_partners": list(df['Country'])[:10],
            "x": 'Gross Import',
            "title": 'Import from',
            "hoverData": dict({
                "Country": False,
                "Gross Import": False,
                "GI": False,
                "Share": True
            }),
            "tip_txt": 'GI',
            "total": human_format(df['Gross Import'].sum())
        })

def get_product_variables(choice, df):
    if choice == "Exports":
        return dict({
            "df": df,
            "values": 'Gross Export',
            "title": 'What did morocco export in 2020',
            "hover_data": ['GE', "Share"],
            "total": human_format(df['Gross Export'].sum())
        })
    elif choice == "Imports":
        return dict({
            "df": df,
            "values": 'Gross Import',
            "title": 'What did morocco Import in 2020',
            "hover_data": ["GI", "Share"],
            "total": human_format(df['Gross Import'].sum())
        })

def get_labor_data():
    df = get_eco_data()
    df["labor force female"] = (df['labor force total'] / 100) * df['labor force female %']
    df['labor force male'] = df['labor force total'] - df["labor force female"]
    df['labor force male %'] = (df['labor force male']*100)/df['labor force total']
    df["LB_total_readable"] = df["labor force total"].apply(lambda x: human_format(x))
    df["LB_female_readable"] = df["labor force female"].apply(lambda x: human_format(x))
    df["LB_male_readable"] = df["labor force male"].apply(lambda x: human_format(x))
    
    return df[["year", "labor force total", "labor force male", "labor force female", "labor force female %", "labor force male %", "LB_total_readable", "LB_male_readable", "LB_female_readable"]].iloc[30:]

def get_unemployment_data():
    df = get_eco_data()
    df["labor force female"] = (df['labor force total'] / 100) * df['labor force female %']
    df['labor force male'] = df['labor force total'] - df["labor force female"]
    df['labor force male %'] = (df['labor force male']*100)/df['labor force total']
    df['unemployed_total'] = (df["labor force total"] / 100) * df["unemployment, total (% of total labor force)"]
    df['unemployed_female'] = (df["labor force female"] / 100) * df["unemployment, female (% of female labor force)"]
    df['unemployed_male'] = (df["labor force male"] / 100) * df["unemployment, male (% of male labor force)"]
    df["unem_total_readable"] = df["unemployed_total"].apply(lambda x: human_format(x))
    df["unem_female_readable"] = df["unemployed_female"].apply(lambda x: human_format(x))
    df["unem_male_readable"] = df["unemployed_male"].apply(lambda x: human_format(x))
    
    return df[["year", "unemployed_total", "unemployed_female", "unemployed_male", "unem_total_readable", "unem_female_readable", "unem_male_readable", "unemployment, total (% of total labor force)", "unemployment, male (% of male labor force)", "unemployment, female (% of female labor force)"]].iloc[31:]

def get_pop_data():
    df = get_demographics_data()
    df["total_pop_r"] = df["pop"].apply(lambda x: human_format(x))
    df["male_pop_r"] = df["pop_male"].apply(lambda x: human_format(x))
    df["female_pop_r"] = df["pop_female"].apply(lambda x: human_format(x))
    df['pop_growth'] = ((df['pop'] / 100) * df['pop_growth_%']).apply(lambda x: human_format(x))
    return df[["year", "pop", "pop_male", "pop_female", "total_pop_r", "male_pop_r", "female_pop_r", "pop_growth", "pop_growth_%"]]

def get_pop_pyramid_data(year):
    df = get_demographics_data()
    def get_ages(x):
        ages = []
        for y in x:
            a = y[6:]
            ages.append(a.replace("to", "-"))
        return ages
    y_age = get_ages(df.columns.values.tolist()[5:26]) # get age values from column names
    x_M = df[["pop_M_0to4","pop_M_5to9","pop_M_10to14","pop_M_15to19","pop_M_20to24","pop_M_25to29","pop_M_30to34","pop_M_35to39","pop_M_40to44","pop_M_45to49","pop_M_50to54","pop_M_55to59","pop_M_60to64","pop_M_65to69","pop_M_70to74","pop_M_75to79","pop_M_80to84","pop_M_85to89","pop_M_90to94","pop_M_95to99","pop_M_100+"]]
    x_M = x_M[df["year"] == year].values.tolist()[0] # get data by year for male pop
    x_F = df[["pop_F_0to4","pop_F_5to9","pop_F_10to14","pop_F_15to19","pop_F_20to24","pop_F_25to29","pop_F_30to34","pop_F_35to39","pop_F_40to44","pop_F_45to49","pop_F_50to54","pop_F_55to59","pop_F_60to64","pop_F_65to69","pop_F_70to74","pop_F_75to79","pop_F_80to84","pop_F_85to89","pop_F_90to94","pop_F_95to99","pop_F_100+"]]
    x_F = x_F[df["year"] == year].values.tolist()[0] # get data by year for female pop
    x_F_int = list(map(int,x_F)) #turn data to a list of inetegrs
    x_F_negative = [-x for x in x_F_int] # negate the values

    return x_M, x_F, x_F_negative, y_age

def get_urbanRural_data():
    df = get_demographics_data()
    return df[["year", "urban_pop", "rural_pop", "urban_pop_growth_%", "rural_pop_growth_%"]]

def get_life_data():
    df = get_demographics_data()
    return df[["year", 'life_exp_total', 'life_exp_male', 'life_exp_female', 'fertility_rate']]

def get_death_data():
    df = get_demographics_data()
    suicides = df[["year", "suicide_rate(per100k)", "suicide_rate_M(per100k)", "suicide_rate_F(per100k)"]].dropna(thresh=2)
    deaths = df[["year", "deaths_5-9", "deaths_10-14", "deaths_15-19", "deaths_20-24"]].dropna(thresh=2)
    return suicides, deaths

# ----- education charts data -----
def get_edu_general_data():
    df = get_education_data()
    return df[["Year", "gov_exp_edu_(%gdp)"]].iloc[13:]

def get_primary_edu_data():
    df = get_education_data()
    # ---- primary teachers data
    df_primary_teachers = df[["Year", "primary_total_teachers", "primary_female_teachers_%"]].iloc[10:]
    df_primary_teachers["primary_female_teachers"] = (df_primary_teachers['primary_total_teachers'] / 100) * df_primary_teachers['primary_female_teachers_%']
    df_primary_teachers["primary_male_teachers"] = df_primary_teachers['primary_total_teachers'] - df_primary_teachers["primary_female_teachers"]
    # ---- primary pupils data
    df_primary_pupils = df[["Year", "primary_total_pupils", "primary_female_pupils_%"]].iloc[10:]
    df_primary_pupils["primary_female_pupils"] = (df_primary_pupils['primary_total_pupils'] / 100) * df_primary_pupils['primary_female_pupils_%']
    df_primary_pupils["primary_male_pupils"] = df_primary_pupils['primary_total_pupils'] - df_primary_pupils["primary_female_pupils"]
    df_primary_pupils["primary_total_pupils_r"] = df_primary_pupils["primary_total_pupils"].apply(lambda x: human_format(x))
    df_primary_pupils["primary_female_pupils_r"] = df_primary_pupils["primary_female_pupils"].apply(lambda x: human_format(x))
    df_primary_pupils["primary_male_pupils_r"] = df_primary_pupils["primary_male_pupils"].apply(lambda x: human_format(x))
    # primary pupil teacher ratio
    df_primary_ratio = df[['Year', "primary_pupil_teacher_ratio"]].iloc[10:]
    # ---- primary duration data
    df_primary_duration = df[["Year", "primary_duration"]].iloc[10:]
    # ---- children out of school data
    df_primary_start_age = df[["Year", "primary_school_startAge"]].iloc[10:]
    df_outOf_school_primary = df[["Year", "outOf_school_primary_total", "outOf_school_primary_male", "outOf_school_primary_female"]].iloc[10:]

    return df_primary_teachers, df_primary_duration, df_primary_pupils, df_outOf_school_primary, df_primary_start_age, df_primary_ratio

def get_secondary_edu_data():
    df = get_education_data()
    # ---- secondary teacher data
    df_secondary_teachers = df[["Year", "secondary_total_teachers", "secondary_male_teachers", "secondary_female_teachers"]].iloc[10:]
    # ---- secondary pupils data
    df_secondary_pupils = df[["Year", "secondary_total_pupils", "secondary_female_pupils_%"]].iloc[10:]
    df_secondary_pupils["secondary_female_pupils"] = (df_secondary_pupils['secondary_total_pupils'] / 100) * df_secondary_pupils['secondary_female_pupils_%']
    df_secondary_pupils["secondary_male_pupils"] = df_secondary_pupils['secondary_total_pupils'] - df_secondary_pupils["secondary_female_pupils"]

    df_secondary_pupils["secondary_total_pupils_r"] = df_secondary_pupils["secondary_total_pupils"].apply(lambda x: human_format(x))
    df_secondary_pupils["secondary_female_pupils_r"] = df_secondary_pupils["secondary_female_pupils"].apply(lambda x: human_format(x))
    df_secondary_pupils["secondary_male_pupils_r"] = df_secondary_pupils["secondary_male_pupils"].apply(lambda x: human_format(x))
    # ------ secondary pupil teacher ratio -------
    df_secondary_ratio = df[["Year", "secondary_pupil_teacher_ratio"]].iloc[11:]
    # ---- out of school data
    df_ouOf_school_secondary = df[["Year", "outOf_school_lowerSecondary_total", "outOf_school_lowerSecondary_male", "outOf_school_lowerSecondary_female"]].iloc[39:]
    # ---- secondary education duration
    df_secondary_duration = df[["Year", "secondary_duration"]].iloc[10:]

    return df_secondary_teachers, df_secondary_pupils, df_secondary_ratio, df_ouOf_school_secondary, df_secondary_duration

def get_tertiary_edu_data():
    df = get_education_data()
    # tertiary enrollement
    df_tertiary_enroll = df[["Year", "tertiary_enroll_female(%gross)", "tertiary_enroll_male(%gross)"]].iloc[10:]
    # pupil - teacher ratio
    df_tertiary_pupil_teacher_ratio = df[["Year", "tertiary_pupil_teacher_ratio"]]
    return df_tertiary_enroll, df_tertiary_pupil_teacher_ratio

def get_literacy_data():
    df = get_education_data()
    return df[["Year", "literacy rate adult", "literacy rate male", "literacy rate female", "literacy rate youth total", "literacy rate youth male", "literacy rate youth female"]].iloc[22:]

# ------ Health data ------
# !!!! the get health data function returns a typle !!!!
def get_health_exp_data():
    df = get_Health_data()
    return df[0][["Year", "current health expenditure % of gdp"]].iloc[40:]

def get_healthy_life_data():
    df = get_Health_data()
    return df[0][["Year","healthy life expectancy at birth -both sexes", "healthy life expectancy at birth -Male", "healthy life expectancy at birth -Female"]].dropna(thresh=2)

def get_hospital_beds_data():
    df = get_Health_data()
    return df[0][["Year", "hospital beds MAR(per 1000 people)", "hospital beds ArabW(per 1000 people)", "hospital beds World(per 1000 people)"]]

def get_immunization_data():
    df = get_Health_data()
    return df[0][["Year", "Immunization, measles %", "Immunization, Hepatitis B %", "Immunization, DPT %", "Immunization, neonatal tetanus %", "Immunization, Polio %", "Immunization, BCG %"]].iloc[22:]

def get_health_personnel_data():
    df = get_Health_data()
    return df[0][["Year", "medical doctors per 10 000 people", "nursing and midwifery personnel per 10 000 people", "dentists per 10 000 people", "medical doctors number", "nursing and midwifery personnel number", "nursing number", "midwifery number", "dentists number"]].iloc[44:58]

def get_male_deaths_causes():
    df = get_Health_data()
    return df[1][["Cause", "Death rate per 100 000 population"]][:15]

def get_female_death_causes():
    df = get_Health_data()
    return df[2][["Cause", "Death rate per 100 000 population"]][:15]

def get_water_data():
    df = get_Health_data()
    safely_managed = df[0][["Year", "urban safely managed drinking water services %", "rural safely managed drinking water services %"]].iloc[40:]
    basic =  df[0][["Year", "urban Basic drinking-water services" , "rural Basic drinking-water services"]].iloc[60:61]
    return safely_managed, basic
