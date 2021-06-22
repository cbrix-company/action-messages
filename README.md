# Cbrix Notifier

This action takes parses various outputs that can be passed onto [cbrix-company/action-notifier](https://github.com/cbrix-company/action-notifier)

Supported channels:
* Slack

## Examples

### Rendering [Bandit](https://github.com/PyCQA/bandit) output for Slack

```yaml
- name: Render Bandit output for slack
  id: bandit-to-slack
  uses: cbrix-company/action-messages@v1
  with:
    tool: bandit
    input-file: 'bandit_output.json'
    renderer: slack
```

## Outputs
```yaml
# rendered message
${{ steps.bandit-to-slack.outputs.message }}

# to check if message is empty
${{ steps.bandit-to-slack.outputs.isEmpty }}
```
