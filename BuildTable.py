from json2table import convert

# Loads templates from the yourapp.templates folder


class BuildTable(object):
    def __init__(self, event):
        self.event = event
        self.build_direction = "TOP_TO_BOTTOM"
        self.table_attributes = {"style": "width:50%"}

    def build(self):
        table = convert(
            self.event,
            build_direction=self.build_direction,
            table_attributes=self.table_attributes)
        print(table)
        return table
