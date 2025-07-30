from setuptools import setup, find_packages

package_name = 'gptbot'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/my_house_world.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='you@example.com',
    description='Test node only package',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
    	'console_scripts': [
            'test_node = gptbot.test_node:main',
            'llm_nav = gptbot.llm_nav:main',
        ],
    },

)
