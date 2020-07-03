# build:
# 	web_build

install:
	pip install --upgrade pip; \
	pip install --upgrade setuptools; \
	pip install -r requirements_python.txt; \
	nodeenv -p; \
	npm i -g npm; \
	cat requirements_node.txt | xargs npm install -g; \
	pip install -e .

# upload:
# 	web_build --upload

# viewlog:
# 	tail -f log/server

# reset:
# 	web_build
# 	web_server restart
