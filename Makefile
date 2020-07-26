.DEFAULT_GOAL := help
.PHONY : clean help ALL


help:
	@echo 'Run `make ALL` to see how things run from scratch'

ALL: clean


clean: clean_sqlize
	@echo --- Cleaning stubs
