from setuptools import setup, find_packages

VERSION = '0.0.1-Alpha-01'

print("""

- upload
    - build wheel: python setup.py bdist_wheel
    - upload to server: python setup.py sdist upload -r internal

- download
    - Just pip install <package>

""")

if __name__ == '__main__':
    setup(
        name='fastapi_quickcrud',
        version=VERSION,
        install_requires=["fastapi","pydantic","SQLAlchemy","StrEnum","psycopg2"],
        python_requires=">=3.6",
        description='A Postgresql Schema based FastAPI router that automatically creates CRUD routes',
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        author='Luis Lui',
        author_email='luis11235178@gmail.com',
        url='https://gitlab.com/luislui/quickcrud',
        license="MIT License",
        keywords=["fastapi", "crud", "restful", "routing", "generator", "crudrouter","postgresql","builder"],
        # packages=find_packages(),
        packages=find_packages('src'),
        package_dir={'': 'src'},
        # package_dir={'': ''},
        setup_requires=["setuptools>=31.6.0"],
        classifiers=[
            "Development Status :: 2 - Pre-Alpha",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python",
            "Topic :: Internet",
            "Topic :: Software Development :: Libraries :: Application Frameworks",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Software Development :: Libraries",
            "Topic :: Software Development :: Code Generators",
            "Topic :: Software Development",
            "Typing :: Typed",
            "Development Status :: 4 - Beta",
            "Environment :: Web Environment",
            "Framework :: AsyncIO",
            "Intended Audience :: Developers",
            "Intended Audience :: Information Technology",
            "Intended Audience :: System Administrators",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
            "Topic :: Internet :: WWW/HTTP",
        ],
        include_package_data=True,
    )
