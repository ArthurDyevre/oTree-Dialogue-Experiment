from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.00,
    'participation_fee': 0.00,
    'doc': "",
}

SESSION_CONFIGS = [

    {
        'name': 'mpl',
        'display_name': "Decision Games 2019",
        'num_demo_participants': 2,
        'app_sequence': ['lottery', 'mpl','eliciting_beliefs_rt'],
        'my_page_timeout_seconds': 60,
    },
    # Note: Use the Server Check tab in oTree to update system requirements
    # 1. download postgresql-10.9-2-windows-x64
    # 2. select the postgresql-10.9-2-windows-x64 package in the download process
    # other session configs go here ...
]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

POINTS_DECIMAL_PLACES = 2


SECRET_KEY = '2(r3#hsqco1!y9+@7a#v&s%ew)3atexw+4#hl11vrdh!*coavf'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

