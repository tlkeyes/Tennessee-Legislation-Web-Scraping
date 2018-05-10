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
    'Bill Session': [],
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

info = {
    "Bill Link": [] ,
    "Bill Number": [], 
    "Bill Session": [],
    "Composite Abstract": [], 
    "Last Action": [], 
    "Date": [] 
}

#####################################
#   HELPER FUNCTIONS
#####################################

def hbTable(data):
    html = data.find('span', id = 'lblHouseVoteData')
    return html

def sbTable(data):
    html = data.find('span', id = 'lblSenateVoteData')
    return html

def startFinish(items):
    start = items.find(":") + 2
    finish = items.find("--") - 1
    voters = items[start:finish].split(",")
    return voters

def collectHtml(soupData):
    if bill[0:2] == 'HB':
        html = hbTable(soupData)
        return html
    else:
        html = sbTable(soupData)
        return html

def firstItem(item):
    position = item.get_text().find(" ")
    return(item.get_text()[:position].strip(" "))

#####################################
#   MAIN FUNCTIONS
#####################################

#############################################################
#   STEPS TO COLLECT DATA
#   1 - Identify table that contains desired data
#   2 - Assign table columns to variables
#   3 - Create list comprehensions for each variable
#   4 - Drop list comprehensions into DataFrame
#     a - Or append records in the case of individual votes
#############################################################

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
        
        # Create list comprehensions to input data into a dataframe
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
    
def collectYesNo(billNumber):
    for items in collectHtml(soup):        
        if bill in items:
            label = str(items)
            if 'FLOOR' in label:
                legislature = 'Floor'
            else:
                legislature = 'Committee'
        for vt in voteType.keys():
            if vt in items:
                for ignore in [vt,'.',u'\xa0']:
                    items = items.replace(ignore,u'')
                voteCollector['Bill Number'].append(billNumber)
                voteCollector['Bill Session'].append(session)
                voteCollector['Label'].append(label)
                voteCollector['Legislature'].append(legislature)
                voteCollector['Vote Type'].append(voteType.get(vt))
                voteCollector['Counts'].append((int(items)))
        for iv in individualVotes.keys():
            if iv in items:
                start = items.find(":") + 2
                finish = items.find("--") - 1
                persons = items[start:finish].split(',')
                for person in persons:
                    personVotes["Person"].append(person)
                    personVotes["Bill Number"].append(billNumber)
                    personVotes["Vote Type"].append(individualVotes.get(iv))
