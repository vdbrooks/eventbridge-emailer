from json2table import convert

# Loads templates from the yourapp.templates folder


class BuildTable(object):
    """
    A class used to represent a table builder

    ...

    Methods
    -------
    build(self)
        Builds the html table from the eventbridge event
    """

    def __init__(self, event):
        """
        Parameters
        ----------
        event : dict
            The event passed to lambda
        build_direction : str
            The direction to build table from event
        table_attributes : dict
            Style options for the table
        """

        self.event = event
        self.build_direction = "TOP_TO_BOTTOM"
        self.table_attributes = {"style": "width:50%"}

    def build(self):
        """Converts the event into an html table using table attributes provided."""

        table = convert(
            self.event,
            build_direction=self.build_direction,
            table_attributes=self.table_attributes)
        print(table)
        return table
