# coding: utf-8
#
# Copyright 2017 The Oppia Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Models for storing the audit logs."""

from __future__ import annotations

from core import feconf
from core.platform import models

from typing import Dict

MYPY = False
if MYPY: # pragma: no cover
    from mypy_imports import base_models
    from mypy_imports import datastore_services

(base_models,) = models.Registry.import_models([models.Names.BASE_MODEL])
datastore_services = models.Registry.import_datastore_services()


class RoleQueryAuditModel(base_models.BaseModel):
    """Records the data for query made to the role structure using admin
    interface.

    Instances of this class are keyed by a custom Id.
    [user_id].[timestamp_in_sec].[intent].[random_number]
    """

    # The user_id of the user making query.
    user_id = datastore_services.StringProperty(required=True, indexed=True)
    # The intent of making query (viewing (by role or username)
    # or updating role).
    intent = datastore_services.StringProperty(required=True, choices=[
        feconf.ROLE_ACTION_ADD,
        feconf.ROLE_ACTION_REMOVE,
        feconf.ROLE_ACTION_VIEW_BY_ROLE,
        feconf.ROLE_ACTION_VIEW_BY_USERNAME
    ], indexed=True)
    # The role being queried for.
    role = datastore_services.StringProperty(default=None, indexed=True)
    # The username in the query.
    username = datastore_services.StringProperty(default=None, indexed=True)

    @staticmethod
    def get_deletion_policy() -> base_models.DELETION_POLICY:
        """Model contains data corresponding to a user: user_id and username
        fields, but it isn't deleted because it is needed for auditing purposes.
        """
        return base_models.DELETION_POLICY.KEEP

    @staticmethod
    def get_model_association_to_user(
    ) -> base_models.MODEL_ASSOCIATION_TO_USER:
        """Model contains data corresponding to a user: user_id and username
        fields, but it isn't exported because it is only used for auditing
        purposes.
        """
        return base_models.MODEL_ASSOCIATION_TO_USER.NOT_CORRESPONDING_TO_USER

    @classmethod
    def get_export_policy(cls) -> Dict[str, base_models.EXPORT_POLICY]:
        """Model contains data corresponding to a user: user_id and username
        fields, but it isn't exported because it is only used for auditing
        purposes.
        """
        return dict(super(cls, cls).get_export_policy(), **{
            'user_id': base_models.EXPORT_POLICY.NOT_APPLICABLE,
            'intent': base_models.EXPORT_POLICY.NOT_APPLICABLE,
            'role': base_models.EXPORT_POLICY.NOT_APPLICABLE,
            'username': base_models.EXPORT_POLICY.NOT_APPLICABLE
        })

    @classmethod
    def has_reference_to_user_id(cls, user_id: str) -> bool:
        """Check whether RoleQueryAuditModel exists for the given user.

        Args:
            user_id: str. The ID of the user whose data should be checked.

        Returns:
            bool. Whether any models refer to the given user ID.
        """
        return cls.query(cls.user_id == user_id).get(keys_only=True) is not None



class UsernameChangeAuditModel(base_models.BaseModel):
    """Records the changes made to usernames via the admin panel."""

    committer_id = (
        datastore_services.StringProperty(required=True, indexed=True))
    old_username = (
        datastore_services.StringProperty(required=True, indexed=True))
    new_username = (
        datastore_services.StringProperty(required=True, indexed=True))

    @staticmethod
    def get_deletion_policy() -> base_models.DELETION_POLICY:
        """Model contains data corresponding to a user: committer_id."""
        return base_models.DELETION_POLICY.NOT_APPLICABLE

    @classmethod
    def has_reference_to_user_id(cls, user_id: str) -> bool:
        """Check if any instance references the given user ID."""
        return cls.query(cls.committer_id == user_id).get(keys_only=True) is not None
from core.domain import base_domain

class UsernameChangeAudit(base_domain.BaseDomainObject):
    """Domain object for username change audit records."""

    def __init__(self, committer_id: str, old_username: str, new_username: str):
        self.committer_id = committer_id
        self.old_username = old_username
        self.new_username = new_username

    def validate(self):
        """Validates properties of UsernameChangeAudit."""
        if not isinstance(self.committer_id, str):
            raise ValueError("committer_id must be a string.")
        if not isinstance(self.old_username, str) or not self.old_username:
            raise ValueError("old_username must be a non-empty string.")
        if not isinstance(self.new_username, str) or not self.new_username:
            raise ValueError("new_username must be a non-empty string.")


class DeletedUser(base_domain.BaseDomainObject):
    """Domain object for deleted users."""

    def __init__(self, user_id: str):
        self.user_id = user_id

    def validate(self):
        """Validates properties of DeletedUser."""
        if not isinstance(self.user_id, str):
            raise ValueError("user_id should be a string.")


class UserEmailPreferences(base_domain.BaseDomainObject):
    """Domain object for user email preferences."""

    def __init__(self, user_id: str, email: str, preferences: dict):
        self.user_id = user_id
        self.email = email
        self.preferences = preferences

    def validate(self):
        """Validates properties of UserEmailPreferences."""
        if not isinstance(self.user_id, str):
            raise ValueError("user_id should be a string.")
        if "@" not in self.email:
            raise ValueError("Invalid email format.")
        if not isinstance(self.preferences, dict):
            raise ValueError("preferences should be a dictionary.")
