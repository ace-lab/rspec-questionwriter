
default: package

install:
	make clean
	make package
	pip install dist/rspecFppGe*.tar.gz

package:
	python setup.py sdist

clean:
	rm -rf dist rspecFppGen.egg-info || true