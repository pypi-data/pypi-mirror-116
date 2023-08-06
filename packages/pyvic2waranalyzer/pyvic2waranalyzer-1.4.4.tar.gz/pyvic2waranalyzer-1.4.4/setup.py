from setuptools import setup, find_packages

extras_require = {
    "docs": ["sphinx==4.1.1", "sphinx-rtd-theme==0.5.2", "sphinxcontrib-napoleon", "sphinxcontrib-serializinghtml",
             "sphinxcontrib-htmlhelp", "sphinxcontrib-applehelp", "sphinxcontrib-jsmath", "myst-parser"]
}

setup(
    name='pyvic2waranalyzer',
    version='1.4.4',
    packages=find_packages(),
    url='https://github.com/InternetExplorer404/PyVic2WarAnalyzer',
    download_url="https://github.com/InternetExplorer404/PyVic2WarAnalyzer/archive/refs/tags/v1.4.4.tar.gz",
    include_package_data=True,
    license='Unlicense',
    author='Alvaro',
    author_email='',
    extras_require=extras_require,
    description='Victoria 2 War Analyzer written in Python!',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Other/Nonlisted Topic',
        'License :: OSI Approved :: The Unlicense (Unlicense)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
