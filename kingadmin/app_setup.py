from django import conf


def kingadmin_setup():
    for app_name in conf.settings.INSTALLED_APPS:
        try:
            __import__('%s.kingadmin' % app_name)

        except ImportError:
            pass