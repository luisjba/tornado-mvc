
submodule_bootstrap_css = assets/css/bootstrap.min.css
submodule_bootstrap_js = assets/js/bootstrap.min.js
jquey_lib = assets/js/jquery-2.2.4.min.js


# all: submodules $(submodule_bootstrap_css)
all: submodules $(submodule_bootstrap_js)

submodules:
	if  git submodule status | grep -q ^[+-]; then git submodule update --init --recursive; else echo "All submodules are up to date"; fi

$(submodule_bootstrap_js): $(submodule_bootstrap_css) $(jquey_lib)
	[ ! -d "'dirname $@'" ] && mkdir -p "`dirname $@`"
	cp submodules/bootstrap/dist/js/bootstrap.min.js $(submodule_bootstrap_js)

$(submodule_bootstrap_css):
	[ ! -d "'dirname $@'" ] && mkdir -p "`dirname $@`"
	cp submodules/bootstrap/dist/css/bootstrap.min.css $@

$(jquey_lib):
	curl https://code.jquery.com/jquery-2.2.4.min.js --output $@