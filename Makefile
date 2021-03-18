.PHONY: all deploy test clean

all:
	@$(MAKE) -f Makefile.test
	@$(MAKE) -f Makefile.deploy

deploy:
	@$(MAKE) -f Makefile.deploy

test:
	@$(MAKE) -f Makefile.test

clean:
	@$(MAKE) -f Makefile.clean

pipeline-policy:
	@$(MAKE) -f Makefile.pipeline
