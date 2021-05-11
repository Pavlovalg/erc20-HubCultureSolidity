# HubCultureSolidity

This is the solidity contracts and tests for the HubCulture Ven bridge.

## TESTING

The tests have been run using Mythril and a Mimir built scripting framework.
Mythril is a Consensus tool for testing low level attacks and for visualizing
the call structure of a smart contract. This system is best run from a docker
due to complex dependency requirements. In order to pull the docker image,
use the `pull_mythril.sh` file. In order to test the smart contracts, use the
`myth_test.sh` file. The output of this test will be printed on stdout.
In order to generate an interactive call graph, use `myth_graph.sh`. This will
output a file named `graph.html` that may be opened in a web browser.

The custom testing framework that is Mimir built is contained in several files.
The logic of the system is defined in `test.py`. In order to run these tests
you must first install all dependencies using

`python3 -m pip install requirements.txt`

The solidity compiler must also be installed for contract testing. For the
latest directions see

https://solidity.readthedocs.io/en/latest/installing-solidity.html#binary-packages

Once the dependencies have been installed you must also have an installed
Parity client. This may be installed using the command

`bash <(curl https://get.parity.io -L)`

Once parity has been installed, Parity must be run using the command

`parity --chain dev --jsonrpc-apis=all`

This will turn on a private test blockchain on the local machine that the
smart contracts may be deployed and tested against.
The other files that are part of the Mimir testing framework are
- `ident.spec` specifies test psuedo-identities using targeted proxies
- `contracts.spec` specifies contracts to be deployed and constructor args
- `test.spec` specifies the actual tests in a scripting language

For details about the scripting language see the comments in `test.spec`.
In order to run tests, execute them using the following command:

`python3.6 test.py`


## CONTRACTS

The contracts are as follows:

  - ERC20Lib: This is a port of the OpenZeppelin ERC20 Contract into a Library.
  - SafeMath: This is the OpenZeppelin SafeMath Library, unmodified.
  - HubCulture: This is an ERC20 implementation using ERC20Lib.

The Hubculture contract has the following sections:

  - Imports: These are the using for statements.
  - Events: These are the HubCulture specific events for server coordination.
  - Declarations: These are declarations of global state variables.
  - Constructor: Just the initiation logic.
  - Modifiers: Access control modifiers.
  - Declarations: These are declarations of global state variables.
  - Owner/Failsafe: Logic for setting/resetting owner/failsafe.
  - Pause Logic: Logic to hault all transfers and transactions.
  - ERC20 Logic: Thinly wraps ERC20Lib
  - Deposit/Withdraw Logic: Facilitates time delay deposits and withdraws.
  - Registration: Allows possession of an account to be proven to HubCulture.


## PERMISSION SCHEME

  - Actors:
    - `owner` (singular address)
    - `failsafe` (singular address)
    - `vaults` (set of addresses)
    - `authorities` (set of addresses)
    - `Token Holders` (set of addresses defined by balances)
    - `Approved External Actors` (set of addresses defined by allowances)

  - Owner Capabilites:
    - Owner may add or remove an authority
    - Owner may add or remove an vault
    - Owner may `pause`
    - Owner may change new arbitrary owner address.
    - Owner may pause

  - Failsafe Capabilities:
    - Failsafe may set new arbitrary failsafe address.
    - Failsafe may `unpause`

  - Vault Capabilities:
    - Vault may release a pending deposit.
    - Vault may revoke a pending deposit.

  - Authority Capabilites:
    - Authority may depisit (mint) tokens into pending.
    - Authority may unregister a user account.
    - Authority may sign (off chain) uuid for user registration.

  - Token Holders
    - Token Holder may withdraw, transfer, and grant allowances of tokens

  - Approved External Actors
    - May cause a transfer of tokens from a third party account once approved.
