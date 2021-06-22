from renderers import BaseMessageRenderer


class DummyMessageRenderer(BaseMessageRenderer):

    def get_context_data(self):
        context = super().get_context_data()
        context['test'] = 'test'
        return context

    def render_to_slack(self):
        return 'test slack message'

    def is_empty(self):
        return False


class TestBaseMessageRenderer:

    def test_constructor(self):
        renderer = DummyMessageRenderer('test')
        assert renderer.output == 'test'
        assert renderer.context == {'test': 'test'}
        assert not renderer.is_empty()
        assert renderer.render_to_slack() == 'test slack message'
        assert renderer.list_renderers() == ['slack']
