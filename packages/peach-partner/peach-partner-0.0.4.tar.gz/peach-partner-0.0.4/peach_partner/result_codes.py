from typing import Dict, List


class ResultCodeException(Exception):
    """Exception raised if failed to add a ResultCode."""

    pass


class ResultCode:
    """Represents a single result code.

    Attributes:
        code (str): code representing the result
        name (str): camelCase name of the result
        description (str): detailed description of the result
    """

    def __init__(self, code: str, name: str, description: str = None):
        """Constructs all the attributes for the ResultCode object.

        Parameters:
            code (str): code representing the result
            name (str): camelCase name of the result
            description (str): detailed description of the result

        Raises:
            ResultCodeException if result code name or number is not provided.
        """

        if not code:
            raise ResultCodeException("Result code number not provided")

        if not name:
            raise ResultCodeException("Result code name not provided")

        self.code = code
        self.name = name
        self.description = description


class ResultCodes:
    """Collection of ResultCodes.

    Usage:
    result_codes.TRANSACTION_SUCCEEDED.code == "000.000.000"
    result_codes.get("000.000.000").name == "TRANSACTION_SUCCEEDED"
    result_codes.get("000.000.000").description == "Transaction succeeded"

    Attributes:
        [ResultCode.name] (ResultCode)
        by_code (dict) ResultCodes indexed by code number
    """

    by_code: Dict[str, ResultCode] = {}

    def __init__(self, codes: List[List[str]]):
        """Calls add_code for each provided result code.

        Parameters:
            codes (list): A list of lists representing result code [number, name, description]
        """
        for c in codes:
            self._add_code(*c)

    def _add_code(self, code: str, name: str, description: str):
        """Creates ResultCode and adds it to self.

        Creates a ResultCode object.
        Then assigns it as an attribute using provided name.
        Then adds it to the `self.by_code` dict

        Parameters:
            code (str): code representing the result
            name (str): camelCase name of the result
            description (str): detailed description of the result

        Raises:
            ResultCodeException for duplicate entries.
        """
        if hasattr(self, name):
            raise ResultCodeException(f"Result code name '{name}' is already defined")

        if self.get(code):
            raise ResultCodeException(f"Result code '{code}' is already defined")

        result_code = ResultCode(code=code, name=name, description=description)
        setattr(self, name, result_code)
        self.by_code[code] = result_code

    def get(self, code: str):
        """Returns the result code identified by code number.

        Parameters:
            code (str): ResultCode number
        """
        return self.by_code.get(code)


result_codes_list = [
    ["000.000.000", "TRANSACTION_SUCCESS", "Transaction succeeded"],
    ["000.000.100", "SUCCESSFUL_REQUEST", "Successful request"],
    [
        "000.100.110",
        "SUCCESSFULLY_PROCESSED_IN_INTEGRATOR_TEST_MODE",
        "Request successfully processed in 'Merchant in Integrator Test Mode'",
    ],
    ["000.200.000", "TRANSACTION_PENDING", "Transaction pending"],
    ["700.400.580", "TRANSACTION_NOT_FOUND", "Cannot find transaction"],
    [
        "800.100.100",
        "TRANSACTION_DECLINED_UNKNOWN_REASON",
        "Transaction declined for unknown reason",
    ],
    [
        "800.100.150",
        "TRANSACTION_DECLINED_REFUND_GAMBLING_TX_NOT_ALLOWED",
        "Transaction declined (refund on gambling tx not allowed)",
    ],
    [
        "800.100.151",
        "TRANSACTION_DECLINED_INVALID_CARD",
        "Transaction declined (invalid card)",
    ],
    [
        "800.100.152",
        "TRANSACTION_DECLINED_BY_AUTH_SYSTEM",
        "Transaction declined by authorization system",
    ],
    [
        "800.100.153",
        "TRANSACTION_DECLINED_INVALID_CVV",
        "Transaction declined (invalid CVV)",
    ],
    [
        "800.100.154",
        "TRANSACTION_DECLINED_MARKED_INVALID",
        "Transaction declined (transaction marked as invalid)",
    ],
    [
        "800.100.155",
        "TRANSACTION_DECLINED_AMOUNT_EXCEED_CREDIT",
        "Transaction declined (amount exceeds credit)",
    ],
    [
        "800.100.156",
        "TRANSACTION_DECLINED_FORMAT_ERROR",
        "Transaction declined (format error)",
    ],
    [
        "800.100.157",
        "TRANSACTION_DECLINED_WRONG_EXPIRY_DATE",
        "Transaction declined (wrong expiry date)",
    ],
    [
        "800.100.158",
        "TRANSACTION_DECLINED_SUSPECTING_MANIPULATION",
        "Transaction declined (suspecting manipulation)",
    ],
    [
        "800.100.159",
        "TRANSACTION_DECLINED_STOLEN_CARD",
        "Transaction declined (stolen card)",
    ],
    [
        "800.100.160",
        "TRANSACTION_DECLINED_CARD_BLOCKED",
        "Transaction declined (card blocked)",
    ],
    [
        "800.100.161",
        "TRANSACTION_DECLINED_INVALID_TRIES",
        "Transaction declined (too many invalid tries)",
    ],
    [
        "800.100.162",
        "TRANSACTION_DECLINED_LIMIT_EXCEEDED",
        "Transaction declined (limit exceeded)",
    ],
    [
        "800.100.163",
        "TRANSACTION_DECLINED_MAXIMUM_TRANSACTION_FREQUENCY_EXCEEDED",
        "Transaction declined (maximum transaction frequency exceeded)",
    ],
    [
        "800.100.164",
        "TRANSACTION_DECLINED_MERCHANT_LIMIT_EXCEEDED",
        "Transaction declined (merchants limit exceeded)",
    ],
    [
        "800.100.165",
        "TRANSACTION_DECLINED_CARD_LOST",
        "Transaction declined (card lost)",
    ],
    [
        "800.100.166",
        "TRANSACTION_DECLINED_INCORRECT_ID",
        "Transaction declined (Incorrect personal identification number)",
    ],
    [
        "800.100.167",
        "TRANSACTION_DECLINED_NO_MATCH",
        "Transaction declined (referencing transaction does not match)",
    ],
    [
        "800.100.168",
        "TRANSACTION_DECLINED_CARD_REGISTERED",
        "Transaction declined (restricted card)",
    ],
    [
        "800.100.169",
        "TRANSACTION_DECLINED_CARD_TYPE_NOT_PROCESSED",
        "Transaction declined (card type is not processed by the authorization center)",
    ],
    [
        "800.100.170",
        "TRANSACTION_DECLINED_NOT_PERMITTED",
        "Transaction declined (transaction not permitted)",
    ],
    [
        "800.100.171",
        "TRANSACTION_DECLINED_PICK_UP_CARD",
        "Transaction declined (pick up card)",
    ],
    [
        "800.100.172",
        "TRANSACTION_DECLINED_ACCOUNT_BLOCKED",
        "Transaction declined (account blocked)",
    ],
    [
        "800.100.173",
        "TRANSACTION_DECLINED_INVALID_CURRENCY",
        "Transaction declined (invalid currency, not processed by authorization center)",
    ],
    [
        "800.100.174",
        "TRANSACTION_DECLINED_INVALID_AMOUNT",
        "Transaction declined (invalid amount)",
    ],
    [
        "800.100.175",
        "TRANSACTION_DECLINED_INVALID_BRAND",
        "Transaction declined (invalid brand)",
    ],
    [
        "800.100.176",
        "TRANSACTION_DECLINED_ACCOUNT_UNAVAILABLE",
        "Transaction declined (account temporarily not available. Please try again later)",
    ],
    [
        "800.100.177",
        "TRANSACTION_DECLINED_EMPTY_AMOUNT",
        "Transaction declined (amount field should not be empty)",
    ],
    [
        "800.100.178",
        "TRANSACTION_DECLINED_WRONG_PIN",
        "Transaction declined (PIN entered incorrectly too often)",
    ],
    [
        "800.100.179",
        "TRANSACTION_DECLINED_WITHDRAWAL_LIMIT",
        "Transaction declined (exceeds withdrawal count limit)",
    ],
    [
        "800.100.190",
        "TRANSACTION_DECLINED_INVALID_CONFIGURATION",
        "Transaction declined (invalid configuration data)",
    ],
    [
        "800.100.191",
        "TRANSACTION_DECLINED_WRONG_STATE",
        "Transaction declined (transaction in wrong state on aquirer side)",
    ],
    [
        "800.100.192",
        "TRANSACTION_DECLINED_INVALID_CVV_AMOUNT_RESERVED",
        "Transaction declined (invalid CVV, Amount has still been reserved on the customer's "
        "card and will be released in a few business days. Please ensure the CVV code is "
        "accurate before retrying the transaction)",
    ],
    [
        "800.100.195",
        "TRANSACTION_DECLINE_NO_USER_ACCOUNT",
        "Transaction declined (UserAccount Number/ID unknown)",
    ],
    [
        "800.100.196",
        "TRANSACTION_DECLINED_REGISTRATION_ERROR",
        "Transaction declined (registration error)",
    ],
    [
        "800.100.197",
        "TRANSACTION_DECLINED_EXT_CANCELLED_REGISTRATION",
        "Transaction declined (registration cancelled externally)",
    ],
    [
        "800.100.198",
        "TRANSACTION_DECLINE_INVALID_HOLDER",
        "Transaction declined (invalid holder)",
    ],
    [
        "800.100.199",
        "TRANSACTION_DECLINED_",
        "Transaction declined (invalid tax number)",
    ],
    ["800.100.200", "REFER_TO_PAYER", "Refer to Payer due to reason not specified"],
    ["800.100.201", "INCORRECT_ACCOUNT_DETAILS", "Account or Bank Details Incorrect"],
    ["800.100.202", "ACCOUNT_CLOSED", "Account Closed"],
    ["800.100.203", "INSUFFICIENT_FUNDS", "Insufficient Funds"],
    ["800.100.204", "MANDATE_EXPIRED", "Mandate Expired"],
    ["800.100.205", "MANDATE_DISCARDED", "Mandate Discarded"],
    [
        "800.100.206",
        "REFUND_REQUESTED_BY_CUSTOMER",
        "Refund of an authorized payment requested by the customer",
    ],
    ["800.100.207", "REFUND_REQUESTED", "Refund requested"],
    [
        "800.100.208",
        "DIRECT_DEBIT_NOT_ENABLED",
        "Direct debit not enabled for the specified account or bank",
    ],
    ["800.100.402", "HOLDER_NOT_VALID", "CC/bank account holder not valid"],
    [
        "800.100.403",
        "TRANSACTION_DECLINED_REVOCATION_AUTH_ORDER",
        "Transaction declined (revocation of authorisation order)",
    ],
    [
        "800.100.500",
        "RECURRING_PAYMENT_STOPPED",
        "Card holder has advised his bank to stop this recurring payment",
    ],
    [
        "800.100.501",
        "RECURRING_PAYMENT_STOPPED_FOR_MERCHANT",
        "Card holder has advised his bank to stop all recurring payments for this merchant",
    ],
    [
        "800.700.100",
        "TRANSACTION_SESSION_IS_BEING_PROCESSED",
        "Transaction for the same session is currently being processed, please try again "
        "later",
    ],
    ["800.700.101", "FAMILY_NAME_TOO_LONG", "Family name too long"],
    ["800.700.201", "GIVEN_NAME_TOO_LONG", "Given name too long"],
    ["800.700.500", "COMPANY_NAME_TOO_LONG", "Company name too long"],
    ["800.800.102", "INVALID_STREET", "Invalid street"],
    ["800.800.202", "INVALID_ZIP", "Invalid zip"],
    ["800.800.302", "INVALID_CITY", "Invalid city"],
    [
        "100.395.501",
        "PENDING_ONLINE_TRANSACTION_TIMEOUT",
        "Previously pending online transfer transaction timed out",
    ],
    ["100.396.101", "USER_CANCELLED", "Cancelled by user"],
    [
        "100.396.104",
        "UNCERTAIN_STATUS",
        "Uncertain status - probably cancelled by user",
    ],
    ["100.380.401", "USER_AUTH_FAIL", "User Authentication Failed"],
    ["100.380.501", "TRANSACTION_TIMEOUT", "Risk management transaction timeout"],
    [
        "100.400.000",
        "TRANSACTION_DECLINED_WRONG_ADDRESS",
        "Transaction declined (Wrong Address)",
    ],
    [
        "100.400.001",
        "TRANSACTION_DECLINED_WRONG_IDENTIFICATION",
        "Transaction declined (Wrong Identification)",
    ],
    [
        "100.400.002",
        "TRANSACTION_DECLINED_INSUFFICIENT_CREDIBILITY",
        "Transaction declined (Insufficient credibility score)",
    ],
    [
        "100.400.100",
        "TRANSACTION_DECLINED_BAD_RATING",
        "Transaction declined - very bad rating",
    ],
    ["100.400.121", "ACCOUNT_BLACKLISTED", "Account blacklisted"],
    ["900.100.200", "GATEWAY_ERROR_RESPONSE", "Error response from connector/acquirer"],
    ["900.300.600", "SESSION_TIMEOUT", "User session timeout"],
]
result_codes = ResultCodes(result_codes_list)
