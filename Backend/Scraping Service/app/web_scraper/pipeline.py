class PrintItemPipeline:
    def process_item(self, item, spider):
        print(item)
        return item

