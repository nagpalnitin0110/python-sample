import numpy as np
import pandas as pd
import sys
import os
import joblib
#import json_format
from flask import Flask, request, jsonify

app = Flask(__name__)

json_data = { 
    "input": {
        "PARAMAPPLICATIONID": 1,
        "locresipincodematch": 1,
        "lockycflag": 1,
        "locwriteoffsuitfilenpa": 0,
        "locmobilematch": 1,
        "lochighestcdloan6m": 10000,
        "lochighestautoloan6m": 10000,
        "lochighesttwloan6m": 10000,
        "lochighestlivecclimit12m": 10000,
        "loctotalalamount": 10000,
        "lochighestplloan12m": 10000,
        "locccbalanceliveamount": 10000,
        "loctotalglamount": 10000,
        "loctotallaphlamount": 10000,
        "loctotalodamount": 10000,
        "loctotalplamount": 10000,
        "loctotalotherloanamount": 10000,
        "loctotaltwloanamount": 10000,
        "lococcupation": "SALARIED",
        "locdob": "1993-02-14",
        "locresipincode": 600089,
        "locnationality": "INDIAN",
        "lociblplccwriteoffsettledsuitfile": 0,
        "locwrittenofftradeslast3y": 0,
        "locwrittenoffamt75k": 0,
        "locpmhcurrentbal25k": [
            "014026000000000000000",
            "015016000000000000000"
        ],
        "locpmhcurrentbal10k": [
            "024006000000000000000",
            "025018000000000000000"
        ],
        "loccibilscore": 790,
        "locwrittenoff10k": 0,
        "loccibilvintage": "2014-02-01",
        "locsecureoverdue": 1000,
        "locunsecureoverdue": 1000,
        "locmlriskscore": 700,
        "loceligibilitybureauliveemigv": 2500,
        "locbureaueligibleloanamountgv": 50000,
        "locunsecuredoutstanding": 1000,
        "lochighesthlclosedloan12m": 10000,
        "locpmhwithin6m": [
            "000000000000090091",
            "000000000000035065"
        ]
    },
    "aliasName": "ibllocpolicy_ibllocrf",
    "type": "POLICY",
    "version": "1.0",
    "paramCPID": 1
}

# 1. IBL saving relationship with minimum EPH (EMI live) of 15K
##### score: ML-Score
##### data['EMI']>15000
def loc_Lac_EMI(score, EMI, C_Score):
###### EMI Cutoff COnditions
    if EMI>15000:
###### check first for ML_Score Condition        
        if score>831:
            if C_Score > 770:
                amount = 8*EMI
                if amount>500000:
                    amount=500000
                else:
                    amount=amount
            else:
                if C_Score > 750:
                    amount = 6*EMI
                    if amount>400000:
                        amount=400000
                    else:
                        amount=amount
                else:
                    if C_Score > 725:
                        amount = 4*EMI
                        if amount>350000:
                            amount=350000
                        else:
                            amount=amount
                    else:
                        if C_Score > 680:
                            amount = 2.5*EMI
                            if amount>250000:
                                amount=250000
                            else:
                                amount=amount
                        else:
                            amount = 0

        else:
            if C_Score > 770:
                amount = 8*EMI
                if amount>450000:
                    amount=450000
                else:
                    amount=amount
            else:
                if C_Score > 750:
                    amount = 6*EMI
                    if amount>350000:
                        amount=350000
                    else:
                        amount=amount
                else:
                    if C_Score > 725:
                        amount = 4*EMI
                        if amount>300000:
                            amount=300000
                        else:
                            amount=amount
                    else:
                        if C_Score> 680:
                            amount = 2.5*EMI
                            if amount>200000:
                                amount=200000
                            else:
                                amount=amount
                        else:
                            amount = 0
    else:
        amount=0
    return amount
                
                
### 2. Basis Live credit card with MOB >= 12 M
##### score: ML-Score
##### Credit Limit
def loc_Lac_CC(score, Credit_Limit):
###### First check for ML-Score    
    if score>831:
        if Credit_Limit > 150000:
            amount = 2.5*Credit_Limit
            if amount>500000:
                amount=500000
            else:
                amount=amount
        else:
            if Credit_Limit > 125000:
                amount = 2.5*Credit_Limit
                if amount>375000:
                    amount=375000
                else:
                    amount=amount
            else:
                if Credit_Limit > 100000:
                    amount = 2.5*Credit_Limit
                    if amount>300000:
                        amount=300000
                    else:
                        amount=amount
                else:
                    if Credit_Limit > 75000:
                        amount = 2*Credit_Limit
                        if amount>200000:
                            amount=200000
                        else:
                            amount=amount
                    else:
                        if Credit_Limit > 50000:
                            amount = 1.5*Credit_Limit
                            if amount>120000:
                                amount=120000
                            else:
                                amount=amount
                        else:
                            if Credit_Limit > 30000:
                                amount = 1*Credit_Limit
                                if amount>50000:
                                    amount=50000
                                else:
                                    amount=amount
                            else:
                                amount=0                                                                
    else:
        if Credit_Limit > 150000:
                amount = 2.25*Credit_Limit
                if amount>500000:
                    amount=500000
                else:
                    amount=amount
        else:
            if Credit_Limit > 125000:
                    amount = 2.25*Credit_Limit
                    if amount>350000:
                        amount=350000
                    else:
                        amount=amount
            else:
                if Credit_Limit > 100000:
                        amount = 2*Credit_Limit
                        if amount>250000:
                            amount=250000
                        else:
                            amount=amount
                else:
                    if Credit_Limit > 75000:
                            amount = 1.5*Credit_Limit
                            if amount>150000:
                                amount=150000
                            else:
                                amount=amount
                    else:
                        if Credit_Limit > 50000:
                                amount = 1.2*Credit_Limit
                                if amount>90000:
                                    amount=90000
                                else:
                                    amount=amount
                        else:
                            if Credit_Limit > 30000:
                                    amount = Credit_Limit
                                    if amount>50000:
                                        amount=50000
                                    else:
                                        amount=amount
                            else:
                                    amount=0
            
    return amount
                            
                            
                            
#### 3. Basis Closed Home Loan with minimum 12 month vintage
#### Score: Ml-Score
#### HL Loan Amount
def loc_Lac_HL(score, loan_amount):
##### Check First ML-Score    
    if score>831:
        if loan_amount > 10000000:
            amount = 500000
        else:
            if loan_amount > 7500000:
                amount = 450000
            else:
                if loan_amount > 4000000:
                    amount = 350000
                else:
                    if  loan_amount > 2500000:
                        amount = 250000
                    else:
                        amount = 0
                                         
    else:
        if loan_amount > 10000000:
            amount = 400000
        else:
            if loan_amount > 7500000:
                amount = 400000
            else:
                if loan_amount > 4000000:
                    amount = 300000
                else:
                    if  loan_amount > 2500000:
                        amount = 200000
                    else:
                        amount = 0
        
    return amount

##### 4. Proposed basis Personal Loan with minimum 12 months vintage
#### Personal Loan Amount > 2 Lakh
##### score: Ml-Score; C_Score: CIBIL
def loc_Lac_PL(score, loan_amount, C_Score):    
##### Check First ML-Score    
    if score >831:
        if C_Score > 750:
                amount = 0.6*loan_amount
                if amount>400000:
                    amount=400000
                else:
                    amount=amount
        else:
            if C_Score > 680:
                amount = 0.6*loan_amount
                if amount>350000:
                        amount=350000
                else:
                        amount=amount     
            else:
                amount = 0
                                         
    else:
        if C_Score > 750:
                amount = 0.5*loan_amount
                if amount>350000:
                    amount=350000
                else:
                    amount=amount
        else:
            if C_Score > 680:
                amount = 0.5*loan_amount
                if amount>300000:
                    amount=300000
                else:
                    amount=amount     
            else:
                amount = 0
        
    return amount
                
##### 5.Customers having an auto loan (Live/closed) on bureau with minimum 6 months vintage
##### Car Loan Amount
##### score ML-Score
def loc_Lac_auto(score, loan_amount):
    
    if score>831:
        if loan_amount > 500000:
            amount = 250000
        else:
            if loan_amount > 400000:
                amount = 150000
            else:
                if loan_amount > 300000:
                    amount = 110000
                else:
                    if  loan_amount > 200000:
                        amount = 75000
                    else:
                        if loan_amount > 150000:
                            amount = 60000
                        else:
                            amount = 0
                                         
    else:
        if loan_amount > 500000:
            amount = 200000
        else:
            if loan_amount > 400000:
                amount = 100000
            else:
                if loan_amount > 300000:
                    amount = 75000
                else:
                    if  loan_amount > 200000:
                        amount = 50000
                    else:
                        if loan_amount > 150000:
                            amount = 40000
                        else:
                            amount = 0
    return amount
                
                
                
##### 6. Customers having a 2-wheeler loan (Live/closed) on bureau with minimum 6 months vintage
### Two wheeler loans
##### Score Ml-Score
def loc_Lac_tw(score, loan_amount):
    
    if score>831:
        if loan_amount > 50000:
            amount = 0.6*loan_amount
        else:
            if loan_amount> 40000:
                amount = 30000
            else:
                amount = 0
                
    else:
        
        if loan_amount > 50000:
            amount = 0.75*loan_amount
        else:
            if loan_amount > 40000:
                amount = 35000
            else:
                amount = 0
    return amount
                
                
##### 7. Customers having a CD loan (Live/closed) on bureau with minimum 6 months vintage
### CD loan amount
##### Score Ml-Score
def loc_Lac_CD(loan_amount):
    ### No need to check the ML-Score
    if loan_amount > 50000:
            amount = 0.6*loan_amount
    else:
        if loan_amount > 40000:
            amount = 30000
        else:
            amount = 0
    return amount
    
#### Pins Sourcing or not sourcing
#### Sourcing Locations
#### Score ML-Score
def loc_Lac_Pin(score, flag):
    ### Check for ML-Score
    if score<686:
        if flag==1:
            amount = 500000
        else:
            amount = 300000
    else:
        amount= 500000
    return amount  
    
#### KYC Sourcing or not sourcing
#### KYC Status
#### Score ML-Score
def loc_Lac_KYC(score, status, mob_match, pin_match):
    ### Check for ML-Score
    if score<686:
        if status==1:
            if mob_match==1 | pin_match==1:
                amount = 500000
            else:
                amount = 50000
        else:
            if mob_match==1 | pin_match==1:
                amount = 60000
            else:
                amount = 50000
    else:
        if status==1:
            amount= 500000
        else:
            amount=60000
    return amount  

df = pd.DataFrame.from_dict(json_data["input"], orient='index').T
print(df)    

def global_Indie(i_data):
    global loc_Lac_EMI
    global loc_Lac_CC
    global loc_Lac_HL
    global loc_Lac_PL
    global loc_Lac_auto
    global loc_Lac_tw
    global loc_Lac_CD
    global loc_Lac_Pin
    global loc_Lac_KYC 
    global df
    import os
    import sys
    import json
    import pandas as pd
    from datetime import datetime, date
    import numpy as np
    from datetime import datetime, timedelta
    import time
    from dateutil import relativedelta
    from functools import reduce
    import flask
    import scipy
    #from PinCodes_List import *;
    from PinCodes_List import Pin_list
            
    import warnings
    warnings.filterwarnings("ignore")
        
    json_data = i_data
    ####### Create DataFrame
    df = pd.DataFrame.from_dict(json_data["input"], orient='index').T
    
    df['locpmhwithin6m'] = df['locpmhwithin6m'].astype(str)
    df['locpmhcurrentbal10k'] = df['locpmhcurrentbal10k'].astype(str)
    df['locpmhcurrentbal25k'] = df['locpmhcurrentbal25k'].astype(str)
    df['locpmhwithin6m'] = df['locpmhwithin6m'].str.strip('[]')
    df['locpmhcurrentbal10k'] = df['locpmhcurrentbal10k'].str.strip('[]')
    df['locpmhcurrentbal25k'] = df['locpmhcurrentbal25k'].str.strip('[]')
    ####
    df['locpmhwithin6m'] = df['locpmhwithin6m'].str.replace(',', '').str.replace('(', '').str.replace(')', '')
    df['locpmhwithin6m'] = df['locpmhwithin6m'].str.replace(',', '').str.replace("'", "")
    ####
    df['locpmhcurrentbal10k'] = df['locpmhcurrentbal10k'].str.replace(',', '').str.replace('(', '').str.replace(')', '')
    df['locpmhcurrentbal10k'] = df['locpmhcurrentbal10k'].str.replace(',', '').str.replace("'", "")
    ####
    df['locpmhcurrentbal25k'] = df['locpmhcurrentbal25k'].str.replace(',', '').str.replace('(', '').str.replace(')', '')
    df['locpmhcurrentbal25k'] = df['locpmhcurrentbal25k'].str.replace(',', '').str.replace("'", "")
    
    
    ##### DPD Modification Functiontemp = '000'
    #------------------------------------------------------------------------------------------------------------------------------
    def dpd_modification(dpd_string, reported_reference_date_difference):
        temp='000'

        if reported_reference_date_difference < 0:
            dpd_string = dpd_string[3:] + str(temp)
            dpd_string = str(dpd_string).strip().upper()
            dpd_string = dpd_string.replace("STD", "000")
            dpd_string = dpd_string.replace("XXX", "000")
            dpd_string = dpd_string.replace("SUB", "091")
            dpd_string = dpd_string.replace("DBT", "091")
            dpd_string = dpd_string.replace("SMA", "061")
            dpd_string = dpd_string.replace("LSS", "091")
            
        if reported_reference_date_difference != 0:
            latest_dpd = '000'
        for i in range(0, reported_reference_date_difference):
            dpd_string = str(latest_dpd) + str(dpd_string)
        # add trailing zeroes to dpd if in case its length is < 108 (3years/36months)
        current_dpd_string_len = len(dpd_string)
        if current_dpd_string_len < 108:
            difference_in_dpd_string_len = 108 - current_dpd_string_len
            final_dpd_string = dpd_string.ljust(difference_in_dpd_string_len + len(dpd_string), '0')
            final_dpd_string = final_dpd_string[0:108]
        else:
            final_dpd_string = dpd_string[0:108]

        return final_dpd_string


    #-----------------------------------------------------------------------------------------------------------------------------
    # method for extracting features from dpd_string
    #-----------------------------------------------------------------------------------------------------------------------------
    def extract_dpd_features(dpd_string):
        dpd_string = str(dpd_string).strip().upper()
        ls = []
        for i in range(0, 108, 3):
            temp = dpd_string[i: i+3]
            if temp == 'XXA':
                temp = "000"
            if temp == "STD":
                temp = "000"
            if temp == "SUB":
                temp = "091"
            if temp == "DBT":
                temp = "091"
            if temp == "SMA":
                temp = "061"
            if temp == "LSS":
                temp = "091"
            if temp == "901":
                temp = "000"
            if temp == "902":
                temp = "091"
            if temp == "903":
                temp = "091"
            if temp == "904":
                temp = "091"
            if temp == "905":
                temp = "061"
            if temp  =="1XX":
                temp = "000"
            temp = temp.strip()
            temp = temp.replace(",", "")
            ls.append(int(temp))

        return ls


    #-----------------------------------------------------------------------------------------------------------------------------
    # function for getting max dpd over a range
    #-----------------------------------------------------------------------------------------------------------------------------
    def get_max_dpd_in_range(dpd_feature, lower_range, upper_range, k,n):
        dpd_feature = dpd_feature[lower_range:upper_range]
        return max(dpd_feature)

    #-----------------------------------------------------------------------------------------------------------------------------
    #function for getting list of gt30 dpd in last [n] months
    #-----------------------------------------------------------------------------------------------------------------------------
    def get_gt30_dpd_in_range(dpd_feature, lower_range, upper_range, k,n):
        dpd_feature = dpd_feature[lower_range:upper_range]
        dpd_feature1 = []
        for i in range(n):
            if dpd_feature[i]>k:
                dpd_feature1.append(1)
            else:
                dpd_feature1.append(0)
                
        return dpd_feature1
    #-----------------------------------------------------------------------------------------------------------------------------
    ## Function for DPD Count
    def get_dpd_count(column):
        dpd_cnt = sum(column)
        return dpd_cnt

    #-----------------------------------------------------------------------------------------------------------------------------
    #### Max DPD reported in [n] months
    #----------------------------------------------------------------------------------------------------------------------------
    def temp_list(Df, column1, column2, k, n):   
        for i in [n]:
            Df['list_DPD>'+str(k)+'_in_last_'+str(i)+'_m'] = Df[column1].apply(lambda x: get_gt30_dpd_in_range(x, 0, i, k, n))
            temp = Df.groupby(column2,as_index=False).agg({'list_DPD>'+str(k)+'_in_last_'+str(i)+'_m':'max'})
            temp.columns = [column2,'list_DPD>'+str(k)+'_in_last_'+str(i)+'_m']
        print(temp.shape)
        temp['Count_DPD>'+str(k)+'_in_last_'+str(i)+'_m'] = temp['list_DPD>'+str(k)+'_in_last_'+str(i)+'_m'].apply(lambda x: get_dpd_count(x))
        return temp
        #temp['Count_DPD>'+str(k)+'_in_last_'+str(i)+'_m'] = sum(temp[list_DPD>'+str(k)+'_in_last_'+str(i)+'_m'])


    df1 = df[['PARAMAPPLICATIONID', 'locpmhwithin6m']]
    df2 = df[['PARAMAPPLICATIONID', 'locpmhcurrentbal10k']]
    df3 = df[['PARAMAPPLICATIONID','locpmhcurrentbal25k']]


    df1.dropna(subset=['locpmhwithin6m'], how='all', inplace=True)
    df2.dropna(subset=['locpmhcurrentbal10k'], how='all', inplace=True)
    df3.dropna(subset=['locpmhcurrentbal25k'], how='all', inplace=True)
    df1.shape, df2.shape, df3.shape

    df1=df1.assign(locpmhwithin6m=df1['locpmhwithin6m'].str.split(',')).explode('locpmhwithin6m')
    df2=df2.assign(locpmhcurrentbal10k=df2['locpmhcurrentbal10k'].str.split(',')).explode('locpmhcurrentbal10k')
    df3=df3.assign(locpmhcurrentbal25k=df3['locpmhcurrentbal25k'].str.split(',')).explode('locpmhcurrentbal25k')

    today = date.today()
    #### Age Calculation Function
    import math
    def calculate_age(row):
        if row['locdob'] == 0 or row['locdob'] == '0':
            return 0
        else:
            born = datetime.strptime(row['locdob'], "%Y-%m-%d").date()
            return (today.year - born.year - ((today.month,
                                              today.day) < (born.month,
                                                            born.day)))
                                                            
                                                            
    df['loc_age'] = df.apply(lambda row : calculate_age(row), axis = 1)

    def calculate_cibil_Vintage_month(row):
        if row['loccibilvintage'] == 0 or row['loccibilvintage'] == '0':
            return 0
        else:
            # convert string to date object
            start_date = datetime.strptime(row['loccibilvintage'], "%Y-%m-%d")
            end_date = datetime.strptime(str(today), "%Y-%m-%d")

            # Get the relativedelta between two dates
            delta = relativedelta.relativedelta(end_date, start_date)
            numberOfMonth = delta.years*12+delta.months
            #print(numberOfMonth)
            return (numberOfMonth)
    df.fillna(0,inplace=True)
    df['loccibilvintagemonthsgv'] = df.apply(lambda row : calculate_cibil_Vintage_month(row), axis = 1)
    def locagerule(row):
        occ = row['lococcupation']  ;
        age = row['loc_age'];
        if(occ == 0):
            return 0
        else:
            if (( occ.upper() == 'SALARIED') and  (( age  <  21 )  or  (  age > 65))):
                return 0
            elif ((( occ.upper() == 'SELF EMPLOYED PROFESSIONAL')) and (( age <  21)  or  ( age > 60))):
                return 0
            else:
                return 1
                
                
    ### Age Rule calculation function
    def locagerule(row):
        occ = row['lococcupation']  ;
        age = row['loc_age'];
        if(occ == 0):
            return 0
        else:
            if (( occ.upper() == 'SALARIED') and  (( age  <  21 )  or  (  age > 65))):
                return 0
            elif ((( occ.upper() == 'SELF EMPLOYED PROFESSIONAL')) and (( age <  21)  or  ( age > 60))):
                return 0
            else:
                return 1
                
    def lociblplccwriteoffsettledsuitfilerule(row):
        if (row['lociblplccwriteoffsettledsuitfile'] > 0) :
            return 0
        else:
            return 1

    #### Nationality Rule
    def locnationalityrule(row):
        if(row['locnationality'] ==0):
            return 0
        else: 
            if (row['locnationality'].upper() == 'INDIAN' or row['locnationality'].upper() == 'INDIA'):
                return 1
            else:
                return 0
                
    def locresiormobmatchrule(row):
        ML =  row['locmlriskscore'] 
        MOB =  row['locmobilematch']
        PIN =  row['locresipincodematch']
        if(ML <=686 and (MOB == 1 or PIN == 1)):
            return 1
        elif( ML >686):
            return 1
        else:
            return 0
    def locwrittenofftradeslast3yrule(row):
        if (row['locwrittenofftradeslast3y'] > 0):
            return 0
        else:
            return 1
    def locwrittenoffamt75krule(row):
        if (row['locwrittenoffamt75k'] > 0):
            return 0
        else:
            return 1
            
    ### locpmhwithin6m
    df1['locpmhwithin6m1'] = df1.apply(lambda x: dpd_modification(x.locpmhwithin6m, 0), axis=1)
    del df1['locpmhwithin6m']
    #df1.head(5)

    #### Creating 'dpd_features' Variable for df1[locpmhwithin6m]
    df1['dpd_feat_locpmhwithin6m1'] = df1['locpmhwithin6m1'].apply(lambda x: extract_dpd_features(x))
    df4=temp_list(df1, 'dpd_feat_locpmhwithin6m1', 'PARAMAPPLICATIONID', 60, 6)
    df4=df4.rename(columns={'list_DPD>60_in_last_6_m': 'list_DPD>60_locpmhwithin6m', 'Count_DPD>60_in_last_6_m': 'Count_DPD>60_locpmhwithin6m'}) 
    df5=temp_list(df1, 'dpd_feat_locpmhwithin6m1', 'PARAMAPPLICATIONID', 30, 6)
    df5=df5.rename(columns={'list_DPD>30_in_last_6_m': 'list_DPD>30_locpmhwithin6m', 'Count_DPD>30_in_last_6_m': 'Count_DPD>30_locpmhwithin6m'}) 
    ### locpmhcurrentbal10k
    df2['locpmhcurrentbal10k1'] = df2.apply(lambda x: dpd_modification(x.locpmhcurrentbal10k, 0), axis=1)
    del df2['locpmhcurrentbal10k']
    #df2.head(5)
    #### Creating 'dpd_features' Variable for df1[locpmhwithin6m]
    df2['dpd_feat_locpmhcurrentbal10k1'] = df2['locpmhcurrentbal10k1'].apply(lambda x: extract_dpd_features(x))
    df8=temp_list(df2, 'dpd_feat_locpmhcurrentbal10k1', 'PARAMAPPLICATIONID', 90, 6)
    df8=df8.rename(columns={'list_DPD>90_in_last_6_m': 'list_DPD>90_locpmhcurrentbal10k', 'Count_DPD>90_in_last_6_m': 'Count_DPD>90_locpmhcurrentbal10k'})
    ### locpmhcurrentbal25k
    df3['locpmhcurrentbal25k1'] = df3.apply(lambda x: dpd_modification(x.locpmhcurrentbal25k, 0), axis=1)
    del df3['locpmhcurrentbal25k']
    #df3.head(5)
    #### Creating 'dpd_features' Variable for df1[locpmhwithin6m]
    df3['dpd_feat_locpmhcurrentbal25k1'] = df3['locpmhcurrentbal25k1'].apply(lambda x: extract_dpd_features(x))
    df9=temp_list(df3, 'dpd_feat_locpmhcurrentbal25k1', 'PARAMAPPLICATIONID', 90, 6)
    df9=df9.rename(columns={'list_DPD>90_in_last_6_m': 'list_DPD>90_locpmhcurrentbal25k', 'Count_DPD>90_in_last_6_m': 'Count_DPD>90_locpmhcurrentbal25k'})
    ### Validated-- Complete Rule
    ##df3[df3['App Id']==50024]
    dfs = [df, df4, df5,df8,df9]
    nan_value = 0
    DataFrame = reduce(lambda left, right: pd.merge(left, right, 
                                                  on='PARAMAPPLICATIONID',
                                                  how='left'), 
                      dfs).fillna(nan_value)

    def locminimumcibilscorerule(row):
        if (row['loccibilscore']  >=  680  ):
            return 1
        else:
            return 0
    def loccibilvintagerule(row):
        if (row['loccibilvintagemonthsgv']    <  12 ):
            return 0
        else:
            return 1
            
    def locsecuredoverduerule(row):
        if ( row['locsecureoverdue'] > 20000):
            return 0
        else:
            return 1
            
    def locunsecuredoverduerule(row):
        if ( row['locunsecureoverdue']  >  5000 ):
            return 0
        else:
            return 1
            
    def locunsecuredoutstandingrule(row):
        if ( row['locunsecuredoutstanding']  >  2000000 ):
            return 0
        else:
            return 1
    def locwriteoffsuitfilenparule(row):
        if (row['locwriteoffsuitfilenpa'] > 0):
                return 0
        else:
            return 1
            
    def locriskscorerule(row):
        if( row['locmlriskscoregv'] >= 417 ):
            return 1
        else:
            return 0
            
    def locdpd90plus25krule(row):
        if row['Count_DPD>90_locpmhcurrentbal25k'] > 0:
            return 0
        else:
            return 1
        
    def locscore650dpd90plus10krule(row):
        if (((row['loccibilscore']  <=  650) and (row['locwrittenofftradeslast3y']>0)) or ( row['Count_DPD>90_locpmhcurrentbal10k'] > 0)):
            return 0
        else:
            return 1
            
    def loc_boundary_rg(row):
        if locagerule(row) == 1:
            if locnationalityrule(row) == 1:
                if lociblplccwriteoffsettledsuitfilerule(row) == 1:
                    if locresiormobmatchrule(row) == 1:
                        return 1
                    else:
                        return "Failed at locresiormobmatchrule"
                else:
                    return "failed at lociblplccwriteoffsettledsuitfilerule"
            else:
                return "Failed at locnationalityrule"
        else:
            return "Failed at locagerule"

    def loc_cibil_black_rule_rg(row):
        if locwrittenofftradeslast3yrule(row) == 1:
            if locwrittenoffamt75krule(row) == 1 :
                if locdpd90plus25krule(row) == 1 :
                    if locscore650dpd90plus10krule(row) == 1:
                        return 1
                    else:
                        return "Failed at locscore650dpd90plus10krule"
                else:
                    return "Failed at locdpd90plus25krule"
            else:
                return "Failed at locwrittenoffamt75krule"
        else:
            return "Failed at locwrittenofftradeslast3yrule"

    #### New Rule
    def locdpd60or30plusin18mrule(row):
        if ( row['Count_DPD>60_locpmhwithin6m']  >  0 or row['Count_DPD>30_locpmhwithin6m'] >=2 ):
            return 0
        else:
            return 1
            
    def loc_cibil_profile_rg(row):
        if( locminimumcibilscorerule(row) == 1 and loccibilvintagerule(row) == 1 and locsecuredoverduerule(row) == 1 and locunsecuredoverduerule(row) == 1 and locunsecuredoutstandingrule(row) == 1 and locdpd60or30plusin18mrule(row) == 1 and locwriteoffsuitfilenparule(row) == 1):
            return 1
        else:
            return 0
        
    #locriskscorerule is there but locmlriskscorerule rule is not there, check it and replace
    def loc_risk_score_rg(row):
        if(locriskscorerule(row)  == 1):  
            return 1
        else:
            return 0
    def Loc_IBL_test(row):
        if(loc_boundary_rg(row)==1):
            if(loc_cibil_black_rule_rg(row)==1):
                if(loc_cibil_profile_rg(row)==1):
                    if(loc_risk_score_rg(row)==1):
                        return "Passed"
                    else:
                        return "Failed at loc_risk_score_rg"
                else:
                    return "Failed at loc_cibil_profile_rg"
            else:
                return "Failed at loc_cibil_black_rule_rg "+ (loc_cibil_black_rule_rg(row))
        else:
            return "Failed at loc_boundary_rg " + (loc_boundary_rg(row))
    
    DataFrame['Test_Results'] = DataFrame.apply(lambda row : Loc_IBL_test(row), axis = 1)
    DataFrame['locresipincode']=DataFrame['locresipincode'].fillna(0)
    DataFrame['locresipincode']=DataFrame['locresipincode'].astype('int64')
    DataFrame['locresipincode'].unique()

    DataFrame['Pin_flag'] = np.where(DataFrame['locresipincode'].isin(Pin_list),1,0)
    DataFrame['Pin_flag'].value_counts()

    DataFrame['locmlriskscore']=DataFrame['locmlriskscore'].astype(int)
    DataFrame['Amount_pin'] = DataFrame.apply(lambda x : loc_Lac_Pin(x.locmlriskscore, x.Pin_flag), axis=1)
    DataFrame['Amount_KYC'] = DataFrame.apply(lambda x : loc_Lac_KYC(x.locmlriskscore, x.lockycflag, x.locmobilematch, x.Pin_flag),  axis=1)

    DataFrame['locmlriskscore']=DataFrame['locmlriskscore'].astype(int)
    DataFrame['Amount_pin'] = DataFrame.apply(lambda x : loc_Lac_Pin(x.locmlriskscore, x.Pin_flag), axis=1)
    DataFrame['Amount_KYC'] = DataFrame.apply(lambda x : loc_Lac_KYC(x.locmlriskscore, x.lockycflag, x.locmobilematch, x.Pin_flag),  axis=1)

    DataFrame['Amount_EMI'] = DataFrame.apply(lambda x : loc_Lac_EMI(x.locmlriskscore, x.loceligibilitybureauliveemigv, x.loccibilscore),  axis=1)
    DataFrame['Amount_CC'] = DataFrame.apply(lambda x : loc_Lac_CC(x.locmlriskscore, x.lochighestlivecclimit12m),  axis=1)
    DataFrame['Amount_HL'] = DataFrame.apply(lambda x : loc_Lac_HL(x.locmlriskscore, x.lochighesthlclosedloan12m),  axis=1)
    DataFrame['Amount_PL'] = DataFrame.apply(lambda x : loc_Lac_PL(x.locmlriskscore, x.lochighestplloan12m, x.loccibilscore),  axis=1)
    DataFrame['Amount_auto'] = DataFrame.apply(lambda x : loc_Lac_auto(x.locmlriskscore, x.lochighestautoloan6m),  axis=1)
    DataFrame['Amount_tw'] = DataFrame.apply(lambda x : loc_Lac_tw(x.locmlriskscore, x.lochighesttwloan6m),  axis=1)
    DataFrame['Amount_CD'] = DataFrame.apply(lambda x : loc_Lac_CD(x.lochighestcdloan6m),  axis=1)

    #### Multimax
    DataFrame["Multi_Max"] = DataFrame[["Amount_EMI", "Amount_HL", "Amount_PL", "Amount_auto", "Amount_tw", "Amount_CD", "Amount_CC"]].max(axis=1)

    DataFrame["Offer"] = DataFrame[["Amount_pin", "Amount_KYC", "Multi_Max"]].min(axis=1)
    DataFrame['locbureaueligibleloanamountgv']=DataFrame['locbureaueligibleloanamountgv'].fillna(0)
    DataFrame['Test_flag'] = np.where(DataFrame['locbureaueligibleloanamountgv']==DataFrame['Offer'],1,0)
    DataFrame['Test_flag'].value_counts()
    data_offer = DataFrame[["PARAMAPPLICATIONID","Test_Results", "locmlriskscore", "loccibilscore", "locbureaueligibleloanamountgv","Amount_pin", "Amount_KYC", "Multi_Max", "Offer"]]
    data_offer=data_offer.fillna(0)
    #data_offer['Pin_flag'] = np.where(data_offer['locsourcinglocelggv']==data['Amount_pin'],1,0)
    #data_offer['Pin_flag'].value_counts()
    #data_offer['KYC_flag'] = np.where(data_offer['lockycresiandmobmatchelggv']==data['Amount_KYC'],1,0)
    #data_offer['Multi_flag'] = np.where(data_offer['loceligibilitymultimaxgv']==data['Multi_Max'],1,0)
   
    return data_offer



#print(global_Indie(json_data))

@app.route('/LOC_APP', methods=['POST'])
def Loc_APP():
    try:
        content = request.json
        uid = content['input']
        X = global_Indie(uid) # pass the input parameter to global_Indie function
        if isinstance(X, dict):
            prediction_json = X
        else:
            result = X['Test_Results']
            input_data = X.to_dict('records')[0]
            amount = X.at[0, 'Offer']
            prediction_json = {"Status": True, "LOC_result": result, "Offer_Amount": str(amount), "Feature_Values": input_data}
    except Exception as e:
        prediction_json = {"Status": False, "Error": str(e)}
    
    return jsonify(prediction_json)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
