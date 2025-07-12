import requests

class SecEdgar:
    """
    A class to handle actions related to SecEdgar like CIK (Central Index Key) lookups.
    """

    headers = {"User-Agent":"MLT fariseltayib@gmail.com"}

    def __init__(self):
        """
        Initializes the SecEdgar with a dictionary of CIK data.
        """
        self.name_to_cik = {}
        self.ticker_to_cik = {}

        # Retrieve fresh CIK data
        self._retrieve_cik_data()

    def _retrieve_cik_data(self):
        link = "https://www.sec.gov/files/company_tickers.json"
        r = requests.get(link, headers=self.headers)
        
        if r.status_code == 200:
            json = r.json()

            for num in json:

                cik = json[num]["cik_str"]
                company = json[num]["title"]
                ticker =  json[num]["ticker"]

                self.name_to_cik[company] = cik
                self.ticker_to_cik[ticker] = cik
        else:
            print(f"Status Code: {r.status_code}, for requesting {link}")

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
    
    def _get_10_digit_cik(self, cik):
        """
        Returns a CIK that's left-padded with zeros to fit 10 digits
        """

        return str(cik).zfill(10)
    
    def _get_company_filings(self, cik):
        """
        Returns the json of a company's filings using a CIK; returns None if status code != 200
        """

        link = f"https://data.sec.gov/submissions/CIK{self._get_10_digit_cik(cik)}.json"
        r = requests.get(link, headers=self.headers)
        if r.status_code == 200:
            json = r.json()
            return json["filings"]
        else:
            print(f"Status Code: {r.status_code}, for requesting {link}")
            return None
    
    def annual_filing(self, cik, year):
        """
        Returns the first 10-K filling for the given CIK and year
        """

        filings = self._get_company_filings(cik)
        data = filings["recent"]

        for i in range (len(data["accessionNumber"])):
            form_type = data["form"][i]
            filing_date = data["filingDate"][i]
            if form_type == "10-K" and filing_date.startswith(str(year)):
                link = (
                    f"https://www.sec.gov/Archives/edgar/data/"
                    f"{self._get_10_digit_cik(cik)}/"
                    f"{data['accessionNumber'][i].replace('-', '')}/"
                    f"{data['primaryDocument'][i]}"
                        
                )
                return link
            
        # if not found
        return None

    def quarterly_filing(self, cik, year, quarter):
        """
        Returns the first 10-Q filling matching the specified year and quarter
        """

        filings = self._get_company_filings(cik)
        data = filings["recent"]

        for i in range(len(data["accessionNumber"])):
            form_type = data["form"][i]
            filing_date = data["filingDate"][i]
            if form_type == "10-Q" and filing_date.startswith(str(year)):
                # Extract month info
                month = int(filing_date[5:7])

                if(
                    (quarter == 1 and 1 <= month <= 3)
                    or (quarter == 2 and 4 <= month <= 6)
                    or (quarter == 3 and 7 <= month <= 9)
                    or (quarter == 4 and 10 <= month <= 12)
                ):
                    link = (
                        f"https://www.sec.gov/Archives/edgar/data/"
                        f"{self._get_10_digit_cik(cik)}/"
                        f"{data['accessionNumber'][i].replace('-', '')}/"
                        f"{data['primaryDocument'][i]}"
                    )
                    return link
        
        # if not found
        return None

mysec = SecEdgar()
print(mysec.quarterly_filing("0000320193", 2025, 2))