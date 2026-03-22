require("@nomicfoundation/hardhat-ethers");
require("dotenv").config();

module.exports = {
  solidity: "0.8.20",
  networks: {
    celo: {
      url: process.env.CELO_RPC_URL || "https://forno.celo.org",
      accounts: process.env.OPERATOR_PRIVATE_KEY
        ? [process.env.OPERATOR_PRIVATE_KEY]
        : [],
      chainId: 42220,
    },
    status: {
      url: process.env.STATUS_NETWORK_RPC || "https://public.sepolia.rpc.status.im",
      accounts: process.env.OPERATOR_PRIVATE_KEY
        ? [process.env.OPERATOR_PRIVATE_KEY]
        : [],
      chainId: 1660990954,
    },
  },
};
