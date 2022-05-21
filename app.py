import streamlit as st
import calorie_count.core as cc
import pandas as pd

st.sidebar.markdown("# Calorie count")
st.sidebar.markdown('Users can type in their body parameters and get an estimation of their recommended daily calories intake. In the second step users can provide information about the type of their sport activity and time they were doing it and get a calculation of spent calories during this activity.')
st.image('https://raw.githubusercontent.com/hexann666/calorie_count/master/data/image_title.JPG')

message_activity_level = 'Please choose your level of activity:\
                \n1 - little to no exercise \
                \n2 - light exercise 1–3 days a week \
                \n3 - moderate exercise 3–5 days a week \
                \n4 - hard exercises 6–7 days a week \
                \n5 - physically demanding job or particularly challenging exercise routine'
message_dict = {'height': 'Input height in cm',
                'weight': 'Input weight in kg',
                'age': 'Input age in full years',
                'gender': 'Input biological gender as w or m',
                'activity': message_activity_level} 

body_params = {}

with st.form(key='my_form_to_submit1'):
    
    period_list = [1, 2, 3, 4, 5]
    col1, col2, col3 = st.columns(3)
    
    with col1:
        body_params['height'] = st.number_input('Input height in cm', min_value=1)

    with col2:
        body_params['weight'] = st.number_input('Input weight in kg', min_value=1)
    
    with col3:
        body_params['age'] = st.number_input('Input age in years', min_value=1)

    body_params['gender'] = st.text_input('Input biological gender as w or m')
    st.markdown('Activity levels:\
                \n1 - little to no exercise \
                \n2 - light exercise 1–3 days a week \
                \n3 - moderate exercise 3–5 days a week \
                \n4 - hard exercises 6–7 days a week \
                \n5 - physically demanding job or particularly challenging exercise routine')
    body_params['activity'] = st.selectbox(label='Select your activity level', options=[1, 2, 3, 4, 5], index=0)
    submit_button1 = st.form_submit_button(label='Submit')



if submit_button1:
    st.write("You entered following body parameters:\n")
    st.write(body_params)
    st.write("You can correct your input by changing it in the corresponding field and pressing Enter")

    bmr, amr = cc.calculate_bmr_amr(body_params)
    st.markdown("Your BMR is") 
    st.write(bmr)
    st.text("Your AMR is")
    st.write(amr)

    with st.form(key='my_form_to_submit2'):
        met_list = pd.read_csv('data/met_list_activities.csv',
                                    sep=';', 
                                    #encoding='ANSI', 
                                    decimal=',', 
                                    error_bad_lines=False)
        nr = 0
        met = 0 
        time = 0
        your_act = ''
        while met == 0:
            your_act = st.text_input('Type in the activity you were doing today:')
            if len(met_list[met_list['SPECIFIC MOTION'].str.contains(your_act)]) >= 1:
                    st.text(met_list[met_list['SPECIFIC MOTION'].str.contains(your_act)])
                    st.text('Select row number of your activity from the list')
                    nr = st.number_input("MET's row number",  min_value=0)
            elif len(met_list[met_list['SPECIFIC MOTION'].str.contains(your_act)]) == 0:
                    st.text('Please type again')
            #elif len(met_list[met_list['SPECIFIC MOTION'].str.contains(your_act)]) == 1:
            #        nr = met_list[met_list['SPECIFIC MOTION'].str.contains(your_act)].index
            met = met_list['METs'].iloc[nr]
            activity = str(met_list['SPECIFIC MOTION'].iloc[nr])

        time = st.number_input('Type in the time of your activity for today in minutes:', min_value=0)
        submit_button2 = st.form_submit_button(label='Calculate')

    if submit_button2:
        burned_cal = met * body_params['weight'] * time/60
        bmr_cal = 1.2 * body_params['weight'] * (24 - time / 60)

        st.text('During your activity you burned following amount of calories:')
        st.write(burned_cal)
        st.text('Your total daily energy expenditure today was:')
        st.write(bmr_cal)