
from blockchain.clients.esplora import EsploraClient
from blockchain.clients.base import APIDownException

DEFAULT_CLIENT = EsploraClient()


def get_transactions_with_largest_ancestry(block_height, limit=10):
    # Get the block hash ID using the height
    block = DEFAULT_CLIENT.get_block_by_height(block_height)

    # Keep a copy of all tx ids which are part of the block
    all_transaction_ids = DEFAULT_CLIENT.get_all_transaction_ids(block.id)

    # Keep a copy of all txs in the block easily accessible using
    # the tx id
    all_transactions = {
        tx.tx_id: tx
        for tx in DEFAULT_CLIENT.get_all_transactions(block.id, total=len(all_transaction_ids))
    }

    # For each transaction in the block, we want to filter out the ones
    # which do not have any parent inputs which are part of the block
    filtered_transactions = []
    for transaction in all_transactions.values():
        has_ancestry = False

        # Check whether at least one parent tx is part of the same block
        for parent_tx_id in transaction.parent_tx_ids:
            if parent_tx_id in all_transaction_ids:
                transaction.add_parent(all_transactions[parent_tx_id])
                has_ancestry = True

        if has_ancestry:
            filtered_transactions.append(transaction)

    # For transactions which have at least one parent in the same block,
    # calculate the ancestry set size i.e. the number of ancestors which are
    # part of the same block
    for transaction in filtered_transactions:
        transaction.calculate_ancenstry_size()

    # Then we just need to sort transactions using the ancestry set size
    sorted_transactions = [
        (tx.tx_id, tx.ancestry_size)
        for tx in sorted(filtered_transactions, key=lambda tx: tx.ancestry_size, reverse=True)
    ]

    return sorted_transactions[:limit]

if __name__ == "__main__":
    try:
        transactions_with_largest_ancestry = get_transactions_with_largest_ancestry(680000)
    except APIDownException:
        logger.info("Invalid input or API error")
    else:
        print("Tx Hash: Ancestry Size")
        for tx in transactions_with_largest_ancestry:
            print(f"{tx[0]}: {tx[1]}")
