import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = ['aiohttp>=3.7.4,<4.0.0']

setuptools.setup(
    name="asyncosu",
    version="0.0.2",
    author="Efehan Atıcı",
    author_email="efehanatici@gmail.com",
    description="Async osu! Api Wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aticie/async_osu_api",
    project_urls={
        "Bug Tracker": "https://github.com/aticie/async_osu_api/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=requirements,
    python_requires=">=3.6",
)
