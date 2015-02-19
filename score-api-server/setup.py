from setuptools import setup


setup(
    name='score-api-server',
    version='1',
    author='Paco Gomez',
    author_email='pgomez@vmware.com',
    packages=['score_api_server'],
    package_data={'score_api_server': ['VERSION']},
    license='LICENSE',
    description='Score service API server',
    zip_safe=False,
    install_requires=[
        'Flask==0.10.1',
        'flask-restful==0.2.5',
        'flask-restful-swagger==0.12',
        'requests==2.2.1',
        'PyYAML==3.10',
        'pyvcloud==9',
        'cloudify-rest-client==3.1'
    ]
)