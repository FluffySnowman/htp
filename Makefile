# Makefile specifically used for testing the api but without asserts or shit
# like that since all I need is the output to show up in the terminal.

# MAKEFLAGS += .SILENT
.SILENT: build run

# shorthands 
h: help 
b: build 
r: run
rb: run-backend

help:
	@echo -e "\nMakefile Help List for HTP\n"
	@echo -e "\t\b\b\b\binstall \t(i)\tInstalls (copies) script to /usr/local/bin"
	@echo -e "\t\b\b\b\brun \t(r)\tRuns the tests"
	@echo -e "\t\b\b\b\bbuild \t(b)\tBuilds the golang backend for testing"
	@echo -e "\t\b\b\b\brun-backend\t(rb)\tBuilds & runs golang backend for testing"
	@echo -e ""
	@echo -e "\t\b\b\b\bhelp \t(h)\tShows this help menu\n"


# Output dir for the golang builds so the dir can be gitignored instead of the
# file itself.
GOLANG_BUILD_DIR := _out
# the file itself that is built
GOLANG_BACKEND_BIN := $(GOLANG_BUILD_DIR)/htp_backend
# the actual htp pythin script 
HTP_SCRIPT_SRC := ./htp.py
# The installation path (global system access) .
# This doesn't have a file extension since there's a shebang at the top of the
# file with #!/usr/bin/env python3 .
HTP_INSTALL_PATH := /usr/local/bin/htp

# Build the golang backend before actually doing any tests etc
build:
	go build -o $(GOLANG_BACKEND_BIN) -ldflags "-s -w" -trimpath main.go 

# run the tests
# run: build
# 	setsid $(GOLANG_BACKEND_BIN) & \
# 	sleep 1 ; \
# 	$(MAKE) run-htp-cmds

# run the backend and the tests and the n exit the backend when the tests are
# done
run: build
	( \
	$(GOLANG_BACKEND_BIN) & \
	BACKEND_PID=$$! ; \
	sleep 1 ; \
	$(MAKE) run-htp-cmds ; \
	kill $$BACKEND_PID \
	)

# runs the golang backend without the tests (used for manual shit)
run-backend: build
	$(GOLANG_BACKEND_BIN)

# the htp commands for the tests
run-htp-cmds:
	@echo -e "[ HTP ] Setting base url"
	$(HTP_SCRIPT_SRC) set-base-url http://localhost:8888
	@echo -e "[ HTP ] Posting for json"
	$(HTP_SCRIPT_SRC) req POST /jsonshit
	$(HTP_SCRIPT_SRC) req POST /jsonshit | jq
	$(HTP_SCRIPT_SRC) req POST / --data username=notuser title=shit description=lol
	$(HTP_SCRIPT_SRC) req GET /doshit
	$(HTP_SCRIPT_SRC) req POST /jsonshit --fields password,username


# copies ./htp.py to /usr/local/bun/htp
install:
	echo -e "Elevated permissions will be needed to install to /usr/local/bin"
	sudo cp -v $(HTP_SCRIPT_SRC) $(HTP_INSTALL_PATH)

