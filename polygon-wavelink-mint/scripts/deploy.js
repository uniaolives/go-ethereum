const hre = require("hardhat");
async function main() {
  const NFT = await hre.ethers.getContractFactory("WavelinkNFT");
  const nft = await NFT.deploy();
  await nft.deployed();
  console.log("NFT deployed to:", nft.address);
}
main();
