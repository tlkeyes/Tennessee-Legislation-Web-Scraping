from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

################################
#   IMPORT HELPER FUNCTIONS
################################
import helperFunctions

session = 110
bill = 'SB0704'
link = f"http://wapp.capitol.tn.gov/apps/BillInfo/Default.aspx?BillNumber={bill}&ga={session}"

pageResponse = requests.get(link, timeout = 15)

soup = BeautifulSoup(pageResponse.content, 'html.parser')


#############################################################
#   STEPS TO COLLECT DATA
#   1 - Identify table that contains desired data
#   2 - Assign table columns to variables
#   3 - Create list comprehensions for each variable
#   4 - Drop list comprehensions into DataFrame
#############################################################

#####################################
#   DEFINE DICTIONARIES
#####################################
    
voteType = {
    'Ayes..':'Yes',
    'Noes..':'No',
    'Present and not voting':'Present - Not Voting'
}

individualVotes = {
    'voting aye were:': 'Yes',
    'voting no were:': 'No',
    'present and not voting were:': 'Present - Not Voting'
}

#############################################
#   DEFINE EMPTY DICTIONARIES TO STORE DATA
#############################################

voteCollector = {
    'Bill Number': [],
    'Label':[],
    'Legislature': [],
    'Vote Type': [],
    'Counts':[]
}

personVotes = {
    'Bill Number': [],
    'Person': [],
    'Vote Type': []
}
    
