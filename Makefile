# Makefile specifically used for testing the api but without asserts or shit
# like that since all I need is the output to show up in the terminal.

# shorthands 
h: help 
b: build 
r: run

help:
	@echo -e "\nMakefile Help List for htp\n"
	@echo -e "\t\b\b\b\bbuild (b)\tBuilds the golang backend for testing"
	@echo -e "\t\b\b\b\brun (r)\tRuns the tests"


# Output dir for the golang builds so the dir can be gitignored instead of the
# file itself.
GOLANG_BUILD_DIR := _out
# the file itself that is built
GOLANG_BACKEND_BIN := $(GOLANG_BUILD_DIR)/htp_backend
# the actual htp pythin script 
HTP_SCRIPT_SRC := ./htp.py

# Build the golang backend before actually doing any tests etc
build:
	go build -o $(GOLANG_BACKEND_BIN) -ldflags "-s -w" -trimpath main.go 

# run the tests
run: build
	$(GOLANG_BACKEND_BIN) & \
	sleep 1 ; \
	$(MAKE) run-htp-cmds

# the htp commands for the tests
run-htp-cmds:
	@echo -e "[ HTP ] Setting base url"
	$(HTP_SCRIPT_SRC) set-base-url http://localhost:8888
	@echo -e "[ HTP ] Posting for json"
	$(HTP_SCRIPT_SRC) req POST /jsonshit | jq


