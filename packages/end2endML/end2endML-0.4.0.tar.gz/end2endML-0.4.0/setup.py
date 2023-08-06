import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="end2endML",
    version="0.4.0",
    author="Yipeng Song",
    author_email="yipeng.song@hotmail.com",
    description="Automate data analysis pipelines",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/YipengUva/end2endml_pkg",
    project_urls={
        "Bug Tracker": "https://gitlab.com/YipengUva/end2endml_pkg/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.19",
        "pandas>=1.1",
        "imbalanced-learn>=0.8.0",
        "scikit-learn>=0.24",
        "pandas-profiling>=2.9.0",
        "joblib",
        "xgboost>=1.4",
        "optuna>=2.7",
    ],
)
