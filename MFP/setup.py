from setuptools import setup, find_packages

# from os.path import join, dirname


setup(
    name='My Framework on Python(WSGI)',
    version='less_1',
    packages=find_packages(),
    # long_description=open(join(dirname(__file__), 'README.txt')).read(),
    install_requires=[
        'gunicorn==20.0.4',
        'Jinja2==2.11.3',
        'MarkupSafe==1.1.1'
    ],
)
