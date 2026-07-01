# Indian Bank API — Node.js / Express

A REST API conversion of the original COBOL `bank-account.cob` program.  
All original business logic (account creation, deposit, withdrawal, balance check) is preserved as REST endpoints.

---

## Tech Stack

- **Runtime:** Node.js
- **Framework:** Express 4
- **Storage:** In-memory (Map) — mirrors COBOL WORKING-STORAGE

---

## Project Structure

```
indian-bank-api/
├── src/
│   ├── index.js                  # Entry point — Express app + server startup
│   ├── routes/
│   │   └── account.routes.js     # Route definitions
│   ├── controllers/
│   │   └── account.controller.js # Request handling + validation (mirrors COBOL PROCEDURE DIVISION)
│   ├── services/
│   │   └── account.service.js    # Business logic (deposit, withdraw, balance)
│   ├── store/
│   │   └── accountStore.js       # In-memory data store (mirrors WORKING-STORAGE)
│   └── utils/
│       └── uuid.js               # UUID generator for accountId
├── api-endpoints.json            # Postman Collection v2.1 — import directly
├── .env.example
├── package.json
└── README.md
```

---

## Setup & Run

```bash
npm install
npm start
```

Server starts at: **http://localhost:3000**

For development with auto-reload:
```bash
npm run dev
```

---

## API Endpoints

### 1. Create Account
**POST** `/api/account/create`

Mirrors COBOL: accepting `WS-ACCOUNT-HOLDER` and `WS-BALANCE`, with all original validations.

**Request Body:**
```json
{
  "accountHolderName": "Rahul Sharma",
  "openingBalance": 10000
}
```

**Success Response (201):**
```json
{
  "success": true,
  "message": "Hello, Rahul Sharma! Your Account is Ready.",
  "data": {
    "accountId": "a1b2c3d4-...",
    "accountHolderName": "Rahul Sharma",
    "balance": 10000,
    "status": "ACTIVE"
  }
}
```

**Validation Errors (400):**
```json
{ "success": false, "error": "[!] Name cannot be blank!", "message": "Exiting... Please try again." }
{ "success": false, "error": "[!] Opening Balance cannot be 0!", "message": "Exiting... Please try again." }
```

---

### 2. Deposit Money
**POST** `/api/account/deposit`

Mirrors COBOL `DEPOSIT-PARA`.

**Request Body:**
```json
{
  "accountId": "<accountId-from-create>",
  "amount": 5000
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "DEPOSIT SUCCESSFUL!",
  "data": {
    "accountHolderName": "Rahul Sharma",
    "amountDeposited": "Rs 5000.00",
    "newBalance": "Rs 15000.00"
  }
}
```

**Validation Error (400):**
```json
{ "success": false, "error": "[!] Amount cannot be 0 or blank!", "message": "Please enter a valid amount." }
```

---

### 3. Withdraw Money
**POST** `/api/account/withdraw`

Mirrors COBOL `WITHDRAW-PARA`.

**Request Body:**
```json
{
  "accountId": "<accountId-from-create>",
  "amount": 3000
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "WITHDRAWAL SUCCESSFUL!",
  "data": {
    "accountHolderName": "Rahul Sharma",
    "amountWithdrawn": "Rs 3000.00",
    "newBalance": "Rs 7000.00"
  }
}
```

**Insufficient Funds Response (422):**
```json
{
  "success": false,
  "message": "[X] TRANSACTION FAILED!",
  "data": {
    "accountHolderName": "Sana Khan",
    "requestedAmount": "Rs 9000.00",
    "availableBalance": "Rs 2000.00",
    "reason": "Insufficient Funds!"
  }
}
```

---

### 4. Check Balance
**GET** `/api/account/balance/:accountId`

Mirrors COBOL `BALANCE-PARA`.

**Success Response (200):**
```json
{
  "success": true,
  "message": "ACCOUNT STATEMENT",
  "data": {
    "accountHolderName": "Amit Kumar",
    "currentBalance": "Rs 20000.00",
    "status": "ACTIVE"
  }
}
```

---

## Postman Collection

Import `api-endpoints.json` directly into Postman:

1. Open Postman → **Import**
2. Select `api-endpoints.json`
3. Run **Create Account** first to get an `accountId`
4. Use that `accountId` in Deposit, Withdraw, and Balance requests

---

## COBOL → Node.js Mapping

| COBOL Construct | Node.js Equivalent |
|---|---|
| `WORKING-STORAGE SECTION` | `src/store/accountStore.js` (in-memory Map) |
| `WS-ACCOUNT-HOLDER PIC A(30)` | `accountHolderName` string field (max 30 chars) |
| `WS-BALANCE PIC 9(8)V99` | `balance` float, stored with `.toFixed(2)` precision |
| `WS-AMOUNT PIC 9(8)V99` | `amount` float in request body |
| `MAIN-PARA` | `POST /api/account/create` controller |
| `DEPOSIT-PARA` | `POST /api/account/deposit` controller |
| `WITHDRAW-PARA` | `POST /api/account/withdraw` controller |
| `BALANCE-PARA` | `GET /api/account/balance/:accountId` controller |
| `DISPLAY` + `STOP RUN` | JSON response with appropriate HTTP status code |

---

## Validation Rules (same as original COBOL)

| Field | Rule | HTTP Status | Error |
|---|---|---|---|
| `accountHolderName` | Cannot be blank/spaces | 400 | `[!] Name cannot be blank!` |
| `openingBalance` | Must be > 0 | 400 | `[!] Opening Balance cannot be 0!` |
| `amount` (deposit/withdraw) | Must be > 0 | 400 | `[!] Amount cannot be 0 or blank!` |
| `amount` (withdraw) | Must not exceed balance | 422 | `Insufficient Funds!` |
| `accountId` | Must exist in store | 404 | `Account not found.` |