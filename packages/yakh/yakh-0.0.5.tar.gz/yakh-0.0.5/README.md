Yet Another Kafka log Handler

This project is currently in BETA and not finished!

## Building a new pip package

First we will build the next version for pypi test and if that works without problems, then it will be built for pypi production

1. Open setup.cfg and increment the version
2. Build the pypi wheel and source package: 

```
$ python3 -m build
```

3. Upload to pypi test:

```
$ python3 -m twine upload --skip-existing --repository testpypi dist/*
```

4. If the upload to test works, then upload to pypi production

```
$ python3 -m twine upload --skip-existing dist/*
```



