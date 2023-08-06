"""This module implements the thing class which is the core element of
this package."""

import os
from os import listdir
from os.path import isfile, join, splitext
import threading
import json
from ast import literal_eval
import uuid
import time
from datetime import datetime
import copy
from s3i import IdentityProvider, TokenType, Directory
from s3i import Repository
from s3i import EventSubscriptionReply, EventUnsubscriptionReply, EventManager, EventFilterType
import s3i.exception
from s3i.broker import Broker, BrokerREST
from s3i.messages import ServiceReply, GetValueReply, SetValueReply
from ml.tools import find_broker_endpoint, XML, DataBase
from ml.app_logger import APP_LOGGER


class BaseVariable:
    """The BaseVariable class holds various urls to s3i services."""

    IDP_URL = "https://idp.s3i.vswf.dev/"
    IDP_REALM = "KWH"
    BROKER_HOST = "rabbitmq.s3i.vswf.dev"
    REPO_WWS_URL = "wss://ditto.s3i.vswf.dev/ws/2"
    REPO_URL = "https://ditto.s3i.vswf.dev/api/2/"
    DIR_URL = "https://dir.s3i.vswf.dev/api/2/"


class Thing:
    """The thing class represents a customizable runtime environment for
    operating Digital Twins complying the Forest Modeling Language (fml40)."""

    def __init__(
            self,
            model: dict,
            client_secret="",
            grant_type="password",
            is_broker=False,
            is_repo=False,
            is_broker_rest=True,
            is_stanford2010=False,
            stanford2010_path=None,
            is_stanford2010_sync=False,
            stanford2010_sync_freq=None,
            is_database=None,
            database_file=None,
            username=None,
            password=None,
    ):
        """
        Constructor

        :param model: edge-device or S³I Repository specified JSON entry, like config file for Digital Twins
        :type model: dict
        :param client_secret: OAuth 2.0 specified client secret, generated in the S³I IdentityProvider
        :type client_secret: str
        :param grant_type: OAuth 2.0 specified grant type to issue a JWT. Here the grant type can be password or client_credentials
        :type grant_type: str
        :param is_broker: whether broker interface is enabled in the ml40::thing instance
        :type is_broker: bool
        :param is_broker_rest: Whether the connection with the S³I Broker is established via HTTP REST
        :type is_broker_rest: bool
        :param is_repo: Whether the thing uses the S³I Repository to launch its Digital Twin in the cloud
        :type is_repo: bool
        :param is_stanford2010: Whether the thing has a extern resource in form of a .hpr data
        :type is_stanford2010: bool
        :param stanford2010_path: absolute path of stanford2010 (hpr) data
        :type stanford2010_path: string
        :param username: OAuth 2.0 specified username, registered in the S³I IdentityProvider. If the grant_type is set as password, the username is required
        :type username: str
        :param password: OAuth 2.0 specified password, registered in the S³I IdentityProvider. If the grant_type is set as password, the password is required

        """

        self.__model = model
        self.__thing_id = model.get("thingId", "")
        self.__policy_id = model.get("policyId", "")
        self.__grant_type = grant_type
        self.__username = username
        self.__password = password
        self.__client_secret = client_secret

        self.__is_broker = is_broker
        self.__is_broker_rest = is_broker_rest
        self.__is_repo = is_repo
        self.__is_stanford2010 = is_stanford2010
        self.__stanford2010_path = stanford2010_path
        self.__is_stanford2010_sync = is_stanford2010_sync
        self.__stanford2010_sync_freq = stanford2010_sync_freq

        self.__is_db = is_database
        self.__db_file = database_file
        self.__db = None

        self.__access_token = ""
        self.__endpoint = ""

        self.__ws_connected = False
        self.broker = None
        self.ws = None
        # TODO: Change the variable name dir, because it is a builtin
        # name.
        self.dir = None
        self.repo = None

        # : Dict[<str>, <str>]
        self.repo_json = dict()
        self.dir_json = dict()
        self.dt_json = dict()

        self.__name = ""
        self.__roles = {}
        self.__features = {}
        self.__ditto_features = {}
        # ??? Is this property necessary? Only used as return value in _getValue()
        self.__resGetValue = list()
        self.__source_obj = None
        attributes = model.get("attributes", None)
        if attributes:
            self.__name = attributes.get("name", "")
        self.__stanford2010 = None
        self.__event_manager = None
        self.user_func_list = list()

    @property
    def model(self):
        """Returns the specification JSON from which this thing has been constructed from.

        :returns: Representation of a ml40 compliant thing.
        :rtype: dict

        """

        return self.__model

    @property
    def stanford2010(self):
        return self.__stanford2010

    @stanford2010.setter
    def stanford2010(self, value):
        self.__stanford2010 = value

    @property
    def db(self):
        return self.__db

    @property
    def ditto_features(self):
        return self.__ditto_features

    @ditto_features.setter
    def ditto_features(self, value):
        self.__ditto_features = value

    @property
    def features(self):
        """Returns thing's features.

        :returns: Features
        :rtype: dict

        """

        return self.__features

    @features.setter
    def features(self, value):
        """Replaces thing's features with value.

        :param value: New collection of features

        """

        self.__features = value

    @property
    def roles(self):
        """Returns the thing's roles.

        :returns: ml40 roles
        :rtype: dict

        """

        return self.__roles

    @roles.setter
    def roles(self, value):
        """Replaces thing's roles with value

        :param value: New collection of roles
        """

        self.__roles = value

    @property
    def client_secret(self):
        """Returns the client secret.

        :returns: Client secret
        :rtype: str

        """

        return self.__client_secret

    @property
    def grant_type(self):
        """Returns the method used to obtain JSON Web Tokens from the S³I IdentityProvider

        :returns: OAuth2 specified grant type [password, client_credentials]
        :rtype: str

        """

        return self.__grant_type

    @property
    def access_token(self):
        """Returns the current JSON Web token.

        :returns: JSON Web token
        :rtype: str

        """
        return self.__access_token

    @property
    def name(self):
        """Returns the name of this thing.

        :returns: name
        :rtype: str

        """

        return self.__name

    @property
    def thing_id(self):
        """Returns the identifier of this thing.

        :returns: identifier
        :rtype: str

        """

        return self.__thing_id

    @property
    def policy_id(self):
        """Returns the identifier of this thing's policy.

        :returns: identifier
        :rtype: str

        """

        return self.__policy_id

    def run_forever(self):
        """Starts the thing in permanent mode.

        """
        __log = "[S3I]: Launch {}".format(self.name)
        APP_LOGGER.info(__log)
        self.__connect_with_idp()
        self.__dir_syn()
        threading.Thread(target=self.__json_syn).start()
        if self.__is_repo:
            threading.Thread(target=self.__repo_syn).start()
        if self.__is_stanford2010:
            threading.Thread(target=self.__stanford2010_syn,
                             args=(self.__stanford2010_path, self.__is_stanford2010_sync,
                                   self.__stanford2010_sync_freq)).start()
        if self.__is_db:
            self.__config_database()

        self.__event_manager = EventManager(
            event_filter_type=EventFilterType.RQL_FILTER,
            ml40_model=self.model
        )
        threading.Thread(target=self.__event_manager.emit_event,
                         args=(self.broker, self.thing_id)).start()

        for func in self.user_func_list:
            threading.Thread(target=func).start()

    def add_user_def(self, func):
        """Insert user-specified function in the thing object.

        :param func: external defined function.

        """
        self.user_func_list.append(func)

    def __json_syn(self, freq=0.1):
        """
        Applies local changes to the original model in the thing object

        :param freq: Frequency of the update
        :type freq: float
        """
        while True:
            try:
                time.sleep(freq)
                self.to_json()
            except:
                continue

    def __dir_syn(self):
        """Applies local changes to the directory entry in the cloud only once.

        """
        self.to_dir_json()
        if self.dir_json is not None:
            self.dir.updateThingIDBased(
                thingID=self.thing_id, payload=self.dir_json
            )

    def __repo_syn(self, freq=0.1):
        """Applies local changes to the repository entry in the cloud.

        :param freq: Frequency of the update.
        :type freq: float
        """
        while self.__is_repo:
            try:
                time.sleep(freq)
                old_repo_json = self.repo_json
                self.to_repo_json()
                # TODO: Clean up this reqion
                if self.repo_json == old_repo_json:
                    continue
                else:
                    self.repo.updateThingIDBased(
                        thingID=self.thing_id, payload=self.repo_json
                    )
            except:
                continue

    def __stanford2010_syn(self, path, is_period=False, freq=10):
        """
        This function finds the .hpr data according to the entered path and read out the content
        """

        def get_hpr_files(path):
            # get all .hpr files under the specified folder
            files = [f for f in listdir(path) if isfile(join(path, f))]
            hpr_files = []
            for file in files:
                filename, file_extension = splitext(file)
                if file_extension == ".hpr":  # in the folder, there is always one hpr data
                    hpr_files.append(file)
            return hpr_files

        def get_timestamp(hpr):
            time_node = hpr.find_nodes("HarvestedProductionHeader/CreationDate")[0]
            time_str = time_node.text
            return time_str.replace(time_str[time_str.rfind("."):time_str.find("+")], "")

        def get_last_hpr(hpr_files, is_remove=False):
            # get the last generated hpr data
            if len(hpr_files) == 0:
                return None
            hpr = XML(path="{0}/{1}".format(path, hpr_files[0]))
            if is_remove:
                os.remove("{0}/{1}".format(path, hpr_files[0]))
            hpr_files.pop(0)

            for filename in hpr_files:
                hpr_temp = XML(path="{0}/{1}".format(path, filename))
                if is_remove:
                    os.remove("{0}/{1}".format(path, filename))
                hpr_timestamp = get_timestamp(hpr)
                hpr_temp_timestamp = get_timestamp(hpr)
                hpr_isotime = datetime.fromisoformat(hpr_timestamp)
                hpr_temp_isotime = datetime.fromisoformat(hpr_temp_timestamp)
                if hpr_isotime < hpr_temp_isotime:
                    hpr = hpr_temp

            return hpr

        while True:
            _stanford2010 = get_last_hpr(get_hpr_files(path), is_remove=is_period)
            time.sleep(1)
            if _stanford2010 is None:
                APP_LOGGER.warn("StanForD2010 Data not found in the specified folder, wait for the data")
                continue
            else:
                self.__stanford2010 = _stanford2010
                APP_LOGGER.info("Successfully parsed the StanForD2010 Data. File removed from the folder")
                break
        while is_period:
            time.sleep(freq)
            hpr_temp = get_last_hpr(hpr_files=get_hpr_files(path), is_remove=is_period)
            if hpr_temp is None:
                continue
            APP_LOGGER.info("Detect new hpr file.")
            isotime_old = datetime.fromisoformat(get_timestamp(self.__stanford2010))
            isotime_new = datetime.fromisoformat(get_timestamp(hpr_temp))
            if isotime_old == isotime_new:
                APP_LOGGER.info("Parsing StanForD2020 data failed. File removed from the folder")
                continue
            else:
                APP_LOGGER.info("Successfully parsed the StanForD2010 Data. File removed from the folder")
                self.__stanford2010 = hpr_temp

    def __config_database(self):
        self.__db = DataBase(db=self.__db_file)
        self.__db.connect()

    def __connect_with_idp(self):
        """Establishes a connection to the S³I IdentityProvider which guarantees,
        that the JSON web token needed to use s3i services.
        be renewed if it has expired.

        """
        __log = "[S3I][IdP]: Connect with S3I IdentityProvider"
        APP_LOGGER.info(__log)
        idp = IdentityProvider(
            grant_type=self.__grant_type,
            client_id=self.__thing_id,
            username=self.__username,
            password=self.__password,
            client_secret=self.__client_secret,
            realm=BaseVariable.IDP_REALM,
            identity_provider_url=BaseVariable.IDP_URL,
        )

        # This may take a while so fetch token directly.
        idp.run_forever(token_type=TokenType.ACCESS_TOKEN, on_new_token=self.__on_token)

    def __on_token(self, token):
        """Updates the JSON Web Token with token and reestablishes connections
        to the s3i services .

        :param token: New JSON Web token
        :type token: str

        """
        APP_LOGGER.info("get new token")
        self.__access_token = token
        self.__connect_with_dir()
        self.__connect_with_repo()
        if self.__is_broker:
            self.__connect_with_broker()

    def __connect_with_dir(self):
        """Initializes the property dir with a Directory object which can be
        used to access the s3i Directory.

        :returns:
        :rtype:

        """

        __log = "[S3I][Dir]: Connect with S3I Directory"
        APP_LOGGER.info(__log)
        self.dir = Directory(
            s3i_dir_url=BaseVariable.DIR_URL, token=self.__access_token
        )

    def __connect_with_repo(self):
        """Initializes the property repo whit a Repository object which can be
        used to access the s3i Repository.

        :returns:
        :rtype:

        """

        __log = "[S3I][Repo]: Connect with S3I Repository"
        APP_LOGGER.info(__log)
        self.repo = Repository(
            s3i_repo_url=BaseVariable.REPO_URL, token=self.__access_token
        )

    def __connect_with_broker(self):
        """Initializes the property broker with a Broker object. Additionally
        a callback function is registered which handles incoming S³I-B Messages
        messages.

        """

        __log = "[S3I][Broker]: Connect with S3I Broker"
        APP_LOGGER.info(__log)
        if self.__is_broker_rest:
            self.broker = BrokerREST(token=self.access_token)

            def receive():
                self.__endpoint = find_broker_endpoint(self.dir, thing_id=self.thing_id)
                while True:
                    try:
                        time.sleep(0.1)
                        msg = self.broker.receive_once(self.__endpoint)
                        msg_to_json = lambda msg: msg if isinstance(msg, dict) else json.loads(msg)
                        if msg == {}:
                            continue
                        else:
                            self.__on_broker_callback(
                                ch=None,
                                method=None,
                                properties=None,
                                body=msg_to_json(msg),
                            )
                    except:
                        continue

            threading.Thread(target=receive).start()

        else:
            if self.broker is None:
                # first time to build a broker instance
                self.__endpoint = find_broker_endpoint(self.dir, thing_id=self.thing_id)
                self.broker = Broker(
                    auth_form="Username/Password",
                    username=" ",
                    password=self.__access_token,
                    host=BaseVariable.BROKER_HOST,
                )

                threading.Thread(
                    target=self.broker.receive,
                    args=(self.__endpoint, self.__on_broker_callback),
                ).start()

            else:
                self.broker.maybe_reconnect(self.access_token)

    def __on_broker_callback(self, ch, method, properties, body):
        """Parses body (content of a S3I-B message) and delegates the
        processing of the message to a separate method. The method is
        selected according to the message's type.

        :param body: S3I-B message

        """
        if isinstance(body, bytes):
            try:
                body = literal_eval(body.decode('utf-8'))
            except ValueError:
                body = json.loads(body)

        elif isinstance(body, int):
            pass
        elif isinstance(body, str):
            pass

        if ch is not None:
            ch.basic_ack(method.delivery_tag)
        try:
            message_type = body.get("messageType")
            if message_type == "userMessage":
                self.on_user_message(body)
            elif message_type == "serviceRequest":
                self.on_service_request(body)
            elif message_type == "getValueRequest":
                self.on_get_value_request(body)
            elif message_type == "getValueReply":
                self.on_get_value_reply(body)
            elif message_type == "serviceReply":
                self.on_service_reply(body)
            elif message_type == "setValueRequest":
                self.on_set_value_request(body)
            elif message_type == "setValueReply":
                self.on_set_value_reply(body)
            elif message_type == "eventSubscriptionRequest":
                self.on_event_subscription_request(body)
            elif message_type == "eventSubscriptionReply":
                self.on_event_subscription_reply(body)
            elif message_type == "eventUnsubscriptionRequest":
                self.on_event_unsubscription_request(body)
            elif message_type == "eventUnsubscriptionReply":
                self.on_event_unsubscription_reply(body)
            elif message_type == "eventMessage":
                self.on_event_message(body)
            else:
                ### TODO send user message reply back
                pass
        except AttributeError:
            pass

    def __send_message_to_broker(self, receiver_endpoints, msg):
        try:
            res = self.broker.send(
                receiver_endpoints=receiver_endpoints,
                msg=json.dumps(msg)
            )
            __log = "[S3I][Broker]: Send a S3I-B message back to the requester"
            APP_LOGGER.info(__log)
            return res

        except s3i.exception.S3IBrokerAMQPError as e:
            __log = "[S3I]: {}".format(e.error_msg)
            APP_LOGGER.critical(__log)

    def on_user_message(self, msg):
        """Handles incoming S³I-B UserMessages.

        :param msg: S³I-B UserMessages

        """
        __log = "[S3I][Broker]: You have received a S3I-B UserMessage"
        APP_LOGGER.info(__log)

    def on_get_value_request(self, msg):
        """Handles incoming GetValueRequest message. Looks up the value specified in msg and
        sends a GetValueReply message back to the sender.

        :param msg: GetValueRequest

        """
        __log = "[S3I][Broker]: You have received a S3I-B GetValueRequest"
        APP_LOGGER.info(__log)

        get_value_reply = GetValueReply()
        request_sender = msg.get("sender")
        request_msg_id = msg.get("identifier")
        request_sender_endpoint = msg.get("replyToEndpoint")
        attribute_path = msg.get("attributePath")
        reply_msg_uuid = "s3i:" + str(uuid.uuid4())
        try:
            __log = "[S3I]: Search the given attribute path: {}".format(attribute_path)
            APP_LOGGER.info(__log)
            value = self._uriToData(attribute_path)
        except KeyError:
            value = "Invalid attribute path"
            __log = "[S3I]: " + value
            APP_LOGGER.critical(__log)

        get_value_reply.fillGetValueReply(
            senderUUID=self.thing_id,
            receiverUUIDs=[request_sender],
            results=value,
            msgUUID=reply_msg_uuid,
            replyingToUUID=request_msg_id,
        )

        res = self.__send_message_to_broker(
            receiver_endpoints=[request_sender_endpoint],
            msg=get_value_reply.msg
        )

        if self.__is_broker_rest:
            if res.status_code == 201:
                __log = "[S3I][Broker]: Send S3I-B GetValueReply back to the requester"
                APP_LOGGER.info(__log)
            else:
                __log = "[S3I[Broker]: " + res.text
                APP_LOGGER.info(__log)

    def _uriToData(self, uri):
        """Returns a copy of the value found at uri.

        :param uri: Path to value
        :rtype: Feature

        """

        if uri == "":
            return self.dt_json
        else:
            uri_list = uri.split("/")
            if uri_list[0] == "features":
                try:
                    return self.dt_json[uri]
                except KeyError:
                    return "Invalid attribute path"

            try:
                self._getValue(self.dt_json, uri_list)
            except:
                return "Invalid attribute path"
            if self.__resGetValue.__len__() == 0:
                return "Invalid attribute path"
            response = copy.deepcopy(self.__resGetValue)
            self.__resGetValue.clear()
            if response.__len__() == 1:
                return response[0]
            else:
                return response

    def _getValue(self, source, uri_list):
        """Searches for the value specified by uri_list in source and stores
        the result in __resGetValue.

        :param source: Object that is scanned
        :param uri_list: List containing path

        """

        # ??? What if the uri points to a Value object?
        # Shouldn't it be serialized?!
        value = source[uri_list[0]]
        if uri_list.__len__() == 1:
            # if is ditto-feature
            if isinstance(value, str):
                try:
                    stringValue_split = value.split(":")
                    if stringValue_split[0] == "ditto-feature":
                        value = self.dt_json["features"][stringValue_split[1]][
                            "properties"
                        ][uri_list[0]]
                except:
                    pass
            self.__resGetValue.append(value)
            return
        if isinstance(value, dict):
            # ??? uri_list.pop(0) better?!
            del uri_list[0]
            self._getValue(value, uri_list)
        if isinstance(value, list):
            if isinstance(value[0], (str, int, float, bool, list)):
                return value
            if isinstance(value[0], dict):
                for item in value:
                    if item["class"] == "ml40::Thing":
                        for i in item["roles"]:
                            if self._findValue(i, uri_list[1]):
                                uri_list_1 = copy.deepcopy(uri_list)
                                del uri_list_1[:2]
                                self._getValue(item, uri_list_1)
                        _f = self._findValue({"identifier": item.get("identifier")}, uri_list[1]) or \
                             self._findValue({"name": item.get("name")}, uri_list[1])
                        if _f:
                            uri_list_1 = copy.deepcopy(uri_list)
                            del uri_list_1[:2]
                            self._getValue(item, uri_list_1)
                    else:
                        if self._findValue(item, uri_list[1]):
                            uri_list_1 = copy.deepcopy(uri_list)
                            del uri_list_1[:2]
                            if not uri_list_1:
                                self.__resGetValue.append(item)
                                return
                            else:
                                self._getValue(item, uri_list_1)
        if isinstance(value, (str, int, float, bool)):
            # if is ditto-feature
            if isinstance(value, str):
                try:
                    stringValue_split = value.split(":")
                    if stringValue_split[0] == "ditto-feature":
                        value = self.dt_json["features"][stringValue_split[1]][
                            "properties"
                        ][uri_list[0]]
                except:
                    pass
            self.__resGetValue.append(value)

    def _findValue(self, json, value):
        """Returns true if value has been found in json, otherwise returns false.

        :param json: dictionary
        :param value:
        :returns:
        :rtype:

        """

        # TODO: Simplify: value in json.values()
        for item in json:
            if json[item] == value:
                # print("Parameter: ", json[item])
                return True
        return False

    def on_service_request(self, body_json):
        """Handles S³I-B ServiceRequests. Executes the method of the
        functionality specified in serviceType and send a ServiceReply
        back to the sender.

        :param body_json: ServiceRequest

        """
        __log = "[S3I][Broker]: You have received a S3I-B ServiceRequest"
        service_type = body_json.get("serviceType")
        parameters = body_json.get("parameters")
        service_reply = ServiceReply()
        service_functionality = service_type.split('/')[0]
        service_functionality_obj = self.features.get(service_functionality)
        if service_functionality_obj is None:
            APP_LOGGER.critical(
                "[S3I]: Functionality %s is not one of the built-in functionalities in %s!"
                % (service_functionality, self.name)
            )
            service_reply.fillServiceReply(
                senderUUID=self.thing_id,
                receiverUUIDs=[body_json.get("sender", None)],
                serviceType=body_json.get("serviceType", None),
                results={"error": "invalid functionalities (serviceType) {}".format(service_functionality)},
                replyingToUUID=body_json.get("identifier", None),
                msgUUID="s3i:{}".format(uuid.uuid4())
            )
        else:
            # TODO: Call right functionality.
            try:
                method = getattr(service_functionality_obj, service_type.split('/')[1])
            except AttributeError:
                APP_LOGGER.critical(
                    "[S3I]: Method %s is not one of the built-in functionalities in %s!" % (
                        service_type.split('/')[1], self.name)
                )
                service_reply.fillServiceReply(
                    senderUUID=self.thing_id,
                    receiverUUIDs=[body_json.get("sender", None)],
                    serviceType=body_json.get("serviceType", None),
                    results={"error": "invalid method {}".format(service_type.split('/')[1])},
                    replyingToUUID=body_json.get("identifier", None),
                    msgUUID="s3i:{}".format(uuid.uuid4())
                )
            except IndexError:
                APP_LOGGER.critical(
                    "[S3I]: ServiceType consists of functionality and method name."
                )
                service_reply.fillServiceReply(
                    senderUUID=self.thing_id,
                    receiverUUIDs=[body_json.get("sender", None)],
                    serviceType=body_json.get("serviceType", None),
                    results={"error": "method missing"},
                    replyingToUUID=body_json.get("identifier", None),
                    msgUUID="s3i:{}".format(uuid.uuid4())
                )
            else:
                __log = "[S3I][Broker]: Execute the function {0} of the class {1}".format(service_type.split('/')[1],
                                                                                          service_type.split('/')[0])
                APP_LOGGER.info(__log)
                try:
                    result = method(**parameters)
                except TypeError:
                    APP_LOGGER.critical("[S3I]: Invalid function arguments")
                    service_reply.fillServiceReply(
                        senderUUID=self.thing_id,
                        receiverUUIDs=[body_json.get("sender", None)],
                        serviceType=body_json.get("serviceType", None),
                        results={"error": "invalid function arguments (parameters)"},
                        replyingToUUID=body_json.get("identifier", None),
                        msgUUID="s3i:{}".format(uuid.uuid4())
                    )
                else:
                    if isinstance(result, bool):
                        result = {"ok": result}
                    elif result is None:
                        result = "None"
                    service_reply.fillServiceReply(
                        senderUUID=self.thing_id,
                        receiverUUIDs=[body_json.get("sender", None)],
                        serviceType=body_json.get("serviceType", None),
                        results=result,
                        replyingToUUID=body_json.get("identifier", None),
                        msgUUID="s3i:{}".format(uuid.uuid4())
                    )

        res = self.__send_message_to_broker(
            receiver_endpoints=[body_json.get("replyToEndpoint", None)],
            msg=service_reply.msg
        )

        if self.__is_broker_rest:
            if res.status_code == 201:
                __log = "[S3I][Broker]: Send a S3I-B ServiceReply back to the requester"
                APP_LOGGER.info(__log)
            else:
                APP_LOGGER.critical(__log)

    def on_set_value_request(self, msg):
        """Handles incoming S³I-B SetValueRequest. Prints the content of msg to stdout.

        :param msg: GetValueReply

        """
        __log = "[S3I][Broker]: You have received a S3I-B SetValueRequest"
        APP_LOGGER.info(__log)

        set_value_reply = SetValueReply()
        request_sender = msg.get("sender")
        request_msg_id = msg.get("identifier")
        request_sender_endpoint = msg.get("replyToEndpoint")
        attribute_path = msg.get("attributePath")
        new_value = msg.get("newValue")
        reply_msg_uuid = "s3i:" + str(uuid.uuid4())

        try:
            __log = "[S3I]: Search for the given attribute path: {}".format(attribute_path)
            APP_LOGGER.info(__log)
            old_value = self._uriToData(attribute_path)
            ins = self._uriToIns(attribute_path)
            APP_LOGGER.info("[S3I]: Change value from {} to {}".format(old_value, new_value))
            result = self._set_value_req(ins, new_value, attribute_path)

        except:
            __log = "[S3I]: Invalid attribute path"
            APP_LOGGER.critical(__log)
            result = False

        set_value_reply.fillSetValueReply(
            senderUUID=self.thing_id,
            receiverUUIDs=[request_sender],
            ok=result,
            replyingToUUID=request_msg_id,
            msgUUID=reply_msg_uuid
        )
        res = self.__send_message_to_broker(
            receiver_endpoints=[request_sender_endpoint],
            msg=set_value_reply.msg
        )

        if self.__is_broker_rest:
            if res.status_code == 201:
                __log = "[S3I][Broker]: Send S3I-B GetValueReply back to the requester"
                APP_LOGGER.info(__log)
            else:
                __log = "[S3I[Broker]: " + res.text
                APP_LOGGER.info(__log)

    def _set_value_req(self, ins, new_value, attribute_path):
        if not isinstance(new_value, dict):
            attr_list = attribute_path.split("/")
            if attr_list.__len__() <= 2:
                APP_LOGGER.info("Not allowed to set attribute {}".format(attribute_path))
                return False
            else:
                if hasattr(ins, attr_list[attr_list.__len__() - 1]):
                    setattr(ins, attr_list[attr_list.__len__() - 1], new_value)
                    return True
                APP_LOGGER.info("{} is not one of the attributes".format(attr_list[attr_list.__len__() - 1]))
                return False
        else:
            for key in new_value.keys():
                if hasattr(ins, key):
                    setattr(ins, key, new_value[key])
                else:
                    APP_LOGGER.info("{} is not one of the attributes".format(key))
                    return False
            return True

    def _uriToIns(self, uri):
        if not uri:
            return None
        uri_list = uri.split("/")
        uri_list.pop(0)  # delete first element "attributes"
        return self._getInstance(self, uri_list)

    def _getInstance(self, source_obj, uri_list):
        if uri_list.__len__() == 0 or uri_list.__len__() == 1:
            ### the original uri was "attributes/features"
            return source_obj

        if "ml40" in uri_list[0]:
            _uri = uri_list[0]
            uri_list.pop(0)
            return self._getInstance(source_obj.features[_uri], uri_list)

        elif uri_list[0] == "features":
            uri_list.pop(0)
            return self._getInstance(source_obj, uri_list)

        elif uri_list[0] == "targets":
            uri_list.pop(0)
            for key in source_obj.targets.keys():
                subthing_dict = source_obj.targets[key].to_subthing_json()
                if subthing_dict.get("name", "") == uri_list[0] or subthing_dict.get("identifier", "") == uri_list[0] \
                        or subthing_dict.get("class", "") == uri_list[0]:
                    uri_list.pop(0)
                    return self._getInstance(source_obj.targets[key], uri_list)

        elif uri_list[0] == "subFeatures":
            uri_list.pop(0)
            for key in source_obj.subFeatures.keys():
                subfeature_dict = source_obj.subFeatures[key].to_json()
                if subfeature_dict.get("name", "") == uri_list[0] or subfeature_dict.get("identifier", "") == uri_list[
                    0] \
                        or subfeature_dict.get("class", "") == uri_list[0]:
                    uri_list.pop(0)
                    return self._getInstance(source_obj.subFeatures[key], uri_list)

    def on_event_subscription_request(self, msg):
        __log = "[S3I][Broker]: You have received a S3I-B EventSubscriptionRequest"
        APP_LOGGER.info(__log)
        rql_expression = msg.get("RQL")
        subscription_status, sub_id = self.__event_manager.add_event(
            filter_expression=rql_expression, subscriber=msg.get("sender"),
            subscriber_endpoint=msg.get("replyToEndpoint")
        )
        __log = "[S3I][Broker]: Validation of RQL syntax: {}".format(subscription_status)
        APP_LOGGER.info((__log))
        event_sub_reply = EventSubscriptionReply()
        event_sub_reply.fillEventSubscriptionReply(
            sender=self.thing_id,
            receivers=[msg.get("sender")],
            subscription_id=sub_id,
            replying_to_message=msg.get("identifier"),
            msg_id = "s3i:" + str(uuid.uuid4()),
            status=subscription_status
        )
        res = self.__send_message_to_broker(
            receiver_endpoints=[msg.get("replyToEndpoint")],
            msg=event_sub_reply.msg
        )

        if self.__is_broker_rest:
            if res.status_code == 201:
                __log = "[S3I][Broker]: Send S3I-B EventSubscriptionReply back to the requester"
                APP_LOGGER.info(__log)
            else:
                __log = "[S3I[Broker]: " + res.text
                APP_LOGGER.info(__log)

    def on_event_unsubscription_request(self, msg):
        __log = "[S3I][Broker]: You have received a S3I-B EventUnsubscriptionRequest"
        APP_LOGGER.info(__log)
        sub_id = msg.get("subscription-id")
        unsubscription_status = self.__event_manager.delete_event(sub_id)
        __log = "[S3I][Broker]: Status of unsubscription event: {}".format(unsubscription_status)
        APP_LOGGER.info(__log)
        event_ubsub_reply = EventUnsubscriptionReply()
        event_ubsub_reply.fillEventUnsubscriptionReply(
            sender=self.thing_id,
            receivers=[msg.get("sender")],
            msg_id = "s3i:" + str(uuid.uuid4()),
            replying_to_message=msg.get("identifier"),
            sub_id=sub_id,
            status=unsubscription_status
        )
        res = self.__send_message_to_broker(
            receiver_endpoints=[msg.get("replyToEndpoint")],
            msg=event_ubsub_reply.msg
        )

        if self.__is_broker_rest:
            if res.status_code == 201:
                __log = "[S3I][Broker]: Send S3I-B EventSubscriptionReply back to the requester"
                APP_LOGGER.info(__log)
            else:
                __log = "[S3I[Broker]: " + res.text
                APP_LOGGER.info(__log)

    def on_event_message(self, msg):
        __log = "[S3I][Broker]: You have received a S3I-B EventMessage"
        APP_LOGGER.info(__log)
        content = msg.get("content")
        sub_id = msg.get("subscription-id")
        time =  msg.get("time")
        __log = "[S3I][Broker]: The event (sub-id: {0} has been trigged at the time {1}, content: {2})".format(
            sub_id, time, content)
        APP_LOGGER.info(__log)

    def on_get_value_reply(self, msg):
        """Handles incoming S³I-B GetValueReply. Prints the content of msg to stdout.

        :param msg: GetValueReply

        """

        # ???: Behavior should be defined by the user! Maybe he want
        # to process the result!
        __log = "[S3I][Broker]: You have received a S3I-B GetValueReply"
        APP_LOGGER.info(__log)
        value = msg.get("value", None)
        if isinstance(value, (dict, list)):
            value = json.dumps(value, indent=2)
        __log = "[S3I][Broker]: The queried value is: {0}".format(value)
        APP_LOGGER.info(__log)

    def on_service_reply(self, msg):
        """Handles incoming S³I-B ServiceReply. Prints the content of msg to stdout.

        :param msg: ServiceReply

        """
        __log = "[S3I][Broker]: You have received a S3I-B ServiceReply"
        APP_LOGGER.info(__log)
        results = msg.get("results", None)
        if isinstance(results, dict):
            results = json.dumps(results, indent=2)

        __log = "[S3I][Broker]: The result is: {0}".format(results)
        APP_LOGGER.info(__log)

    def on_set_value_reply(self, msg):
        """Handles incoming S³I-B SetValueReply. Prints the content of msg to stdout.

        :param msg: GetValueReply

        """
        __log = "[S3I][Broker]: You have received a S3I-B SetValueReply"
        APP_LOGGER.info(__log)
        result = msg.get("ok", None)
        __log = "[S3I][Broker]: The status of value setting: {0}".format(result)
        APP_LOGGER.info(__log)

    def on_event_subscription_reply(self, msg):
        """
        Handles incoming S3I-B EventSubscriptionReply. Prints the content of msg to stdout
        :param msg: EventSubscriptionReply
        :type msg: dict
        """

        __log = "[S3I][Broker]: You have received a S3I-B EventSubscriptionReply"
        APP_LOGGER.info(__log)
        result = msg.get("ok", None)
        sub_id = msg.get("subscription-id")
        __log = "[S3I][Broker]: The status of event subscription (subcription-id: {0}) is {1}".format(sub_id, result)
        APP_LOGGER.info(__log)

    def on_event_unsubscription_reply(self, msg):
        """
        Handles incoming S3I-B EventUnsubscriptionReply. Prints the content of msg to stdout
        :param msg: EventUnsubscriptionReply
        :type msg: dict
        """
        __log = "[S3I][Broker]: You habe received a S3I-B EventUnsubscriptionReply"
        APP_LOGGER.info(__log)
        result = msg.get("ok", None)
        sub_id = msg.get("subscription-id")
        __log = "[S3I][Broker]: The status of event unsubscription (subscription-id: {0}): {1}".format(sub_id, result)
        APP_LOGGER.info(__log)

    def to_dir_json(self):
        """Returns a dictionary representing this thing's directory entry.

        :returns: Directory representation of this object
        :rtype: dict

        """

        self.dir_json = self.dir.queryThingIDBased(self.thing_id)
        if self.thing_id is not None:
            self.dir_json["thingId"] = self.thing_id
        if self.policy_id is not None:
            self.dir_json["policyId"] = self.policy_id
        if self.name is not None:
            self.dir_json["attributes"]["name"] = self.name
        if self.features.get("ml40::Location") is not None:
            self.dir_json["attributes"]["location"] = {
                "longitude": self.features.get("ml40::Location").to_json()["longitude"],
                "latitude": self.features.get("ml40::Location").to_json()["latitude"]
            }
        self.dir_json["attributes"]["dataModel"] = "fml40"
        self.dir_json["attributes"]["thingStructure"] = {
            "class": "ml40::Thing",
            "links": []
        }
        for key in self.roles.keys():
            role_entry = {
                "association": "roles",
                "target": self.roles[key].to_json()
            }
            self.dir_json["attributes"]["thingStructure"]["links"].append(role_entry)

        for key in self.features.keys():
            feature_target = {
                "class": self.features[key].to_json()["class"],
            }
            if self.features[key].to_json().get("identifier") is not None:
                feature_target["identifier"] = self.features[key].to_json()["identifier"]

            feature_entry = {"association": "features", "target": feature_target}
            # if the feature has targets, like ml40::Composite
            if hasattr(self.features[key], "targets"):
                feature_entry["target"]["links"] = list()
                for target in self.features[key].targets.keys():
                    target_json = (
                        self.features[key].targets[target].to_subthing_dir_json()
                    )
                    feature_entry["target"]["links"].append(target_json)
            self.dir_json["attributes"]["thingStructure"]["links"].append(feature_entry)
        return self.dir_json

    def to_repo_json(self):
        """Returns a dictionary representing this thing's repository entry.

        :returns: Repository representation of this object
        :rtype: dict

        """

        self.repo_json = self.dt_json
        return self.repo_json

    def to_json(self):
        """Returns a dictionary representing this thing in it's current state.

        :returns: Representation of this object
        :rtype: dict

        """

        self.dt_json = {
            "thingId": self.thing_id,
            "policyId": self.policy_id,
            "attributes": {
                "class": "ml40::Thing",
                "name": self.name,
            },
        }
        if self.roles:
            self.dt_json["attributes"]["roles"] = list()
        if self.features:
            self.dt_json["attributes"]["features"] = list()
        if self.ditto_features:
            self.dt_json["features"] = dict()
        for key in self.roles.keys():
            self.dt_json["attributes"]["roles"].append(self.roles[key].to_json())
        for key in self.features.keys():
            self.dt_json["attributes"]["features"].append(self.features[key].to_json())
        for key in self.ditto_features.keys():
            self.dt_json["features"][key] = self.ditto_features[key].to_json()
        self.__event_manager.subject_updated(cur_ml40=self.dt_json)
        return self.dt_json

    def to_subthing_json(self):
        """Returns a dictionary representing this thing in it's current state
        as a subordinate thing. This representation should be used for
        subordinate things in s3i repository entries.

        :returns: Representation of this object as a subordinate thing
        :rtype: dict

        """

        json_out = {
            "class": "ml40::Thing",
            "name": self.name,
            "roles": [],
            "features": [],
        }
        if self.thing_id:
            json_out["identifier"] = self.thing_id
        else:
            if self.model["attributes"].get("identifier") is not None:
                json_out["identifier"] = self.model["attributes"]["identifier"]
        for key in self.roles.keys():
            json_out["roles"].append(self.roles[key].to_json())
        for key in self.features.keys():
            json_out["features"].append(self.features[key].to_json())
        return json_out

    def to_subthing_dir_json(self):
        """Returns a dictionary representing this thing in it's current state
        as a subordinate thing. This representation should be used for
        subordinate things in s3i directory entries.

        :returns: Representation of this object as a subordinate thing.
        :rtype: dict

        """

        json_out = {"class": "ml40::Thing", "links": []}
        if self.thing_id:
            json_out["identifier"] = self.thing_id
        for key in self.roles.keys():
            role_entry = {"association": "roles", "target": self.roles[key].to_json()}
            json_out["links"].append(role_entry)
        for key in self.features.keys():
            feature_target = {
                "class": self.features[key].to_json()["class"],
            }
            if self.features[key].to_json().get("identifier") is not None:
                feature_target["identifier"] = self.features[key].to_json()["identifier"]
            feature_entry = {"association": "features", "target": feature_target}
            json_out["links"].append(feature_entry)
        return json_out
