/**
 * In-memory store to hold account data.
 * Mirrors the COBOL WORKING-STORAGE SECTION variables:
 *   WS-ACCOUNT-HOLDER  PIC A(30)
 *   WS-BALANCE         PIC 9(8)V99
 * Each session in COBOL held a single account; here we support multiple accounts
 * identified by a generated accountId, persisted in memory for the server lifetime.
 */
const accounts = new Map();

const set = (key, value) => accounts.set(key, value);
const get = (key) => accounts.get(key);
const has = (key) => accounts.has(key);
const del = (key) => accounts.delete(key);
const all = () => Array.from(accounts.values());

module.exports = { set, get, has, del, all };