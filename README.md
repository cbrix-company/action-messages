# Cbrix Notifier

This action takes various parsed security tool inputs and notifies a communication channel

Supported channels:
* Slack

## Example usage

```yaml
- name: Bandit Notifier
  uses: cbrix-company/action-notifier@v1
  with:
    tool: bandit
    output-file: 'bandit_output.json'
    repo-name: $GITHUB_REPOSITORY
    slack-token: ${{ secrets.SLACK_TOKEN }}
    slack-channel: ${{ secrets.SLACK_CHANNEL_ID }}
```
