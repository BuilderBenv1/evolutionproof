// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC20 {
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
}

/**
 * @title StETHTreasury
 * @notice Principal-protected yield treasury for AI agent operating budget.
 *         The agent can only spend yield (wstETH appreciation), never the principal.
 *         Owner configures recipient whitelist and per-tx caps.
 */
contract StETHTreasury {
    address public owner;
    address public agent;
    IERC20 public wstETH;

    uint256 public principalDeposited;
    uint256 public totalWithdrawn;
    uint256 public perTxCap;

    mapping(address => bool) public recipientWhitelist;

    event Deposited(address indexed from, uint256 amount);
    event YieldWithdrawn(address indexed recipient, uint256 amount);
    event AgentUpdated(address indexed oldAgent, address indexed newAgent);
    event RecipientWhitelisted(address indexed recipient, bool allowed);
    event PerTxCapUpdated(uint256 oldCap, uint256 newCap);

    modifier onlyOwner() {
        require(msg.sender == owner, "StETHTreasury: caller is not the owner");
        _;
    }

    modifier onlyAgent() {
        require(msg.sender == agent, "StETHTreasury: caller is not the agent");
        _;
    }

    constructor(address _wstETH, address _agent) {
        owner = msg.sender;
        wstETH = IERC20(_wstETH);
        agent = _agent;
        perTxCap = type(uint256).max; // No cap by default
    }

    /**
     * @notice Deposit wstETH into the treasury. Only owner can deposit.
     *         The deposited amount becomes locked principal.
     */
    function deposit(uint256 amount) external onlyOwner {
        require(amount > 0, "StETHTreasury: zero deposit");
        require(
            wstETH.transferFrom(msg.sender, address(this), amount),
            "StETHTreasury: transfer failed"
        );
        principalDeposited += amount;
        emit Deposited(msg.sender, amount);
    }

    /**
     * @notice Calculate spendable yield.
     *         Yield = current balance - principal + totalWithdrawn - totalWithdrawn
     *         Simplified: current balance - principal (since we track withdrawals)
     */
    function getSpendableYield() public view returns (uint256) {
        uint256 currentBalance = wstETH.balanceOf(address(this));
        if (currentBalance <= principalDeposited) {
            return 0;
        }
        return currentBalance - principalDeposited;
    }

    /**
     * @notice Agent withdraws yield to a whitelisted recipient.
     */
    function withdrawYield(uint256 amount, address recipient) external onlyAgent {
        require(amount > 0, "StETHTreasury: zero withdrawal");
        require(amount <= perTxCap, "StETHTreasury: exceeds per-tx cap");
        require(recipientWhitelist[recipient], "StETHTreasury: recipient not whitelisted");

        uint256 available = getSpendableYield();
        require(amount <= available, "StETHTreasury: insufficient yield");

        totalWithdrawn += amount;
        require(
            wstETH.transfer(recipient, amount),
            "StETHTreasury: transfer failed"
        );

        emit YieldWithdrawn(recipient, amount);
    }

    // --- Owner admin functions ---

    function setAgent(address _agent) external onlyOwner {
        emit AgentUpdated(agent, _agent);
        agent = _agent;
    }

    function setRecipientWhitelist(address recipient, bool allowed) external onlyOwner {
        recipientWhitelist[recipient] = allowed;
        emit RecipientWhitelisted(recipient, allowed);
    }

    function setPerTxCap(uint256 cap) external onlyOwner {
        emit PerTxCapUpdated(perTxCap, cap);
        perTxCap = cap;
    }

    /**
     * @notice Emergency: owner can recover principal only.
     *         This is NOT callable by the agent.
     */
    function emergencyWithdrawPrincipal(address to) external onlyOwner {
        uint256 amount = principalDeposited;
        principalDeposited = 0;
        require(wstETH.transfer(to, amount), "StETHTreasury: transfer failed");
    }
}
