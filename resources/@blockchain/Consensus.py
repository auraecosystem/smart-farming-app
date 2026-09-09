class Blockchain:

    def __init__(self, consensus):

        self.consensus = consensus
        self.chain = []

        self.create_genesis_block()

    def create_genesis_block(self):

        genesis = Block(
            index=0,
            data="Genesis Block",
            previous_hash="0"
        )

        self.chain.append(genesis)

    def add_block(self, block):

        previous_block = self.chain[-1]

        block.previous_hash = (
            previous_block.hash
        )

        if not self.consensus.validate_block(
            block
        ):
            raise ValueError(
                "Block rejected by consensus"
            )

        self.chain.append(block)

    def validate_chain(self):

        for i in range(
            1,
            len(self.chain)
        ):

            current = self.chain[i]

            previous = self.chain[i - 1]

            if (
                current.previous_hash
                != previous.hash
            ):
                return False

            if (
                current.hash
                != current.compute_hash()
            ):
                return False

        return True
