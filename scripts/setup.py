import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FiBar: diameter measuring package", 
    version="0.1",
    author="Marilin Moor",
    author_email="marilin.moor@gmail.com",
    description="Diameter measuring image processing tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['image processing', 'diameter measuring', 'biology'],
    license='General Public License v. 3',
    packages=setuptools.find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'matplotlib==3.1.2',
        'numpy==1.22.4',
        'opencv_contrib_python==4.5.5.62',
        'opencv_python==4.7.0.72',
        'plantcv==3.14.2',
        'pykuwahara==0.3.2',
        'pytesseract==0.3.10',
        'scikit-image==0.18.3',
        'mizani==0.7.3',
        'pandas==2.0.3',
        # 'tensorflow==2.12.0',
        # 'tensorflow-estimator== 2.12.0',
        # 'tensorflow-io-gcs-filesystem==0.24.0',
        'torch==2.2.0',
        'torchvision==0.17.0',
    ]
    
)