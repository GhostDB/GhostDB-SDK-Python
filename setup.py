from setuptools import setup

def readme():
    with open("README.rst") as f:
        return f.read()

setup(
    name="ghostdb",
    version="1.0.0",
    description="Python SDK for GhostDB Cache",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Jake Grogan",
    author_email="jake.grogan8@mail.dcu.ie",
    license="MIT",
    packages=["GhostDB"],
    package_data={
        "GhostDB": [
            "tests/ghostdb_sim.conf",
            "tests/ghostdb_test.conf"
        ]
    },
    install_requires=[
        "requests",
    ],
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose'],
)