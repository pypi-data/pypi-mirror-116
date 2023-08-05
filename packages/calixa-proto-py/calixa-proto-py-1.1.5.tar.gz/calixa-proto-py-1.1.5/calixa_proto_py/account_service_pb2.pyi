# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from account_pb2 import (
    Account as account_pb2___Account,
    AccountUser as account_pb2___AccountUser,
    AccountUserAssociation as account_pb2___AccountUserAssociation,
    AccountUserRole as account_pb2___AccountUserRole,
)

from common_pb2 import (
    ExternalId as common_pb2___ExternalId,
    RequestContext as common_pb2___RequestContext,
)

from entity_pb2 import (
    Entity as entity_pb2___Entity,
)

from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
    FileDescriptor as google___protobuf___descriptor___FileDescriptor,
)

from google.protobuf.field_mask_pb2 import (
    FieldMask as google___protobuf___field_mask_pb2___FieldMask,
)

from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer as google___protobuf___internal___containers___RepeatedCompositeFieldContainer,
    RepeatedScalarFieldContainer as google___protobuf___internal___containers___RepeatedScalarFieldContainer,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from typing import (
    Iterable as typing___Iterable,
    Optional as typing___Optional,
    Text as typing___Text,
)

from typing_extensions import (
    Literal as typing_extensions___Literal,
)


builtin___bool = bool
builtin___bytes = bytes
builtin___float = float
builtin___int = int


DESCRIPTOR: google___protobuf___descriptor___FileDescriptor = ...

class CreateAccountRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def account(self) -> account_pb2___Account: ...

    @property
    def request_context(self) -> common_pb2___RequestContext: ...

    def __init__(self,
        *,
        account : typing___Optional[account_pb2___Account] = None,
        request_context : typing___Optional[common_pb2___RequestContext] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"account",b"account",u"request_context",b"request_context"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"account",b"account",u"request_context",b"request_context"]) -> None: ...
type___CreateAccountRequest = CreateAccountRequest

class CreateAccountUserRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def accountUser(self) -> account_pb2___AccountUser: ...

    @property
    def request_context(self) -> common_pb2___RequestContext: ...

    def __init__(self,
        *,
        accountUser : typing___Optional[account_pb2___AccountUser] = None,
        request_context : typing___Optional[common_pb2___RequestContext] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"accountUser",b"accountUser",u"request_context",b"request_context"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"accountUser",b"accountUser",u"request_context",b"request_context"]) -> None: ...
type___CreateAccountUserRequest = CreateAccountUserRequest

class CreateAccountUserRoleRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def accountUserRole(self) -> account_pb2___AccountUserRole: ...

    @property
    def request_context(self) -> common_pb2___RequestContext: ...

    def __init__(self,
        *,
        accountUserRole : typing___Optional[account_pb2___AccountUserRole] = None,
        request_context : typing___Optional[common_pb2___RequestContext] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"accountUserRole",b"accountUserRole",u"request_context",b"request_context"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"accountUserRole",b"accountUserRole",u"request_context",b"request_context"]) -> None: ...
type___CreateAccountUserRoleRequest = CreateAccountUserRoleRequest

class GetAccountUserRoleRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    organization_id: typing___Text = ...
    role_id: typing___Text = ...
    name: typing___Text = ...

    def __init__(self,
        *,
        organization_id : typing___Optional[typing___Text] = None,
        role_id : typing___Optional[typing___Text] = None,
        name : typing___Optional[typing___Text] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"keys",b"keys",u"name",b"name",u"role_id",b"role_id"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"keys",b"keys",u"name",b"name",u"organization_id",b"organization_id",u"role_id",b"role_id"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions___Literal[u"keys",b"keys"]) -> typing_extensions___Literal["role_id","name"]: ...
type___GetAccountUserRoleRequest = GetAccountUserRoleRequest

class GetAccountUsersRoleRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    organization_id: typing___Text = ...

    def __init__(self,
        *,
        organization_id : typing___Optional[typing___Text] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"organization_id",b"organization_id"]) -> None: ...
type___GetAccountUsersRoleRequest = GetAccountUsersRoleRequest

class UpdateAccountUserRoleRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def role(self) -> account_pb2___AccountUserRole: ...

    @property
    def update_mask(self) -> google___protobuf___field_mask_pb2___FieldMask: ...

    @property
    def request_context(self) -> common_pb2___RequestContext: ...

    def __init__(self,
        *,
        role : typing___Optional[account_pb2___AccountUserRole] = None,
        update_mask : typing___Optional[google___protobuf___field_mask_pb2___FieldMask] = None,
        request_context : typing___Optional[common_pb2___RequestContext] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"request_context",b"request_context",u"role",b"role",u"update_mask",b"update_mask"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"request_context",b"request_context",u"role",b"role",u"update_mask",b"update_mask"]) -> None: ...
type___UpdateAccountUserRoleRequest = UpdateAccountUserRoleRequest

class RemoveAccountUserAssociationRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    organization_id: typing___Text = ...
    account_id: typing___Text = ...
    canonical_account_id: typing___Text = ...
    account_user_ids: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text] = ...
    canonical_account_user_ids: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text] = ...

    @property
    def request_context(self) -> common_pb2___RequestContext: ...

    def __init__(self,
        *,
        organization_id : typing___Optional[typing___Text] = None,
        account_id : typing___Optional[typing___Text] = None,
        canonical_account_id : typing___Optional[typing___Text] = None,
        account_user_ids : typing___Optional[typing___Iterable[typing___Text]] = None,
        canonical_account_user_ids : typing___Optional[typing___Iterable[typing___Text]] = None,
        request_context : typing___Optional[common_pb2___RequestContext] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"account",b"account",u"account_id",b"account_id",u"canonical_account_id",b"canonical_account_id",u"request_context",b"request_context"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"account",b"account",u"account_id",b"account_id",u"account_user_ids",b"account_user_ids",u"canonical_account_id",b"canonical_account_id",u"canonical_account_user_ids",b"canonical_account_user_ids",u"organization_id",b"organization_id",u"request_context",b"request_context"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions___Literal[u"account",b"account"]) -> typing_extensions___Literal["account_id","canonical_account_id"]: ...
type___RemoveAccountUserAssociationRequest = RemoveAccountUserAssociationRequest

class UpdateAccountUserAssociationRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    organization_id: typing___Text = ...
    account_id: typing___Text = ...
    canonical_account_id: typing___Text = ...

    @property
    def associations(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[account_pb2___AccountUserAssociation]: ...

    @property
    def request_context(self) -> common_pb2___RequestContext: ...

    def __init__(self,
        *,
        organization_id : typing___Optional[typing___Text] = None,
        account_id : typing___Optional[typing___Text] = None,
        canonical_account_id : typing___Optional[typing___Text] = None,
        associations : typing___Optional[typing___Iterable[account_pb2___AccountUserAssociation]] = None,
        request_context : typing___Optional[common_pb2___RequestContext] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"account",b"account",u"account_id",b"account_id",u"canonical_account_id",b"canonical_account_id",u"request_context",b"request_context"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"account",b"account",u"account_id",b"account_id",u"associations",b"associations",u"canonical_account_id",b"canonical_account_id",u"organization_id",b"organization_id",u"request_context",b"request_context"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions___Literal[u"account",b"account"]) -> typing_extensions___Literal["account_id","canonical_account_id"]: ...
type___UpdateAccountUserAssociationRequest = UpdateAccountUserAssociationRequest

class UpdateAccountRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def account(self) -> account_pb2___Account: ...

    @property
    def update_mask(self) -> google___protobuf___field_mask_pb2___FieldMask: ...

    @property
    def request_context(self) -> common_pb2___RequestContext: ...

    def __init__(self,
        *,
        account : typing___Optional[account_pb2___Account] = None,
        update_mask : typing___Optional[google___protobuf___field_mask_pb2___FieldMask] = None,
        request_context : typing___Optional[common_pb2___RequestContext] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"account",b"account",u"request_context",b"request_context",u"update_mask",b"update_mask"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"account",b"account",u"request_context",b"request_context",u"update_mask",b"update_mask"]) -> None: ...
type___UpdateAccountRequest = UpdateAccountRequest

class UpdateAccountUserRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def accountUser(self) -> account_pb2___AccountUser: ...

    @property
    def update_mask(self) -> google___protobuf___field_mask_pb2___FieldMask: ...

    @property
    def request_context(self) -> common_pb2___RequestContext: ...

    def __init__(self,
        *,
        accountUser : typing___Optional[account_pb2___AccountUser] = None,
        update_mask : typing___Optional[google___protobuf___field_mask_pb2___FieldMask] = None,
        request_context : typing___Optional[common_pb2___RequestContext] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"accountUser",b"accountUser",u"request_context",b"request_context",u"update_mask",b"update_mask"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"accountUser",b"accountUser",u"request_context",b"request_context",u"update_mask",b"update_mask"]) -> None: ...
type___UpdateAccountUserRequest = UpdateAccountUserRequest

class SaveOpportunityEntityRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def request_context(self) -> common_pb2___RequestContext: ...

    @property
    def opportunity_entity(self) -> entity_pb2___Entity: ...

    def __init__(self,
        *,
        request_context : typing___Optional[common_pb2___RequestContext] = None,
        opportunity_entity : typing___Optional[entity_pb2___Entity] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"opportunity_entity",b"opportunity_entity",u"request_context",b"request_context"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"opportunity_entity",b"opportunity_entity",u"request_context",b"request_context"]) -> None: ...
type___SaveOpportunityEntityRequest = SaveOpportunityEntityRequest

class GetOpportunityEntitiesRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    organization_id: typing___Text = ...
    canonical_opportunity_id: typing___Text = ...

    def __init__(self,
        *,
        organization_id : typing___Optional[typing___Text] = None,
        canonical_opportunity_id : typing___Optional[typing___Text] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"canonical_opportunity_id",b"canonical_opportunity_id",u"organization_id",b"organization_id"]) -> None: ...
type___GetOpportunityEntitiesRequest = GetOpportunityEntitiesRequest

class SaveExternalAccountEntityRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    external_api_account_id: typing___Text = ...

    @property
    def request_context(self) -> common_pb2___RequestContext: ...

    @property
    def external_entity(self) -> entity_pb2___Entity: ...

    @property
    def related_external_entity_ids(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[common_pb2___ExternalId]: ...

    def __init__(self,
        *,
        request_context : typing___Optional[common_pb2___RequestContext] = None,
        external_entity : typing___Optional[entity_pb2___Entity] = None,
        related_external_entity_ids : typing___Optional[typing___Iterable[common_pb2___ExternalId]] = None,
        external_api_account_id : typing___Optional[typing___Text] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"external_entity",b"external_entity",u"request_context",b"request_context"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"external_api_account_id",b"external_api_account_id",u"external_entity",b"external_entity",u"related_external_entity_ids",b"related_external_entity_ids",u"request_context",b"request_context"]) -> None: ...
type___SaveExternalAccountEntityRequest = SaveExternalAccountEntityRequest

class SaveExternalAccountUserEntityRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def request_context(self) -> common_pb2___RequestContext: ...

    @property
    def external_entity(self) -> entity_pb2___Entity: ...

    @property
    def related_external_entity_ids(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[common_pb2___ExternalId]: ...

    def __init__(self,
        *,
        request_context : typing___Optional[common_pb2___RequestContext] = None,
        external_entity : typing___Optional[entity_pb2___Entity] = None,
        related_external_entity_ids : typing___Optional[typing___Iterable[common_pb2___ExternalId]] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"external_entity",b"external_entity",u"request_context",b"request_context"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"external_entity",b"external_entity",u"related_external_entity_ids",b"related_external_entity_ids",u"request_context",b"request_context"]) -> None: ...
type___SaveExternalAccountUserEntityRequest = SaveExternalAccountUserEntityRequest
