
class APIDownException(Exception):
    pass


class BaseBlockChainClient(object):
    def get_block_by_height(self, block_height):
        raise NotImplementedError

    def get_all_transactions(self, block_id):
        raise NotImplementedError

    def get_all_transaction_ids(self, block_id):
        raise NotImplementedError
