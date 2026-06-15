module github.com/giantswarm/oncall-shift-reporter

go 1.25.0

require (
	github.com/PagerDuty/go-pagerduty v1.8.0
	github.com/nlopes/slack v0.6.0
)

require (
	github.com/google/go-querystring v1.1.0 // indirect
	github.com/gorilla/websocket v1.2.0 // indirect
	github.com/pkg/errors v0.8.1 // indirect
	github.com/stretchr/testify v1.7.0 // indirect
)

replace golang.org/x/crypto v0.17.0 => golang.org/x/crypto v0.53.0

replace golang.org/x/sys v0.15.0 => golang.org/x/sys v0.46.0
