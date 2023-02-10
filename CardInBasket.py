class CardInBasket:
    count_id = 0

    # initializer method
    def __init__(self, id, name, type, price, rarity, booster, description, inPack):
        CardInBasket.count_id += 1

        self.__id = id
        self.__name = name
        self.__type = type
        self.__price = price
        self.__rarity = rarity
        self.__booster = booster
        self.__description = description
        self.__inPack = False

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__type

    def get_price(self):
        return self.__price

    def get_rarity(self):
        return self.__rarity

    def get_booster(self):
        return self.__booster

    def get_description(self):
        return self.__description

    def get_inPack(self):
        return self.__inPack
