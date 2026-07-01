const express = require('express');
const accountRoutes = require('./routes/account.routes');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/', (req, res) => {
  res.json({
    bank: 'Indian Bank',
    message: 'Welcome to Indian Bank API',
    version: '1.0.0',
    endpoints: {
      'POST /api/account/create': 'Create a new bank account',
      'POST /api/account/deposit': 'Deposit money into an account',
      'POST /api/account/withdraw': 'Withdraw money from an account',
      'GET /api/account/balance/:accountId': 'Check account balance'
    }
  });
});

app.use('/api/account', accountRoutes);

app.use((req, res) => {
  res.status(404).json({ success: false, error: 'Route not found' });
});

app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ success: false, error: 'Internal Server Error' });
});

app.listen(PORT, () => {
  console.log('************************************');
  console.log('*                                  *');
  console.log('*      WELCOME TO INDIAN BANK      *');
  console.log('*                                  *');
  console.log('************************************');
  console.log(`Server running on http://localhost:${PORT}`);
});

module.exports = app;