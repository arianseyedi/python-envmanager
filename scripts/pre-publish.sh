rm -rf dist
rm -rf build
rm -rf envmanager.egg-info
source venv/bin/activate
python setup.py sdist
python setup.py bdist_wheel