import json

from renderers import BanditMessageRenderer

from .utils import load_fixture


class TestBanditMessageRenderer:

    renderer = BanditMessageRenderer

    def test_list_renderers(self):
        self.renderer.list_renderers == ['slack']

    def test_context_data_no_results(self):
        output = load_fixture('bandit_no_results.json')
        renderer = self.renderer(output)
        assert renderer.context == {
            'top_issues': [],
            'distribution': {
                'UNDEFINED': 0,
                'LOW': 0,
                'MEDIUM': 0,
                'HIGH': 0
            },
            'runtime': '2021-06-13T18:31:06Z'
        }

    def test_context_data_with_results(self):
        output = load_fixture('bandit_with_results.json')
        renderer = self.renderer(output)
        assert renderer.context == {
            'top_issues': [
                (
                    0,
                    1,
                    2,
                    'test_package/password.py',
                    "Possible hardcoded password: 'root'",
                    (
                        '1 def someFunction2(password):\n2'
                        '     if password == "root":\n3'
                        '         print("OK, logged in")\n'
                    ),
                    2,
                    'LOW'
                )
            ],
            'distribution': {
                'UNDEFINED': 0,
                'LOW': 1,
                'MEDIUM': 0,
                'HIGH': 0
            },
            'runtime': '2021-06-13T18:31:06Z'
        }

    def test_is_empty_no_results(self):
        output = load_fixture('bandit_no_results.json')
        renderer = self.renderer(output)
        assert renderer.is_empty()

    def test_is_empty_with_results(self):
        output = load_fixture('bandit_with_results.json')
        renderer = self.renderer(output)
        assert not renderer.is_empty()

    def test_render_to_slack(self):
        output = load_fixture('bandit_with_results.json')
        renderer = self.renderer(output, repository='cbrix-company/test')
        message = renderer.render_to_slack()
        assert json.loads(message) == {
            'blocks': [
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': (
                            '*Security Control:* Bandit\n'
                            '*Repo:* cbrix-company/test\n'
                            '*Run time:* 2021-06-13T18:31:06Z\n'
                            '*Output:* Link\n'
                            '*Findings:* High (0), Medium (0), Low (1)\n\n\n'
                            '*Top Findings:*'
                        )
                    }
                },
                {
                    'type': 'divider'
                },
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': (
                            '*Finding #1*\n\n'
                            '*Name:* Possible hardcoded password: \'root\'\n'
                            '*Filename:* test_package/password.py\n'
                            '*Line number:* 2\n'
                            '*Severity:* LOW\n'
                            '```'
                                '1 def someFunction2(password):\n'
                                '2     if password == "root":\n'
                                '3         print("OK, logged in")\n'
                            '```'
                        )
                    }
                }
            ]
        }
