import json

from .base import BaseMessageRenderer


class BanditMessageRenderer(BaseMessageRenderer):
    """
    Renders top 2 bandit findings
    """

    LEVELS = {
        'UNDEFINED': 0,
        'LOW': 1,
        'MEDIUM': 2,
        'HIGH': 3,
    }

    message_header = (
        "*Security Control:* Bandit\n"
        "*Repo:* {repo_name}\n"
        "*Run time:* {runtime}\n"
        "*Output:* Link\n"
        '*Findings:* High ({high}), Medium ({medium}), Low ({low})\n\n\n'
        "*Top Findings:*"
    )

    def get_context_data(self):
        distribution = {
            'UNDEFINED': 0,
            'LOW': 0,
            'MEDIUM': 0,
            'HIGH': 0,
        }

        results = []
        for idx, result in enumerate(self.input['results']):
            issue_severity = result['issue_severity']
            distribution[issue_severity] += 1
            issue_confidence = result['issue_confidence']
            results.append(
                (
                    idx,
                    self.__class__.LEVELS[issue_severity],
                    self.__class__.LEVELS[issue_confidence],
                    result['filename'],
                    result['issue_text'],
                    result['code'],
                    result['line_number'],
                    issue_severity,
                )
            )

        sorted_by_severity = sorted(results, key=lambda x: x[1], reverse=True)
        sorted_by_confidence = sorted(sorted_by_severity, key=lambda x: x[2], reverse=True)

        return {
            'top_issues': sorted_by_confidence[:2],
            'distribution': distribution,
            'runtime': self.input['generated_at'],
        }

    def is_empty(self):
        return len(self.input['results']) > 0

    def render_to_slack(self):
        repo_name = self.context['repository']
        distribution = self.context['distribution']
        runtime = self.context['runtime']

        high = distribution["HIGH"]
        medium = distribution["MEDIUM"]
        low = distribution["LOW"]

        msg_data = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": self.__class__.message_header.format(
                        repo_name=repo_name,
                        runtime=runtime,
                        high=high,
                        medium=medium,
                        low=low
                    ),
                }
            },
            {
                "type": "divider"
            },
        ]

        for idx, finding in enumerate(self.context['top_issues']):
            name = finding[4]
            file_name = finding[3]
            line = finding[6]
            severity = finding[7]
            code = finding[5]
            block_text = (
                f"*Finding #{idx+1}*\n\n"
                f"*Name:* {name}\n"
                f"*Filename:* {file_name}\n"
                f"*Line number:* {line}\n"
                f"*Severity:* {severity}\n```{code}```"
            )

            block = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": block_text
                }
            }

            msg_data.append(block)

        return json.dumps({'blocks': msg_data}, separators=(',', ':'))
