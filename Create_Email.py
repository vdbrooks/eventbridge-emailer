from jinja2 import Environment, PackageLoader

# Loads templates from the yourapp.templates folder
env = Environment(loader=PackageLoader('emailer', 'templates'))


class Create_Email(object):
    def __init__(self, event, custom_event):
        self.event = event
        self.custom_event = custom_event

    def _render(self, filename, event):
        try:
            template = env.get_template(filename)

            return template.render(event=self.custom_event)
        except Exception as e:
            print("Ran into the following error: \n" + str(e))

    def make_html(self, filename, context):
        html = self._render(filename, context)
        return html

    def text(self, filename, context):
        self._text = self._render(filename, context)

    # def send(self, from_addr=None):
        # Same as before...
