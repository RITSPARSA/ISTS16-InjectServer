clean:
	find . -name *.pyc -exec rm -fv {} +;
	rm -fr results/ injects/
