
default: package

package:
	python setup.py sdist
	cp dist/rspecFppGe*.tar.gz ../

clean:
	rm -rf dist rspecFppGen.egg-info || true
	rm -rf ../rspecFppGe*.tar.gz