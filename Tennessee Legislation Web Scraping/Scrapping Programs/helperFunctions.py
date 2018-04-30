#############################################################
#   FUNCTIONS USED LATER ON IN PROGRAM
#############################################################
def firstItem(item):
    position = item.get_text().find(" ")
    return(item.get_text()[:position].strip(" "))
