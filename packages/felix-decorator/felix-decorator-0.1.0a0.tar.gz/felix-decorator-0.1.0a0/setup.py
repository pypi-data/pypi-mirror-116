from setuptools import find_packages, setup

import felix


EXTRAS_REQUIRE = {
    'build': ['setuptools', 'twine', 'wheel'],
    'qa': ['flake8'],
    'test': ['mypy', 'pytest'],
}

EXTRAS_REQUIRE['dev'] = (
    EXTRAS_REQUIRE['build'] +
    EXTRAS_REQUIRE['qa'] +
    EXTRAS_REQUIRE['test']
)


if __name__ == '__main__':
    setup(
        name='felix-decorator',
        version=felix.__version__,
        url='https://github.com/zzhengnan/felix',
        author='Zhengnan Zhao',
        description="A collection of handy decorators for Python",
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        packages=find_packages(),
        python_requires='>=3.7',
        extras_require=EXTRAS_REQUIRE,
        classifiers=[
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
        ]
    )
