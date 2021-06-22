class BaseMessageRenderer:
    """
    Base class for rendering a message from external input for a specific communication channel

    def parse(self):
        return {}

    def render_to_slack(self):
        return {}

    def is_empty(self):
        return False
    """

    def __init__(self, output, **context):
        self.output
        self.context = context
        self.context.update(self.parse())

    def parse(self):
        raise NotImplementedError

    def is_empty(self):
        raise NotImplementedError

    @classmethod
    def list_renderers(cls):
        fn_pattern = 'render_to_'
        return [fn.split(fn_pattern)[-1] for fn in cls.__dir__() if fn.startswith(fn_pattern)]

