from giantstar.globalSetting import plus_setting
from giantstar.drivers.compatorDriver import SetVariable


class DriverBy:
    api = plus_setting.HTTP_DRIVER
    web = plus_setting.WEB_DRIVER
    app = plus_setting.APP_DRIVER
    user_kw = plus_setting.KW_DRIVER
    debug = plus_setting.DEBUG_DRIVER
    set_variable = SetVariable


class SimpleDriverBy:
    api = plus_setting.HTTP_SIMPLE_DRIVER
    web = plus_setting.WEB_SIMPLE_DRIVER
    app = plus_setting.APP_SIMPLE_DRIVER
    user_kw = plus_setting.KW_DRIVER
    debug = plus_setting.DEBUG_DRIVER
    set_variable = SetVariable
