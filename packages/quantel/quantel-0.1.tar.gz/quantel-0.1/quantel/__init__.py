import asyncio
from typing import Union, List, Dict

import aiohttp
import requests

from quantel.exceptions import InvalidAPIKey, GatewayError


class _Ticker:

    def __init__(self, symbols: Union[list, str], host: str, api_key: str, asynchronous: bool = False):
        self.asynchronous = asynchronous
        self.api_key = api_key
        self.host = host

        if isinstance(symbols, str):
            symbols = symbols.split(" ")

        self.symbols = list(self._chunks(symbols, 30))

    def _get_data(self, endpoint) -> List[Dict]:

        headers = {
            "x-rapidapi-key": self.api_key,
            "user-agent": "Quantel Python Library v0.1"
        }

        if self.asynchronous:
            tasks = asyncio.get_event_loop().run_until_complete(self._submit_async(headers, endpoint))
        else:
            tasks = self._submit_sync(headers, endpoint)

        result = filter(None, tasks)
        flat = [x for sublist in result for x in sublist]
        return flat

    async def _submit_async(self, headers, endpoint):
        async with aiohttp.ClientSession(headers=headers) as session:
            tasks = []
            for chunk in self.symbols:
                joined_symbols = ",".join(chunk)
                tasks.append(asyncio.ensure_future(self._get_data_async(session, endpoint, joined_symbols)))
            res = await asyncio.gather(*tasks)
            return res

    async def _get_data_async(self, session, endpoint, symbols):
        async with session.get(f"{self.host}{endpoint}/{symbols}") as response:
            if response.status == 200:
                return await response.json()

    def _submit_sync(self, headers, endpoint):
        tasks = []

        session = requests.Session()
        session.headers.update(headers)
        for chunk in self.symbols:
            joined_symbols = ",".join(chunk)
            tasks.append(self._get_data_sync(session, endpoint, joined_symbols))

        return tasks

    def _get_data_sync(self, session, endpoint, symbols):

        res = session.get(f"{self.host}{endpoint}/{symbols}")

        if res.status_code == 200:
            return res.json()

    def _chunks(self, l, n):
        n = max(1, n)
        return (l[i:i + n] for i in range(0, len(l), n))

    @property
    def income_statement(self) -> List[Dict]:
        """
        Get income statements

        Returns:

        """
        return self._get_data("income-statement")

    @property
    def income_statement_growth(self) -> List[Dict]:
        """
        Get income statements growth

        Returns:
        """
        return self._get_data("income-statement-growth")

    @property
    def balance_sheet(self) -> List[Dict]:
        """
        Get balance sheets

        Returns:
        """
        return self._get_data("balance-sheet-statement")

    @property
    def balance_sheet_growth(self) -> List[Dict]:
        """
        Get balance sheets growth

        Returns:
        """
        return self._get_data("balance-sheet-statement-growth")

    @property
    def cash_flow(self) -> List[Dict]:
        """
        Get cash flow statements

        Returns:
        """
        return self._get_data("cash-flow-statement")

    @property
    def cash_flow_growth(self) -> List[Dict]:
        """
        Get cash flow statements growth

        Returns:
        """
        return self._get_data("cash-flow-statement-growth")

    @property
    def ratios(self) -> List[Dict]:
        """
        Get key financial ratios

        Returns:
        """
        return self._get_data("ratios")

    @property
    def enterprise_values(self) -> List[Dict]:
        """
        Get enterprise values

        Returns:
        """
        return self._get_data("enterprise-values")

    @property
    def key_metrics(self) -> List[Dict]:
        """
        Get key financial metrics

        Returns:
        """
        return self._get_data("key-metrics")

    @property
    def analyst_estimates(self) -> List[Dict]:
        """
        Get analyst estimates of key financial figures

        Returns:
        """
        return self._get_data("analyst-estimates")

    @property
    def shares_float(self) -> List[Dict]:
        """
        Get shares float and outstanding

        Returns:
        """
        return self._get_data("shares-float")

    @property
    def quote(self) -> List[Dict]:
        """
        Get up to date quote

        Returns:
        """
        return self._get_data("quote")

    @property
    def profile(self) -> List[Dict]:
        """
        Get company profile

        Returns:
        """
        return self._get_data("profile")

    @property
    def insider_transactions(self) -> List[Dict]:
        """
        Get all insider transactions

        Returns:
        """

        # TODO: Add months parameter.
        return self._get_data("insider-transactions")

    @property
    def insider_transactions_summarized(self) -> List[Dict]:
        """
        Get insider transactions summarized

        Returns:
        """
        # TODO: Add months parameter.
        return self._get_data("insider-transactions-summarized")

    @property
    def share_ownership(self) -> List[Dict]:
        """
        Get share owning groups

        Returns:
        """
        return self._get_data("share-ownership")

    @property
    def key_executives(self) -> List[Dict]:
        """
        Get key executives in org

        Returns:
        """
        return self._get_data("key-executives")


class Quantel(object):

    def __init__(self, api_key: str, validate: bool = True):
        """
        Authenticate with the Quantel Finance API

        Args:
            api_key: Quantel Finance API Key
            validate: Validate API Key

        Example:

            >>> from quantel import Quantel
            >>>
            >>> qt = Quantel(api_key="<quantel-api-key>")
        """
        self.api_key = api_key
        self.host = "https://quantel-io.p.rapidapi.com/"

        if validate:
            self._validate_api()

    def _validate_api(self) -> bool:

        headers = {
            "x-rapidapi-key": self.api_key,
            "user-agent": "Quantel Python Library v0.1"
        }
        res = requests.get(self.host, headers=headers)

        if res.status_code in (401, 403):
            """
            401 is an Unauthorized status code. 
            403 is an Access Forbidden code.
            
            Both indicate that the API key was not accepted by RapidAPI
            """
            raise InvalidAPIKey(
                "Your API Key is invalid. You may have entered your API Key incorrectly, or have not subscribed to the API.\n"
                "https://quantel.io/faq#invalid_api_key")

        elif res.status_code == 503:

            raise GatewayError(
                "Unable to connect to the API server. If the error persists, please reach out to the team at contact@quantel.io"
            )

        elif res.status_code == 404:
            """
            404 not found indicates that RapidAPI accepted the API key in this case.
            """
            return True

    def ticker(self, symbols: Union[list, str], asynchronous: bool = False) -> _Ticker:
        """

        Args:
            symbols: List of tickers, or space separated string
            asynchronous: Enable asynchronous lookup of tickers

        Example:
            >>> qt.ticker("GOOG")

        Returns:

            Ticker class

        """
        return _Ticker(symbols, self.host, self.api_key, asynchronous)
