import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
sentry_sdk.init(
    dsn="https://544451623b974a929e3f99ee6f10d3e8@sentry.io/1777574",
    integrations=[FlaskIntegration()]
)
