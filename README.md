# monero-lw

Monero lightwallet project.

Runs a private `monero-lws` service in the background with an API layer above that for authentication.

Will be adding client side application to tie the whole thing together.

## Links

* https://github.com/moneroexamples/openmonero
* https://github.com/vtnerd/monero-lws/tree/feature/no_auth_admin
* https://github.com/vtnerd/monero-lws/blob/feature/no_auth_admin/docs/administration.md
* https://github.com/monero-project/meta/blob/master/api/lightwallet_rest.md
* https://github.com/CryptoGrampy/monero-lws-admin
* https://www.npmjs.com/package/@mymonero/mymonero-wallet-manager/v/3.0.0
* https://github.com/mymonero/mymonero-utils/tree/master/packages/mymonero-lws-client
* https://github.com/mymonero/mymonero-utils/tree/master/packages/mymonero-monero-client
* https://github.com/mymonero/mymonero-utils/tree/master/packages/mymonero-wallet-manager

## Notes

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