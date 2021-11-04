import requests
from requests import HTTPError
from blockchain.clients.base import BaseBlockChainClient, APIDownException
from blockchain import Block, Transaction


class EsploraClient(BaseBlockChainClient):
    base_url = "https://blockstream.info/api"

    def _make_request(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except HTTPError as e:
            raise APIDownException("API Error") from e

        return response

    def get_block_by_height(self, block_height):
        response = self._make_request(f"{self.base_url}/block-height/{block_height}")
        return Block(
            response.text,
            block_height
        )

    def get_all_transactions(self, block_id, total=None):
        page_size = 25
        idx = 0
        has_more_txs = True

        while has_more_txs:
            response = self._make_request(f"{self.base_url}/block/{block_id}/txs/{idx}")
            transactions = response.json()

            has_more_txs = len(transactions) == page_size
            idx += page_size

            if total is not None:
                has_more_txs = total > idx

            for transaction in transactions:
                yield Transaction(
                    transaction["txid"],
                    [vin["txid"] for vin in transaction["vin"]]
                )

    def get_all_transaction_ids(self, block_id):
        response = self._make_request(f"{self.base_url}/block/{block_id}/txids")
        return response.json()
