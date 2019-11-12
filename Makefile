
submodule_bootstrap_css = assets/css/bootstrap.css
submodule_bootstrap_js = assets/js/bootstrap.js


# all: submodules $(submodule_bootstrap_css)
all: submodules

submodules:
	if  git submodule status | grep -q ^[+-]; then git submodule update --init --recursive; else echo "All submodules are up to date"; fi

# $(submodule_bootstrap_css): 

