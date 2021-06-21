class MessageBuilderBase:
    """
        message_builder = BanditMessageBuilder()
        message_builder.render_to_slack()
        message_builder.render_to_email()
    """

    def __init__(self, output, **context):
        self.output
        self.context = context
        self.context.update(self.parse())

    def parse(self):
        raise NotImplementedError

    def is_empty(self):
        raise NotImplementedError

    def render_to_slack(self):
        raise NotImplementedError
