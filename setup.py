"""Setup configuration for ncaa_d1_team_normalizer package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ncaa_d1_team_normalizer",
    version="0.1.0",
    author="dburge86",
    author_email="dburge86@users.noreply.github.com",
    description="Normalize NCAA D1 Men's Basketball team names to ESPN canonical format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dburge86/ncaa-basketball-team-normalizer",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.0",
            "black>=23.0.0",
            "mypy>=1.5.0",
        ],
    },
    keywords="ncaa basketball sports data normalization espn",
    project_urls={
        "Bug Reports": "https://github.com/dburge86/ncaa-basketball-team-normalizer/issues",
        "Source": "https://github.com/dburge86/ncaa-basketball-team-normalizer",
    },
)
