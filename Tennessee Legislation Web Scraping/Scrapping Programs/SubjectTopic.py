from bs4 import BeautifulSoup
import requests
import pandas as pd

#############################################################
#   BELOW ARE THE THREE (3) STEPS TO IMPORTING THE DATA
#   1 - test link to estabilish starting location for program
#       a. This should later be replaced 
#   2 - fetch all house and senate bill information
#   3 - parse the html from pageRespose
#############################################################
testLink = "http://wapp.capitol.tn.gov/apps/subjectindex/BillsBySubject.aspx?Primarysubject=2170&GA=109"

def subjectTopicData(pagelink, subject = 'HealthCare'):   
    pageResponse = requests.get(pagelink, timeout = 15)
   
    soup = BeautifulSoup(pageResponse.content, 'html.parser')

    #############################################################
    #   STEPS TO COLLECT DATA
    #   1 - Identify table that contains desired data
    #   2 - Assign table columns to variables
    #   3 - Create list comprehensions for each variable
    #   4 - Drop list comprehensions into DataFrame
    #############################################################
    billTable = soup.find('label', {'id':'generatedcontent'})

    linkCell = billTable.find_all('td', attrs={"width":"10%", "valign":"TOP"})
    numberCell = billTable.find_all('td', attrs={"width":"10%", "valign":"TOP"})
    summaryCell = billTable.find_all('td', attrs={"width":"45%","valign":"top"})
    lastActionCell = billTable.find_all('td', attrs={"width":"35%", "valign":"top"})
    dateCell = billTable.find_all('td', attrs={"width":"10%", "valign":"top"})

    link = [bl.find('a').get('href').strip(" ") for bl in linkCell]
    billNumber = [bn.find('a').get_text() for bn in numberCell]
    summary = [s.get_text().strip(" ") for s in summaryCell]
    lastAction = [la.get_text().strip(" ") for la in lastActionCell]
    date = [firstItem(d) for d in dateCell]

    information = pd.DataFrame({
        "Bill Link": link, 
        "Bill Number": billNumber,
        "Subject": subject,
        "Composite Abstract": summary,
        "Last Action": lastAction,
        "Date": date
        })
    
    information.to_csv('information.csv')

subjectTopicData(pagelink=testLink)