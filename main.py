from scrape import Scrape
from parse import Parse


if __name__ == "__main__":
    
    scraper = Scrape(username, password)
    parse = Parse()

    while True: 
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        street_address = input("Street Address: ")
        city = input("City: ")
        state = input("State: ")
        zip_code = input("Zip Code: ")

        infomation = {
                'LastName': f'{last_name}',
                'FirstName': f'{first_name}',
                'StreetAddress': f'{street_address}',
                'City': f'{city}',
                'State': f'{state}',
                'Zip': f'{zip_code}',
            }
        
        #update.searchPerson(infomation)
        soup = scraper.scrapePersonInfo(infomation)
        lexId = parse.parseLexId(soup, infomation)
        soup = scraper.scrapePersonInfo(lexId)
        print(parse.getRecentAddress(soup))


