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


