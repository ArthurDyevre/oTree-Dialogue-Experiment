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
        'name': 'V3_TP12_EBRT',
        'display_name': "App of Treatments V03: Lottery > Risk > EBRT",
        'num_demo_participants': 2,
        'app_sequence': ['lottery', 'mpl','eliciting_beliefs_rt'],
        'my_page_timeout_seconds': 500,
    },
    {
        'name': 'V4_TP1_EBRT',
        'display_name': "App of Treatments V04: Lottery > Risk > TP1 EBRT",
        'num_demo_participants': 2,
        'app_sequence': ['lottery', 'mpl', 'eliciting_beliefs_rt_TP1'],
        'my_page_timeout_seconds': 500,
    },
    {
        'name': 'V4_TP12_EBRT',
        'display_name': "App of Treatments V04: Lottery > Risk > TP12 EBRT",
        'num_demo_participants': 2,
        'app_sequence': ['lottery', 'mpl', 'eliciting_beliefs_rt_TP12'],
        'my_page_timeout_seconds': 500,
    },
    {
        'name': 'V4_TP12D_EBRT',
        'display_name': "App of Treatments V04: Lottery > Risk > TP12D EBRT",
        'num_demo_participants': 2,
        'app_sequence': ['lottery', 'mpl', 'eliciting_beliefs_rt_TP12D'],
        'my_page_timeout_seconds': 500,
    },
    # Note: change the app sequence to try the other subsessions
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

