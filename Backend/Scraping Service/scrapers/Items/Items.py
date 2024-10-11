from scrapy.item import Item, Field


class VehicleItem(Item):
    url = Field()
    _id = Field()
    title = Field()
    price = Field()
    details = Field()