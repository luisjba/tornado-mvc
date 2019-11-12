
submodule_bootstrap_css = assets/css/bootstrap.css
submodule_bootstrap_js = assets/js/bootstrap.js


# all: submodules $(submodule_bootstrap_css)
all: submodules $(submodule_bootstrap_js)

submodules:
	if  git submodule status | grep -q ^[+-]; then git submodule update --init --recursive; else echo "All submodules are up to date"; fi

$(submodule_bootstrap_js): $(submodule_bootstrap_css)
	[ ! -d `dirname $(submodule_bootstrap_js)` ] && mkdir -p `dirname $(submodule_bootstrap_js)`
	cp submodules/bootstrap/dist/js/bootstrap.min.js $(submodule_bootstrap_js)

$(submodule_bootstrap_css):
	[ ! -d `dirname $(submodule_bootstrap_css)` ] && mkdir -p `dirname $(submodule_bootstrap_css)`
	cp submodules/bootstrap/dist/css/bootstrap.min.css $(submodule_bootstrap_css) 
