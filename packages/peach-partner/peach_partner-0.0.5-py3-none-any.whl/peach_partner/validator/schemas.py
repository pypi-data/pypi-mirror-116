from iso4217 import Currency
from marshmallow import INCLUDE, Schema, fields, validate, validates, ValidationError
from ..result_codes import result_codes

PAYMENT_TYPE_DEBIT = "DB"
PAYMENT_TYPE_REFUND = "RF"


class Regexp(validate.Regexp):
    """Extends validate.Regexp to add desired error response."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, error="Must match {regex}")


class CustomerSchema(Schema):
    """Optional object sent if Partner requires customer data."""

    email = fields.Email(validate=validate.Length(min=6, max=128))
    fax = fields.Str(validate=Regexp(regex=r"^[+0-9][0-9 \.()/-]{7,25}$"))
    givenName = fields.Str(
        validate=Regexp(regex=r"^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,127}$")
    )
    surname = fields.Str(
        validate=Regexp(regex=r"^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,127}$")
    )
    mobile = fields.Str(validate=Regexp(regex=r"^[+0-9][0-9 \.()/-]{5,25}$"))
    phone = fields.Str(validate=Regexp(regex=r"^[+0-9][0-9 \.()/-]{7,25}$"))
    ip = fields.IP()
    merchantCustomerLanguage = fields.Str(validate=validate.Length(min=1, max=255))
    status = fields.Str(validate=validate.Length(min=1, max=255))
    merchantCustomerId = fields.Str(validate=validate.Length(min=1, max=255))
    taxId = fields.Str(validate=validate.Length(min=1, max=100))
    taxType = fields.Str(validate=validate.Length(min=1, max=255))

    class Meta:
        unknown = INCLUDE


class CardSchema(Schema):
    """The card data structure holds all information regarding a credit or debit card."""

    number = fields.Str(required=True, validate=Regexp(regex=r"^[0-9]{12,19}$"))
    cvv = fields.Str(validate=Regexp(regex=r"^[0-9]{3,4}$"))
    expiryMonth = fields.Str(required=True, validate=Regexp(regex=r"^(0[1-9]|1[0-2])$"))
    expiryYear = fields.Str(required=True, validate=Regexp(regex=r"^(20)([0-9]{2})$"))
    holder = fields.Str(
        validate=Regexp(regex=r"^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,127}$")
    )


class DataSchema(Schema):
    """Optional object that can be used for billing/shipping information."""

    city = fields.Str(validate=validate.Length(min=1, max=48))
    company = fields.Str(validate=validate.Length(min=1, max=255))
    country = fields.Str(validate=Regexp(regex=r"^[A-Z]{2}$"))
    houseNumber1 = fields.Str(validate=validate.Length(min=1, max=100))
    postcode = fields.Str(validate=validate.Length(min=1, max=16))
    state = fields.Str(validate=Regexp(regex=r"^[a-zA-Z0-9\.]{1,10}$"))
    street1 = fields.Str(validate=validate.Length(min=1, max=95))
    street2 = fields.Str(validate=validate.Length(min=1, max=95))
    customer = fields.Nested(CustomerSchema())

    class Meta:
        unknown = INCLUDE


class BaseSchema(Schema):
    """Schema with fields common to refund and debit requests and responses."""

    uniqueId = fields.UUID(required=True)
    amount = fields.Str(required=True, validate=Regexp(regex=r"[0-9]{1,10}(.[0-9]{2})?"))
    currency = fields.Str(required=True, validate=validate.Length(equal=3))
    paymentBrand = fields.Str(required=True, validate=validate.Length(min=1, max=255))

    @validates("currency")
    def validate_currency(self, value, **kwargs):
        """Validating currency."""
        try:
            Currency(value)
        except ValueError:
            raise ValidationError("Must be a valid ISO-4217, 3-character currency.")


class DebitRequestSchema(BaseSchema):
    """Represents initial debit request fields sent by Peach to Partner API."""

    configuration = fields.Dict(required=True)
    paymentType = fields.Str(
        required=True, validate=validate.Equal(comparable=PAYMENT_TYPE_DEBIT)
    )
    customer = fields.Nested(CustomerSchema())
    customerParameters = fields.Dict()
    merchantName = fields.Str(validate=validate.Length(min=1, max=255))
    merchantTransactionId = fields.Str(validate=validate.Length(min=8, max=255))
    merchantInvoiceId = fields.Str(
        validate=Regexp(regex=r"^[\w~!@#$%\^&*()+\-,./:?\][\\\{}`;|\"']{8,255}$")
    )
    notificationUrl = fields.Url(required=True)
    shopperResultUrl = fields.Url(required=True)
    card = fields.Nested(CardSchema)
    billing = fields.Nested(DataSchema())
    shipping = fields.Nested(DataSchema())

    class Meta:
        unknown = INCLUDE


class Result(Schema):
    """Result fields sent in the debit response."""

    code = fields.Str(required=True, validate=Regexp(regex=r"^([0-9]{3}.[0-9]{3}.[0-9]{3})?$"))
    description = fields.Str(required=True, validate=validate.Length(min=1, max=255))

    @validates("code")
    def validate_code(self, value, **kwargs):
        """Validating result code."""
        if not result_codes.get(value):
            raise ValidationError(f"Unknown result code {value}.")


class Parameter(Schema):
    """Parameters sent in the redirect object."""

    name = fields.Str(required=True)
    value = fields.Str(required=True)


class Redirect(Schema):
    """Fields used to provide the redirect information."""

    url = fields.URL(required=True)
    method = fields.Str(required=True, validate=validate.OneOf(choices=["GET", "POST"]))
    parameters = fields.List(fields.Nested(Parameter), required=True)


class DebitResponseSchema(BaseSchema):
    """Defines fields to be sent as a debit response."""

    paymentType = fields.Str(
        required=True, validate=validate.Equal(comparable=PAYMENT_TYPE_DEBIT)
    )
    result = fields.Nested(Result, required=True)
    resultDetails = fields.Dict(required=True)
    redirect = fields.Nested(Redirect, required=True)
    connectorTxID1 = fields.UUID(required=True)
    timestamp = fields.DateTime(required=True)

    class Meta:
        unknown = INCLUDE


class RefundRequestSchema(BaseSchema):
    """Refund transaction request sent by Peach to Partner API."""

    configuration = fields.Dict(required=True)

    paymentType = fields.Str(
        required=True, validate=validate.Equal(comparable=PAYMENT_TYPE_REFUND)
    )
    customer = fields.Nested(CustomerSchema())
    customParameters = fields.Dict()
    notificationUrl = fields.URL(required=True)

    class Meta:
        unknown = INCLUDE


class RefundResponseSchema(BaseSchema):
    """Defines fields to be sent as a refund response."""

    paymentType = fields.Str(
        required=True, validate=validate.Equal(comparable=PAYMENT_TYPE_DEBIT)
    )
    result = fields.Nested(Result, required=True)
    resultDetails = fields.Dict(required=True)
    connectorTxID1 = fields.UUID(required=True)
    timestamp = fields.DateTime(required=True)
