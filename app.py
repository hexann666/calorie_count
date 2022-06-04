from itertools import count
import streamlit as st
import calorie_count.core as cc
import pandas as pd
import requests, json

def get_activity_sum(df):
    """
    Returns a DataFrame with summed time for each activity and number of user, who did it, in the data base.

    Parameters:
        df
        DataFrame with activity information, must contain columns 'activity', 'time'

    Result:
        df_sum
        DataFrame with columns activity, time, number_user 

    """
    import pandas as pd
    
    df_sum = df.groupby('activity').sum()
    c = df.groupby('activity').count()
    df_sum = pd.concat([df_sum, c], axis=1)
    df_sum.columns = ['time', 'number_user']
    df_sum = df_sum.reset_index()
    return df_sum

st.set_page_config(page_title='Calorie count', page_icon='🖖')

st.sidebar.markdown("# Calorie count")
st.sidebar.markdown('First you will provide your **height**, **weight** and **age** and calculate your **Basal Metabolic Rate**, the number of calories required to keep your body functioning at rest.')
st.sidebar.markdown('After choosing your usual level of activity the **Active Metabolic Rate**, the number of calories that we consume on a daily basis depending on our height, gender, age, weight and entered activity level whilst maintaining current weight, will be calculated.')
st.sidebar.markdown('To calculate **daily energy expenditure** type in the activity you were doing today and choose activity from the list. It will determine the Metabolic Equivalent of Task (**MET**). Additionally you will enter the **time** you spent doing this activity.')
st.image('https://raw.githubusercontent.com/hexann666/calorie_count/master/data/image_title_cropped.JPG')

message_activity_level = '1 - little to no exercise \
                \n2 - light exercise 1–3 days a week \
                \n3 - moderate exercise 3–5 days a week \
                \n4 - hard exercises 6–7 days a week \
                \n5 - physically demanding job or particularly challenging exercise routine'

body_params = {}

col1, col2, col3, col4 = st.columns(4)

with col1:
    body_params['height'] = st.number_input('Height in cm', min_value=0)

with col2:
    body_params['weight'] = st.number_input('Weight in kg', min_value=0)
    
with col3:
    body_params['age'] = st.number_input('Age in years', min_value=0)

with col4:
    body_params['gender'] = st.radio(
        "Biological gender",
        ('w', 'm'))
    #body_params['gender'] = st.text_input('Biological gender w/m', max_chars=1)

with st.expander("See activity levels"):
    st.markdown(message_activity_level)

body_params['activity_level'] = st.selectbox(label='Select your activity level', 
                            options=[1, 2, 3, 4, 5], 
                            index=0,
                            key = 'key1')

st.write("You entered following body parameters. You can correct your input by changing it in the corresponding field and pressing Enter")
df = pd.DataFrame.from_dict(body_params, orient='index', columns=['Your input values'])
st.dataframe(df.astype(str))

if st.button('Calculate bmr'):
    bmr, amr = cc.calculate_bmr_amr(body_params)
    st.write(f"Your BMR is {bmr:.0f}")
    st.write(f"Your AMR is {amr:.0f}")
    st.text('\n')

met_list = pd.read_csv('data/met_list_activities.csv',
                                        sep=';', 
                                        #encoding='ANSI', 
                                        decimal=',', 
                                        error_bad_lines=False)
nr = 0
met = 0 
time = 0
counts = 0
burned_cal, bmr_cal = 0, 0
your_act = '0'

#your_act = st.text_input('Type in the activity you were doing today:')
your_act = st.selectbox(label='Possible activities', 
                        options=list(met_list['SPECIFIC MOTION']), 
                        index=0,
                        key=counts)
counts += 1

if len(met_list[met_list['SPECIFIC MOTION'].str.contains(your_act)]) == 1:
    met = float(met_list[met_list['SPECIFIC MOTION'].str.contains(your_act)]['METs'])

st.write(f'You selected {your_act} with MET of {met}')
time = st.number_input('Type in the time of your activity for today in minutes:', min_value=0)
burned_cal = met * body_params['weight'] * time/60
bmr_cal = 1.2 * body_params['weight'] * (24 - time / 60)
#st.write("DB token", st.secrets["db_token"])
#st.write("DB ID:", st.secrets["db_id"])
if st.button('Calculate'):
    st.write(f'During {time} min of {your_act} you burned {burned_cal:.0f} kcal.')
    st.write(f'Your total daily energy expenditure was {round((burned_cal + bmr_cal), 2):.0f} kcal today')
    body_params['activity'] = your_act
    body_params['time'] = time
    body_params = {str(key): str(value) for key, value in body_params.items()}
    
    # contact Notion API without user interactions

    NS = cc.NotionSync(st.secrets['db_token'], st.secrets['db_id'])
    NS.add_entry(body_params)
    data = NS.query_databases()
    df = cc.extract_data_to_df(data)
    df_sum = cc.get_activity_sum(df)
    df_sum.sort_values(by='time', ascending=False, inplace=True)    
    number = int(df_sum['number_user'][df_sum['activity']==your_act])

    # output for results of data base querying
    if number > 1:
        st.write(f'{number} users of this site were doing {your_act}')
    elif number == 1:
        st.write(f'{number} user of this site was doing {your_act}')
    fig = cc.show_hist(df_sum.head(10))
    st.write(fig)
