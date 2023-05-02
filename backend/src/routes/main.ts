import express from 'express';
import controller from '../interfaces/main';
const router = express.Router();

router.get('/accounts', controller.listAccounts);
router.get('/addressInfo', controller.getAddressInfo);

export = router;