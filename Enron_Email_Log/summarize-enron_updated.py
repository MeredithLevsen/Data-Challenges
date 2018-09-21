#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Coding test
Meredith Levsen
Updated 9/21/2018

Input file: Email history log csv file
    Must be a csv file with 6 columns in the following order:
        1. time: (integer) the time the email was sent (in unix time)
        2. message_id: unique email identifier
        3. sender: who sent the email
        4. recipients: who the email was addressed to (multiple recipients 
        separated with '|')
        5. 'topic': empty column
        6. 'mode': in this case, it always says email. 

Output: 
    
    1. A .csv file with three columns---"person", "sent", "received"---where the
    final two columns contain the number of emails that person sent or received 
    in the data set. This file should be sorted by the number of emails sent.
    
    2. A PNG image visualizing the number of emails sent over time by some of the
    most prolific senders in (1); time is plotted in a meaningful way.
    
    3. A visualization (and a PNG file) that shows, for the same people, the number of unique 
    people/email addresses who contacted them over the same time period. It 
    shows the relative number of contacts received per person.
"""


#import sys
import pandas as pd

# Import class to make output1
import Sent_Received_Summarizer as srs

# Import classes to make plots for outputs 2 and 3
import Plot_Monthly_Email_Activity as eplt_classes 

# Set abreviations for custum classes
out1 = srs.Sent_Received_Summarizer()
eplt = eplt_classes.Plot_Monthly_Email_Activity()


#This deals with the pesky "SettingWithCopy" warning.
pd.options.mode.chained_assignment = None


# Import email history log .csv file
#file_name = sys.argv[1]
#df_log = pd.read_csv( file_name, 
#                     names = ['time', 'message_id', 'sender', 'recipients', 'topic', 'mode'])

# import raw csv data file
df_log = pd.read_csv('enron-event-history-all.csv', 
                      names = ['time', 'message_id', 'sender', 'recipients',
                               'topic', 'mode'])

''' 
Output # 1: 
A .csv file with three columns---"person", "sent", "received"---where the
final two columns contain the number of emails that person sent or received 
in the data set. This file should be sorted by the number of emails sent.

example output

person      sent (sorted)      received
name        # emails sent      # emails received
...         ...                ...
'''

# Run class with functions to generate output:
df_output1 = out1.make_df_sent_received_counts(df_log)

print('Output1 is complete! It has been saved as a csv file.')


'''
Output # 2: 
A PNG image visualizing the number of emails sent over time by some of the
most prolific senders in Output #1. 
'''

# Prep the data and get it in the proper format for plotting:
# this produces the dataframe for plotting (df_sent_plot) and a list of the 
# 'big senders' (i.e., those who sent the most emails overall; big_senders_list)
df_sent_plot, big_senders_list = eplt.prep_df_log_for_sent_plot (df_log, 
                                                                 df_output1,
                                                                 how_many_big_senders = 5)

# Plot data and save plot as a png file:
eplt.graph_monthly_emails_sent( df_sent_plot )

'''
Output # 3: 
A visualization that shows, for the same people, the relative number of unique 
people/email addresses who contacted them over the same time period. (Note:
    relative refers to within each person.)
'''

# Prep data for plotting: 
# this produces the dataframe that will be plotted. 
df_contacts = eplt.make_df_unique_senders_monthly(df_log, df_output1, 
                                                  df_sent_plot)

# Plot data. Also save it as a png file for good measure. 
eplt.graph_monthly_contacts_received( df_contacts )

print("Yay! The script has finished running.")

