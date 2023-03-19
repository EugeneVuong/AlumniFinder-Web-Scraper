from bs4 import BeautifulSoup as bs
import re
from parseutil import parseUtil
import usaddress
import datetime

class Parse:
    
    def parseLexId(self, soupPage: bs, info: dict):
        if soupPage is None:
            return 

        for soup in soupPage:
            table = soup.find('table', id='srcTbl')
            for alumni_data in table.find_all('tbody'):
                rows = alumni_data.find_all('tr', id = re.compile("^r_\d"))
                for row in rows:
                    name = parseUtil.formatText(row.find_all('td')[1].text.strip())
                    data_address = parseUtil.formatText(row.find_all('td')[3].find('span').text.strip())
                    lex_id_1 = 0
                    lex_id_2 = 0
                    
                    try:
                        data_address = parseUtil.formatText(row.find_all('td')[3].find('span').text.strip())
                        if parseUtil.check_address(info.get("StreetAddress"), data_address):
                            lex_id_1 = parseUtil.formatText(row.find_all('td')[2].find_all('div')[0].find('a').text.strip())
                    except:
                        lex_id_1 = 'N/A'
                    
                    try:
                        if parseUtil.check_person_name(info.get("FirstName"), info.get("LastName"), name):
                            lex_id_2 = parseUtil.formatText(row.find_all('td')[2].find_all('div')[0].find('a').text.strip())
                    except:
                        lex_id_2 = 'N/A'
                    
                    if lex_id_1 == lex_id_2 and (lex_id_1 and lex_id_2) != 'N/A':
                        return lex_id_2
        return None

    def getJson(self, soupPage: bs):
        if soupPage is None:
            return 

        result = {"Results": []}
        for soup in soupPage:
            table = soup.find('table', id='srcTbl')
            for alumni_data in table.find_all('tbody'):
                rows = alumni_data.find_all('tr', id = re.compile("^r_\d"))
                for row in rows:

                    
                    
                    try:
                        lex_id = parseUtil.formatText(row.find_all('td')[2].find_all('div')[0].find('a').text.strip())
                    except:
                        lex_id = None

                    try:
                        name = parseUtil.formatText(row.find_all('td')[1].text.strip())
                    except:
                        name = None


                    try:
                        geolocation = parseUtil.formatText(row.find_all('td')[3].find('span').text.strip())
                        
                        try:
                            address = ''
                            state = ''
                            city = ''
                            zip = ''
                            for location in usaddress.parse(geolocation):
                                # print(location)
                                if location[1] != 'ZipCode' and location[1] != 'StateName' and location[1] != 'PlaceName':
                                    address += location[0] + ' '
                                elif location[1] == 'ZipCode':
                                    zip += location[0]
                                elif location[1] == 'StateName':
                                    state += location[0]
                                elif location[1] == 'PlaceName':
                                    city += location[0] + ' '
                        except:
                            address = None
                            zip = None
                            state = None
                            city = None

                    except:
                        geolocation = None
                        address = None
                        zip = None
                        state = None
                        city = None


                    try:
                        date = parseUtil.formatText(row.find_all('td')[3].find('div', class_ = 'hData').text.strip())
                        date = re.sub(' +', '', date).split('-')
                        if(len(date) == 2):
                            date_first_seen = date[0]
                            date_last_seen = date[1]
                        elif(len(date) == 1):
                            date_first_seen = None
                            date_last_seen = date[0]
                    except:
                        date_first_seen = None
                        date_last_seen = None
                    
                    try:
                        deceased = parseUtil.formatText(row.find_all('td')[2].find('b', {'style': 'color: red;'}).text.strip())
                    except:
                        deceased = None
                    

                        

                    person_infomation = {
                        "LexId": lex_id,
                        "Name": name,
                        "Location": geolocation,
                        "Address": address,
                        "State": state,
                        "City": city,
                        "Zip Code": zip,
                        "Date First Seen": date_first_seen,
                        "Date Last Seen": date_last_seen,
                        "Deceased": deceased
                    }



                    result['Results'].append(person_infomation)
        return result


    def getRecentAddress(self, soupPage: bs):

        if soupPage is None: return
        maxDate = datetime.date(datetime.MINYEAR, 1, 1)
        
        

        for soup in soupPage:
            table = soup.find('table', id='srcTbl')
            for alumni_data in table.find_all('tbody'):
                rows = alumni_data.find_all('tr', id = re.compile("^r_\d"))
                for row in rows:
                    #print("age", row.find_all('td')[2])

                    try:
                        testDate = parseUtil.formatText(row.find_all('td')[3].find('div', class_ = 'hData').text.strip())
                        testDate = re.sub(' +', '', testDate).split('-')
                        if(len(testDate) == 2):
                            test_date_last_seen = testDate[1]
                        elif(len(testDate) == 1):
                            test_date_last_seen = testDate[0]
                    except:
                        test_date_last_seen = None

                    try:
                        test_geolocation = parseUtil.formatText(row.find_all('td')[3].find('span').text.strip())
                    except:
                        test_geolocation = None
                    
                    if((maxDate < parseUtil.turnToDateTime(test_date_last_seen)) and test_geolocation is not None):
                        maxDate = parseUtil.turnToDateTime(test_date_last_seen)
                        try:
                            lex_id = parseUtil.formatText(row.find_all('td')[2].find_all('div')[0].find('a').text.strip())
                        except:
                            lex_id = None

                        try:
                            name = parseUtil.formatText(row.find_all('td')[1].text.strip())
                        except:
                            name = None


                        try:
                            geolocation = parseUtil.formatText(row.find_all('td')[3].find('span').text.strip())
                            
                            try:
                                address = ''
                                state = ''
                                city = ''
                                zip = ''
                                for location in usaddress.parse(geolocation):
                                    # print(location)
                                    if location[1] != 'ZipCode' and location[1] != 'StateName' and location[1] != 'PlaceName':
                                        address += location[0] + ' '
                                    elif location[1] == 'ZipCode':
                                        zip += location[0]
                                    elif location[1] == 'StateName':
                                        state += location[0]
                                    elif location[1] == 'PlaceName':
                                        city += location[0] + ' '
                            except:
                                address = None
                                zip = None
                                state = None
                                city = None

                        except:
                            geolocation = None
                            address = None
                            zip = None
                            state = None
                            city = None


                        try:
                            date = parseUtil.formatText(row.find_all('td')[3].find('div', class_ = 'hData').text.strip())
                            date = re.sub(' +', '', date).split('-')
                            if(len(date) == 2):
                                date_first_seen = date[0]
                                date_last_seen = date[1]
                            elif(len(date) == 1):
                                date_first_seen = None
                                date_last_seen = date[0]
                        except:
                            date_first_seen = None
                            date_last_seen = None
                        
                        try:
                            deceased = parseUtil.formatText(row.find_all('td')[2].find('b', {'style': 'color: red;'}).text.strip())
                        except:
                            deceased = None
        
        person_infomation = {
                        "LexId": lex_id,
                        "Name": name,
                        "Location": geolocation,
                        "Address": address,
                        "State": state,
                        "City": city,
                        "Zip Code": zip,
                        "Date First Seen": date_first_seen,
                        "Date Last Seen": date_last_seen,
                        "Deceased": deceased
                    }

        return person_infomation