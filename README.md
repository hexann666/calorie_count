# Calorie count



The aim of the project is to build a web application, where users can type in their body parameters and get an estimation of their recommended daily calories intake. In the second step users can provide information about the type of their sport activity and time they were doing it and get a calculation of spent calories during this activity.

Documentation is available at https://hexann666.github.io/calorie_count/

Online version is available at https://share.streamlit.io/hexann666/calorie_count/app.py

# Install

`pip install calorie_count`

# Run app

`streamlit run app.py`

To run app locally Notion API needs a folder .streamlit in the main calorie_count folder, where a secrets.toml file with secrets db_token and db_id should be stored for connection with Notion API.

If you deploy the app by yourself, you need to input the secrets for Notion API in the app settings to be able to connect with the database. When deploying the streamlit app, go to Advanced settings and type in your secrets with keys db_token and db_id.

## Releases (defined according to the Lab's formal requirements)

### Release 1

- git repository available on GitLab/Hub
- git structure with readme, docs, tests
- documentation
- unit tests
- pip package

### Release 2

- Web-Application with Streamlit (Web-UI)

### Release 3

- Data bank with Notion ("Datawarehouse") 
- docker container

## Technical requirements

- System shall provide input fields for the input parameters (height, weight, age, gender, activity level).
- User should input the body parameters in the order, in which system will request them and confirm that the input is complete.
- System should store the variables provided by user until the end of transaction.
- If all input variables are valid, system should calculate calorie intake recommendation and show it on the screen.
- System shall provide input fields for the activity name and time.
- User should enter her activity name in the field and confirm that the input is complete.
- After the input was confirmed by user, system shall look up the input string in the data base in the column activity_name.
- It there is no search result, system shall show a message 'Please type again', wait for the new input and repeat the serach as soon as the new input is confirmed.
- If there is only one match result, system shall keep the value from the column "METs".
- If there is more than one result, system shall show all results.
- If system provides to user multiple results, she should choose her activity from the provided list and type in the respective number. System should keep the value from the column "METs" for the row number, that was typed in by the user.
- If MET value is saved and body parameters are available from the previous step, system shall calculate the spent calories and total calories for the day.
- If calculation step succeeded, system shall print the result on the screen.
- The input variables and results shall not be stored after the last result is displayed.

## How to use

First you will provide your height, weight and age and calculate your Basal Metabolic Rate, the number of calories required to keep your body functioning at rest.

After choosing your usual level of activity the Active Metabolic Rate, the number of calories that we consume on a daily basis depending on our height, gender, age, weight and entered activity level whilst maintaining current weight, will be calculated. Output of the function should be stored in a variable to pass it to the next function.

Than you will be asked to type in the activity you were doing today. If there are more than one activities matching your input, you will select one from the lst that matches your search pattern. Additionally you will enter the time you were doing this activity.

`import calorie_count.core as cc`

`body_parameters = cc.input_body_parameters()`

`cc.calculate_bmr_amr(body_parameters)`

`cc.calculate_burned_calories(body_parameters)`

**Note**

Pip is doing canonicalization while processing Setup.py to a package and automatically changes dots and underscore to dashes. That's why during installation the name of the package is shown as calorie-count and calorie-count-version-nr, although in all the documentation the name of the package is specified as calorie_count.

**Sources:**

for the formulas:    https://www.verywellfit.com/how-many-calories-do-i-need-each-day-2506873

for the MET values:  https://golf.procon.org/met-values-for-800-activities/
