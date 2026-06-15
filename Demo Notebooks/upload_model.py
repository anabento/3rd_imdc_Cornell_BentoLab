import os
import pandas as pd
import mosqlient as mosq
from datetime import date
from dotenv import load_dotenv

##########################
## Put the API key here ##
##########################

api_key = ...

# Retrieve API key from Ana's Mosqclimate account.
## Log into https://mosqlimate.org using GH of @anabento.
## Go to "Auth" tab in profile overview.


##################
## Upload model ##
##################

# Function `upload_model` of `mosqlient` deprecated (IMDC 2026)
# Upload model by logging into https://mosqlimate.org with @anabento's GH account and adding a new model

import sys
sys.exit()

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
        commit = "36c4db312b09df8dec4786cb9380617fe68de2e0"
        # load validation experiment data
        forecast = pd.read_csv(f'../data/interim/{ID}.csv', index_col=0)
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