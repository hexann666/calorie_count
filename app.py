import streamlit as st
import calorie_count.core as cc
import pandas as pd

st.set_page_config(page_title='Calorie count', page_icon='🖖')

st.sidebar.markdown("# Calorie count")
st.sidebar.markdown('First you will provide your height, weight and age and calculate your Basal Metabolic Rate, the number of calories required to keep your body functioning at rest.')
st.sidebar.markdown('After choosing your usual level of activity the Active Metabolic Rate, the number of calories that we consume on a daily basis depending on our height, gender, age, weight and entered activity level whilst maintaining current weight, will be calculated.')
st.sidebar.markdown('To calculate daily energy expenditure type in the activity you were doing today and choose the row number of activity from the list that matches your search pattern. Additionally you will enter the time you were doing this activity.')
st.image('https://raw.githubusercontent.com/hexann666/calorie_count/master/data/image_title.JPG')

message_activity_level = '1 - little to no exercise \
                \n2 - light exercise 1–3 days a week \
                \n3 - moderate exercise 3–5 days a week \
                \n4 - hard exercises 6–7 days a week \
                \n5 - physically demanding job or particularly challenging exercise routine'

body_params = {}

col1, col2, col3, col4 = st.columns(4)

with col1:
    body_params['height'] = st.number_input('Height in cm', min_value=1)

with col2:
    body_params['weight'] = st.number_input('Weight in kg', min_value=1)
    
with col3:
    body_params['age'] = st.number_input('Age in years', min_value=1)

with col4:
    body_params['gender'] = st.text_input('Biological gender w/m', max_chars=1)

with st.expander("See activity levels"):
    st.markdown(message_activity_level)

body_params['activity'] = st.selectbox(label='Select your activity level', options=[1, 2, 3, 4, 5], index=0)

st.write("You entered following body parameters:")
st.write(body_params)
st.write("You can correct your input by changing it in the corresponding field and pressing Enter")


if st.button('Calculate bmr'):
    bmr, amr = cc.calculate_bmr_amr(body_params)
    st.write(f"Your BMR is {bmr:.0f}")
    st.write(f"Your AMR is {amr:.0f}")
    st.text('\n')

#my_expander = st.expander(label='Calculate energy expenditure')
  

met_list = pd.read_csv('data/met_list_activities.csv',
                                        sep=';', 
                                        #encoding='ANSI', 
                                        decimal=',', 
                                        error_bad_lines=False)
nr = 0
met = 0 
time = 0
burned_cal, bmr_cal = 0, 0
your_act = ''
while met == 0:
        your_act = st.text_input('Type in the activity you were doing today:')
        if len(met_list[met_list['SPECIFIC MOTION'].str.contains(your_act)]) >= 1:
            st.text(met_list[met_list['SPECIFIC MOTION'].str.contains(your_act)])
            st.text('Select row number of your activity from the list')
            nr = st.number_input("Your activity's row number",  min_value=0)
        elif len(met_list[met_list['SPECIFIC MOTION'].str.contains(your_act)]) == 0:
            st.text('Please type again')
        met = met_list['METs'].iloc[nr]
        activity = str(met_list['SPECIFIC MOTION'].iloc[nr])

time = st.number_input('Type in the time of your activity for today in minutes:', min_value=0)
burned_cal = met * body_params['weight'] * time/60
bmr_cal = 1.2 * body_params['weight'] * (24 - time / 60)
if st.button('Calculate'):
        st.write(f'During {time} min of {activity} you burned {burned_cal:.0f} kcal.')
        st.write(f'Your total daily energy expenditure was {round((burned_cal + bmr_cal), 2):.0f} kcal today')
    #clicked = st.button('Calculate')