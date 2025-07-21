from setuptools import setup, find_packages

setup(
    name="afotorelocate",
    version="0.1.0",
    description="Herramienta para reubicar y renombrar fotos",
    author="Ime",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # Las dependencias se leen de requirements.txt
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "afotorelocate=main:main"
        ]
    },
)
