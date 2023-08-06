# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['psycopg2_iam']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.14,<2.0', 'psycopg2-binary>=2.8,<3.0']

setup_kwargs = {
    'name': 'psycopg2-iam',
    'version': '1.1.0',
    'description': 'Custom Connection Factory class (RDS, Redshift) with build-in IAM authentication and SSL bundle downloader support.',
    'long_description': '# psycopg2-iam\n\nCustom Connection Factory class (RDS, Redshift) with build-in IAM authentication and SSL bundle downloader support.\n\n## Installation\n\nInstall package\n\n```\npoetry add psycopg2-iam\n```\n\n## Usage\n\n### Create connection directly from secret\n```python\nfrom psycopg2_iam import connect\n\nconn = connect(secret="secretId")\n```\n\n### Using connect function \n\n```python\nfrom psycopg2_iam import connect\nconnect(dsn="...")\n```\n\n### Pass connection factory class to psycopg2.connect()\n\n```python\nimport psycopg2 \nfrom psycopg2_iam import IAMConnection\n\npsycopg2.connect(dsn="...", connection_factory=IAMConnection)\n```\n\n### Create DSN from AWS generated RDS secret\n\n```python\nimport boto3\nimport json\nimport psycopg2 \nfrom psycopg2_iam import IAMConnection, dsn_from_rds_secret\n\nsecrets = boto3.client("secretsmanager")\ndb_secret = json.loads(secrets.get_secret_value(SecretId="/dynks/rds/readonly").get("SecretString"))\n\npsycopg2.connect(dsn=dsn_from_rds_secret(db_secret), connection_factory=IAMConnection)\n```\n',
    'author': 'Epsy Engineering',
    'author_email': 'engineering@epsyhealth.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/epsyhealth/psycopg2-iam',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
