const { v4: uuidv4 } = require('../utils/uuid');
const store = require('../store/accountStore');

// ─── CREATE ACCOUNT ───────────────────────────────────────────────────────────
const createAccount = (accountHolderName, openingBalance) => {
  const accountId = uuidv4();
  const account = {
    accountId,
    accountHolderName,
    balance: parseFloat(openingBalance.toFixed(2)),
    status: 'ACTIVE',
    createdAt: new Date().toISOString()
  };
  store.set(accountId, account);
  return account;
};

// ─── GET ACCOUNT ──────────────────────────────────────────────────────────────
const getAccount = (accountId) => {
  return store.get(accountId) || null;
};

// ─── DEPOSIT ──────────────────────────────────────────────────────────────────
const deposit = (accountId, amount) => {
  const account = store.get(accountId);
  if (!account) return null;
  account.balance = parseFloat((account.balance + amount).toFixed(2));
  store.set(accountId, account);
  return account;
};

// ─── WITHDRAW ─────────────────────────────────────────────────────────────────
const withdraw = (accountId, amount) => {
  const account = store.get(accountId);
  if (!account) return null;
  account.balance = parseFloat((account.balance - amount).toFixed(2));
  store.set(accountId, account);
  return account;
};

// ─── CLOSE ACCOUNT (DELETE) ───────────────────────────────────────────────────
const closeAccount = (accountId) => {
  const account = store.get(accountId);
  if (!account) return null;
  account.status = 'CLOSED';
  account.closedAt = new Date().toISOString();
  store.set(accountId, account);
  return account;
};

// ─── UPDATE ACCOUNT (PUT) ─────────────────────────────────────────────────────
const updateAccount = (accountId, accountHolderName) => {
  const account = store.get(accountId);
  if (!account) return null;
  account.accountHolderName = accountHolderName;
  account.updatedAt = new Date().toISOString();
  store.set(accountId, account);
  return account;
};

module.exports = {
  createAccount,
  getAccount,
  deposit,
  withdraw,
  closeAccount,
  updateAccount
};