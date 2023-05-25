init:
	git clone --recursive --branch develop https://github.com/vtnerd/monero-lws
	git clone https://github.com/lalanza808/docker-monero-node
	git clone https://github.com/CryptoGrampy/mymonero-web-js

build:
	docker-compose build

release:
	docker-compose -f dev.compose.yaml build
	docker tag monero-lw_mymonero-web lalanza808/mymonero-web:latest
	docker tag monero-lw_monero-lws lalanza808/lws:latest
	docker tag monero-lw_lwsadmin lalanza808/lwsadmin:latest
	docker push lalanza808/mymonero-web
	docker push lalanza808/lws
	docker push lalanza808/lwsadmin