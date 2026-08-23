# oncall-shift-reporter

A Helm chart for oncall-shift-reporter

**Homepage:** <https://github.com/giantswarm/oncall-shift-reporter>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| image.registry | string | `"gsoci.azurecr.io"` |  |
| image.name | string | `"giantswarm/oncall-shift-reporter"` |  |
| image.tag | string | `""` |  |
| slack.key | string | `""` |  |
| pagerduty.auth_token | string | `""` |  |
| global.podSecurityStandards.enforced | bool | `false` |  |
