from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='chaosgenius',
    version='0.0.1',
    url='https://github.com/chaos-genius/chaos_genius',
    author='Chaos Genius Team',
    author_email='manas@chaosgenius.io',
    description='Chaos Genius: The Open-Source Business Observability Platform',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'click'
    ],
    entry_points='''
        [console_scripts]
        chaosgenius=app:cli
    '''
)
