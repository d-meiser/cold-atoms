	pip install --verbose .
  cp -r tests /tmp
  cd /tmp/tests
  nosetests
  cd -

