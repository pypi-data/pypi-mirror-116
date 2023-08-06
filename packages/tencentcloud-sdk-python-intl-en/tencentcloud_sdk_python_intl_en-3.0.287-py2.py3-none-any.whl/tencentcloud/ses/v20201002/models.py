# -*- coding: utf8 -*-
# Copyright (c) 2017-2021 THL A29 Limited, a Tencent company. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import warnings

from tencentcloud.common.abstract_model import AbstractModel


class Attachment(AbstractModel):
    """Attachment structure, including attachment name and content after base64 encoding.

    """

    def __init__(self):
        """
        :param FileName: Attachment name, which cannot exceed 255 characters. Some attachment types are not supported. For details, see [Attachment Types](https://intl.cloud.tencent.com/document/product/1288/51951?from_cn_redirect=1).\n        :type FileName: str\n        :param Content: Attachment content after base64 encoding. A single attachment cannot exceed 5 MB. Note: Tencent Cloud APIs require that a request packet should not exceed 10 MB. If you are sending multiple attachments, the total size of these attachments cannot exceed 10 MB.\n        :type Content: str\n        """
        self.FileName = None
        self.Content = None


    def _deserialize(self, params):
        self.FileName = params.get("FileName")
        self.Content = params.get("Content")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BlackEmailAddress(AbstractModel):
    """Email address blocklist structure, including the blocklisted address and the time when it is blocklisted.

    """

    def __init__(self):
        """
        :param BounceTime: Time when the email address is blocklisted.\n        :type BounceTime: str\n        :param EmailAddress: Blocklisted email address.\n        :type EmailAddress: str\n        """
        self.BounceTime = None
        self.EmailAddress = None


    def _deserialize(self, params):
        self.BounceTime = params.get("BounceTime")
        self.EmailAddress = params.get("EmailAddress")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateEmailAddressRequest(AbstractModel):
    """CreateEmailAddress request structure.

    """

    def __init__(self):
        """
        :param EmailAddress: Your sender address. (You can create up to 10 sender addresses for each domain.)\n        :type EmailAddress: str\n        :param EmailSenderName: Sender name.\n        :type EmailSenderName: str\n        """
        self.EmailAddress = None
        self.EmailSenderName = None


    def _deserialize(self, params):
        self.EmailAddress = params.get("EmailAddress")
        self.EmailSenderName = params.get("EmailSenderName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateEmailAddressResponse(AbstractModel):
    """CreateEmailAddress response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateEmailIdentityRequest(AbstractModel):
    """CreateEmailIdentity request structure.

    """

    def __init__(self):
        """
        :param EmailIdentity: Your sender domain. You are advised to use a third-level domain, for example, mail.qcloud.com.\n        :type EmailIdentity: str\n        """
        self.EmailIdentity = None


    def _deserialize(self, params):
        self.EmailIdentity = params.get("EmailIdentity")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateEmailIdentityResponse(AbstractModel):
    """CreateEmailIdentity response structure.

    """

    def __init__(self):
        """
        :param IdentityType: Verification type. The value is fixed to `DOMAIN`.\n        :type IdentityType: str\n        :param VerifiedForSendingStatus: Verification passed or not.\n        :type VerifiedForSendingStatus: bool\n        :param Attributes: DNS information that needs to be configured.\n        :type Attributes: list of DNSAttributes\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.IdentityType = None
        self.VerifiedForSendingStatus = None
        self.Attributes = None
        self.RequestId = None


    def _deserialize(self, params):
        self.IdentityType = params.get("IdentityType")
        self.VerifiedForSendingStatus = params.get("VerifiedForSendingStatus")
        if params.get("Attributes") is not None:
            self.Attributes = []
            for item in params.get("Attributes"):
                obj = DNSAttributes()
                obj._deserialize(item)
                self.Attributes.append(obj)
        self.RequestId = params.get("RequestId")


class CreateEmailTemplateRequest(AbstractModel):
    """CreateEmailTemplate request structure.

    """

    def __init__(self):
        """
        :param TemplateName: Template name.\n        :type TemplateName: str\n        :param TemplateContent: Template content.\n        :type TemplateContent: :class:`tencentcloud.ses.v20201002.models.TemplateContent`\n        """
        self.TemplateName = None
        self.TemplateContent = None


    def _deserialize(self, params):
        self.TemplateName = params.get("TemplateName")
        if params.get("TemplateContent") is not None:
            self.TemplateContent = TemplateContent()
            self.TemplateContent._deserialize(params.get("TemplateContent"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateEmailTemplateResponse(AbstractModel):
    """CreateEmailTemplate response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DNSAttributes(AbstractModel):
    """Describes the domain name, record type, expected value, and currently configured value of DNS records.

    """

    def __init__(self):
        """
        :param Type: Record types: CNAME, A, TXT, and MX.\n        :type Type: str\n        :param SendDomain: Domain name.\n        :type SendDomain: str\n        :param ExpectedValue: Expected value.\n        :type ExpectedValue: str\n        :param CurrentValue: Currently configured value.\n        :type CurrentValue: str\n        :param Status: Approved or not. The default value is `false`.\n        :type Status: bool\n        """
        self.Type = None
        self.SendDomain = None
        self.ExpectedValue = None
        self.CurrentValue = None
        self.Status = None


    def _deserialize(self, params):
        self.Type = params.get("Type")
        self.SendDomain = params.get("SendDomain")
        self.ExpectedValue = params.get("ExpectedValue")
        self.CurrentValue = params.get("CurrentValue")
        self.Status = params.get("Status")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteBlackListRequest(AbstractModel):
    """DeleteBlackList request structure.

    """

    def __init__(self):
        """
        :param EmailAddressList: List of email addresses to be unblocklisted. Enter at least one address.\n        :type EmailAddressList: list of str\n        """
        self.EmailAddressList = None


    def _deserialize(self, params):
        self.EmailAddressList = params.get("EmailAddressList")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteBlackListResponse(AbstractModel):
    """DeleteBlackList response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteEmailAddressRequest(AbstractModel):
    """DeleteEmailAddress request structure.

    """

    def __init__(self):
        """
        :param EmailAddress: Sender address.\n        :type EmailAddress: str\n        """
        self.EmailAddress = None


    def _deserialize(self, params):
        self.EmailAddress = params.get("EmailAddress")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteEmailAddressResponse(AbstractModel):
    """DeleteEmailAddress response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteEmailIdentityRequest(AbstractModel):
    """DeleteEmailIdentity request structure.

    """

    def __init__(self):
        """
        :param EmailIdentity: Sender domain.\n        :type EmailIdentity: str\n        """
        self.EmailIdentity = None


    def _deserialize(self, params):
        self.EmailIdentity = params.get("EmailIdentity")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteEmailIdentityResponse(AbstractModel):
    """DeleteEmailIdentity response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteEmailTemplateRequest(AbstractModel):
    """DeleteEmailTemplate request structure.

    """

    def __init__(self):
        """
        :param TemplateID: Template ID\n        :type TemplateID: int\n        """
        self.TemplateID = None


    def _deserialize(self, params):
        self.TemplateID = params.get("TemplateID")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteEmailTemplateResponse(AbstractModel):
    """DeleteEmailTemplate response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class EmailIdentity(AbstractModel):
    """Sender domain verification list structure

    """

    def __init__(self):
        """
        :param IdentityName: Sender domain.\n        :type IdentityName: str\n        :param IdentityType: Verification type. The value is fixed to `DOMAIN`.\n        :type IdentityType: str\n        :param SendingEnabled: Verification passed or not.\n        :type SendingEnabled: bool\n        """
        self.IdentityName = None
        self.IdentityType = None
        self.SendingEnabled = None


    def _deserialize(self, params):
        self.IdentityName = params.get("IdentityName")
        self.IdentityType = params.get("IdentityType")
        self.SendingEnabled = params.get("SendingEnabled")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EmailSender(AbstractModel):
    """Describes sender information.

    """

    def __init__(self):
        """
        :param EmailAddress: Sender address.\n        :type EmailAddress: str\n        :param EmailSenderName: Sender name.
Note: this field may return `null`, indicating that no valid values can be obtained.\n        :type EmailSenderName: str\n        :param CreatedTimestamp: Creation time.
Note: this field may return `null`, indicating that no valid values can be obtained.\n        :type CreatedTimestamp: int\n        """
        self.EmailAddress = None
        self.EmailSenderName = None
        self.CreatedTimestamp = None


    def _deserialize(self, params):
        self.EmailAddress = params.get("EmailAddress")
        self.EmailSenderName = params.get("EmailSenderName")
        self.CreatedTimestamp = params.get("CreatedTimestamp")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GetEmailIdentityRequest(AbstractModel):
    """GetEmailIdentity request structure.

    """

    def __init__(self):
        """
        :param EmailIdentity: Sender domain.\n        :type EmailIdentity: str\n        """
        self.EmailIdentity = None


    def _deserialize(self, params):
        self.EmailIdentity = params.get("EmailIdentity")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GetEmailIdentityResponse(AbstractModel):
    """GetEmailIdentity response structure.

    """

    def __init__(self):
        """
        :param IdentityType: Verification type. The value is fixed to `DOMAIN`.\n        :type IdentityType: str\n        :param VerifiedForSendingStatus: Verification passed or not.\n        :type VerifiedForSendingStatus: bool\n        :param Attributes: DNS configuration details.\n        :type Attributes: list of DNSAttributes\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.IdentityType = None
        self.VerifiedForSendingStatus = None
        self.Attributes = None
        self.RequestId = None


    def _deserialize(self, params):
        self.IdentityType = params.get("IdentityType")
        self.VerifiedForSendingStatus = params.get("VerifiedForSendingStatus")
        if params.get("Attributes") is not None:
            self.Attributes = []
            for item in params.get("Attributes"):
                obj = DNSAttributes()
                obj._deserialize(item)
                self.Attributes.append(obj)
        self.RequestId = params.get("RequestId")


class GetEmailTemplateRequest(AbstractModel):
    """GetEmailTemplate request structure.

    """

    def __init__(self):
        """
        :param TemplateID: Template ID.\n        :type TemplateID: int\n        """
        self.TemplateID = None


    def _deserialize(self, params):
        self.TemplateID = params.get("TemplateID")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GetEmailTemplateResponse(AbstractModel):
    """GetEmailTemplate response structure.

    """

    def __init__(self):
        """
        :param TemplateContent: Template content.\n        :type TemplateContent: :class:`tencentcloud.ses.v20201002.models.TemplateContent`\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.TemplateContent = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TemplateContent") is not None:
            self.TemplateContent = TemplateContent()
            self.TemplateContent._deserialize(params.get("TemplateContent"))
        self.RequestId = params.get("RequestId")


class GetSendEmailStatusRequest(AbstractModel):
    """GetSendEmailStatus request structure.

    """

    def __init__(self):
        """
        :param RequestDate: Sent date. This parameter is required. You can only query the sending status for a single date at a time.\n        :type RequestDate: str\n        :param Offset: Offset. Default value: `0`\n        :type Offset: int\n        :param Limit: Maximum number of pulled entries. The maximum value is `100`.\n        :type Limit: int\n        :param MessageId: `MessageId` field returned by the `SendMail` API\n        :type MessageId: str\n        :param ToEmailAddress: Recipient email address\n        :type ToEmailAddress: str\n        """
        self.RequestDate = None
        self.Offset = None
        self.Limit = None
        self.MessageId = None
        self.ToEmailAddress = None


    def _deserialize(self, params):
        self.RequestDate = params.get("RequestDate")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.MessageId = params.get("MessageId")
        self.ToEmailAddress = params.get("ToEmailAddress")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GetSendEmailStatusResponse(AbstractModel):
    """GetSendEmailStatus response structure.

    """

    def __init__(self):
        """
        :param EmailStatusList: Email sending status list\n        :type EmailStatusList: list of SendEmailStatus\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.EmailStatusList = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("EmailStatusList") is not None:
            self.EmailStatusList = []
            for item in params.get("EmailStatusList"):
                obj = SendEmailStatus()
                obj._deserialize(item)
                self.EmailStatusList.append(obj)
        self.RequestId = params.get("RequestId")


class GetStatisticsReportRequest(AbstractModel):
    """GetStatisticsReport request structure.

    """

    def __init__(self):
        """
        :param StartDate: Start date.\n        :type StartDate: str\n        :param EndDate: End date.\n        :type EndDate: str\n        :param Domain: Sender domain.\n        :type Domain: str\n        :param ReceivingMailboxType: Recipient address type, for example, gmail.com.\n        :type ReceivingMailboxType: str\n        """
        self.StartDate = None
        self.EndDate = None
        self.Domain = None
        self.ReceivingMailboxType = None


    def _deserialize(self, params):
        self.StartDate = params.get("StartDate")
        self.EndDate = params.get("EndDate")
        self.Domain = params.get("Domain")
        self.ReceivingMailboxType = params.get("ReceivingMailboxType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GetStatisticsReportResponse(AbstractModel):
    """GetStatisticsReport response structure.

    """

    def __init__(self):
        """
        :param DailyVolumes: Daily email sending statistics.\n        :type DailyVolumes: list of Volume\n        :param OverallVolume: Overall email sending statistics.\n        :type OverallVolume: :class:`tencentcloud.ses.v20201002.models.Volume`\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.DailyVolumes = None
        self.OverallVolume = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DailyVolumes") is not None:
            self.DailyVolumes = []
            for item in params.get("DailyVolumes"):
                obj = Volume()
                obj._deserialize(item)
                self.DailyVolumes.append(obj)
        if params.get("OverallVolume") is not None:
            self.OverallVolume = Volume()
            self.OverallVolume._deserialize(params.get("OverallVolume"))
        self.RequestId = params.get("RequestId")


class ListBlackEmailAddressRequest(AbstractModel):
    """ListBlackEmailAddress request structure.

    """

    def __init__(self):
        """
        :param StartDate: Start date in the format of `YYYY-MM-DD`\n        :type StartDate: str\n        :param EndDate: End date in the format of `YYYY-MM-DD`\n        :type EndDate: str\n        :param Limit: Common parameter. It must be used with `Offset`.\n        :type Limit: int\n        :param Offset: Common parameter. It must be used with `Limit`. Maximum value of `Limit`: `100`.\n        :type Offset: int\n        :param EmailAddress: You can specify an email address to query.\n        :type EmailAddress: str\n        :param TaskID: You can specify a task ID to query.\n        :type TaskID: str\n        """
        self.StartDate = None
        self.EndDate = None
        self.Limit = None
        self.Offset = None
        self.EmailAddress = None
        self.TaskID = None


    def _deserialize(self, params):
        self.StartDate = params.get("StartDate")
        self.EndDate = params.get("EndDate")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.EmailAddress = params.get("EmailAddress")
        self.TaskID = params.get("TaskID")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ListBlackEmailAddressResponse(AbstractModel):
    """ListBlackEmailAddress response structure.

    """

    def __init__(self):
        """
        :param BlackList: List of blocklisted addresses.\n        :type BlackList: list of BlackEmailAddress\n        :param TotalCount: Total number of blocklisted addresses.\n        :type TotalCount: int\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.BlackList = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("BlackList") is not None:
            self.BlackList = []
            for item in params.get("BlackList"):
                obj = BlackEmailAddress()
                obj._deserialize(item)
                self.BlackList.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class ListEmailAddressRequest(AbstractModel):
    """ListEmailAddress request structure.

    """


class ListEmailAddressResponse(AbstractModel):
    """ListEmailAddress response structure.

    """

    def __init__(self):
        """
        :param EmailSenders: Details of sender addresses.
Note: this field may return `null`, indicating that no valid values can be obtained.\n        :type EmailSenders: list of EmailSender\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.EmailSenders = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("EmailSenders") is not None:
            self.EmailSenders = []
            for item in params.get("EmailSenders"):
                obj = EmailSender()
                obj._deserialize(item)
                self.EmailSenders.append(obj)
        self.RequestId = params.get("RequestId")


class ListEmailIdentitiesRequest(AbstractModel):
    """ListEmailIdentities request structure.

    """


class ListEmailIdentitiesResponse(AbstractModel):
    """ListEmailIdentities response structure.

    """

    def __init__(self):
        """
        :param EmailIdentities: List of sender domains.\n        :type EmailIdentities: list of EmailIdentity\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.EmailIdentities = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("EmailIdentities") is not None:
            self.EmailIdentities = []
            for item in params.get("EmailIdentities"):
                obj = EmailIdentity()
                obj._deserialize(item)
                self.EmailIdentities.append(obj)
        self.RequestId = params.get("RequestId")


class ListEmailTemplatesRequest(AbstractModel):
    """ListEmailTemplates request structure.

    """

    def __init__(self):
        """
        :param Limit: Number of templates to get. This parameter is used for pagination.\n        :type Limit: int\n        :param Offset: Template offset to get. This parameter is used for pagination.\n        :type Offset: int\n        """
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ListEmailTemplatesResponse(AbstractModel):
    """ListEmailTemplates response structure.

    """

    def __init__(self):
        """
        :param TemplatesMetadata: List of email templates.\n        :type TemplatesMetadata: list of TemplatesMetadata\n        :param TotalCount: Total number of templates.\n        :type TotalCount: int\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.TemplatesMetadata = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TemplatesMetadata") is not None:
            self.TemplatesMetadata = []
            for item in params.get("TemplatesMetadata"):
                obj = TemplatesMetadata()
                obj._deserialize(item)
                self.TemplatesMetadata.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class SendEmailRequest(AbstractModel):
    """SendEmail request structure.

    """

    def __init__(self):
        """
        :param FromEmailAddress: Sender address. Enter a sender address, for example, noreply@mail.qcloud.com. To display the sender name, enter the address in the following format:  
sender &lt;email address&gt;. For example: 
Tencent Cloud team &lt;noreply@mail.qcloud.com&gt;\n        :type FromEmailAddress: str\n        :param Destination: Recipient email addresses. You can send an email to up to 50 recipients at a time. Note: the email content will display all recipient addresses. To send one-to-one emails to several recipients, please call the API multiple times to send the emails.\n        :type Destination: list of str\n        :param Subject: Email subject.\n        :type Subject: str\n        :param ReplyToAddresses: Reply-to address. You can enter a valid personal email address that can receive emails. If this field is left empty, reply emails will be sent to Tencent Cloud.\n        :type ReplyToAddresses: str\n        :param Template: Template when sending emails using a template.\n        :type Template: :class:`tencentcloud.ses.v20201002.models.Template`\n        :param Simple: Email content when sending emails by calling the API.\n        :type Simple: :class:`tencentcloud.ses.v20201002.models.Simple`\n        :param Attachments: Email attachments\n        :type Attachments: list of Attachment\n        """
        self.FromEmailAddress = None
        self.Destination = None
        self.Subject = None
        self.ReplyToAddresses = None
        self.Template = None
        self.Simple = None
        self.Attachments = None


    def _deserialize(self, params):
        self.FromEmailAddress = params.get("FromEmailAddress")
        self.Destination = params.get("Destination")
        self.Subject = params.get("Subject")
        self.ReplyToAddresses = params.get("ReplyToAddresses")
        if params.get("Template") is not None:
            self.Template = Template()
            self.Template._deserialize(params.get("Template"))
        if params.get("Simple") is not None:
            self.Simple = Simple()
            self.Simple._deserialize(params.get("Simple"))
        if params.get("Attachments") is not None:
            self.Attachments = []
            for item in params.get("Attachments"):
                obj = Attachment()
                obj._deserialize(item)
                self.Attachments.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SendEmailResponse(AbstractModel):
    """SendEmail response structure.

    """

    def __init__(self):
        """
        :param MessageId: Unique ID generated when receiving the message\n        :type MessageId: str\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.MessageId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.MessageId = params.get("MessageId")
        self.RequestId = params.get("RequestId")


class SendEmailStatus(AbstractModel):
    """Describes the email sending status.

    """

    def __init__(self):
        """
        :param MessageId: `MessageId` field returned by the `SendEmail` API\n        :type MessageId: str\n        :param ToEmailAddress: Recipient email address\n        :type ToEmailAddress: str\n        :param FromEmailAddress: Sender email address\n        :type FromEmailAddress: str\n        :param SendStatus: Tencent Cloud processing status:
0: successful.
1001: internal system exception.
1002: internal system exception.
1003: internal system exception.
1003: internal system exception.
1004: email sending timeout.
1005: internal system exception.
1006: you have sent too many emails to the same address in a short period.
1007: the email address is in the blocklist.
1009: internal system exception.
1010: daily email sending limit exceeded.
1011: no permission to send custom content. Use a template.
2001: no results found.
3007: invalid template ID or unavailable template.
3008: template status exception.
3009: no permission to use this template.
3010: the format of the `TemplateData` field is incorrect. 
3014: unable to send the email because the sender domain is not verified.
3020: the recipient email address is in the blocklist.
3024: failed to pre-check the email address format.
3030: email sending is restricted temporarily due to high bounce rate.
3033: the account has insufficient balance or overdue payment.\n        :type SendStatus: int\n        :param DeliverStatus: Recipient processing status:
0: Tencent Cloud has accepted the request and added it to the send queue.
1: the email is delivered successfully, `DeliverTime` indicates the time when the email is delivered successfully.
2: the email is discarded. `DeliverMessage` indicates the reason for discarding.
3: the recipient's ESP rejects the email, probably because the email address does not exist or due to other reasons.
8: the email is delayed by the ESP. `DeliverMessage` indicates the reason for delay.\n        :type DeliverStatus: int\n        :param DeliverMessage: Description of the recipient processing status\n        :type DeliverMessage: str\n        :param RequestTime: Timestamp when the request arrives at Tencent Cloud\n        :type RequestTime: int\n        :param DeliverTime: Timestamp when Tencent Cloud delivers the email\n        :type DeliverTime: int\n        :param UserOpened: Whether the recipient has opened the email\n        :type UserOpened: bool\n        :param UserClicked: Whether the recipient has clicked the links in the email\n        :type UserClicked: bool\n        :param UserUnsubscribed: Whether the recipient has unsubscribed from emails sent by the sender\n        :type UserUnsubscribed: bool\n        :param UserComplainted: Whether the recipient has reported the sender\n        :type UserComplainted: bool\n        """
        self.MessageId = None
        self.ToEmailAddress = None
        self.FromEmailAddress = None
        self.SendStatus = None
        self.DeliverStatus = None
        self.DeliverMessage = None
        self.RequestTime = None
        self.DeliverTime = None
        self.UserOpened = None
        self.UserClicked = None
        self.UserUnsubscribed = None
        self.UserComplainted = None


    def _deserialize(self, params):
        self.MessageId = params.get("MessageId")
        self.ToEmailAddress = params.get("ToEmailAddress")
        self.FromEmailAddress = params.get("FromEmailAddress")
        self.SendStatus = params.get("SendStatus")
        self.DeliverStatus = params.get("DeliverStatus")
        self.DeliverMessage = params.get("DeliverMessage")
        self.RequestTime = params.get("RequestTime")
        self.DeliverTime = params.get("DeliverTime")
        self.UserOpened = params.get("UserOpened")
        self.UserClicked = params.get("UserClicked")
        self.UserUnsubscribed = params.get("UserUnsubscribed")
        self.UserComplainted = params.get("UserComplainted")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Simple(AbstractModel):
    """Email content, which can be plain text (TEXT), pure code (HTML), or a combination of TEXT and HTML (recommended).

    """

    def __init__(self):
        """
        :param Html: HTML code after base64 encoding. To ensure correct display, this parameter should include all code information and cannot contain external CSS.\n        :type Html: str\n        :param Text: Plain text content after base64 encoding. If HTML is not involved, the plain text will be displayed in the email. Otherwise, this parameter represents the plain text style of the email.\n        :type Text: str\n        """
        self.Html = None
        self.Text = None


    def _deserialize(self, params):
        self.Html = params.get("Html")
        self.Text = params.get("Text")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Template(AbstractModel):
    """Template information, including template ID, template variable parameters, etc.

    """

    def __init__(self):
        """
        :param TemplateID: Template ID. If you don’t have any template, please create one.\n        :type TemplateID: int\n        :param TemplateData: Variable parameters in the template. Please use `json.dump` to format the JSON object into a string type. The object is a set of key-value pairs. Each key denotes a variable, which is represented by {{key}}. The key will be replaced with the corresponding value (represented by {{value}}) when sending the email.\n        :type TemplateData: str\n        """
        self.TemplateID = None
        self.TemplateData = None


    def _deserialize(self, params):
        self.TemplateID = params.get("TemplateID")
        self.TemplateData = params.get("TemplateData")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TemplateContent(AbstractModel):
    """Template content, which must include at least one of TEXT and HTML. A combination of TEXT and HTML is recommended.

    """

    def __init__(self):
        """
        :param Html: HTML code after base64 encoding.\n        :type Html: str\n        :param Text: Text content after base64 encoding.\n        :type Text: str\n        """
        self.Html = None
        self.Text = None


    def _deserialize(self, params):
        self.Html = params.get("Html")
        self.Text = params.get("Text")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TemplatesMetadata(AbstractModel):
    """Template list structure.

    """

    def __init__(self):
        """
        :param CreatedTimestamp: Creation time.\n        :type CreatedTimestamp: int\n        :param TemplateName: Template name.\n        :type TemplateName: str\n        :param TemplateStatus: Template status. 1: under review; 0: approved; 2: rejected; other values: unavailable.\n        :type TemplateStatus: int\n        :param TemplateID: Template ID.\n        :type TemplateID: int\n        :param ReviewReason: Review reply\n        :type ReviewReason: str\n        """
        self.CreatedTimestamp = None
        self.TemplateName = None
        self.TemplateStatus = None
        self.TemplateID = None
        self.ReviewReason = None


    def _deserialize(self, params):
        self.CreatedTimestamp = params.get("CreatedTimestamp")
        self.TemplateName = params.get("TemplateName")
        self.TemplateStatus = params.get("TemplateStatus")
        self.TemplateID = params.get("TemplateID")
        self.ReviewReason = params.get("ReviewReason")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateEmailIdentityRequest(AbstractModel):
    """UpdateEmailIdentity request structure.

    """

    def __init__(self):
        """
        :param EmailIdentity: Domain to be verified.\n        :type EmailIdentity: str\n        """
        self.EmailIdentity = None


    def _deserialize(self, params):
        self.EmailIdentity = params.get("EmailIdentity")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateEmailIdentityResponse(AbstractModel):
    """UpdateEmailIdentity response structure.

    """

    def __init__(self):
        """
        :param IdentityType: Verification type. The value is fixed to `DOMAIN`.\n        :type IdentityType: str\n        :param VerifiedForSendingStatus: Verification passed or not.\n        :type VerifiedForSendingStatus: bool\n        :param Attributes: DNS information that needs to be configured.\n        :type Attributes: list of DNSAttributes\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.IdentityType = None
        self.VerifiedForSendingStatus = None
        self.Attributes = None
        self.RequestId = None


    def _deserialize(self, params):
        self.IdentityType = params.get("IdentityType")
        self.VerifiedForSendingStatus = params.get("VerifiedForSendingStatus")
        if params.get("Attributes") is not None:
            self.Attributes = []
            for item in params.get("Attributes"):
                obj = DNSAttributes()
                obj._deserialize(item)
                self.Attributes.append(obj)
        self.RequestId = params.get("RequestId")


class UpdateEmailTemplateRequest(AbstractModel):
    """UpdateEmailTemplate request structure.

    """

    def __init__(self):
        """
        :param TemplateContent: Template content.\n        :type TemplateContent: :class:`tencentcloud.ses.v20201002.models.TemplateContent`\n        :param TemplateID: Template ID.\n        :type TemplateID: int\n        :param TemplateName: Template name.\n        :type TemplateName: str\n        """
        self.TemplateContent = None
        self.TemplateID = None
        self.TemplateName = None


    def _deserialize(self, params):
        if params.get("TemplateContent") is not None:
            self.TemplateContent = TemplateContent()
            self.TemplateContent._deserialize(params.get("TemplateContent"))
        self.TemplateID = params.get("TemplateID")
        self.TemplateName = params.get("TemplateName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateEmailTemplateResponse(AbstractModel):
    """UpdateEmailTemplate response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class Volume(AbstractModel):
    """Statistics structure.

    """

    def __init__(self):
        """
        :param SendDate: Date
Note: this field may return `null`, indicating that no valid values can be obtained.\n        :type SendDate: str\n        :param RequestCount: Number of email requests.\n        :type RequestCount: int\n        :param AcceptedCount: Number of email requests accepted by Tencent Cloud.\n        :type AcceptedCount: int\n        :param DeliveredCount: Number of delivered emails.\n        :type DeliveredCount: int\n        :param OpenedCount: Number of users (deduplicated) who opened emails.\n        :type OpenedCount: int\n        :param ClickedCount: Number of recipients who clicked on links in emails.\n        :type ClickedCount: int\n        :param BounceCount: Number of bounced emails.\n        :type BounceCount: int\n        :param UnsubscribeCount: Number of users who canceled subscriptions.
Note: this field may return `null`, indicating that no valid values can be obtained.\n        :type UnsubscribeCount: int\n        """
        self.SendDate = None
        self.RequestCount = None
        self.AcceptedCount = None
        self.DeliveredCount = None
        self.OpenedCount = None
        self.ClickedCount = None
        self.BounceCount = None
        self.UnsubscribeCount = None


    def _deserialize(self, params):
        self.SendDate = params.get("SendDate")
        self.RequestCount = params.get("RequestCount")
        self.AcceptedCount = params.get("AcceptedCount")
        self.DeliveredCount = params.get("DeliveredCount")
        self.OpenedCount = params.get("OpenedCount")
        self.ClickedCount = params.get("ClickedCount")
        self.BounceCount = params.get("BounceCount")
        self.UnsubscribeCount = params.get("UnsubscribeCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        