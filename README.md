# Project goal

Calorie count allows you to estimate your daily average calory demand based on your body parameters, such as weight, height, age, biological gender and average activity level and update this daily depending on your current daily activity to give you information on your actual calorie needs according to your particular daily routine.

# Infractructure

The project documentation will be created with [nbdev](https://nbdev.fast.ai/).

## Technical Requirements

The app consists of two parts: calculating bmr and calculating spent calories depending on the activity.

**Count bmr**
- The user should input her body parameters: weight, height, age, biological gender.
- The user can not enter any other format than integer for weight, height, age and only two expressions for biological gender: 'w' and 'm'. If other is provedid, ssystem must show an error and abort process.
- The user should input the level of her activities as one of 5 expressions from 1 to 5. If any other input is provided system must show an error and abort the process.
- If input parameters are provided in the correct format, the system must calculate the bmr using provided input parameters.
- The system must show the user the result of calculations.

**Calculating spent calories**
- The user should choose one activity type from the list in the app: 
  - user provides a search term; 
  - if the term is not matched in the names of activities, ask the user to rephrase search term; 
  - if the term is matched and has more than one search results, system must show the matches to user 
  - the user must choose one by typing in the id number of selected activity
- The user must enter the length of her activity in minutes. Input can not be in any other format than integer.
- The system must calculate the spent calories.
- The system must show the user the result of calculations.

## Previewing Documents Locally 

It is often desirable to preview nbdev generated documentation locally before having it built and rendered by GitHub Pages.  This requires you to run Jekyll locally, which requires installing Ruby and Jekyll. Instructions on how to install Jekyll are provided [on Jekyll's site](https://jekyllrb.com/). You can run the command `make docs_serve` from the root of your repo to serve the documentation locally after calling `nbdev_build_docs` to generate the docs. 

In order to allow you to run Jekyll locally this project contains manifest files, called Gem files, that specify all Ruby dependencies for Jekyll & nbdev. **If you do not plan to preview documentation locally**, you can choose to delete `docs/Gemfile` and `docs/Gemfile.lock` from your nbdev project (for example, after creating a new repo from this template). 
