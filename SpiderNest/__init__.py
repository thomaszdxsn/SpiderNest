from dynaconf import settings as dyna_settings, Validator
import sentry_sdk

# 在生产环境应用sentry
if dyna_settings.ENV_FOR_DYNACONF == 'production':
    sentry_sdk.init(dyna_settings.SENTRY_DSN)


# 验证配置数据是否齐全
dyna_settings.validators.register(
    Validator('SENTRY_DSN', must_exist=True, env='production'),
)

dyna_settings.validators.validate()