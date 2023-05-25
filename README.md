# monero-lw

Monero lightwallet project. Packages the following services in one package:

* `monero-lws` by [vtnerd](https://github.com/vtnerd/monero-lws) - scans your wallet's view keys in the background
* `lwsadmin` by [lza_menace](https://lzahq.tech) - backend CRUD app for managing the LWS backend
* `monerod` by [The Monero Project](https://github.com/monero-project/monero) - node for syncing Monero blockchain transactions
* `mymonero-web` by [MyMonero](https://mymonero.com) but forked and cleaned up for personal use by [CryptoGrampy](https://github.com/CryptoGrampy/mymonero-web-js) - the web wallet client


## Setup

Works on Linux, built on Ubuntu 22.

1. Install packages
2. Clone the repo
3. Clone other projects
4. Build container images
5. Run containers
6. Initialize admin - note address and key

```
# 1
sudo apt install docker.io docker-compose python3 python3-venv make

# 2
git clone https://git.cloud.lzahq.tech/nerodev/monero-lw && cd monero-lw

# 3
git clone --recursive --branch develop https://github.com/vtnerd/monero-lws
git clone https://github.com/lalanza808/docker-monero-node
git clone https://github.com/CryptoGrampy/mymonero-web-js

# 4
docker-compose build

# 5
docker-compose up -d

# 6
docker exec -ti monero-lws monero-lws-admin create_admin
```

Proceed to setup your user at http://127.0.0.1:5000/setup - use the LWS admin address and key from `# 6`.

Start adding wallets.


### Links

* https://github.com/moneroexamples/openmonero
* https://github.com/vtnerd/monero-lws/tree/feature/no_auth_admin
* https://github.com/vtnerd/monero-lws/blob/feature/no_auth_admin/docs/administration.md
* https://github.com/monero-project/meta/blob/master/api/lightwallet_rest.md
* https://github.com/CryptoGrampy/monero-lws-admin
* https://www.npmjs.com/package/@mymonero/mymonero-wallet-manager/v/3.0.0
* https://github.com/mymonero/mymonero-utils/tree/master/packages/mymonero-lws-client
* https://github.com/mymonero/mymonero-utils/tree/master/packages/mymonero-monero-client
* https://github.com/mymonero/mymonero-utils/tree/master/packages/mymonero-wallet-manager

### Notes

```
accept_requests: {"type": "import"|"create", "addresses":[...]}
add_account: {"address": ..., "key": ...}
list_accounts: {}
list_requests: {}
modify_account_status: {"status": "active"|"hidden"|"inactive", "addresses":[...]}
reject_requests: {"type": "import"|"create", "addresses":[...]}
rescan: {"height":..., "addresses":[...]}
webhook_add: {"type":"tx-confirmation", "address":"...", "url":"...", ...} with optional fields:
    token: A string to be returned when the webhook is triggered
    payment_id: 16 hex characters representing a unique identifier for a transaction
webhook_delete
```