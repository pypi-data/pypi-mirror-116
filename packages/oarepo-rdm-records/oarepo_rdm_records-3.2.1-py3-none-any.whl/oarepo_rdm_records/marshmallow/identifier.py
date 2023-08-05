# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""RDM record schemas."""
from marshmallow_utils.fields import SanitizedUnicode
from marshmallow_utils.schemas import IdentifierSchema as IS
from oarepo_taxonomies.marshmallow import TaxonomyField

from oarepo_rdm_records.config import RDM_RECORDS_IDENTIFIERS_SCHEMES
from oarepo_rdm_records.marshmallow.mixins import TitledMixin
from oarepo_rdm_records.marshmallow.resource import ResourceType


class IdentifierSchema(IS):
    """Identifier schema with optional status field."""
    status = SanitizedUnicode()


class RelatedIdentifierSchema(IS):
    """Related identifier schema."""



    def __init__(self, **kwargs):
        """Related identifier schema constructor."""
        super().__init__(allowed_schemes=RDM_RECORDS_IDENTIFIERS_SCHEMES, **kwargs)

    relation_type = TaxonomyField(mixins=[TitledMixin], required=True)
    resource_type = ResourceType()
