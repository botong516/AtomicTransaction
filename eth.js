const API_URL = "https://eth-goerli.g.alchemy.com/v2/My1jLwhPFHl15osPFaC_ss4yeUOtyAhl"
const PUBLIC_KEY = "0xFBfEdaB2c5b9455e40954291969B44D87F1B5728";
const PRIVATE_KEY = "865477fe2571fe9c516908b9f7d595beeec048f675f9541c3bf51502412867de";

const { createAlchemyWeb3 } = require("@alch/alchemy-web3")
const web3 = createAlchemyWeb3(API_URL)

const contract = require("./IntroToBlockchainNFT.json")
const contractAddress = "0x978A328Cc24C0b50a0D9F97787938E67CF09F9A9"
const nftContract = new web3.eth.Contract(contract.abi, contractAddress)

async function sendTx(tx) {
    const signPromise = web3.eth.accounts.signTransaction(tx, PRIVATE_KEY);
    signPromise.then((signedTx) => {
          web3.eth.sendSignedTransaction(
            signedTx.rawTransaction,
            function (err, hash) {
              if (!err) {
                console.log("The hash of your transaction is: ", hash)
              } else {
                console.log("Something went wrong when submitting your transaction:", err)
              }
            }
          )
        }).catch((err) => {
          console.log("Promise failed:", err)
    })
}

async function mintNFT(tokenURI) {

  let hashOfName = "09475853f47d08097798d487c0680ca326a2ce7f09801a4c005ef125133b27d5";

  let nonce = await web3.eth.getTransactionCount(PUBLIC_KEY, "latest") //get latest nonce

  const tx1 = {
    from: PUBLIC_KEY,
    to: contractAddress,
    nonce: nonce,
    gas: 500000,
    data: nftContract.methods.enterAddressIntoBook(hashOfName).encodeABI()
  }

  await sendTx(tx1);

  nonce += 1; 

  const tx2 = {
    from: PUBLIC_KEY,
    to: contractAddress,
    nonce: nonce,
    gas: 500000,
    data: nftContract.methods.mintNFT().encodeABI()
  }

  await sendTx(tx2);

}

mintNFT()
