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

    def _get_data(self, endpoint, **kwargs) -> List[Dict]:

        headers = {
            "x-rapidapi-key": self.api_key,
            "user-agent": "Quantel Python Library v0.1"
        }

        if self.asynchronous:
            tasks = asyncio.get_event_loop().run_until_complete(self._submit_async(headers, endpoint, **kwargs))
        else:
            tasks = self._submit_sync(headers, endpoint, **kwargs)

        result = filter(None, tasks)
        flat = [x for sublist in result for x in sublist]
        return flat

    async def _submit_async(self, headers, endpoint, **kwargs):
        async with aiohttp.ClientSession(headers=headers) as session:
            tasks = []
            for chunk in self.symbols:
                joined_symbols = ",".join(chunk)
                tasks.append(asyncio.ensure_future(self._get_data_async(session, endpoint, joined_symbols, **kwargs)))
            res = await asyncio.gather(*tasks)
            return res

    async def _get_data_async(self, session, endpoint, symbols, **kwargs):
        async with session.get(f"{self.host}{endpoint}/{symbols}", params=kwargs) as response:
            if response.status == 200:
                return await response.json()

    def _submit_sync(self, headers, endpoint, **kwargs):
        tasks = []

        session = requests.Session()
        session.headers.update(headers)
        for chunk in self.symbols:
            joined_symbols = ",".join(chunk)
            tasks.append(self._get_data_sync(session, endpoint, joined_symbols, **kwargs))

        return tasks

    def _get_data_sync(self, session, endpoint, symbols, **kwargs):

        res = session.get(f"{self.host}{endpoint}/{symbols}", params=kwargs)

        if res.status_code == 200:
            return res.json()

    def _chunks(self, l, n):
        n = max(1, n)
        return (l[i:i + n] for i in range(0, len(l), n))

    def income_statement(self) -> List[Dict]:
        """
        Get income statements

        Exchanges supported

        - NASDAQ
        - NYSE (New York Stock Exchange)
        - XETRA (German Electronic Exchange)
        - ASX (Australian Stock Exchange)
        - TSX (Toronto Stock Exchange)
        - ENX (EuroNext)
        - NSE (National Stock Exchange of India)
        - LSE (London Stock Exchange)
        - MOEX (Moscow Stock Exchange)
        - HKEX (Hong Kong Stock Exchange)
        - SIX (Swiss Stock Exchange)
        - OSE (Oslo Stock Exchange)

        Not supported.

        - N/A

        Returns:

        """
        return self._get_data("income-statement")

    def income_statement_growth(self) -> List[Dict]:
        """
        Get income statements growth

        Exchanges supported

        - NASDAQ
        - NYSE (New York Stock Exchange)
        - XETRA (German Electronic Exchange)
        - ASX (Australian Stock Exchange)
        - TSX (Toronto Stock Exchange)
        - ENX (EuroNext)
        - NSE (National Stock Exchange of India)
        - LSE (London Stock Exchange)
        - MOEX (Moscow Stock Exchange)
        - HKEX (Hong Kong Stock Exchange)
        - SIX (Swiss Stock Exchange)
        - OSE (Oslo Stock Exchange)

        Not supported.

        - N/A

        Returns:
        """
        return self._get_data("income-statement-growth")

    def balance_sheet(self) -> List[Dict]:
        """
        Get balance sheets

        Exchanges supported

        - NASDAQ
        - NYSE (New York Stock Exchange)
        - XETRA (German Electronic Exchange)
        - ASX (Australian Stock Exchange)
        - TSX (Toronto Stock Exchange)
        - ENX (EuroNext)
        - NSE (National Stock Exchange of India)
        - LSE (London Stock Exchange)
        - MOEX (Moscow Stock Exchange)
        - HKEX (Hong Kong Stock Exchange)
        - SIX (Swiss Stock Exchange)
        - OSE (Oslo Stock Exchange)

        Not supported.

        - N/A

        Returns:
        """
        return self._get_data("balance-sheet-statement")

    def balance_sheet_growth(self) -> List[Dict]:
        """
        Get balance sheets growth

        Exchanges supported

        - NASDAQ
        - NYSE (New York Stock Exchange)
        - XETRA (German Electronic Exchange)
        - ASX (Australian Stock Exchange)
        - TSX (Toronto Stock Exchange)
        - ENX (EuroNext)
        - NSE (National Stock Exchange of India)
        - LSE (London Stock Exchange)
        - MOEX (Moscow Stock Exchange)
        - HKEX (Hong Kong Stock Exchange)
        - SIX (Swiss Stock Exchange)
        - OSE (Oslo Stock Exchange)

        Not supported.

        - N/A

        Returns:
        """
        return self._get_data("balance-sheet-statement-growth")

    def cash_flow(self) -> List[Dict]:
        """
        Get cash flow statements

        Exchanges supported

        - NASDAQ
        - NYSE (New York Stock Exchange)
        - XETRA (German Electronic Exchange)
        - ASX (Australian Stock Exchange)
        - TSX (Toronto Stock Exchange)
        - ENX (EuroNext)
        - NSE (National Stock Exchange of India)
        - LSE (London Stock Exchange)
        - MOEX (Moscow Stock Exchange)
        - HKEX (Hong Kong Stock Exchange)
        - SIX (Swiss Stock Exchange)
        - OSE (Oslo Stock Exchange)

        Not supported.

        - N/A

        Returns:
        """
        return self._get_data("cash-flow-statement")

    def cash_flow_growth(self) -> List[Dict]:
        """
        Get cash flow statements growth

        Exchanges supported

        - NASDAQ
        - NYSE (New York Stock Exchange)
        - XETRA (German Electronic Exchange)
        - ASX (Australian Stock Exchange)
        - TSX (Toronto Stock Exchange)
        - ENX (EuroNext)
        - NSE (National Stock Exchange of India)
        - LSE (London Stock Exchange)
        - MOEX (Moscow Stock Exchange)
        - HKEX (Hong Kong Stock Exchange)
        - SIX (Swiss Stock Exchange)
        - OSE (Oslo Stock Exchange)

        Not supported.

        - N/A

        Returns:
        """
        return self._get_data("cash-flow-statement-growth")

    def ratios(self) -> List[Dict]:
        """
        Get key financial ratios

        Exchanges supported

        - NASDAQ
        - NYSE (New York Stock Exchange)
        - XETRA (German Electronic Exchange)
        - ASX (Australian Stock Exchange)
        - TSX (Toronto Stock Exchange)
        - ENX (EuroNext)
        - NSE (National Stock Exchange of India)
        - LSE (London Stock Exchange)
        - MOEX (Moscow Stock Exchange)
        - HKEX (Hong Kong Stock Exchange)
        - SIX (Swiss Stock Exchange)

        Not supported.

        - OSE (Oslo Stock Exchange)

        Returns:
        """
        return self._get_data("ratios")

    def enterprise_values(self) -> List[Dict]:
        """
        Get enterprise values

        Exchanges supported

        - NASDAQ
        - NYSE (New York Stock Exchange)
        - XETRA (German Electronic Exchange)
        - ASX (Australian Stock Exchange)
        - TSX (Toronto Stock Exchange)
        - ENX (EuroNext)
        - NSE (National Stock Exchange of India)
        - LSE (London Stock Exchange)
        - MOEX (Moscow Stock Exchange)
        - HKEX (Hong Kong Stock Exchange)
        - SIX (Swiss Stock Exchange)

        Not supported.

        - OSE (Oslo Stock Exchange)

        Returns:
        """
        return self._get_data("enterprise-values")

    def key_metrics(self) -> List[Dict]:
        """
        Get key financial metrics

        Exchanges supported

        - NASDAQ
        - NYSE (New York Stock Exchange)
        - XETRA (German Electronic Exchange)
        - ASX (Australian Stock Exchange)
        - TSX (Toronto Stock Exchange)
        - ENX (EuroNext)
        - NSE (National Stock Exchange of India)
        - LSE (London Stock Exchange)
        - MOEX (Moscow Stock Exchange)
        - HKEX (Hong Kong Stock Exchange)
        - SIX (Swiss Stock Exchange)
        - OSE (Oslo Stock Exchange)

        Not supported.

        - N/A

        Returns:
        """
        return self._get_data("key-metrics")

    def analyst_estimates(self) -> List[Dict]:
        """
        Get analyst estimates of key financial figures

        Exchanges supported

        - NASDAQ
        - NYSE (New York Stock Exchange)
        - XETRA (German Electronic Exchange)
        - ASX (Australian Stock Exchange)
        - TSX (Toronto Stock Exchange)
        - ENX (EuroNext)
        - NSE (National Stock Exchange of India)
        - LSE (London Stock Exchange)
        - MOEX (Moscow Stock Exchange)
        - HKEX (Hong Kong Stock Exchange)
        - SIX (Swiss Stock Exchange)
        - OSE (Oslo Stock Exchange)

        Not supported.

        - N/A

        Returns:
        """
        return self._get_data("analyst-estimates")

    def shares_float(self) -> List[Dict]:
        """
        Get shares float and outstanding

        Exchanges supported

        - NASDAQ
        - NYSE (New York Stock Exchange)
        - XETRA (German Electronic Exchange)
        - ASX (Australian Stock Exchange)
        - TSX (Toronto Stock Exchange)
        - ENX (EuroNext)
        - NSE (National Stock Exchange of India)
        - LSE (London Stock Exchange)
        - MOEX (Moscow Stock Exchange)
        - HKEX (Hong Kong Stock Exchange)
        - SIX (Swiss Stock Exchange)

        Not supported.

        - OSE (Oslo Stock Exchange)

        Returns:
        """
        return self._get_data("shares-float")

    def quote(self) -> List[Dict]:
        """
        Get up to date quote

        Exchanges supported

        - NASDAQ
        - NYSE (New York Stock Exchange)
        - XETRA (German Electronic Exchange)
        - ASX (Australian Stock Exchange)
        - TSX (Toronto Stock Exchange)
        - ENX (EuroNext)
        - NSE (National Stock Exchange of India)
        - LSE (London Stock Exchange)
        - MOEX (Moscow Stock Exchange)
        - HKEX (Hong Kong Stock Exchange)
        - SIX (Swiss Stock Exchange)

        Not supported.

        - OSE (Oslo Stock Exchange)

        Returns:
        """
        return self._get_data("quote")

    def profile(self) -> List[Dict]:
        """
        Get company profile

        Exchanges supported

        - NASDAQ
        - NYSE (New York Stock Exchange)
        - XETRA (German Electronic Exchange)
        - ASX (Australian Stock Exchange)
        - TSX (Toronto Stock Exchange)
        - ENX (EuroNext)
        - NSE (National Stock Exchange of India)
        - LSE (London Stock Exchange)
        - MOEX (Moscow Stock Exchange)
        - HKEX (Hong Kong Stock Exchange)
        - SIX (Swiss Stock Exchange)

        Not Supported.

        - OSE (Oslo Stock Exchange)

        Returns:
        """
        return self._get_data("profile")

    def insider_transactions(self, months: int = None) -> List[Dict]:
        """
        Get all insider transactions

        Exchanges supported

        - NASDAQ
        - NYSE (New York Stock Exchange)
        - XETRA (German Electronic Exchange)
        - ASX (Australian Stock Exchange)

        Not supported.

        - TSX (Toronto Stock Exchange)
        - ENX (EuroNext)
        - NSE (National Stock Exchange of India)
        - LSE (London Stock Exchange)
        - MOEX (Moscow Stock Exchange)
        - HKEX (Hong Kong Stock Exchange)
        - SIX (Swiss Stock Exchange)

        Returns:
        """

        # TODO: Add months parameter.
        return self._get_data("insider-transactions", months=months)

    def insider_transactions_summarized(self, months: int = None) -> List[Dict]:
        """
        Get insider transactions summarized

        Exchanges supported

        - NASDAQ
        - NYSE (New York Stock Exchange)
        - XETRA (German Electronic Exchange)
        - ASX (Australian Stock Exchange)

        Not supported.

        - TSX (Toronto Stock Exchange)
        - ENX (EuroNext)
        - NSE (National Stock Exchange of India)
        - LSE (London Stock Exchange)
        - MOEX (Moscow Stock Exchange)
        - HKEX (Hong Kong Stock Exchange)
        - SIX (Swiss Stock Exchange)

        Returns:
        """
        # TODO: Add months parameter.
        return self._get_data("insider-transactions-summarized", months=months)

    def share_ownership(self) -> List[Dict]:
        """
        Get share owning groups

        Exchanges supported

        - NASDAQ
        - NYSE (New York Stock Exchange)
        - XETRA (German Electronic Exchange)
        - ASX (Australian Stock Exchange)
        - TSX (Toronto Stock Exchange)
        - ENX (EuroNext)
        - NSE (National Stock Exchange of India)
        - LSE (London Stock Exchange)
        - MOEX (Moscow Stock Exchange)
        - HKEX (Hong Kong Stock Exchange)
        - SIX (Swiss Stock Exchange)
        - OSE (Oslo Stock Exchange)

        Not Supported.

        - N/A

        Returns:
        """
        return self._get_data("share-ownership")

    def key_executives(self) -> List[Dict]:
        """
        Get key executives in org

        Exchanges supported

        - NASDAQ
        - NYSE (New York Stock Exchange)
        - XETRA (German Electronic Exchange)
        - ASX (Australian Stock Exchange)
        - TSX (Toronto Stock Exchange)
        - ENX (EuroNext)
        - NSE (National Stock Exchange of India)
        - LSE (London Stock Exchange)
        - MOEX (Moscow Stock Exchange)
        - HKEX (Hong Kong Stock Exchange)
        - SIX (Swiss Stock Exchange)
        - OSE (Oslo Stock Exchange)

        Not Supported.

        - N/A

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
