# *  greenland5 -- A Pythonic Eco System                                       |
# *  Copyright (C) 2020  M E Leypold  -----------------------------------------|
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.


all:: quick-check

IN-ROOT-PROJECT := \
  $(shell if test -f ../pyproject.toml && test -f ../Maintainer.mk; \
             then echo true; \
             else echo false; fi \
   )

ifeq ($(IN-ROOT-PROJECT),true)
include ../Maintainer.mk
# Note: This pulls in additional targets that are only useful when developing Greenland5 as a whole.
endif

NAME          := $(shell grep "^name *=" setup.cfg  | awk '{print $$3}')
SOURCES       = $(shell find . \( -name '.[a-z]*' -type d -prune \) \
                        -o \( -type f \( -name '*.py' -o -name '*.ini' -o -name '*.txt' -name '*.toml' \) -print \))

check_release_ready: check check_copyright check_git tox check_build

check_git::
	# What we test needs to be what we checked in
	test $$( git status -s | wc -l ) -eq 0                       # everything checked in?

check_build::
	# All the following build methods must work
        # AFAIK the PEP 518 builder is the most critical
	pip wheel --use-feature=in-tree-build --no-deps .            # Can build via PIP
	twine check $$(ls -1t *.whl | head -1)                       # Twine likes the resulting wheel
	rm -rf *.whl
	python setup.py sdist                                        # Can build source dist via setuptools
	python setup.py bdist_wheel                                  # Can build a wheel via setuptools
	twine check $$(ls -1t dist/*.whl | head -1)                  # Twine likes the resulting wheels
	twine check $$(ls -1t dist/*.tar.gz | head -1)               # Twine likes the resulting source dist
	python setup.py bdist                                        # Can build binary dist via setuptools
	twine check $$(ls -1t dist/*.tar.gz | head -1)               # Twine likes the resulting binary dist
	python -m build                                              # Can build with PEP 518 builder
	twine check $$(ls -1t dist/*.whl | head -1)                  # Twine likes the resulting wheels
	twine check $$(ls -1t dist/*.tar.gz | head -1)               # Twine likes the resulting source dist

check_copyright::
	# Does every source file have a copyright notice?
	code=0; \
        for F in $(SOURCES); do \
          echo -n "$$F ... "; \
	  if ! test 0 -eq "$$(wc -l "$$F" | cut -d' ' -f1)"; then \
             if head -2 $$F | tail -1 | grep Copyright >/dev/null 2>&1; then \
                echo "OK."; \
             else \
                code=1; \
                echo "FAILED."; \
             fi; \
          else \
            echo "OK."; \
          fi; \
        done; \
        exit $$code

ifeq ($(wildcard tox.ini),tox.ini)
tox::
	tox
else
tox::

endif


check::
	pytest; ERR=$$?; if test $$ERR -eq 5; then ERR=0; fi; exit $$ERR

quick-check::
	pytest -m smoke; ERR=$$?; if test $$ERR -eq 5; then ERR=0; fi; exit $$ERR	

clean::
	find . -name '*~' | xargs rm -rf
	rm -rf doc/build
	rm -f *.whl *.tar.gz *.zip *.tgz
