build:
	web_build

install:
	pip install -r requirements_python.txt
	nodeenv -p
	npm i -g npm
	cat requirements_node.txt | xargs npm install -g
	curl -sL $(shell curl -s https://api.github.com/repos/validator/validator/releases/latest | python3 -c "import sys, json; gh = json.load(sys.stdin); a = [print(item['browser_download_url']) for item in gh['assets'] if item['name'].startswith('vnu.jar') and item['name'].endswith('.zip')]") | bsdtar -x -f - -C $(VIRTUAL_ENV)/bin --strip-components 1 dist/vnu.jar
	pip install -e .
	web_install_js_libs

upload:
	web_build --upload

viewlog:
	tail -f log/server

reset:
	web_build
	web_server restart
