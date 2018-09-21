#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 08:49:07 2018

@author: meredithlevsen

ForcePoint Coding Exam
"""

import pandas as pd

class Sent_Received_Summarizer():
    ''' This class contains functions that produce summaries of the number of 
    emails sent and received by each person listed in a email history log
    (i.e., Output #1 for Code Exam). '''
    
     
    def __init__(self):
        '''Placeholder for initializations .'''
        
    
    
    def make_received_col (self, df_log, 
                           recipient_colname = 'recipients', 
                           recipient_sep = '|'):
        '''
        This function takes a dataframe containing a column ('recipient_colname')
        that contains the recipients of each email (1 email per row). 
        Different recipients are separated by 'recipient_sep'.
        Output: a new DF with 2 columns: 'person' (each email recipient), and 
            'received' (number of emails received by each person).
        '''
        # Split the recipients column by '|' into as many columns as needed:
        df_received = df_log[recipient_colname].str.split(recipient_sep, expand = True)
    
        # Put it into a dataframe with one column containing count data 
        # (with each person/recipient stored in index)
        df_received = pd.melt(df_received, value_name = 'received')
        
        df_received = df_received['received'].value_counts() # count # of recipient occurrences
            # (Assumes recipient only occurs once per email)
        df_received = pd.DataFrame(df_received) # turn series into a df
        df_received.reset_index(level=0, inplace=True) # make index into a column (i.e., 'person')
        df_received.columns = ['person', 'received'] # rename columns
        
        return df_received
    
    
    def make_sent_col (self, df_log, sender_colname = 'sender'): 
        '''
        This function takes a dataframe containing email event log history
        and returns a dataframe containing each sender and how many emails they sent.
        Arguments: 
        - df: dataframe
        - sender_colname: name of column in df that contains sender of each email
        '''
        # Make new df with count values for each sender in the log
        df_sent = df_log[sender_colname].value_counts()
        df_sent = pd.DataFrame(df_sent)
        df_sent.reset_index(level=0, inplace = True)
        df_sent.columns = ['person', 'sent']
        
        return df_sent
    
    
    
    def make_df_sent_received_counts (self, df_log, 
                                      recipient_colname = 'recipients',
                                      recipient_sep = '|',
                                      sender_colname = 'sender'): 
        '''
        Input: 
            df: dataframe containing email event log history
        Output: 
            dataframe containing each 'person' in the log, and how many 
        emails they 'sent' and 'received'.
        '''
        
        df_received = self.make_received_col(df_log, 
                                        recipient_colname, 
                                        recipient_sep)
        
        df_sent = self.make_sent_col(df_log,
                                sender_colname)
        
        # Merge sent and received dfs
        df_output1 = pd.merge(df_sent, df_received, 
                             how = 'outer', 
                             on = 'person')
        # Fill all NaNs with 0
        df_output1 = df_output1.fillna(0)
        
        # Sort by sent (descending)
        df_output1 = df_output1.sort_values(by = 'sent', ascending = False)
        
        df_output1.to_csv('Output1_Sent_Received_Summary.csv', index = False)
        
        return df_output1
