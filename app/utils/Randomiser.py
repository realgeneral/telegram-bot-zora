import random


class Randomiser:

    @staticmethod
    def mintPrice():
        return round(random.uniform(0.00001, 3), 5)

    @staticmethod
    def mintLimitPerAddress():
        return random.randint(2, 5000)

    @staticmethod
    def editionSize():
        return random.randint(10, 9999)

    @staticmethod
    def royaltyBPS():
        return random.randint(1, 15)