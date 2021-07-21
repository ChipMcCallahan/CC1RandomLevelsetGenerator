from setuptools import setup, find_packages

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='cc1_random_levelset_generator',
    url='https://github.com/ChipMcCallahan/CC1RandomLevelsetGenerator',
    author='Chip McCallahan',
    author_email='thisischipmccallahan@gmail.com',
    # Needed to actually package something
    packages=find_packages(),
    # Needed for dependencies
    install_requires=[
        'cc1_levelset_proto @ git+https://github.com/ChipMcCallahan/CC1LevelsetProto',
        'cc1_levelset_io @ git+https://github.com/ChipMcCallahan/CC1LevelsetIO',
    ],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='GNU General Public License v3.0',
    description='Randomly generate levelset from a customized pool of input levelsets.',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)