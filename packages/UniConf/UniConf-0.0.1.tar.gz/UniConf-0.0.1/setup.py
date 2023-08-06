from setuptools import setup

setup(name="UniConf",
      version="0.0.1",
      description="Allows you to conveniently create and modify a configuration file.",
      author="Fima20",
      author_email="dmitriy2000ms@yandex.ru",
      license='LGPLv3',
      packages=["uniconf", "uniconf.res"],
      install_requires=["configparser", "datetime"],
      zip_safe=False,)