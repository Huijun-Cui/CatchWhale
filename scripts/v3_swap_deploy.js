// We require the Hardhat Runtime Environment explicitly here. This is optional
// but useful for running the script in a standalone fashion through `node <script>`.
//
// You can also run a script with `npx hardhat run <script>`. If you do that, Hardhat
// will compile your contracts, add the Hardhat Runtime Environment's members to the
// global scope, and execute the script.
const hre = require("hardhat");

async function main() {
 

  const lockedAmount = hre.ethers.utils.parseEther("1");

  const swap_v3 = await hre.ethers.getContractFactory("SwapExamples");
  var router_v3_addr = '0xE592427A0AEce92De3Edee1F18E0157C05861564'
  const swap_c = await swap_v3.deploy(router_v3_addr);

  await swap_c.deployed();

  console.log(
    `SwapExamples deployed to ${swap_c.address}`
  );
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
