from setuptools import setup, find_packages

setup(
    name="nova-synapse",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        line.strip()
        for line in open("requirements.txt")
        if not line.startswith("#") and "platform_system" not in line
    ],
    author="Manolozero1",
    author_email="your.email@example.com",
    description="NOVA-Synapse: Sistema adaptativo de asistencia virtual",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Manolozero1/nova-synapse",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "nova-synapse=nova_synapse.main:main",
        ],
    },
)