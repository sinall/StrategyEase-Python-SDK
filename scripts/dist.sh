CWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPT_DIR=$(dirname "$0")
HOME_DIR=$SCRIPT_DIR/..

cd $HOME_DIR
rm -rf dist/*
python3 setup.py sdist
python3 setup.py bdist_wheel --universal
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
cd $CWD
