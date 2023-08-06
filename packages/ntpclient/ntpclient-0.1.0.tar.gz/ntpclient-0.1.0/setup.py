import setuptools 

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'ntpclient',
    version = '0.1.0',
    author = 'Kaan Yavas',
    author_email = 'yavas.kaann@gmail.com',
    description = 'NTP Client connection and send to commands to Server',
    long_description = long_description,
    long_description_context_type = "text/markdown",
    packages = setuptools.find_packages(),
    url = 'https://github.com/yvsKaan/ntpserver'
)