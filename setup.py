import setuptools

setuptools.setup(
    name="deconz_exporter",
    version="0.0.1",
    author="Kristof Jakab",
    url="https://github.com/jaksi/deconz_exporter",
    packages=setuptools.find_packages(),
    install_requires=['requests', 'prometheus-client'],
    entry_points={"console_scripts": ["deconz_exporter = deconz_exporter:main"]},
)
