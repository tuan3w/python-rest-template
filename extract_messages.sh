#!/bin/bash

pybabel extract  -k _ -o locales/base.pot .
pybabel update -i locales/base.pot -d locales -D base