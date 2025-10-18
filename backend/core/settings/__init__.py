import os


# Keep at the end
if os.getenv('PIPELINE') == 'production':
    from .production import *
else:
    from .dev import *