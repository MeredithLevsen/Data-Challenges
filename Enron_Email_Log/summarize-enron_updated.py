#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Coding test
Meredith Levsen
9/20/2018
"""


#import sys
import pandas as pd

# Import class to make output1
import Sent_Received_Summarizer as srs

# Import classes to make plots for outputs 2 and 3
import Plot_Monthly_Email_Activity as eplt_classes 


out1 = srs.Sent_Received_Summarizer()
eplt = eplt_classes.Plot_Monthly_Email_Activity()

# Import classes
#import Sent_Received_Summarizer as srs



# Import email history log .csv file
#file_name = sys.argv[1]
#df_log = pd.read_csv( file_name, 
#                     names = ['time', 'message_id', 'sender', 'recipients', 'topic', 'mode'])

# import raw csv data file
#df_log = pd.read_csv('enron-event-history-all.csv', 
#                      names = ['time', 'message_id', 'sender', 'recipients',
#                               'topic', 'mode'])

''' 
Output # 1: 
A .csv file with three columns---"person", "sent", "received"---where the
final two columns contain the number of emails that person sent or received 
in the data set. This file should be sorted by the number of emails sent.
(MVP: DataFrame)

example output

person      sent (sorted)      received
name        # emails sent      # emails received
...         ...                ...

Approach
1. List of all names included in recipients and sender
2. count occurrences of name in sender
3. count occurrences of name in recipient

'''

# Run class with functions to generate output:
df_output1 = out1.make_df_sent_received_counts(df_log)



'''
Output # 2: 
A PNG image visualizing the number of emails sent over time by some of the
most prolific senders in (1). 
There are no specific guidelines regarding the format and specific content of 
the visualization---you can choose which and how many senders to include, 
and the type of plot---
but you should strive to make it as clear and informative as possible, 
making sure to represent time in some meaningful way.
'''

# Prep the data and get it in the proper format for plotting:
df_sent_plot, big_senders_list = eplt.prep_df_log_for_sent_plot (df_log , df_output1)

# For some reason, this statement is unhappy liviing inside the function. 
# Need to fix. 
df_sent_plot['date_month'] = df_sent_plot['date_month'].astype('datetime64')

eplt.graph_monthly_emails_sent(df_sent_plot)

### With more time, I would make sure that missing dates were coded as 0
# for each person. 


'''
Output # 3: 
A visualization that shows, for the same people, the number of unique 
people/email addresses who contacted them over the same time period. The raw 
number of unique incoming contacts is not quite as important as the relative 
numbers (compared across the individuals from (2) ) and how they change 
over time.
'''

##### Output #3: 
df_contacts = eplt.make_df_unique_senders_monthly(df_log, df_output1)

df_contacts['date_month'] = df_contacts['date_month'].astype('datetime64')

eplt.graph_monthly_contacts_received( df_contacts )

print("Yay! The script has finished running.")

