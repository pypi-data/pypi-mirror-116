import os

current_version = '1.3.0'
upgrad_type = 'minor'

cmds = [
    f'bumpversion --current-version {current_version} {upgrad_type} setup.py onnc/bench/__init__.py',
    "python setup.py sdist bdist_wheel",
    "tar tzf dist/onnc-bench*.tar.gz",
    "twine check dist/*",
    #"twine upload --repository-url https://test.pypi.org/legacy/ dist/*",
    "twine upload dist/*"
]

os.system("  &&  ".join(cmds))
