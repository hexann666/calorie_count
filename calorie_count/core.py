# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['setup_logger', 'logger', 'input_body_parameters', 'calculate_bmr_amr', 'calculate_burned_calories']

# Cell

#export
def setup_logger(loggerName='calorie_count_logger', logFile='log/calorie_count.log'):
    """
    Returns a logger with the specified name or "calorie_count_logger", if loggerName is None.
    Generated logs will be stored in the specified file or in log/calorie_count.log, if logFile is None


    Parameters:

        loggerName: string
        a name for logger, that is used in getLogger

        logFile: string
        file name, where logs are stored

    Return:

        logger
        logger used in the calorie_count functions


    logger = logging.getLogger(loggerName)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(logFile)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y/%m/%d %I:%M:%S')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
    """
logger = setup_logger()


# Cell
def input_body_parameters():
    """
    returns a dictionary with user input of body parameters: height, weight, age, gender and activity level

    Raises:

        AssertError: if inputs of type int are negative

        AssertError: if inputs of type string are not 'w' or 'm'

    Return:

        dict
        a dictionary with body parameters as keys and their values as values
    """
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

    input_values = [170, 56, 41,'m', 1]
    body_params = {}
    n = range(len(message_dict))
    zipped = zip(message_dict.keys(), n)
    assert len(input_values) == len(message_dict)
    for param, nr in zipped:
        if param =='gender':
            try:
                body_params[param] = input(message_dict[param])
            except:
                body_params[param] = input_values[nr]
            assert body_params[param] == 'w' or body_params[param] == 'm', 'gender value should be w or m'
        else:
            try:
                body_params[param] = int(input(message_dict[param]))
            except:
                body_params[param] = input_values[nr]
            assert body_params[param] > 0, 'Please provide a positive value'

        body_params[param] = body_params[param]

        print(f'Your {param} is {body_params[param]}')
    #logger.info('user input complete')
    return body_params


def calculate_bmr_amr(body_parameters):
    """
    returns basal metabolic rate (bmr) and active metabolic rate (amr)

    Parameters:

        body_parameters: dict
        dictionary with body parameters as keys and their values as values

    Returns:

        float
        basal metabolic rate (bmr)

        float
        active metabolic rate (amr)
    """
    dict_activity = {1:1.2, 2:1.37, 3:1.55, 4:1.725, 6:1.9}

    if body_parameters['gender'] == 'w':
        bmr = float(655.1 + (9.563 * body_parameters['weight']) +
            (1.850 * body_parameters['height']) -
            (4.676 * body_parameters['age']))
    else:
        bmr = float(66.47 + (13.75 * body_parameters['weight']) +
            (5.003 * body_parameters['height']) -
            (6.755 * body_parameters['age']))

    amr = bmr * dict_activity[body_parameters['activity']]
    #logger.info('calculate_bmr_amr complete')
    print(f'\nYour BMR is {bmr:.1f}')
    print(f'To stay at your current weight you need to consume {amr:.0f} calories')
    return bmr, amr


def calculate_burned_calories(body_parameters):
    """
    Returns the amount of calories burned during activity and during the day apart of activity.

    To calculate calories for specific activity its MET value is chosen from the table.
    To assign MET user should type in the name of her activity for the search.
    If user doesn't provide this information, activity is considered to be standing and light effort with MET of 1.4
    Calories burned during rest of the day are calculated with standard MET of 1.2.

    Parameters:

        body_parameters: dict
        dictionary with body parameters as keys and their values as values

    Returns:

        float
        amount of calories burned during activity

        float
        amount of calories burned during the day apart of activity
    """
    import pandas as pd

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
        try:
            your_act = input('Type in the activity you were doing today:')
        except:
            your_act = 'standing, light effort tasks'
        # cheking, if the typed activity is in the list of activities
        if len(met_list[met_list['SPECIFIC MOTION'].str.contains(your_act)]) > 1:
            print('\n', met_list[met_list['SPECIFIC MOTION'].str.contains(your_act)])
            try:
                nr = int(input('\nSelect MET of your activity from the list'))
            except:
                nr = 176
        elif len(met_list[met_list['SPECIFIC MOTION'].str.contains(your_act)]) == 0:
            print('Please type again')
        elif len(met_list[met_list['SPECIFIC MOTION'].str.contains(your_act)]) == 1:
            nr = met_list[met_list['SPECIFIC MOTION'].str.contains(your_act)].index
        met = float(met_list['METs'].iloc[nr])
        activity = str(met_list['SPECIFIC MOTION'].iloc[nr])
    try:
        time = int(input('Type in the time of your activity for today in minutes:'))
    except:
        time = 30

    burned_cal = met * body_parameters['weight'] * time/60
    bmr_cal = 1.2 * body_parameters['weight'] * (24 - time / 60)
    #logger.info('calculate_burned_calories complete')
    print(f'\nDuring {time} min of {activity} you burned {burned_cal:.0f} kcal.')
    print(f'Your total daily energy expenditure was {round((burned_cal + bmr_cal), 2):.0f} kcal today')
    return burned_cal, bmr_cal