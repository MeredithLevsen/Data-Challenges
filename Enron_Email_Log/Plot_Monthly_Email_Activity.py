#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Functions for plotting email records
@author: meredithlevsen
"""

import pandas as pd
from datetime import datetime

# Visualization
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter




class Plot_Monthly_Email_Activity():
    
    def __init__(self):
        '''Initialize objects.'''
        
        #self.big_senders_list = []
        self.df_mo = []
        self.df_cnt = []
        
        ### Add try statement here!!! To see if file exists.
        # If it doesn't exist, import srs class and create it. 
        #self.df_output1 = pd.read_csv('Output1_Sent_Received_Summary.csv')
    
    
    def make_big_senders_list (self, 
                               df_output1, 
                              how_many_big_senders = 5,
                              df_output1_person_colname = 'person' ):
        # Make a list of the "Big Senders" (i.e., most prolific email senders)
        big_senders_list = list(df_output1[df_output1_person_colname].iloc[ : how_many_big_senders])
        
        return big_senders_list

    
    def retain_big_senders_df_log ( self, df_log , df_output1, big_senders_list , 
                                       df_log_person_colname = 'sender' ) :
        '''
        Retain only the top [how_many] most prolific email senders in the df_log. 
        Requires summary df with number of emails sent per person (stored in 
        df_output1).
        '''
        # Make a list of the "Big Senders" (i.e., most prolific email senders)
        #self.big_senders_list = df_output1[df_output1_person_colname].iloc[ : how_many_big_senders]
        
        # Retain only the big senders in df_log
        df_log = df_log [ df_log [df_log_person_colname].isin(big_senders_list) == True]
        
        return df_log

    
    def add_date_cols_to_df_log ( self, df_log , unix_time_colname = 'time' ) :
        ''' 
        Converts unix time (unix_time_colname) to human readable dates. 
        Adds two new columns (date, date_month) to df_log.
        '''
        #### Add try statement here to figure out whether it's ms or sec! 
        
        # Note: unix_time/1000 in order to convert unix ms time to sec
        unix_to_date_converter = lambda unix_time: datetime.utcfromtimestamp(int(unix_time)/1000).strftime('%Y-%m-%d')
        df_log['date'] = df_log[unix_time_colname].apply(unix_to_date_converter) 
        
        unix_to_month_converter = lambda unix_time: datetime.utcfromtimestamp(int(unix_time)/1000).strftime('%Y-%m')
        df_log['date_month'] = df_log[unix_time_colname].apply(unix_to_month_converter)
        
        return df_log
        
    
    def make_df_sum_sent_monthly ( self , df_log , 
                                     df_log_person_colname = 'sender' , 
                                     date_month_colname = 'date_month' ):
        '''
        Creates a df that contains the number of emails sent per month per person.
        Input: df_log with a column (date_month_colname) specifying the date 
            the emails were sent in 'YYYY-MM' format.
        '''
        ##### Add try to test whether the date is specified correctly! 
        
        df_mo = []
        df_mo = df_log[ df_log_person_colname ].groupby(df_log[date_month_colname]).value_counts()
        df_mo = pd.DataFrame(df_mo) # turn series into dataframe
        df_mo.columns = ['sent'] # name email count column
        df_mo.reset_index( level = [0, 1], # turn multi-indices into columns
                          inplace = True)
        return df_mo
    
    
    def prep_df_log_for_sent_plot (self , df_log , df_output1 , 
                                    how_many_big_senders = 5 , 
                                    df_log_person_colname = 'sender' ,
                                    df_output1_person_colname = 'person' ,
                                    unix_time_colname = 'time' ,
                                    date_month_colname = 'date_month' ):
        '''
        Creates a df used to plot the number of emails sent per month for the 
        top (default: 5) most prolific senders.
        '''
        big_senders_list = self.make_big_senders_list (df_output1, 
                                                            how_many_big_senders,
                                                            df_output1_person_colname)
        
        df_log = self.retain_big_senders_df_log ( df_log , 
                                       df_output1 ,
                                       big_senders_list , 
                                       df_log_person_colname ) 
        df_log = self.add_date_cols_to_df_log ( df_log , 
                                          unix_time_colname ) 
        df_mo = self.make_df_sum_sent_monthly ( df_log , 
                                           df_log_person_colname , 
                                           date_month_colname)
        return df_mo, big_senders_list
    
    
    def graph_monthly_emails_sent ( self, df_mo ,
                                   person_colname = 'sender' , 
                                   date_month_colname = 'date_month' ,
                                   y_axis_colname = 'sent', 
                                   x_display_interval = 3 ,
                                   fig_width = 15 ,
                                   fig_height = 8) :
        '''
        Plots the number of emails sent per month for each sender (separate lines).
        x_display_interval: Interval between the x-axis tick mark labels
            (default of 3 means it only labels every 3rd month on tick mark)
        '''
        #### To-Do: Add KWARGS! Make months_labels_fmt a **KWARGS. and maybe month labels?
        #### Add a try to check the date format? 
    
        # Format date_month column as a datetime object
        # (Note: this will reset the date so that it's the 1st of the month)
        #df_mo['date_month'] = df_mo['date_month'].astype("datetime64")    
        
        # Set the interval between x-axis tick mark labels
        month_labels = MonthLocator( range(1, 13), 
                                     bymonthday = 1, 
                                     interval = x_display_interval)
        month_labels_fmt = DateFormatter("%b '%y") 
        
        fig, ax = plt.subplots( figsize = (fig_width, fig_height) )
        for person in df_mo[ person_colname ].unique() : 
            ax.plot_date( df_mo.loc[ df_mo [ person_colname ] == person ][ date_month_colname ],
                         df_mo.loc[ df_mo [ person_colname ] == person ][ y_axis_colname ] , 
                         '-',
                         label = person)
        ax.legend(loc='upper left')
        ax.xaxis.set_major_locator(month_labels)
        ax.xaxis.set_major_formatter(month_labels_fmt)
        ax.xaxis.set_minor_locator(MonthLocator())  # every month
        ax.set_xlabel('Time in Months', fontsize = 12)
        ax.set_ylabel('Number of Emails Sent per Month', fontsize = 12)
        ax.set_title('Output 2: Emails Sent per Month for the Most Prolific Email Senders',
                     fontsize = 14)
        ax.autoscale_view()
        fig.autofmt_xdate()
        
        #plt.show()
        fig.savefig('output2_emails_sent.png', bbox_inches='tight')
    
    
    
    
    ### Output 3 functions: 
    def make_df_unique_senders_monthly (self, df_log , df_output1 ,
                                     how_many_big_senders = 5 , 
                                     recipient_colname = 'recipients' , 
                                     recipient_sep = '|' ,
                                     df_output1_person_colname = 'person' ,
                                     df_log_person_colname = 'sender' , 
                                     unix_time_colname = 'time' ,
                                     date_month_colname = 'date_month' ):
        '''
        This function 
        Input: A dataframe of email log history containing a column 
        ('recipient_colname') that contains the recipients of each email 
        (1 email per row). Different recipients are separated by 'recipient_sep'.
        Output: a new DF with 3 columns: 
            'person' (each email recipient; only includes top most prolific email senders), and 
            'date_month' (month in 'YYYY-MM' format), and 
            'unique_email_senders' (number of individuals who contacted each person per month).
        
        '''
        
        # Split the recipients column by '|' into as many columns as needed:
        df_cnt = df_log[recipient_colname].str.split(recipient_sep, expand = True)
        
        df_cnt = pd.concat([df_log[[unix_time_colname, df_log_person_colname]], 
                            df_cnt], axis = 1)
        
        # Put it into a dataframe with one column containing count data 
        # (with each person/recipient stored in index)
        df_cnt = pd.melt(df_cnt, id_vars = [unix_time_colname, 
                                            df_log_person_colname],
                              value_name = 'recipient')
        
        # Make a list of the "Big Senders" (i.e., most prolific email senders)
        big_senders_list = self.make_big_senders_list (df_output1, 
                                                       how_many_big_senders,
                                                       df_output1_person_colname)
        #big_senders_list = df_output1[df_output1_person_colname].iloc[ : how_many_big_senders]
        
        # Keep only recipients who are Big Senders: 
        df_cnt = df_cnt.loc[df_cnt['recipient'].isin(big_senders_list)]
        
        # Add human readable dates to df
        df_cnt = self.add_date_cols_to_df_log ( df_cnt , unix_time_colname)
        
        # To get unique contacts per month: 
        # Remove duplicates of 'sender' + 'received' + 'date_month'
        df_cnt = df_cnt[[df_log_person_colname, 'recipient', date_month_colname]].drop_duplicates()
        
        ### Count (non-dupliacte) sender values. grouped by 'received' and 'date_month'
        df_cnt = df_cnt[df_log_person_colname].groupby([df_cnt['recipient'], 
                                 df_cnt[date_month_colname]]).count()
        
        df_cnt = pd.DataFrame(df_cnt) # turn series into a df
        df_cnt.reset_index(level=[0,1], inplace=True) # make indices into columns
        df_cnt.columns = ['person', date_month_colname, 'unique_email_senders'] # rename columns
        
        return df_cnt 
    

    # Graph number of unique contacts per month: 
    def graph_monthly_contacts_received ( self, df_mo ,
                                   person_colname = 'person' , 
                                   date_month_colname = 'date_month' ,
                                   y_axis_colname = 'unique_email_senders', 
                                   x_display_interval = 3 ,
                                   fig_width = 15 ,
                                   fig_height = 8) :
        '''
        Plots the number of emails sent per month for each sender (separate lines).
        x_display_interval: Interval between the x-axis tick mark labels
            (default of 3 means it only labels every 3rd month on tick mark)
        '''
        #### To-Do: Add KWARGS! Make months_labels_fmt a **KWARGS. and maybe month labels?
        #### Add a try to check the date format? 
    
        # Format date_month column as a datetime object
        # (Note: this will reset the date so that it's the 1st of the month)
        #df_mo['date_month'] = df_mo['date_month'].astype("datetime64")    
        
        # Set the interval between x-axis tick mark labels
        month_labels = MonthLocator( range(1, 13), 
                                     bymonthday = 1, 
                                     interval = x_display_interval)
        month_labels_fmt = DateFormatter("%b '%y") 
        
        fig, ax = plt.subplots( figsize = (fig_width, fig_height) )
        for person in df_mo[ person_colname ].unique() : 
            ax.plot_date( df_mo.loc[ df_mo [ person_colname ] == person ][ date_month_colname ],
                         df_mo.loc[ df_mo [ person_colname ] == person ][ y_axis_colname ] , 
                         '-',
                         label = person)
        ax.legend(loc='upper left')
        ax.xaxis.set_major_locator(month_labels)
        ax.xaxis.set_major_formatter(month_labels_fmt)
        ax.xaxis.set_minor_locator(MonthLocator())  # every month
        ax.set_xlabel('Time in Months', fontsize = 12)
        ax.set_ylabel('Number of Unique Contacts Received per Month', fontsize = 12)
        ax.set_title('Output 3: Number of Individual People per Month who Emailed the Most Prolific Email Senders',
                     fontsize = 14)
        ax.autoscale_view()
        fig.autofmt_xdate()
        
        #plt.show()
        fig.savefig('output3_contacts_received.png', bbox_inches='tight')
    
