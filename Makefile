


all: submodules

submodules:
	if  git submodule status | grep -q ^[+-]; then git submodule update --init --recursive; else echo "All submodules are up to date"; fi