init:
	git clone --recursive --branch develop https://github.com/vtnerd/monero-lws
	git clone https://github.com/lalanza808/docker-monero-node
	git clone https://github.com/CryptoGrampy/mymonero-web-js

build:
	docker-compose build
