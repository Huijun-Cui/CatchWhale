require("@nomicfoundation/hardhat-toolbox");

/** @type import('hardhat/config').HardhatUserConfig */

module.exports = {
  solidity:{
    compilers:[
      {
        version:"0.7.6",
        settings:{
          optimizer:{
            enabled: true,
            runs: 500,
            details:{
              yul:false
            }
          }
        }
      }
    ] 
  },
  networks:{
    test:{
      allowUnlimitedContractSize: true,
      url:'http://127.0.0.1:8545/',
      accounts:['0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80']
    }
  }
};
