import setuptools
    
setuptools.setup(
    name="CWT_MP", 
    version=2,
    description="A tensorflow 2.0 Continuous Wavelet Transform with Mixed Precision Support",
    long_description=open('README.md').read(),
    packages=['CWT_MP'],
    install_requires=['numpy', 'tensorflow'],
    python_requires='>=3.6',
)
