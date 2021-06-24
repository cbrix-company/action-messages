# Github Action - Messages

This action is designed to take input from a range of security tools, parse it and render it to a message format like e.g. Slack or Email.

This action's outputs can be passed onto [cbrix-company/action-notifier](https://github.com/cbrix-company/action-notifier) which is responsible for sending messages.

Supported message formats:
* Slack

Supported inputs:
* Bandit

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

    # github inputs that could be needed for rendering a message
    repository: ${{ github.repository }}
    ref: ${{ github.ref }}
    actor: ${{ github.actor }}
    run_id: ${{ github.run_id }}
    sha: ${{ github.sha }}
```

## Outputs
```yaml
# rendered message
${{ steps.bandit-to-slack.outputs.output-file }}

# to check if message is empty
${{ steps.bandit-to-slack.outputs.isEmpty }}
```
