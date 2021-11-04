class Block(object):
    def __init__(self, id, height):
        self.id = id
        self.height = height


class Transaction(object):
    def __init__(self, tx_id, parent_tx_ids):
        self.tx_id = tx_id
        self.parent_tx_ids = parent_tx_ids

        self.parent_txs = []
        self.ancestry_size = None

    def add_parent(self, parent_tx):
        if parent_tx not in self.parent_txs:
            self.parent_txs.append(parent_tx)

    def calculate_ancenstry_size(self):
        if self.ancestry_size is None:
            ancestry_size = 0

            for parent_tx in self.parent_txs:
                ancestry_size += parent_tx.calculate_ancenstry_size() + 1

            self.ancestry_size = ancestry_size

        return self.ancestry_size

