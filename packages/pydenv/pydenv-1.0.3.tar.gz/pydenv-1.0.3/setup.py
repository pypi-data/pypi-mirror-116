from setuptools import setup

setup(
    name = 'pydenv',
    version = '1.0.3',
    author = 'Felipe Leite',
    author_email = 'felipecostasilvaleite@hotmail.com',
    packages = ['pydenv'],
    description = 'Provisionador de ambiente de desenvolvimento',
    long_description = 'Pacote que visa realizar o provisionamento de '
                        + 'um ambiente de desenvolvimento utiliando diversos pacotes, '
                        + 'como pylint, pydocstyle e afins...',
    url = 'https://github.com/felipe-almeida-costa-leite/pydenv',
    project_urls = {
        'Código fonte': 'https://github.com/felipe-almeida-costa-leite/pydenv',
        'Download': 'https://github.com/felipe-almeida-costa-leite/pydenv/1.0.0.zip'
    },
    license = 'MIT',
    keywords = 'Ambiente de desenvolvimento',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Scientific/Engineering :: Physics'
    ]
)
