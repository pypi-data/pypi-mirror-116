"""This module provides functionalities for setting up a command line
parser and some functions to extract data from parsed command line arguments.
"""

import argparse
import json
from s3i import IdentityProvider, TokenType


GRANT_TYPES = ("client_credentials", "password")


def configure_client_parser(parser):
    """Adds subparsers to parser allowing the specification of a
    client via file or terminal input.

    :param parser: Parser to be modified
    :returns: Modified parser
    :rtype: argparse.ArgumentParser
    """

    # Setup a parser for file input
    subparsers = parser.add_subparsers(required=True, dest="client")
    client_file_parser = subparsers.add_parser(
        "cfi", help="Specify client and seceret via file input."
    )
    client_file_parser.add_argument("cfp", help="Filepath")

    # Setup a parser for user input
    client_ui_parser = subparsers.add_parser(
        "cui", help="Specify client and secret via terminal."
    )
    client_ui_parser.add_argument(
        "-c", default="admin-cli", help="Client name: admin-cli is default"
    )
    client_ui_parser.add_argument(
        "-cs", default="", help="Client secret: empty string is default"
    )
    return client_file_parser, client_ui_parser


def configure_user_parser(parser):
    """Adds subparsers to parser allowing the specification of a
    username and a password via file or terminal input.

    :param parser: Parser to be modified
    :returns: Modified parser
    :rtype: argparse.ArgumentParser
    """
    # Setup a parser for file input
    subparsers = parser.add_subparsers(required=True, dest="user")
    user_file_parser = subparsers.add_parser(
        "ufi", help="Specifiy username and password via file input."
    )
    user_file_parser.add_argument("ufp", help="Filepath to credentials.")

    # Setup a parser for user input
    user_ui_parser = subparsers.add_parser(
        "uui", help="Specify username and password via terminal."
    )
    user_ui_parser.add_argument("-u", required=True, help="Username")
    user_ui_parser.add_argument("-up", required=True, help="User password")
    return user_file_parser, user_ui_parser


def configure_credentials_parser(parser):
    """Adds arguments to parser allowing to specify the grant type
    used to retrieve a java web token.  Afterwards
    configure_client_parser and configure_user_parser are called.

    :param parser: Parser to be modified
    :returns: Modified parser
    :rtype: argparse.ArgumentParser
    """
    parser.add_argument(
        "--g",
        choices=GRANT_TYPES,
        default=GRANT_TYPES[0],
        help=f"Specify grant type ({GRANT_TYPES[0]} is default)",
    )
    parser.add_argument(
        "--scope", default="email", help="Specifiy the scope (email is default)"
    )

    cfi_parser, cui_parser = configure_client_parser(parser)
    __cfi_ufi_parser, __cfi_uui_parser = configure_user_parser(cfi_parser)
    __cui_ufi_parser, __cui_uui_parser = configure_user_parser(cui_parser)
    return parser


def get_token_from_args(args):
    """Extracts the credentials from args and returns a java web
    token.

    :param args: argparse.Namespace object
    :returns: A java webo token or an error message.
    :rtype: str
    """

    grant_type = args.g
    scope = args.scope
    client = None
    secret = None
    username = None
    password = None

    if args.client == "cfi":
        filepath = args.cfp
        client, secret = parse_client_id_and_secret(filepath)
    else:
        client = args.c
        secret = args.cs

    if args.user == "ufi":
        filepath = args.ufp
        username, password = parse_username_and_password(filepath)
    else:
        username = args.u
        password = args.up

    token = get_access_token(grant_type,
                             client,
                             secret,
                             username,
                             password,
                             scope)
    return str(token)


def parse_username_and_password(filepath):
    """Reads the file specified by filepath and returns username and
    password.

    :param filepath: Path to a json file
    :returns: Username and password
    :rtype: (str, str)
    """
    username = None
    password = None
    if filepath is not None:
        with open(filepath, "r") as json_f:
            js_object = json.load(json_f)
            username = js_object["name"]
            password = js_object["password"]
    return username, password


def parse_client_id_and_secret(filepath):
    """Reads the file specified by filepath and returns the client id
    and the client secret.

    :param filepath: Path to a json file
    :returns: Client id and client secret
    :rtype: (str, str)
    """
    client_id = None
    client_secret = None
    if filepath is not None:
        with open(filepath, "r") as json_f:
            js_object = json.load(json_f)
            client_id = js_object.get("thingId", None)
            if not client_id:
                client_id = js_object.get("identifier")
            client_secret = js_object.get("client_secret")
            if not client_secret:
                client_secret = js_object.get("secret")
    return client_id, client_secret


def get_access_token(grant_type, client_id, client_secret, username, password, scope):
    """Returns a java web token.

    :param grant_type: method used to retrieve the token
    :param client_id: s3i specific client identifier
    :param client_secret: secret of the client
    :param username: username
    :param password: password
    :param scope:
    :returns: java web token
    :rtype: str

    """

    idp = IdentityProvider(
        grant_type=grant_type,
        client_id=client_id,
        username=username,
        password=password,
        client_secret=client_secret,
        realm="KWH",
        identity_provider_url="https://idp.s3i.vswf.dev/",
    )
    return idp.get_token(TokenType.ACCESS_TOKEN, scope=scope)
