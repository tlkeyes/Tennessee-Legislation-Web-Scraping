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

info = {
    "Bill Link": [] ,
    "Bill Number": [], 
    "Bill Session": [],
    "Composite Abstract": [], 
    "Last Action": [], 
    "Date": [] 
}

def firstItem(item):
    position = item.get_text().find(" ")
    return(item.get_text()[:position].strip(" "))

def collectBills(maxSession):
    for j in range(99,(maxSession)):
        pageLink = f"http://wapp.capitol.tn.gov/apps/subjectindex/BillsBySubject.aspx?Primarysubject=2170&GA={j}"
        
        # fetch all house and senate bill information
        pageResponse = requests.get(pageLink, timeout=15)

        # parse html
        soup = BeautifulSoup(pageResponse.content, 'html.parser')
        
        # find part of page that has the table inside of it
        allBills = soup.find('label', {'id':'generatedcontent'})

        # in general, there are (4) columns that we are interested in. 
        # assign the column data, by cell
        billLinkCell = allBills.find_all('td', attrs={"width":"10%", "valign":"TOP"})
        billNumberCell = allBills.find_all('td', attrs={"width":"10%", "valign":"TOP"})
        summaryCell = allBills.find_all('td', attrs={"width":"45%","valign":"top"})
        lastActionCell = allBills.find_all('td', attrs={"width":"35%", "valign":"top"})
        dateCell = allBills.find_all('td', attrs={"width":"10%", "valign":"top"})
        
        #info["Bill Link"].append([bl.find('a').get('href').strip(" ") for bl in billLinkCell])
        
        billLink = [bl.find('a').get('href').strip(" ") for bl in billLinkCell]
        billNumber = [bn.find('a').get_text() for bn in billNumberCell]
        compositeAbstract = [s.get_text().strip(" ") for s in summaryCell]
        lastAction = [la.get_text().strip(" ") for la in lastActionCell]
        date = [firstItem(d) for d in dateCell]
        
        for item in billLink:
            info["Bill Link"].append(item)
        for item in billNumber:
            info["Bill Number"].append(item)
        for item in compositeAbstract:
            info["Composite Abstract"].append(item)
        for item in lastAction:
            info["Last Action"].append(item)
        for item in date:
            info["Date"].append(item)
            info["Bill Session"].append(j)