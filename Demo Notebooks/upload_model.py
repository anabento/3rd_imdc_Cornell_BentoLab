import os
import pandas as pd
import mosqlient as mosq
from datetime import date
from dotenv import load_dotenv

challenge_year = 2026

##########################
## Put the API key here ##
##########################

api_key = 'anabento:68ff4487-a072-4dda-b45d-a7742cc00cec'

# Retrieve API key from Ana's Mosqclimate account.
## Log into https://mosqlimate.org using GH of @anabento.
## Go to "Auth" tab in profile overview.


##################
## Upload model ##
##################

# Function `upload_model` of `mosqlient` deprecated (IMDC 2026)
# Upload model by logging into https://mosqlimate.org with @anabento's GH account and adding a new model

#####################
## Upload forecast ##
#####################

# define validation experiment indices..
validation_indices = [1, 2, 3, 4] # None (forecast), or [1, 2, 3, 4] (validation)

# validation
if validation_indices:
    # .. and loop over them
    for validx in validation_indices:
        # set correct ID and description
        ID = f"endemic_channel-validation_{validx}"
        description = f"Validation {validx} (Cornell_BentoLab - NegBinom Endemic Channel). Authored by Tijs W. Alleman & Ana I. Bento."
        commit = "49b7a28eecd946e3609d94d2bafe231d74b87070"
        # load validation experiment data
        forecast = pd.read_csv(f'../data/interim/model_output/sprint_{challenge_year}/{ID}.csv', index_col=0)
        # get the ufs..
        ufs = forecast['adm_1'].unique().tolist()
        # ..and loop over them
        for uf in ufs:
            # slice data
            df = forecast[forecast['adm_1'] == uf].reset_index()
            # push the prediction
            res = mosq.upload_prediction(
                api_key = api_key,
                repository = 'https://github.com/anabento/3rd_imdc_Cornell_BentoLab',
                description = description, 
                commit = commit,
                disease = 'A90', # dengue
                case_definition = 'probable',
                adm_level=1,
                adm_1=f'{uf}',
                published = True,
                prediction = df,
                ) 
# forecast
else:
    # TODO: Changed in 2026 challenge
    pass