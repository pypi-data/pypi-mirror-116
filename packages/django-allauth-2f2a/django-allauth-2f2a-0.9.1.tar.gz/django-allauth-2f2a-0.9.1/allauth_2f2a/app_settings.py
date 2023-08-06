# ******************************************************************************
#
# app_settings.py:  application settings loaded from settings.py
#
# SPDX-License-Identifier: Apache-2.0
#
# django-allauth-2f2a, a 2fa adapter for django-allauth.
#
# ******************************************************************************
#
# Copyright 2016-2021 Víðir Valberg Guðmundsson and Percipient
# Networks, LLC.
# Copyright 2021 Jeremy A Gray <gray@flyquackswim.com>.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you
# may not use this file except in compliance with the License.  You
# may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.  See the License for the specific language governing
# permissions and limitations under the License.
#
# ******************************************************************************
#
"""Application settings loaded from settings.py."""

from allauth.account import app_settings as allauth_settings
from django.conf import settings

TEMPLATE_EXTENSION = getattr(
    settings,
    "ALLAUTH_2F2A_TEMPLATE_EXTENSION",
    allauth_settings.TEMPLATE_EXTENSION,
)

ALWAYS_REVEAL_BACKUP_TOKENS = bool(
    getattr(
        settings,
        "ALLAUTH_2F2A_ALWAYS_REVEAL_BACKUP_TOKENS",
        True,
    ),
)

QRCODE_TYPE = getattr(
    settings,
    "ALLAUTH_2F2A_QRCODE_TYPE",
    "data",
)

TWOFA_FORMS = getattr(
    settings,
    "ALLAUTH_2F2A_2FA_FORMS",
    {
        "authentication": "allauth_2f2a.forms.TOTPAuthenticateForm",
        "device": "allauth_2f2a.forms.TOTPDeviceForm",
        "remove": "allauth_2f2a.forms.TOTPDeviceRemoveForm",
    },
)
