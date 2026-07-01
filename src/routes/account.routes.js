const express = require('express');
const router = express.Router();
const accountController = require('../controllers/account.controller');

router.post('/create', accountController.createAccount);
router.post('/deposit', accountController.deposit);
router.post('/withdraw', accountController.withdraw);
router.get('/balance/:accountId', accountController.checkBalance);
router.delete('/close/:accountId', accountController.closeAccount);
router.put('/update/:accountId', accountController.updateAccount);

module.exports = router;