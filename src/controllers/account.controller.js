const accountService = require('../services/account.service');

// ─── CREATE ACCOUNT ───────────────────────────────────────────────────────────
const createAccount = (req, res) => {
  const { accountHolderName, openingBalance } = req.body;

  if (!accountHolderName || typeof accountHolderName !== 'string' || accountHolderName.trim() === '') {
    return res.status(400).json({
      success: false,
      error: '[!] Name cannot be blank!',
      message: 'Exiting... Please try again.'
    });
  }

  const parsedBalance = parseFloat(openingBalance);
  if (openingBalance === undefined || openingBalance === null || isNaN(parsedBalance) || parsedBalance <= 0) {
    return res.status(400).json({
      success: false,
      error: '[!] Opening Balance cannot be 0!',
      message: 'Exiting... Please try again.'
    });
  }

  const trimmedName = accountHolderName.trim().substring(0, 30);
  const result = accountService.createAccount(trimmedName, parsedBalance);

  return res.status(201).json({
    success: true,
    message: `Hello, ${result.accountHolderName}! Your Account is Ready.`,
    data: {
      accountId: result.accountId,
      accountHolderName: result.accountHolderName,
      balance: result.balance,
      status: 'ACTIVE'
    }
  });
};

// ─── DEPOSIT ──────────────────────────────────────────────────────────────────
const deposit = (req, res) => {
  const { accountId, amount } = req.body;

  if (!accountId) {
    return res.status(400).json({
      success: false,
      error: '[!] Account ID is required!',
      message: 'Exiting... Please try again.'
    });
  }

  const parsedAmount = parseFloat(amount);
  if (isNaN(parsedAmount) || parsedAmount <= 0) {
    return res.status(400).json({
      success: false,
      error: '[!] Deposit amount must be greater than 0!',
      message: 'Exiting... Please try again.'
    });
  }

  const result = accountService.deposit(accountId, parsedAmount);
  if (!result) {
    return res.status(404).json({
      success: false,
      error: '[!] Account not found!',
      message: 'Exiting... Please try again.'
    });
  }

  return res.status(200).json({
    success: true,
    message: `Deposit of ${parsedAmount} successful!`,
    data: {
      accountId: result.accountId,
      accountHolderName: result.accountHolderName,
      balance: result.balance,
      status: result.status
    }
  });
};

// ─── WITHDRAW ─────────────────────────────────────────────────────────────────
const withdraw = (req, res) => {
  const { accountId, amount } = req.body;

  if (!accountId) {
    return res.status(400).json({
      success: false,
      error: '[!] Account ID is required!',
      message: 'Exiting... Please try again.'
    });
  }

  const parsedAmount = parseFloat(amount);
  if (isNaN(parsedAmount) || parsedAmount <= 0) {
    return res.status(400).json({
      success: false,
      error: '[!] Withdrawal amount must be greater than 0!',
      message: 'Exiting... Please try again.'
    });
  }

  const account = accountService.getAccount(accountId);
  if (!account) {
    return res.status(404).json({
      success: false,
      error: '[!] Account not found!',
      message: 'Exiting... Please try again.'
    });
  }

  if (account.balance < parsedAmount) {
    return res.status(400).json({
      success: false,
      error: '[!] Insufficient balance!',
      message: 'Exiting... Please try again.'
    });
  }

  const result = accountService.withdraw(accountId, parsedAmount);

  return res.status(200).json({
    success: true,
    message: `Withdrawal of ${parsedAmount} successful!`,
    data: {
      accountId: result.accountId,
      accountHolderName: result.accountHolderName,
      balance: result.balance,
      status: result.status
    }
  });
};

// ─── CHECK BALANCE ────────────────────────────────────────────────────────────
const checkBalance = (req, res) => {
  const { accountId } = req.params;

  if (!accountId) {
    return res.status(400).json({
      success: false,
      error: '[!] Account ID is required!',
      message: 'Exiting... Please try again.'
    });
  }

  const account = accountService.getAccount(accountId);
  if (!account) {
    return res.status(404).json({
      success: false,
      error: '[!] Account not found!',
      message: 'Exiting... Please try again.'
    });
  }

  return res.status(200).json({
    success: true,
    message: 'Balance fetched successfully!',
    data: {
      accountId: account.accountId,
      accountHolderName: account.accountHolderName,
      balance: account.balance,
      status: account.status
    }
  });
};

// ─── CLOSE ACCOUNT (DELETE) ───────────────────────────────────────────────────
const closeAccount = (req, res) => {
  const { accountId } = req.params;

  if (!accountId) {
    return res.status(400).json({
      success: false,
      error: '[!] Account ID is required!',
      message: 'Exiting... Please try again.'
    });
  }

  const account = accountService.getAccount(accountId);
  if (!account) {
    return res.status(404).json({
      success: false,
      error: '[!] Account not found!',
      message: 'Exiting... Please try again.'
    });
  }

  const result = accountService.closeAccount(accountId);

  return res.status(200).json({
    success: true,
    message: `Account of ${result.accountHolderName} has been successfully closed.`,
    data: {
      accountId: result.accountId,
      accountHolderName: result.accountHolderName,
      balance: result.balance,
      status: result.status,
      closedAt: result.closedAt
    }
  });
};

// ─── UPDATE ACCOUNT (PUT) ─────────────────────────────────────────────────────
const updateAccount = (req, res) => {
  const { accountId } = req.params;
  const { accountHolderName } = req.body;

  if (!accountId) {
    return res.status(400).json({
      success: false,
      error: '[!] Account ID is required!',
      message: 'Exiting... Please try again.'
    });
  }

  if (!accountHolderName || typeof accountHolderName !== 'string' || accountHolderName.trim() === '') {
    return res.status(400).json({
      success: false,
      error: '[!] Name cannot be blank!',
      message: 'Exiting... Please try again.'
    });
  }

  const account = accountService.getAccount(accountId);
  if (!account) {
    return res.status(404).json({
      success: false,
      error: '[!] Account not found!',
      message: 'Exiting... Please try again.'
    });
  }

  if (account.status === 'CLOSED') {
    return res.status(400).json({
      success: false,
      error: '[!] Cannot update a closed account!',
      message: 'Exiting... Please try again.'
    });
  }

  const trimmedName = accountHolderName.trim().substring(0, 30);
  const result = accountService.updateAccount(accountId, trimmedName);

  return res.status(200).json({
    success: true,
    message: `Account updated successfully!`,
    data: {
      accountId: result.accountId,
      accountHolderName: result.accountHolderName,
      balance: result.balance,
      status: result.status,
      updatedAt: result.updatedAt
    }
  });
};

module.exports = {
  createAccount,
  deposit,
  withdraw,
  checkBalance,
  closeAccount,
  updateAccount
};