require('dotenv').config()

import { Request, Response, NextFunction } from 'express';
import axios, { Axios, AxiosResponse } from 'axios';

const LWS_URL = process.env.LWS_URL ?? "http://127.0.0.1:8080";
const LWS_ADMIN_URL = process.env.LWS_ADMIN_URL ?? "http://127.0.0.1:8081";

// interface Auth {
//     auth: String;
// }

// accept_requests: {"type": "import"|"create", "addresses":[...]}
// add_account: {"address": ..., "key": ...}
// list_accounts: {}
// list_requests: {}
// modify_account_status: {"status": "active"|"hidden"|"inactive", "addresses":[...]}
// reject_requests: {"type": "import"|"create", "addresses":[...]}
// rescan: {"height":..., "addresses":[...]}
// webhook_add: {"type":"tx-confirmation", "address":"...", "url":"...", ...} with optional fields:
//     token: A string to be returned when the webhook is triggered
//     payment_id: 16 hex characters representing a unique identifier for a transaction
// webhook_delete

const listAccounts = async (req: Request, res: Response, next: NextFunction) => {
    let response: AxiosResponse = await axios.post(`${LWS_ADMIN_URL}/list_accounts`, {
        "auth": ""
    });
    return res.status(200).json({
        message: response.data
    });
};

const getAddressInfo = async (req: Request, res: Response, next: NextFunction) => {
    let response: AxiosResponse = await axios.post(`${LWS_URL}/get_address_info`, {
        "address": "",
        "view_key": ""
    });
    return res.status(200).json({
        message: response.data
    });
}

export default { listAccounts, getAddressInfo };
