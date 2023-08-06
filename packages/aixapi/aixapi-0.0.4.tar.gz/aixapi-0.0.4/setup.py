import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aixapi",
    version="0.0.4",
    author="AIx Solutions Group, Inc",
    author_email="info@aixsolutionsgroup.com",
    description="AI for everyone. With this API, you can access GPT-J. "
                "GPT-J is as powerful as OpenAI's GPT-3 Curie engine.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AIx-Solutions/aix-gpt-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
