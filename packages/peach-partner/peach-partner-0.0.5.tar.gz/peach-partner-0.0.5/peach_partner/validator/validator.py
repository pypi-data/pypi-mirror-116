from typing import Type, Union

from .schemas import (
    DebitRequestSchema,
    DebitResponseSchema,
    RefundRequestSchema,
    RefundResponseSchema,
)
from ..result_codes import result_codes


ValidateRequestReturnType = dict[str, Union[bool, dict[str, str], list[str]]]
ValidateResponseReturnType = dict[str, Union[bool, list[str]]]


def _validate_request(schema: Type, data: dict) -> ValidateRequestReturnType:
    """Validate Peach request fields.

        Arguments:
        schema: Schema class defined in .schemas
        data (dict): request fields as defined in spec

    Returns:
        (dict): validated data
    """
    response: ValidateRequestReturnType = dict(valid=True)
    errors = schema().validate(data)
    if errors:
        response["valid"] = False
        response["result"] = dict(
            # TODO modify result_codes to support typing
            code=result_codes.INVALID_OR_MISSING_PARAMETER.code,  # type: ignore
            description=result_codes.INVALID_OR_MISSING_PARAMETER.description,  # type: ignore
        )
        response["errors"] = errors
        parameter_errors = []
        for field in errors:
            parameter_errors.append(f"{field}: {errors[field]}")

        response["parameterErrors"] = parameter_errors
    return response


def _validate_response(schema: Type, data: dict) -> ValidateResponseReturnType:
    """Validate endpoint response fields.

        Arguments:
        schema: Schema class defined in .schemas
        data (dict): response fields as defined in spec

    Returns:
        (dict): validated data
    """
    errors = schema().validate(data)
    response: ValidateResponseReturnType = dict(valid=True)
    if errors:
        response["valid"] = False
        response["errors"] = errors

    return response


def validate_debit_request(data: dict) -> ValidateRequestReturnType:
    """Validates Debit request data.

    Arguments:
        data (dict): debit request fields as defined in spec

    Returns:
        (dict): validated data
    """
    return _validate_request(DebitRequestSchema, data)


def validate_debit_response(data: dict) -> ValidateResponseReturnType:
    """Validates Debit response data.

    Arguments:
        data (dict): debit response fields as defined in spec

    Returns:
        (dict): validated data
    """
    return _validate_response(DebitResponseSchema, data)


def validate_refund_request(data: dict) -> ValidateRequestReturnType:
    """Validates Refund request data.

    Arguments:
        data (dict): refund request fields as defined in spec

    Returns:
        (dict): validated data
    """
    return _validate_request(RefundRequestSchema, data)


def validate_refund_response(data: dict) -> ValidateResponseReturnType:
    """Validates Refund response data.

    Arguments:
        data (dict): refund response fields as defined in spec

    Returns:
        (dict): validated data
    """
    return _validate_response(RefundResponseSchema, data)
