from setuptools import setup, find_packages

setup(
    name="sports-betting-system",
    version="1.0.0",
    description="Autonomous Sports Betting Analysis and Execution System",
    author="Betting System Team",
    author_email="info@bettingsystem.com",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "python-dotenv",
        "requests",
        "pandas",
        "numpy",
        "scikit-learn",
        "xgboost",
        "psycopg2-binary",
        "sqlalchemy",
        "flask",
        "flask-cors",
    ],
)
