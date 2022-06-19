
ifeq (, $(shell which python3))
ifeq (, $(shell which python))
$(error "No python or python3 in $(PATH)")
endif
pyPath = $(shell which python)
else
pyPath = $(shell which python3)
endif

default: package

install:
	make clean
	make package
	$(pyPath) -m pip install dist/rspecFppGe*.tar.gz

package:
	$(pyPath) setup.py sdist

clean:
	rm -rf dist rspecFppGen.egg-info || true
