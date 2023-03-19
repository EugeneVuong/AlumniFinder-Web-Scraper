import re
import unicodedata
import datetime

class parseUtil(object):
 
    @staticmethod
    def formatText(text: str):
        '''
        Removes unnecessory spaces and unicode

            Parameters:
                text (str): unformatted text

            Returns:
                formatted_text (str): formatted text
        '''
        unformated_text = text.strip()
        formatted_text = re.sub(' +', ' ', unicodedata.normalize("NFKD", unformated_text).strip())
        formatted_text = formatted_text.replace("\n", '')
        formatted_text = formatted_text.replace("\r", '')
        return str(formatted_text)

    @staticmethod
    def check_address(input_address, data_address):
        if re.search(input_address.upper(), data_address.upper()): return True
        return False


    @staticmethod
    def check_person_name(input_first, input_last, data_name):
        if re.search(input_first.upper(), data_name.upper()) and re.search(input_last.upper(), data_name.upper()): return True
        return False

    @staticmethod
    def turnToDateTime(date: str):
        if date is None or date == '': return datetime.date(datetime.MINYEAR, 1, 1)

        dateSplit = date.split('/')
        dateSplit = [eval(i) for i in dateSplit]





        match len(dateSplit):
            case 3:
                return datetime.date(dateSplit[2], dateSplit[0], dateSplit[1])

            case 2:
                return datetime.date(dateSplit[1], dateSplit[0], 1)

            case 1:
                return datetime.date(dateSplit[0], 1, 1)


            case _:
                return datetime.date(datetime.MINYEAR, 1, 1)


        

    
    
    