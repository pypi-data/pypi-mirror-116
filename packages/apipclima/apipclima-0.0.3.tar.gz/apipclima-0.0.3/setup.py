
from setuptools import setup
import os


# User-friendly description from README.md
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

setup(
    name = 'apipclima',
    version = '0.0.3',
    install_requires=["pandas","numpy",
    "requests","xarray","scipy",
    "cftime"
    ],
    author = 'Felipe Odorizi de Mello',
    author_email = 'felipeodorizi@gmail.com',
    packages = ['pclima'],
    description = 'Módulo para recuperação de dados climáticos do PCBr.',
    long_description="""# PClima API\n\n\n## PClima API - Módulo para recuperação de dados climáticos do PCBr.\n\n\n# DESCRIPTION\n\n\n

    A documentação do Projeto pode ser encontrada no Portal
          http://pclima.inpe.br/
    As escolhas para o download de dados são definidas através 
     de um JSON que pode ser gerado utilizando do Portal API.
          http://pclima.inpe.br/analise/API
 
    versão do Python em que foi testada: 3.6
     
    exemplo de uso da API

    Token: consultar a documentação para a geração do Token

    Copiar o Token, no arquivo $HOME/.pclimaAPIrc (em ambiente Unix/Linux/Mac).
    No Windows colocar o arquivo .pclimaAPIrc no diretório inicial do usuário (ex. C:\\User\\Cliente)


    import clima as pcl

    Client = pcl.Client()

    data = Client.getData(
    { "formato": "CSV", "conjunto": "PR0002", "modelo": "MO0003", "experimento": "EX0003", "periodo": "PE0000", "cenario": "CE0001", "variavel": "VR0001", "frequenciaURL": "Mensal", "frequencia": "FR0003", "produto": "PDT0001", "localizacao": "Ponto", "localizacao_pontos": "-23.56/-46.62", "varCDO": "tasmax" }
    )

    Client.save(data,"file.csv")

    \n""",
    long_description_content_type='text/markdown',
    url = 'https://github.com/felipeodorizi/pclima',
    project_urls = {
        'Código fonte': 'https://github.com/felipeodorizi/pclima',
        'Download': 'https://github.com/felipeodorizi/pclima/apipclima-0.0.3.tar.gz'
    },
    license = 'MIT',
    keywords = 'recuperação de dados climáticos',
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