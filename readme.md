# Procuret Python

A Python library for interfacing with Procuret API.
[Procuret](https://procuret.com) is a
business - to - business payment platform that allows customers to pay
for purchases over time, while the supplier is paid upfront.

## Contents

1. [Installation](#installation)
2. [Documentation](#documentation)
3. [Support](#support)

## Installation

Procuret Python may be [installed via PIP](https://pypi.org/project/procuret):

```bash
$ pip install procuret
```

To update Procuret Python to the latest version, use `pip --upgrade`:

```bash
$ pip install --upgrade procuret
```

## Documentation

Procuret Python offers a library of classes that map to services provided
by the Procuret API.

### `Session`

Sessions are the means of authenticating requests to the Procuret API. All
requests to Procuret API, save for those creating Sessions themselves, require
a Session.

In Procuret Python, the `Session` class will handle all authentication for you.
For example, it will compute the SHA256 signature that must be included
in your HTTP headers.

#### Properties

- `.session_id: int` - A 63-bit positive integer uniquely identifying this
`Session`. `Session` will include this number in requests to Procuret API, so
that Procuret API can identify you.
- `.api_key` - A 192-bit random number encoded in urlsafe base64 and generated
in a cryptographically secure manner. `Session` will use this key to sign your
requests to Procuret API using the SHA256 algorithm.

#### Methods

##### `.create_with_email(...) -> Session`

Use `.create_with_email()` to create a new `Session`. This is analogous to
"logging in" to the Procuret API.

###### Parameters

1. `email: str` - Your account email
2. `plaintext_secret: str` - Your plaintext passphrase
3. `perspective: Perspective` - an instance of `Perspective`
4. `code: str` - A two factor authentication code. Obtain via `SecondFactorCode`
5. `lifecycle: Lifecycle` - Defaults to `.LONG_LIVED`

###### Example Usage

```python
session = Session.create_with_email(
    email='me@somedomain.com',
    plaintext_secret='excellent passphrase',
    perspective=Perspective.SUPPLIER,
    code='123456'
)
```

##### `.from_interactive_prompt() -> Session`

Call this method to use an interactive `Session` creation procedure.

### `SecondFactorCode`

`SecondFactorCode` allows you to generate two-factor authentication codes for
use in creating `Session` instances.

#### Methods

##### `.create_with_email(...) -> None`

This method will cause a two-factor authorisation code to be sent to the
communication method associated with your Procuret account. You can then
use that code as the `code` parameter when creating a `Session`.

###### Parameters

1. `email: str` - Your account email
2. `plaintext_secret: str` - Your plaintext passphrase
3. `perspective: Perspective` - an instance of `Perspective`

###### Example Usage

```python
SecondFactorCode.create_with_email(
    email='someone@somewhere.com',
    plaintext_secret='excellent passphrase',
    perspective=Perspective.BUSINESS
)
```

### `InstalmentLink`

`InstalmentLink` facilitates the creation of customised links to the Procuret
Instalment Product (PIP). PIP allows a customer Business to pay for a purchase
over time, while you the Supplier are paid upfront.

When you create an `InstalmentLink`, you can ask Procuret to send an email
to the customer Business on your behalf.

#### Properties

- `.invitee_email: str` - The email address you associated with the link
- `.invoice_amount: Decimal` - The invoice amount presented by the link
- `.invoice_identifier: str` - The invoice ID presented by the link
- `.url: str` - The URL of the link

#### Methods

##### `.create(...) -> InstalmentLink`

###### Parameters

1. `supplier: Union[int, EntityHeadline]` - Either the unique integer
identifier of your Supplier entity in Procuret, or an instead of
`EntityHeadline` describing your Supplier entity.
2. `invoice_amount: Decimal` - The amount that you wish to charge the customer,
in Australian dollars.
3. `invoice_email: str` - The email address you wish to associate with this
link.
4. `invoice_identifier: str` - Your own identifier for the invoice. For
example, you might use an invoice number from your accounting system.
5. `communication: CommunicationOption` - An instance of `CommunicationOption`,
which will tell Procuret API what you want it to do with the supplied email
address.
6. `session: Session` - An instance of `Session`, which will be used to
authenticate your request.

###### Example usage

```python
# First we get a Session. In this case we authenticate with email and
# passphrase. In a real integration, you might store the Session elsehwhere.
session = Session.create_with_email(
    email=email,
    plaintext_secret=secret,
    perspective=Perspective.SUPPLIER,
    code='12346'  # Obtained via `SecondFactorCode`
)

# Now we use the Session in an InstalmentLink.create() call, along with
# the parameters describing the link. By supplying
# CommunicationOption.EMAIL_CUSTOMER, we tell Procuret that we would like
# Procuret to send an email to the customer on our behalf inviting them
# to pay using the link.
link = InstalmentLink.create(
    supplier=supplier_id,
    invoice_amount=Decimal('422.42'),
    invitee_email='someone@great-domain.org',
    invoice_identifier='T 055',
    communication=CommunicationOption.EMAIL_CUSTOMER,
    session=session
)
```

### `Perspective`

Perspective is an enumeration of possible angles from which a client
can engage with Procuret. If you wish to use Procuret services from
the perspective of a Supplier, you will create a `Session` with the
`Perspective.SUPPLIER` case.

#### Cases

- `.SUPPLIER`
- `.BUSINESS`

### Lifecycle

An enumeration of possible `Session` lifecycles - A "short lived" `Session` will
expire after a period of disuse. A "long lived" `Session` will never expire,
and must be manually deleted.

Consider opting for a short-lived `Session` wherever practical, to reduce the
probability of the stored credential being compromised.

#### Cases

- `.LONG_LIVED`
- `.SHORT_LIVED`

### `CommunicationOption`

An enumeration of instructions you can send Procuret in some contexts, to
tell it how you wish for it to contact (or not contact) the a customer.

#### Cases

- `.EMAIL_CUSTOMER` - Procuret will contact the customer by email
- `.DO_NOT_CONTACT_CUSTOMER` - Procuret will not try to contact the customer


## Support

Please contact us anytime at [support@procuret.com](mailto:support@procuet.com)
with any questions. To chat with us less formally, please feel free to tweet
[@hugh_jeremy](https://twitter.com/hugh_jeremy).

For more general information about Procuret, please visit
[procuret.com](https://procuret.com).
