# Peach Partner Library

## Overview

**Peach Partner Library** is a platform agnostic Python package to help integrating PeachPayments with their partners.


**Documentation**:

**Source Code**: https://gitlab.com/peachpayments/peach-partner-python/

---

## Usage
Package requires Python 3.9+

### Installation
```sh
# pip
$ pip3 install peach-partner
```
```sh
# poetry
$ poetry add peach-partner
```
### Result codes
```python
from peach_partner.result_codes import result_codes

result_codes.TRANSACTION_SUCCEEDED.code == "000.000.000"
result_codes.get("000.000.000").name == "TRANSACTION_SUCCEEDED"
result_codes.get("000.000.000").description == "Transaction succeeded"
```
### Field validation
TODO
### Authentication
TODO
