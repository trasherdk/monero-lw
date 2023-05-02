# monero-lws frontend

Client side web application for managing wallets in `monero-lws`.

Everything is stored client side, encrypted.

/ - redirect to /setup if user not setup, to /login if not authenticated
/setup - first time setup user account, encrypted session
/login - log into encrypted session
/wallet/add - add a wallet to LWS
/wallet/:id - show wallet details (balances, txes, etc)
/wallet/:id/remove - remove a wallet from LWS
/wallet/:id/resync - resync wallet

