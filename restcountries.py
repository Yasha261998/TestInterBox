import requests
from requests.exceptions import JSONDecodeError
from typing import Union, List, Dict
import pandas as pd


class RestCountries:
    """Get info for country.
    Used restcountries v3.1.

    :param _main_url:
        Url to api (private).

    :param _fields:
        Fields by default for every request (private).
    """

    _main_url = "https://restcountries.com/v3.1"
    _fields={"fields": ["name", "capital", "flags"]}

    def _print_table(self, data: List) -> None:
        """Print table to console.

        :param data:
            Output data.
        """
                
        for country in data:
            country["name"] = country["name"]["common"]
            if len(country["capital"]) == 0:
                country["capital"] = "None"
            elif len(country["capital"]) == 1:
                country["capital"] = country["capital"][0]
            country["flags"] = country["flags"]["png"]
            
        df = pd.DataFrame(data)
        df = df[["name", "capital", "flags"]]
        print(df.to_string(header=["Name", "Capital city", "Flag"],
                           justify="center",
                           index=False))
        print("\n")

    def _get_request(self, url: str, params=None) -> Union[None, List]:
        """Get request by url with parameters.

        :param url:
            Url for request.

        :param params:
            Parameters for request (optional, default=None).

        :returns:
            Response to request.
        """
        
        if params is None:
            response = requests.get(url,
                                    params=self._fields)
        else:
            response = requests.get(url,
                                    params=params)
        if response.status_code == requests.codes.ok:
            try:
                result = response.json()
            except JSONDecodeError as ex:
                print(f"JSONDecodeError (get_all): {ex}")
                return None
            else:
                return result
        else:
            print(f"Error response url: {url}: {response.text}")
            return None

    def get_all(self) -> bool:
        """Get all countries and display result.
        
        :returns:
            Operation status.
        """
        
        url = "/".join((self._main_url, "all"))
        res = self._get_request(url)
        if res:
            self._print_table(res)
            return True
        return False

    def get_by_name(self, name: str) -> bool:
        """Search by country name and display result.

        :param name:
            Common or official name.
        
        :returns:
            Operation status.
        """
        
        url = "/".join((self._main_url, "name", name))
        res = self._get_request(url)
        if res:
            self._print_table(res)
            return True
        return False

    def get_by_fullname(self, fullname: str) -> bool:
        """Search by country name and display result.
        Is used to find an exact match.

        :param fullname:
            Common or official name.
            
        :returns:
            Operation status.
        """
        
        url = "/".join((self._main_url, "name", fullname))
        self._fields["fullText"] = "true"
        res = self._get_request(url, params=self._fields)
        if res:
            self._print_table(res)
            return True
        return False

    def get_by_code(self, code: Union[int, str]) -> bool:
        """Search by country code and display result.

        :param code:
            Country code.
            
        :returns:
            Operation status.
        """

        # convert int code to str
        if isinstance(code, int):
            code = str(code)

        url = "/".join((self._main_url, "alpha", code))
        res = self._get_request(url)
        if res:
            if isinstance(res, list):
                self._print_table(res)
            else:
                self._print_table([res])
            return True
        return False
    
    def get_by_listcodes(self, code: List[Union[int, str]]) -> bool:
        """Search by list of country codes and display result.

        :param code:
            Country code or list codes.
            
        :returns:
            Operation status.
        """

        url = "/".join((self._main_url, "alpha"))
        self._fields["codes"] = code
        res = self._get_request(url, params=self._fields)
        if res:
            self._print_table(res)
            return True
        return False

    def get_by_currency(self, code: str) -> bool:
        """Search by currency code and display result.

        :param code:
            Currency code.
            
        :returns:
            Operation status.
        """

        url = "/".join((self._main_url, "currency", code))
        res = self._get_request(url)
        if res:
            self._print_table(res)
            return True
        return False

    def get_by_demonym(self, demonym: str) -> bool:
        """Search by how a citizen is called

        :param demonym:
            Demonym.
            
        :returns:
            Operation status
        """

        url = "/".join((self._main_url, "demonym", demonym))
        res = self._get_request(url)
        if res:
            self._print_table(res)
            return True
        return False

    def get_by_lang(self, lang: str) -> bool:
        """Search by language code or name.

        :param lang:
            Language code or name.
            
        :returns:
            Operation status.
        """

        url = "/".join((self._main_url, "lang", lang))
        res = self._get_request(url)
        if res:
            self._print_table(res)
            return True
        return False


    def get_by_capital(self, capital: str) -> bool:
        """Search by capital city.

        :param capital:
            Capital city.
            
        :returns:
            Operation status.
        """

        url = "/".join((self._main_url, "capital", capital))
        res = self._get_request(url)
        if res:
            self._print_table(res)
            return True
        return False

    def get_by_region(self, region: str) -> bool:
        """Search by region.

        :param region:
            Region.
            
        :returns:
            Operation status.
        """

        url = "/".join((self._main_url, "region", region))
        res = self._get_request(url)
        if res:
            self._print_table(res)
            return True
        return False

    def get_by_subregion(self, subregion: str) -> bool:
        """Search by subregion.

        :param subregion:
            Subregion.
            
        :returns:
            Operation status.
        """

        url = "/".join((self._main_url, "subregion", subregion))
        res = self._get_request(url)
        if res:
            self._print_table(res)
            return True
        return False
        
    def get_by_translation(self, translation: str) -> bool:
        """Search by translation.

        :param translation:
            Translation of country.
        :returns:
            Operation status.
        """

        url = "/".join((self._main_url, "translation", translation))
        res = self._get_request(url)
        if res:
            self._print_table(res)
            return True
        return False


if __name__ == "__main__":
    country = RestCountries()
    country.get_all()
    country.get_by_name("deutschland")
    country.get_by_fullname("Germany")
    country.get_by_code("col")
    country.get_by_listcodes([170,"pe"])
    country.get_by_currency("cop")
    country.get_by_demonym("peruvian")
    country.get_by_lang("spanish")
    country.get_by_capital("tallinn")
    country.get_by_region("europe")
    country.get_by_subregion("Northern Europe")
    country.get_by_translation("germany")
    
