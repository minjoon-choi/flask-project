from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'\xab\xa7\x1c\xa0\x04\x99\xe3)\x13\x1e\xeb\x01\xc5\xb6m#'