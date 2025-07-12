import requests

class SecEdgar:
    """
    A class to handle actions related to SecEdgar like CIK (Central Index Key) lookups.
    """

    link = "https://www.sec.gov/files/company_tickers.json"

    def __init__(self):
        """
        Initializes the SecEdgar with a dictionary of CIK data.
        """
        self.name_to_cik = {}
        self.ticker_to_cik = {}

        # Retrieve fresh CIK data
        self._retrieve_cik_data()

    def _retrieve_cik_data(self):
        headers = {"User-Agent":"MLT fariseltayib@gmail.com"}
        r = requests.get(self.link, headers=headers)
        
        if r.status_code == 200:
            json = r.json()
            
            for num in json:

                cik = json[num]["cik_str"]
                company = json[num]["title"]
                ticker =  json[num]["ticker"]

                self.name_to_cik[company] = cik
                self.ticker_to_cik[ticker] = cik
        else:
            print(f"Status Code: {r.status_code}, for requesting {self.link}")

    def get_name_to_cik(self):
        """
        Returns the dictionary mapping company names to CIKs.
        """

        return self.name_to_cik
    
    def get_ticker_to_cik(self):
        """
        Returns the dictionary mapping stock tickers to CIKs.
        """

        return self.ticker_to_cik