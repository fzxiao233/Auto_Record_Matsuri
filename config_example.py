config = {
    'enable_proxy': False,
    'proxy': '',
    'ddir': '/home/ubuntu/Matsuri',
    'sec': 15,
    'error_sec': 5,
    'enable_bot': False,
    'bot_host': '',
    'group_id': [],
    'bot_token': '',
    'enable_upload': True,
    'upload_by': 'bd',
    'enable_mongodb': False,
    's3_server': '',
    's3_access_key': '',
    's3_secret_key': '',
    'youtube': {
        'enable': True,
        'enable_temp': False,
        'enable_temp_bot_notice': True,
        'enable_temp_download': True,
        'quality': '720p',
        'api_key': '',
        'users': [
            {
                'target_id': 'UCQ0UDLQCjY0rmuxCDE38FGg',
                'bot_notice': True,
                'download': True
            },
            {
                'target_id': 'UCl_gCybOJRIgOXw6Qb4qJzQ',
                'ddir': 'rushia',
                'bot_notice': False,
                'download': True
            }
        ]
    },
    'twitcasting': {
        'enable': True,
        'users': [
            {
                'target_id': 'natsuiromatsuri',
                'bot_notice': True,
                'download': True
            }
        ]
    },
    'mirrativ': {
        'enable': True,
        'users': [
            {
                'target_id': '3264432',
                'bot_notice': True,
                'download': True
            }
        ]
    },
    'openrec': {
        'enable': True,
        'users': [
            {
                'target_id': 'natsuiromatsuri',
                'bot_notice': True,
                'download': True
            }
        ]
    },
    'bilibili': {
        'enable': True,
        'users': [
            {
                'target_id': '336731767',
                'bot_notice': True,
                'download': True
            }
        ]
    }
}
