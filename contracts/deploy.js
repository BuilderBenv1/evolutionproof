/**
 * Hardhat deployment script for StETHTreasury
 * Deploy to Celo mainnet with bridged wstETH
 *
 * Usage:
 *   npx hardhat run contracts/deploy.js --network celo
 */

const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying StETHTreasury with account:", deployer.address);

  const balance = await hre.ethers.provider.getBalance(deployer.address);
  console.log("Account balance:", hre.ethers.formatEther(balance), "CELO");

  // wstETH address on Celo (bridged via Wormhole)
  const WSTETH_ADDRESS = process.env.WSTETH_ADDRESS_CELO;
  if (!WSTETH_ADDRESS) {
    throw new Error("WSTETH_ADDRESS_CELO not set in environment");
  }

  // Agent address (operator wallet)
  const AGENT_ADDRESS = deployer.address; // Agent is deployer by default

  console.log("wstETH address:", WSTETH_ADDRESS);
  console.log("Agent address:", AGENT_ADDRESS);

  // Deploy
  const StETHTreasury = await hre.ethers.getContractFactory("StETHTreasury");
  const treasury = await StETHTreasury.deploy(WSTETH_ADDRESS, AGENT_ADDRESS);
  await treasury.waitForDeployment();

  const treasuryAddress = await treasury.getAddress();
  console.log("StETHTreasury deployed to:", treasuryAddress);

  // Configure: whitelist the agent as a recipient
  const tx1 = await treasury.setRecipientWhitelist(AGENT_ADDRESS, true);
  await tx1.wait();
  console.log("Agent whitelisted as recipient");

  // Set a per-tx cap (0.01 wstETH = conservative)
  const perTxCap = hre.ethers.parseEther("0.01");
  const tx2 = await treasury.setPerTxCap(perTxCap);
  await tx2.wait();
  console.log("Per-tx cap set to 0.01 wstETH");

  console.log("\n--- Deployment Summary ---");
  console.log("StETHTreasury:", treasuryAddress);
  console.log("Owner:", deployer.address);
  console.log("Agent:", AGENT_ADDRESS);
  console.log("wstETH:", WSTETH_ADDRESS);
  console.log("\nAdd to .env:");
  console.log(`TREASURY_CONTRACT=${treasuryAddress}`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
