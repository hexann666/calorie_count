# Calorie count

The aim of the project is to build a web application, where users can type in their body parameters and get an estimation of their recommended daily calories intake. In the second step users can provide information about the type of their sport activity and time they were doing it and get a calculation of spent calories during this activity.

## Install

`pip install calorie_count`

## Releases (defined according to the Lab's formal requirements)

### Release 1:

- git repository available on GitLab/Hub
- git structure with readme, docs, tests
- documentation
- unit tests
- docker container
- pip package

### Release 2 (to define)

- Web-Application with Streamlit (Web-UI) (alternatively Flask or FastAPI)*

### Release 3 (to define)

- Webscraper - (get data)
- Data bank ("Datawarehouse") 
- (Optional) Kubernetes (eg. Okteto)
- (Optional) Worfklow in MLops-Stil

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
- the input variables and results shall not be stored after the last result is displayed.
