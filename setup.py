from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="athena-chat",
    version="0.1.0",
    author="1tsMeMario",
    author_email="91571045+1tsMeMario@users.noreply.github.com",
    description="A Streamlit-based interface for lmstudio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/1tsMeMario/streamlit-athenachat",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
) 