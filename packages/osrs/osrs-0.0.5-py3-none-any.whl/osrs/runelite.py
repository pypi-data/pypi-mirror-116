import requests


class RunelitePrices:
    base_url = 'https://prices.runescape.wiki/api/v1/osrs/'

    def __init__(self, identification: str):
        self.header = {'user-agent': identification}
        self.item_list = None

    def items(self) -> list:
        # contains id => name
        if not self.item_list:
            url = f'{self.base_url}/mapping'
            self.item_list = requests.get(url, headers=self.header).json()
        return self.item_list

    def prices(self, interval: str, timestamp: int = None) -> dict:
        # timestamp must be unix timestamp
        url = f'{self.base_url}/{interval}'

        param = dict()
        param['timestamp'] = timestamp

        data = requests.get(url, headers=self.header, params=param).json()
        return data

    def timeseries(self, interval: str, id: int = None, name: str = None) -> dict:
        # how can i make it so an item name can be provided => name to id is in the /mapping endpoint (see items)
        if name:
            if self.item_list is None:
                self.items()
            for item in self.item_list:
                if name == item['name']:
                    id = int(item['id'])
                    break

        url = f'{self.base_url}/timeseries'

        param = dict()
        param['id'] = int(id)
        param['timestep'] = interval

        data = requests.get(url, headers=self.header, params=param).json()
        return data

    def latest(self) -> dict:
        url = f'{self.base_url}/latest'
        data = requests.get(url, headers=self.header).json()
        return data
