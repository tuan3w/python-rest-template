# python-rest-template

A clean Python template for your next REST projects.


## Setup
You need to install [Pipenv](https://pipenv.pypa.io/en/latest/) in your machine.

```bash
$ pipenv shell
$ pipenv install
```

## Run app

```bash
$ cp config.yaml.example config.yaml
$ # update your app config in config.yaml
$ pipenv run app
```

Now, you can check API docs located at http://localhost:8000/docs .

## Test apps

```bash
$ pipenv run test
```

To show code coverage, just run:

```bash
$ pipenv run test-cov
```

In order to show code coverage in VsCode, you will need to install [Coverage Gutters extension](https://marketplace.visualstudio.com/items?itemName=ryanluker.vscode-coverage-gutters) and then generate `coverage.xml` file via command:
```bash
$ pipenv run test-cov-xml
```

## Database migration

```bash
$ cp alembic.ini.example alembic.ini
$ # update alembic.ini config file
$ alembic upgrade head
```

## Error code localization with i18n

```bash
$ ./extract_messages.sh
$ # update your translation in `base.po` files
$ ./update_translation.sh
```

## License

[MIT](LICENSE)