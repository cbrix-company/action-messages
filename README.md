# Cbrix Notifier

This action takes parses various outputs that can be passed onto [cbrix-company/action-notifier](https://github.com/cbrix-company/action-notifier)

Supported channels:
* Slack

## Example usage

### Slack & Bandit

```yaml
- name: Parse Bandit output
  uses: cbrix-company/action-messages@v1
  with:
    tool: bandit
    input-file: 'bandit_output.json'
    message-type: slack
    repo-name: $GITHUB_REPOSITORY
```

### Full pipeline with notifier

In combination with the [cbrix-company/action-notifier](https://github.com/cbrix-company/action-notifier), you can pass the output of the `cbrix-company/action-messages`

```yaml
name: Python Security

on: [push]

jobs:
  Bandit:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2


    - name: Set up Python 3.8
      uses: actions/setup-python@v2
      with:
        python-version: 3.8

    - name: install bandit
      run: |
        python -m pip install bandit

    - name: run bandit
      continue-on-error: true
      run: |
        python -m bandit -f json -o bandit.json -r .


    - name: Parse Bandit output
      id: bandit-message
      uses: cbrix-company/action-messages@v1
      with:
        tool: bandit
        input-file: 'bandit.json'
        message-type: slack
        repo-name: $GITHUB_REPOSITORY

    - name: Notifier
      if: steps.bandit-message.outputs.isEmpty != 'true'
      uses: cbrix-company/action-notifier@v1
      with:
        slack-token: ${{ secrets.SLACK_TOKEN }}
        slack-channel: ${{ secrets.SLACK_CHANNEL_ID }}
```

### Full pipeline with notifier and timeframe caching

```yaml
name: Python Security

on: [push]

jobs:
  Bandit:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2


    - name: Set up Python 3.8
      uses: actions/setup-python@v2
      with:
        python-version: 3.8

    - name: install bandit
      run: |
        python -m pip install bandit

    - name: run bandit
      continue-on-error: true
      run: |
        python -m bandit -f json -o bandit.json -r .


    - name: Parse Bandit output
      id: bandit-message
      uses: cbrix-company/action-messages@v1
      with:
        tool: bandit
        input-file: 'bandit.json'
        message-type: slack
        repo-name: $GITHUB_REPOSITORY


    - name: Determine timeframe
      uses: cbrix-company/action-notifier-timeframe@v1
      id: timeframe
      with:
        time-unit: minutes
        interval: 5

    - name: Notify Cache
      id: cache
      if: steps.bandit-message.outputs.isEmpty != 'true'
      uses: actions/cache@v2
      with:
        path: ~/timeframe-locks
        key: ${{ github.repository }}-${{ steps.timeframe.outputs.timeframe }}

    - name: Notifier
      if: |
        steps.bandit-message.outputs.isEmpty != 'true' && steps.cache.outputs.cache-hit != 'true'
      uses: cbrix-company/action-notifier@v1
      with:
        slack-token: ${{ secrets.SLACK_TOKEN }}
        slack-channel: ${{ secrets.SLACK_CHANNEL_ID }}
```
