import codecs
import os
import re

from setuptools import find_packages, setup


###############################################################################

NAME = "attrs"
PACKAGES = find_packages(where="src")
META_PATH = os.path.join("src", "attr", "__init__.py")
KEYWORDS = ["class", "attribute", "boilerplate"]
PROJECT_URLS = {
    "Documentation": "https://www.attrs.org/",
    "Bug Tracker": "https://github.com/python-attrs/attrs/issues",
    "Source Code": "https://github.com/python-attrs/attrs",
}
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
INSTALL_REQUIRES = []
EXTRAS_REQUIRE = {
    "docs": ["sphinx", "zope.interface"],
    "tests": [
        "coverage",
        "hypothesis",
        "pympler",
        "pytest>=4.3.0",  # 4.3.0 dropped last use of `convert`
        "six",
        "zope.interface",
    ],
}
EXTRAS_REQUIRE["dev"] = (
    EXTRAS_REQUIRE["tests"] + EXTRAS_REQUIRE["docs"] + ["pre-commit"]
)
EXTRAS_REQUIRE["azure-pipelines"] = EXTRAS_REQUIRE["tests"] + [
    "pytest-azurepipelines"
]

###############################################################################

HERE = os.path.abspath(os.path.dirname(__file__))
br = os.linesep


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


META_FILE = read(META_PATH)


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta), META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


VERSION = find_meta("version")
URL = find_meta("url")
LONG = (
    read("README.rst")
    + br*2
    + "Release Information" + br
    + "===================" + br*2
    + re.search(
        fr"(\d+.\d.\d \(.*?\){br}.*?){br*3}----{br*3}",
        read("CHANGELOG.rst"),
        re.S,
    ).group(1) + br*2
    + "`Full changelog "
    + f"<{URL}en/stable/changelog.html>`_.{br*2}"
    + read("AUTHORS.rst")
)


if __name__ == "__main__":
    setup(
        name=NAME,
        description=find_meta("description"),
        license=find_meta("license"),
        url=URL,
        project_urls=PROJECT_URLS,
        version=VERSION,
        author=find_meta("author"),
        author_email=find_meta("email"),
        maintainer=find_meta("author"),
        maintainer_email=find_meta("email"),
        keywords=KEYWORDS,
        long_description=LONG,
        long_description_content_type="text/x-rst",
        packages=PACKAGES,
        package_dir={"": "src"},
        python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
        zip_safe=False,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,
        include_package_data=True,
    )
