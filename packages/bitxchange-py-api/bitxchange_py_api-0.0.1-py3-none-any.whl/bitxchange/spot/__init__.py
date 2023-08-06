from .market import Market
from .account import Account


class Spot(Market, Account):
    def __init__(
        self,
        base_url="https://exchangeapi.bit-xchange.co",
        key=None,
        secret=None
    ):
        super().__init__(base_url, key, secret)