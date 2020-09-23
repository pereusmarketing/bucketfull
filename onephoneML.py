#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 09:53:40 2020

@author: jeremiahmcleod
"""

#instructions: (do not change layout)
# ML phone number must be separated from ext., if country code other than +1 is used - delete row before importing. 

#1  Specify column names in line #23 as ref for original list.
#2  Change campaign name on line #24. Change filepath line #27
#   Change filepath to write file on line #45
#3  Shift+enter to execute cell. this outputs dnc ready file.

#useable column names
# 'first_name', 'last_name', 'title', 'company', 'address_1', 'phone_number'
# 'alt_phone', 'city', 'state', 'zip', 'country', 'linkedin', 'website', 
# 'phone_number_ext', 'email', 'industry' 'full_name'
#  ColumnNames in exact order appeared on csv:

import pandas as pd
columnNames = ['first_name','last_name','title','phone_number','phone_ext',
               'email','address1', 'city',
               'state','zip']
campaign = 'SHP Past Clients 1'


df = pd.read_csv("/Users/jeremiahmcleod/Desktop/PereusMarketing/SHP_oldie.csv")
df_orig = df
df.reset_index()
df.columns = columnNames
df = df[df['phone_number'].notna()]
df = df.drop_duplicates(['phone_number','first_name','last_name'],keep='last')
#del df['approval']
import re
df['phone_number'] = [re.sub("[^0-9,'']","", str(x)) for x in df['phone_number']]
df['phone_number'] = df['phone_number'].astype(str).astype(str)
df['phone_number'] = [s.lstrip("1") for s in df.phone_number]
df['phone_number'] = df['phone_number'].str[:10]
df['phone_number'] = df['phone_number'].astype(str).astype(int)
df['phone_number'] = df['phone_number'].astype(int).astype(int)
df = df.drop(df[df.phone_number < 1000000000].index)
df['phone_number'] = df['phone_number'].astype(int).astype(int)

#4  Upload this file to dnc for compliance scan
df.to_csv("/Users/jeremiahmcleod/Desktop/PereusMarketing/compliancescan103.csv")

#%%
#5  Change filename to extracted(detailed) file from dnc compliance scan line #54


#8  How many Leads? Specify Line #74 place a '#' at start of line 75 if all leads used
#9  Shift+Enter
searchfor = ['2018', '2019','2020',';;;W',';;W','Litigator']
#searchfor = [';;;W',';;W','Litigator']
Vonage = [';;;W',';;W']
df43 = pd.read_csv(r"/Users/jeremiahmcleod/Downloads/compliancescan103_1115819659/detailed.csv")
df43 = df43.iloc[1:]
df43.columns = ['phone_number','result_code', 'reserved', 'reason', 'state', 'country', 'city',
                'carrier_info', 'new_reassigned', 'tz_code', 'calling_window', 'utcoffset',
                'dnc_today', 'calltimereset', 'ebr_type', 'wireless', 'line_type']
df430 = df43[['phone_number','reason']]
df431 = df.merge(df430, left_on='phone_number', right_on='phone_number')
df431 = df431.drop_duplicates(['phone_number','first_name','last_name','email'],keep='last')

df431['reason'] = df431['reason'].astype(str).astype(str)
df19 = df431[df431['reason'].str.contains('|'.join(searchfor))]
df25 = df431[df431['reason'].str.contains('|'.join(Vonage))]
df431 = df431[~df431.reason.str.contains('|'.join(searchfor))]
df431.insert(loc=0,column='approval_',value='Approved')
#df431.insert(loc=0,column='campaign_',value=campaign)
df431[0:100].to_csv("/Users/jeremiahmcleod/Desktop/PereusMarketing/vanillasoft_upload.csv")
writer = pd.ExcelWriter('/Users/jeremiahmcleod/Desktop/PereusMarketing/marketing_list.xlsx', engine='xlsxwriter')
df_orig.to_excel(writer, sheet_name='original_ml')
#df431.insert(loc=0,column='sales_associate',value=salesAssociate)
df431.to_excel(writer, sheet_name='approved_leads')
del df431['approval_']
del df431['reason']
df431[0:100].to_excel(writer, sheet_name='leads4camp')
df431[101:].to_excel(writer,sheet_name='use_next_camp')
df19.to_excel(writer,sheet_name='denied_leads')
df25.to_excel(writer,sheet_name='vonage_leads')
writer.save()

#10 file is saved, upload to google sheets and then vanillasoft



#%% copy contents to line #41 if phone_number_ext column if used
df['phone_number_ext'] = [re.sub("[^0-9,''+]","", str(x)) for x in df['phone_number_ext']]


#%% check if email is valid (beta) - does not currently work
df['email'] = [re.sub("[A-Za-z0-9._+]+@[A-Za-z]+.(com|org|edu|net)"," ", 
                      str(x)) for x in df['email']]





