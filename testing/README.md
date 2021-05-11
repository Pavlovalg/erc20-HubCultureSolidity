# Testing Browser Interfaces Against a Local Node

In order to test these contracts against a browser, several steps are needed.
- Have Parity installed
- Run Parity as follows:
  `parity --chain dev --jsonrpc-apis all`
- Now go to the following url in your browser:
  `https://remix.ethereum.org/`
- In order to use Parity to deploy the contracts from remix:
  - Remix will start on the compile menu
  - ![Alt text](./compile_menu.png?=true)
  - Click on the settings menu. You should see this now:
  - ![Alt text](./settings_menu.png?=true)
  - Click `Enable Personal Mode`
  - Go to the Run menu and select one of the following options for the `Environment settings`:
  - ![Alt text](./run_injected.png?=true)
  - ![Alt text](./run_web3.png?=true)
  - The `Injected Web3` option will allow you to use MetaMask and the `Web3 Provider` option will allow you to use Parity directly.
  - If you use `Web3 Provider`, the account password is the empty string
  - If you use `Injected Web3` the password is whatever you made the password for your MetaMask account. If you use MetaMask you may need to fund this account. If you do, see this repo:
  [devsend](https://github.com/mimirblockchainsolutions/devsend)
  - If using MetaMask you must also select the network as `Local Host 8545` See Below:
  - ![Alt text](./localhost.png?=true)
  - Once you have your provider all set up, you must deploy the contract. This can be done by clicking the `Deploy` button on the run menu screen
  - In order to get the source code for deployment, you may use the `condensed.sol` file from the utils directory.
  - If yo uchange the contracts a new condensed file may be built by running `python3.6 condenser.py` from the utils directory.
  - This will create a new contract that you may send transactions against through Remix. You may take the address of this account out of Remix and put it into the javascript files. Once this is done, the javascript will work as expected except for the remote node. This will fail, because our nodes are pointed at the Main Net and you are testing against a local dev chain. The contract will not exist on the Main Net at this address.
