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


class ApplySnapshotRequest(AbstractModel):
    """ApplySnapshot request structure.

    """

    def __init__(self):
        """
        :param SnapshotId: Snapshot ID, which can be queried via [DescribeSnapshots](https://intl.cloud.tencent.com/document/product/362/15647?from_cn_redirect=1).\n        :type SnapshotId: str\n        :param DiskId: ID of the original cloud disk corresponding to the snapshot, which can be queried via the API [DescribeDisks](https://intl.cloud.tencent.com/document/product/362/16315?from_cn_redirect=1).\n        :type DiskId: str\n        """
        self.SnapshotId = None
        self.DiskId = None


    def _deserialize(self, params):
        self.SnapshotId = params.get("SnapshotId")
        self.DiskId = params.get("DiskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ApplySnapshotResponse(AbstractModel):
    """ApplySnapshot response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AttachDetail(AbstractModel):
    """This describes the number of mounted and mountable data disks of an instance.

    """

    def __init__(self):
        """
        :param InstanceId: Instance ID\n        :type InstanceId: str\n        :param AttachedDiskCount: The number of instances mounted to data disk.\n        :type AttachedDiskCount: int\n        :param MaxAttachCount: The maximum number of instances that can be mounted to data disk.\n        :type MaxAttachCount: int\n        """
        self.InstanceId = None
        self.AttachedDiskCount = None
        self.MaxAttachCount = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.AttachedDiskCount = params.get("AttachedDiskCount")
        self.MaxAttachCount = params.get("MaxAttachCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AttachDisksRequest(AbstractModel):
    """AttachDisks request structure.

    """

    def __init__(self):
        """
        :param InstanceId: ID of the CVM instance on which the cloud disk will be mounted. It can be queried via the API [DescribeInstances](https://intl.cloud.tencent.com/document/product/213/15728?from_cn_redirect=1).\n        :type InstanceId: str\n        :param DiskIds: ID of the elastic cloud disk to be mounted, which can be queried through the API [DescribeDisks](https://intl.cloud.tencent.com/document/product/362/16315?from_cn_redirect=1). A maximum of 10 elastic cloud disks can be mounted in a single request.\n        :type DiskIds: list of str\n        :param DeleteWithInstance: Optional parameter. If this is not passed only the mount operation is executed. If `True` is passed, the cloud disk will be configured to be terminated when the server it is mounted to is terminated. This is only valid for pay-as-you-go cloud disks.\n        :type DeleteWithInstance: bool\n        :param AttachMode: (Optional) Specifies the cloud disk mounting method. It’s only valid for BM models. Valid values: <br><li>PF<br><li>VF\n        :type AttachMode: str\n        """
        self.InstanceId = None
        self.DiskIds = None
        self.DeleteWithInstance = None
        self.AttachMode = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.DiskIds = params.get("DiskIds")
        self.DeleteWithInstance = params.get("DeleteWithInstance")
        self.AttachMode = params.get("AttachMode")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AttachDisksResponse(AbstractModel):
    """AttachDisks response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class AutoSnapshotPolicy(AbstractModel):
    """This describes the detailed information of the scheduled snapshot policy.

    """

    def __init__(self):
        """
        :param AutoSnapshotPolicyId: Scheduled snapshot policy ID.\n        :type AutoSnapshotPolicyId: str\n        :param AutoSnapshotPolicyName: Scheduled snapshot policy name.\n        :type AutoSnapshotPolicyName: str\n        :param AutoSnapshotPolicyState: Scheduled snapshot policy state. Value range:<br><li>NORMAL: Normal<br><li>ISOLATED: Isolated.\n        :type AutoSnapshotPolicyState: str\n        :param IsActivated: Whether scheduled snapshot policy is activated.\n        :type IsActivated: bool\n        :param IsPermanent: Whether the snapshot created by this scheduled snapshot policy is retained permanently.\n        :type IsPermanent: bool\n        :param RetentionDays: Number of days the snapshot created by this scheduled snapshot policy is retained.\n        :type RetentionDays: int\n        :param CreateTime: The time the scheduled snapshot policy was created.\n        :type CreateTime: str\n        :param NextTriggerTime: The time the scheduled snapshot will be triggered again.\n        :type NextTriggerTime: str\n        :param Policy: The policy for executing the scheduled snapshot.\n        :type Policy: list of Policy\n        :param DiskIdSet: The list of cloud disk IDs that the current scheduled snapshot policy is bound to.\n        :type DiskIdSet: list of str\n        """
        self.AutoSnapshotPolicyId = None
        self.AutoSnapshotPolicyName = None
        self.AutoSnapshotPolicyState = None
        self.IsActivated = None
        self.IsPermanent = None
        self.RetentionDays = None
        self.CreateTime = None
        self.NextTriggerTime = None
        self.Policy = None
        self.DiskIdSet = None


    def _deserialize(self, params):
        self.AutoSnapshotPolicyId = params.get("AutoSnapshotPolicyId")
        self.AutoSnapshotPolicyName = params.get("AutoSnapshotPolicyName")
        self.AutoSnapshotPolicyState = params.get("AutoSnapshotPolicyState")
        self.IsActivated = params.get("IsActivated")
        self.IsPermanent = params.get("IsPermanent")
        self.RetentionDays = params.get("RetentionDays")
        self.CreateTime = params.get("CreateTime")
        self.NextTriggerTime = params.get("NextTriggerTime")
        if params.get("Policy") is not None:
            self.Policy = []
            for item in params.get("Policy"):
                obj = Policy()
                obj._deserialize(item)
                self.Policy.append(obj)
        self.DiskIdSet = params.get("DiskIdSet")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BindAutoSnapshotPolicyRequest(AbstractModel):
    """BindAutoSnapshotPolicy request structure.

    """

    def __init__(self):
        """
        :param AutoSnapshotPolicyId: ID of scheduled snapshot policy to be bound.\n        :type AutoSnapshotPolicyId: str\n        :param DiskIds: List of cloud disk IDs to be bound. Maximum of 80 cloud disks can be bound per request.\n        :type DiskIds: list of str\n        """
        self.AutoSnapshotPolicyId = None
        self.DiskIds = None


    def _deserialize(self, params):
        self.AutoSnapshotPolicyId = params.get("AutoSnapshotPolicyId")
        self.DiskIds = params.get("DiskIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BindAutoSnapshotPolicyResponse(AbstractModel):
    """BindAutoSnapshotPolicy response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateAutoSnapshotPolicyRequest(AbstractModel):
    """CreateAutoSnapshotPolicy request structure.

    """

    def __init__(self):
        """
        :param Policy: The policy for executing the scheduled snapshot.\n        :type Policy: list of Policy\n        :param AutoSnapshotPolicyName: The name of the scheduled snapshot policy to be created. If it is left empty, the default is 'Not named'. The maximum length cannot exceed 60 bytes.\n        :type AutoSnapshotPolicyName: str\n        :param IsActivated: Whether or not the scheduled snapshot policy is activated. FALSE: Not activated. TRUE: Activated. The default value is TRUE.\n        :type IsActivated: bool\n        :param IsPermanent: Whether the snapshot created by this scheduled snapshot policy is retained permanently. FALSE: Not retained permanently. TRUE: Retained permanently. The default value is FALSE.\n        :type IsPermanent: bool\n        :param RetentionDays: The number of days that a snapshot created by this scheduled snapshot policy is retained. The default value is 7. If this parameter is specified, the IsPermanent input parameter can not be TRUE, otherwise a conflict will occur.\n        :type RetentionDays: int\n        :param DryRun: Whether to create an execution policy for the scheduled snapshot. TRUE: Only the time of the initial backup needs to be obtained, and no scheduled snapshot policy is actually created. FALSE: Create. The default value is FALSE.\n        :type DryRun: bool\n        """
        self.Policy = None
        self.AutoSnapshotPolicyName = None
        self.IsActivated = None
        self.IsPermanent = None
        self.RetentionDays = None
        self.DryRun = None


    def _deserialize(self, params):
        if params.get("Policy") is not None:
            self.Policy = []
            for item in params.get("Policy"):
                obj = Policy()
                obj._deserialize(item)
                self.Policy.append(obj)
        self.AutoSnapshotPolicyName = params.get("AutoSnapshotPolicyName")
        self.IsActivated = params.get("IsActivated")
        self.IsPermanent = params.get("IsPermanent")
        self.RetentionDays = params.get("RetentionDays")
        self.DryRun = params.get("DryRun")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateAutoSnapshotPolicyResponse(AbstractModel):
    """CreateAutoSnapshotPolicy response structure.

    """

    def __init__(self):
        """
        :param AutoSnapshotPolicyId: The ID of the newly created scheduled snapshot policy.\n        :type AutoSnapshotPolicyId: str\n        :param NextTriggerTime: The time that initial backup will start.\n        :type NextTriggerTime: str\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.AutoSnapshotPolicyId = None
        self.NextTriggerTime = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoSnapshotPolicyId = params.get("AutoSnapshotPolicyId")
        self.NextTriggerTime = params.get("NextTriggerTime")
        self.RequestId = params.get("RequestId")


class CreateDisksRequest(AbstractModel):
    """CreateDisks request structure.

    """

    def __init__(self):
        """
        :param Placement: The location of the instance. The availability zone and the project that the instance belongs to can be specified using this parameter. If the project is not specified, it will be created under the default project.\n        :type Placement: :class:`tencentcloud.cbs.v20170312.models.Placement`\n        :param DiskChargeType: Cloud disk billing method. POSTPAID_BY_HOUR: pay as you go by hour<br><li>CDCPAID: Billed together with the bound dedicated cluster<br>For information about the pricing of each method, see the cloud disk [Pricing Overview](https://intl.cloud.tencent.com/document/product/362/2413?from_cn_redirect=1).\n        :type DiskChargeType: str\n        :param DiskType: Cloud disk media type. Valid values: <br><li>CLOUD_BASIC: HDD cloud disk<br><li>CLOUD_PREMIUM: Premium Cloud Storage<br><li>CLOUD_SSD: SSD<br><li>CLOUD_HSSD: Enhanced SSD<br><li>CLOUD_TSSD: Tremendous SSD\n        :type DiskType: str\n        :param DiskName: The displayed name of the cloud disk. If it is left empty, the default is 'Not named'. The maximum length cannot exceed 60 bytes.\n        :type DiskName: str\n        :param Tags: Cloud disk binding tag.\n        :type Tags: list of Tag\n        :param SnapshotId: Snapshot ID. If this parameter is specified, the cloud disk is created based on the snapshot. The snapshot type must be a data disk snapshot. The snapshot can be queried in the DiskUsage field in the output parameter through the API [DescribeSnapshots](https://intl.cloud.tencent.com/document/product/362/15647?from_cn_redirect=1).\n        :type SnapshotId: str\n        :param DiskCount: If the number of cloud disks to be created is left empty, the default is 1. There is a limit to the maximum number of cloud disks that can be created for a single request. For more information, please see [CBS Use Limits](https://intl.cloud.tencent.com/doc/product/362/5145?from_cn_redirect=1).\n        :type DiskCount: int\n        :param ThroughputPerformance: Extra performance purchased for a cloud disk.<br>This optional parameter is only valid for Tremendous SSD (CLOUD_TSSD) and Enhanced SSD (CLOUD_HSSD).\n        :type ThroughputPerformance: int\n        :param DiskSize: Cloud hard disk size (in GB). <br><li> If `SnapshotId` is passed, `DiskSize` cannot be passed. In this case, the size of the cloud disk is the size of the snapshot. <br><li>To pass `SnapshotId` and `DiskSize` at the same time, the size of the disk must be larger than or equal to the size of the snapshot. <br><li>For information about the size range of cloud disks, see cloud disk [Product Types](https://intl.cloud.tencent.com/document/product/362/2353?from_cn_redirect=1).\n        :type DiskSize: int\n        :param Shareable: The default of optional parameter is False. When True is selected, the cloud disk will be created as a shareable cloud disk.\n        :type Shareable: bool\n        :param ClientToken: A string to ensure the idempotency of the request, which is generated by the client. Each request shall have a unique string with a maximum of 64 ASCII characters. If this parameter is not specified, the idempotency of the request cannot be ensured.\n        :type ClientToken: str\n        :param Encrypt: This parameter is used to create an encrypted cloud disk. Its value is always ENCRYPT.\n        :type Encrypt: str\n        :param DiskChargePrepaid: Relevant parameter settings for the prepaid mode (i.e., monthly subscription). The monthly subscription cloud disk purchase attributes such as usage period and whether or not auto-renewal is set up can be specified using this parameter. <br>This parameter is required when creating a prepaid cloud disk. This parameter is not required when creating an hourly postpaid cloud disk. \n        :type DiskChargePrepaid: :class:`tencentcloud.cbs.v20170312.models.DiskChargePrepaid`\n        :param DeleteSnapshot: Whether to delete the associated non-permanent snapshots when a cloud disk is terminated. Valid values: `0` (do not delete); `1` (delete). Default value: `0`. To find out whether a snapshot is permanent, you can call the `DescribeSnapshots` API and check the `IsPermanent` field (`true`: permanent; `false`: non-permanent) in its response.\n        :type DeleteSnapshot: int\n        """
        self.Placement = None
        self.DiskChargeType = None
        self.DiskType = None
        self.DiskName = None
        self.Tags = None
        self.SnapshotId = None
        self.DiskCount = None
        self.ThroughputPerformance = None
        self.DiskSize = None
        self.Shareable = None
        self.ClientToken = None
        self.Encrypt = None
        self.DiskChargePrepaid = None
        self.DeleteSnapshot = None


    def _deserialize(self, params):
        if params.get("Placement") is not None:
            self.Placement = Placement()
            self.Placement._deserialize(params.get("Placement"))
        self.DiskChargeType = params.get("DiskChargeType")
        self.DiskType = params.get("DiskType")
        self.DiskName = params.get("DiskName")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.SnapshotId = params.get("SnapshotId")
        self.DiskCount = params.get("DiskCount")
        self.ThroughputPerformance = params.get("ThroughputPerformance")
        self.DiskSize = params.get("DiskSize")
        self.Shareable = params.get("Shareable")
        self.ClientToken = params.get("ClientToken")
        self.Encrypt = params.get("Encrypt")
        if params.get("DiskChargePrepaid") is not None:
            self.DiskChargePrepaid = DiskChargePrepaid()
            self.DiskChargePrepaid._deserialize(params.get("DiskChargePrepaid"))
        self.DeleteSnapshot = params.get("DeleteSnapshot")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateDisksResponse(AbstractModel):
    """CreateDisks response structure.

    """

    def __init__(self):
        """
        :param DiskIdSet: List of created cloud disk IDs. \n        :type DiskIdSet: list of str\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.DiskIdSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DiskIdSet = params.get("DiskIdSet")
        self.RequestId = params.get("RequestId")


class CreateSnapshotRequest(AbstractModel):
    """CreateSnapshot request structure.

    """

    def __init__(self):
        """
        :param DiskId: ID of the cloud disk, for which a snapshot needs to be created. It can be queried via the API [DescribeDisks](https://intl.cloud.tencent.com/document/product/362/16315?from_cn_redirect=1).\n        :type DiskId: str\n        :param SnapshotName: Snapshot name. If it is left empty, the new snapshot name is "Not named" by default.\n        :type SnapshotName: str\n        :param Deadline: Expiration time of the snapshot. The snapshot will be automatically deleted upon expiration.\n        :type Deadline: str\n        """
        self.DiskId = None
        self.SnapshotName = None
        self.Deadline = None


    def _deserialize(self, params):
        self.DiskId = params.get("DiskId")
        self.SnapshotName = params.get("SnapshotName")
        self.Deadline = params.get("Deadline")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateSnapshotResponse(AbstractModel):
    """CreateSnapshot response structure.

    """

    def __init__(self):
        """
        :param SnapshotId: ID of the new snapshot.\n        :type SnapshotId: str\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.SnapshotId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.SnapshotId = params.get("SnapshotId")
        self.RequestId = params.get("RequestId")


class DeleteAutoSnapshotPoliciesRequest(AbstractModel):
    """DeleteAutoSnapshotPolicies request structure.

    """

    def __init__(self):
        """
        :param AutoSnapshotPolicyIds: List of scheduled snapshot policy IDs to be deleted.\n        :type AutoSnapshotPolicyIds: list of str\n        """
        self.AutoSnapshotPolicyIds = None


    def _deserialize(self, params):
        self.AutoSnapshotPolicyIds = params.get("AutoSnapshotPolicyIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteAutoSnapshotPoliciesResponse(AbstractModel):
    """DeleteAutoSnapshotPolicies response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteSnapshotsRequest(AbstractModel):
    """DeleteSnapshots request structure.

    """

    def __init__(self):
        """
        :param SnapshotIds: List of IDs of snapshots to be deleted, which can be queried via [DescribeSnapshots](https://intl.cloud.tencent.com/document/product/362/15647?from_cn_redirect=1).\n        :type SnapshotIds: list of str\n        :param DeleteBindImages: Whether to forcibly delete the image associated with the snapshot\n        :type DeleteBindImages: bool\n        """
        self.SnapshotIds = None
        self.DeleteBindImages = None


    def _deserialize(self, params):
        self.SnapshotIds = params.get("SnapshotIds")
        self.DeleteBindImages = params.get("DeleteBindImages")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteSnapshotsResponse(AbstractModel):
    """DeleteSnapshots response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeAutoSnapshotPoliciesRequest(AbstractModel):
    """DescribeAutoSnapshotPolicies request structure.

    """

    def __init__(self):
        """
        :param AutoSnapshotPolicyIds: List of scheduled snapshot policy IDs to be queried. The parameter does not support specifying both `SnapshotIds` and `Filters`.\n        :type AutoSnapshotPolicyIds: list of str\n        :param Filters: Filter conditions. Specification of both the `AutoSnapshotPolicyIds` and `Filters` parameters is not supported.<br><li>auto-snapshot-policy-id - Array of String - Required or not: No - (Filter condition) Filters according to the scheduled snapshot policy ID. The format of the scheduled snapshot policy ID is as follows: `asp-11112222`. <br><li>auto-snapshot-policy-state - Array of String - Required or not: No - (Filter condition) Filters according to the status of the scheduled snapshot policy. The format of the scheduled snapshot policy ID is as follows: `asp-11112222`. (NORMAL: normal | ISOLATED: isolated)<br><li>auto-snapshot-policy-name - Array of String - Required or not: No - (Filter condition) Filters according to the name of the scheduled snapshot policy.\n        :type Filters: list of Filter\n        :param Limit: Number of results to be returned. Default is 20. Maximum is 100. For more information on `Limit`, please see relevant sections in API [Introduction](https://intl.cloud.tencent.com/document/product/362/15633?from_cn_redirect=1).\n        :type Limit: int\n        :param Offset: Offset. Default is 0. For more information on `Offset`, please see relevant sections in API [Introduction](https://intl.cloud.tencent.com/document/product/362/15633?from_cn_redirect=1).\n        :type Offset: int\n        :param Order: Outputs the ordering of the scheduled snapshot lists. Value range: <br><li>ASC: Ascending order <br><li>DESC: Descending order.\n        :type Order: str\n        :param OrderField: The sorting filter applied to the scheduled snapshot list. Value range: <Sort by creation time of scheduled snapshot. By default, this is sorted by creation time.\n        :type OrderField: str\n        """
        self.AutoSnapshotPolicyIds = None
        self.Filters = None
        self.Limit = None
        self.Offset = None
        self.Order = None
        self.OrderField = None


    def _deserialize(self, params):
        self.AutoSnapshotPolicyIds = params.get("AutoSnapshotPolicyIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.Order = params.get("Order")
        self.OrderField = params.get("OrderField")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAutoSnapshotPoliciesResponse(AbstractModel):
    """DescribeAutoSnapshotPolicies response structure.

    """

    def __init__(self):
        """
        :param TotalCount: The quantity of valid scheduled snapshot policies.\n        :type TotalCount: int\n        :param AutoSnapshotPolicySet: List of scheduled snapshot policies.\n        :type AutoSnapshotPolicySet: list of AutoSnapshotPolicy\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.TotalCount = None
        self.AutoSnapshotPolicySet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("AutoSnapshotPolicySet") is not None:
            self.AutoSnapshotPolicySet = []
            for item in params.get("AutoSnapshotPolicySet"):
                obj = AutoSnapshotPolicy()
                obj._deserialize(item)
                self.AutoSnapshotPolicySet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDiskAssociatedAutoSnapshotPolicyRequest(AbstractModel):
    """DescribeDiskAssociatedAutoSnapshotPolicy request structure.

    """

    def __init__(self):
        """
        :param DiskId: The ID of the queried cloud disk.\n        :type DiskId: str\n        """
        self.DiskId = None


    def _deserialize(self, params):
        self.DiskId = params.get("DiskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDiskAssociatedAutoSnapshotPolicyResponse(AbstractModel):
    """DescribeDiskAssociatedAutoSnapshotPolicy response structure.

    """

    def __init__(self):
        """
        :param TotalCount: The quantity of scheduled snapshots binded to cloud disk.\n        :type TotalCount: int\n        :param AutoSnapshotPolicySet: List of scheduled snapshots bound to cloud disk.\n        :type AutoSnapshotPolicySet: list of AutoSnapshotPolicy\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.TotalCount = None
        self.AutoSnapshotPolicySet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("AutoSnapshotPolicySet") is not None:
            self.AutoSnapshotPolicySet = []
            for item in params.get("AutoSnapshotPolicySet"):
                obj = AutoSnapshotPolicy()
                obj._deserialize(item)
                self.AutoSnapshotPolicySet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDiskConfigQuotaRequest(AbstractModel):
    """DescribeDiskConfigQuota request structure.

    """

    def __init__(self):
        """
        :param InquiryType: Inquiry type. Value range: INQUIRY_CBS_CONFIG: query the configuration list of cloud disks <br><li>INQUIRY_CVM_CONFIG: query the configuration list of cloud disks and instances.\n        :type InquiryType: str\n        :param Zones: Query configuration under one or more [availability zone](https://intl.cloud.tencent.com/document/product/213/15753?from_cn_redirect=1#ZoneInfo).\n        :type Zones: list of str\n        :param DiskChargeType: Billing mode. Value range: <br><li>POSTPAID_BY_HOUR: postpaid.\n        :type DiskChargeType: str\n        :param DiskTypes: Cloud disk media type. Valid values: <br><li>CLOUD_BASIC: HDD cloud disk<br><li>CLOUD_PREMIUM: Premium Cloud Storage<br><li>CLOUD_SSD: SSD<br><li>CLOUD_HSSD: Enhanced SSD\n        :type DiskTypes: list of str\n        :param DiskUsage: The system disk or data disk. Value range: <br><li>SYSTEM_DISK: System disk <br><li>DATA_DISK: Data disk.\n        :type DiskUsage: str\n        :param InstanceFamilies: Filter by the instance model series, such as S1, I1 and M1. For more information, please see [Instance Types](https://intl.cloud.tencent.com/document/product/213/11518?from_cn_redirect=1)\n        :type InstanceFamilies: list of str\n        :param CPU: Instance CPU cores.\n        :type CPU: int\n        :param Memory: Instance memory size.\n        :type Memory: int\n        """
        self.InquiryType = None
        self.Zones = None
        self.DiskChargeType = None
        self.DiskTypes = None
        self.DiskUsage = None
        self.InstanceFamilies = None
        self.CPU = None
        self.Memory = None


    def _deserialize(self, params):
        self.InquiryType = params.get("InquiryType")
        self.Zones = params.get("Zones")
        self.DiskChargeType = params.get("DiskChargeType")
        self.DiskTypes = params.get("DiskTypes")
        self.DiskUsage = params.get("DiskUsage")
        self.InstanceFamilies = params.get("InstanceFamilies")
        self.CPU = params.get("CPU")
        self.Memory = params.get("Memory")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDiskConfigQuotaResponse(AbstractModel):
    """DescribeDiskConfigQuota response structure.

    """

    def __init__(self):
        """
        :param DiskConfigSet: List of cloud disk configurations.\n        :type DiskConfigSet: list of DiskConfig\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.DiskConfigSet = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DiskConfigSet") is not None:
            self.DiskConfigSet = []
            for item in params.get("DiskConfigSet"):
                obj = DiskConfig()
                obj._deserialize(item)
                self.DiskConfigSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDiskOperationLogsRequest(AbstractModel):
    """DescribeDiskOperationLogs request structure.

    """

    def __init__(self):
        """
        :param Filters: Filter conditions. The following conditions are supported:
<li>disk-id - Array of String - Required or not: Yes - Filter by cloud disk ID, with maximum of 10 cloud disk IDs able to be specified per request.\n        :type Filters: list of Filter\n        :param BeginTime: The start time of the operation logs to be queried, for example: '2019-11-22 00:00:00"\n        :type BeginTime: str\n        :param EndTime: The end time of the operation logs to be queried, for example: '2019-11-22 23:59:59"\n        :type EndTime: str\n        """
        self.Filters = None
        self.BeginTime = None
        self.EndTime = None


    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.BeginTime = params.get("BeginTime")
        self.EndTime = params.get("EndTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDiskOperationLogsResponse(AbstractModel):
    """DescribeDiskOperationLogs response structure.

    """

    def __init__(self):
        """
        :param DiskOperationLogSet: List of cloud disk operation logs.\n        :type DiskOperationLogSet: list of DiskOperationLog\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.DiskOperationLogSet = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DiskOperationLogSet") is not None:
            self.DiskOperationLogSet = []
            for item in params.get("DiskOperationLogSet"):
                obj = DiskOperationLog()
                obj._deserialize(item)
                self.DiskOperationLogSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDisksRequest(AbstractModel):
    """DescribeDisks request structure.

    """

    def __init__(self):
        """
        :param DiskIds: Query by one or more cloud disk IDs, such as `disk-11112222`. For the format of this parameter, please see the ids.N section of the API [Introduction](https://intl.cloud.tencent.com/document/product/362/15633?from_cn_redirect=1). This parameter does not support specifying both `DiskIds` and `Filters`.\n        :type DiskIds: list of str\n        :param Filters: Filters. You cannot specify `DiskIds` and `Filters` at the same time. <br><li>disk-usage - Array of String - Optional - Filters by cloud disk type. (SYSTEM_DISK: system disk | DATA_DISK: data disk) <br><li>disk-charge-type - Array of String - Optional - Filters by cloud disk billing method. (POSTPAID_BY_HOUR: pay-as-you-go) <br><li>portable - Array of String- Optional - Filters by whether the cloud disk is elastic or not. (TRUE: elastic | FALSE: non-elastic) <br><li>project-id - Array of Integer - Optional - Filters by the ID of the project to which a cloud disk belongs. <br><li>disk-id - Array of String - Optional - Filters by cloud disk ID, such as `disk-11112222`. <br><li>disk-name - Array of String - Optional - Filters by cloud disk name. <br><li>disk-type - Array of String - Optional - Filters by cloud disk media type (CLOUD_BASIC: HDD cloud disk | CLOUD_PREMIUM: Premium Cloud Storage | CLOUD_SSD: SSD cloud disk.) <br><li>disk-state - Array of String - Optional - Filters by cloud disk state. (UNATTACHED: not mounted | ATTACHING: being mounted | ATTACHED: mounted | DETACHING: being unmounted | EXPANDING: being expanded | ROLLBACKING: being rolled back | TORECYCLE: to be repossessed.) <br><li>instance-id - Array of String - Optional - Filters by the ID of the CVM instance on which a cloud disk is mounted. You can use this parameter to query the cloud disks mounted on specific CVMs. <br><li>zone - Array of String - Optional - Filters by [availability zone](https://intl.cloud.tencent.com/document/product/213/15753?from_cn_redirect=1#ZoneInfo) <br><li>instance-ip-address - Array of String - Optional - Filters by the private or public IP of the CVM on which a cloud disk is mounted. <br><li>instance-name - Array of String - Optional - Filters by the name of the instance on which a cloud disk is mounted. <br><li>tag-key - Array of String - Optional - Filters by tag key. <br><li>tag-value - Array of String - Optional - Filters by tag value. <br><li>tag:tag-key - Array of String - Optional - Filters by tag key-value pair. Please replace `tag-key` with a specific tag key.\n        :type Filters: list of Filter\n        :param Offset: Offset. Default is 0. For more information on `Offset`, please see relevant sections in API [Introduction](https://intl.cloud.tencent.com/document/product/362/15633?from_cn_redirect=1).\n        :type Offset: int\n        :param Limit: Number of results to be returned. Default is 20. Maximum is 100. For more information on `Limit`, please see relevant sections in API [Introduction](https://intl.cloud.tencent.com/document/product/362/15633?from_cn_redirect=1).\n        :type Limit: int\n        :param Order: Outputs the ordering of the cloud disk list. Value range: <br><li>ASC: Ascending order <br><li>DESC: Descending order.\n        :type Order: str\n        :param OrderField: The field by which the cloud disk list is sorted. Value range: <br><li>CREATE_TIME: sorted by the creation time of cloud disks <br><li>DEADLINE: sorted by the expiration time of cloud disks<br>By default, the cloud disk list is sorted by the creation time of cloud disks.\n        :type OrderField: str\n        :param ReturnBindAutoSnapshotPolicy: Whether the ID of the periodic snapshot policy bound to the cloud disk needs to be returned in the cloud disk details. TRUE: return; FALSE: do not return.\n        :type ReturnBindAutoSnapshotPolicy: bool\n        """
        self.DiskIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None
        self.Order = None
        self.OrderField = None
        self.ReturnBindAutoSnapshotPolicy = None


    def _deserialize(self, params):
        self.DiskIds = params.get("DiskIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.Order = params.get("Order")
        self.OrderField = params.get("OrderField")
        self.ReturnBindAutoSnapshotPolicy = params.get("ReturnBindAutoSnapshotPolicy")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDisksResponse(AbstractModel):
    """DescribeDisks response structure.

    """

    def __init__(self):
        """
        :param TotalCount: The quantity of cloud disks meeting the conditions.\n        :type TotalCount: int\n        :param DiskSet: List of cloud disk details.\n        :type DiskSet: list of Disk\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.TotalCount = None
        self.DiskSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("DiskSet") is not None:
            self.DiskSet = []
            for item in params.get("DiskSet"):
                obj = Disk()
                obj._deserialize(item)
                self.DiskSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInstancesDiskNumRequest(AbstractModel):
    """DescribeInstancesDiskNum request structure.

    """

    def __init__(self):
        """
        :param InstanceIds: ID of the CVM instance can be queried via the API [DescribeInstances](https://intl.cloud.tencent.com/document/product/213/15728?from_cn_redirect=1).\n        :type InstanceIds: list of str\n        """
        self.InstanceIds = None


    def _deserialize(self, params):
        self.InstanceIds = params.get("InstanceIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeInstancesDiskNumResponse(AbstractModel):
    """DescribeInstancesDiskNum response structure.

    """

    def __init__(self):
        """
        :param AttachDetail: The quantity of mounted and mountable elastic cloud disks for each cloud virtual machine\n        :type AttachDetail: list of AttachDetail\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.AttachDetail = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("AttachDetail") is not None:
            self.AttachDetail = []
            for item in params.get("AttachDetail"):
                obj = AttachDetail()
                obj._deserialize(item)
                self.AttachDetail.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeSnapshotOperationLogsRequest(AbstractModel):
    """DescribeSnapshotOperationLogs request structure.

    """

    def __init__(self):
        """
        :param Filters: Filter conditions. The following conditions are supported:
<li>snapshot-id - Array of String - Required or not: Yes - Filter by snapshot ID, with maximum of 10 snapshot IDs able to be specified per request.\n        :type Filters: list of Filter\n        :param BeginTime: The start time of the operation logs to be queried, for example: '2019-11-22 00:00:00"\n        :type BeginTime: str\n        :param EndTime: The end time of the operation logs to be queried, for example: '2019-11-22 23:59:59"\n        :type EndTime: str\n        """
        self.Filters = None
        self.BeginTime = None
        self.EndTime = None


    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.BeginTime = params.get("BeginTime")
        self.EndTime = params.get("EndTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSnapshotOperationLogsResponse(AbstractModel):
    """DescribeSnapshotOperationLogs response structure.

    """

    def __init__(self):
        """
        :param SnapshotOperationLogSet: List of snapshot operation logs.\n        :type SnapshotOperationLogSet: list of SnapshotOperationLog\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.SnapshotOperationLogSet = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("SnapshotOperationLogSet") is not None:
            self.SnapshotOperationLogSet = []
            for item in params.get("SnapshotOperationLogSet"):
                obj = SnapshotOperationLog()
                obj._deserialize(item)
                self.SnapshotOperationLogSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeSnapshotSharePermissionRequest(AbstractModel):
    """DescribeSnapshotSharePermission request structure.

    """

    def __init__(self):
        """
        :param SnapshotId: The ID of the snapshot to be queried. You can obtain this by using [DescribeSnapshots](https://intl.cloud.tencent.com/document/api/362/15647?from_cn_redirect=1).\n        :type SnapshotId: str\n        """
        self.SnapshotId = None


    def _deserialize(self, params):
        self.SnapshotId = params.get("SnapshotId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSnapshotSharePermissionResponse(AbstractModel):
    """DescribeSnapshotSharePermission response structure.

    """

    def __init__(self):
        """
        :param SharePermissionSet: The set of snapshot sharing information\n        :type SharePermissionSet: list of SharePermission\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.SharePermissionSet = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("SharePermissionSet") is not None:
            self.SharePermissionSet = []
            for item in params.get("SharePermissionSet"):
                obj = SharePermission()
                obj._deserialize(item)
                self.SharePermissionSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeSnapshotsRequest(AbstractModel):
    """DescribeSnapshots request structure.

    """

    def __init__(self):
        """
        :param SnapshotIds: List of snapshot IDs to be queried. The parameter does not support specifying both `SnapshotIds` and `Filters`.\n        :type SnapshotIds: list of str\n        :param Filters: Filters. It cannot be specified together with `SnapshotIds`.<br><li>snapshot-id - Array of String - Optional - Filters by snapshot ID, such as `snap-11112222`.<br><li>snapshot-name - Array of String - Optional - Filters by snapshot name. <br><li>snapshot-state - Array of String - Optional - Filters by snapshot state (NORMAL: normal | CREATING: creating | ROLLBACKING: rolling back). <br><li>disk-usage - Array of String - Optional - Filters by the type of the cloud disk from which a snapshot is created (SYSTEM_DISK: system disk | DATA_DISK: data disk).<br><li>project-id - Array of String - Optional - Filters by the ID of the project to which a cloud disk belongs. <br><li>disk-id - Array of String - Optional - Filters by the ID of the cloud disk from which a snapshot is created.<br><li>zone - Array of String - Optional - Filters by [availability zone](https://intl.cloud.tencent.com/document/product/213/15753?from_cn_redirect=1#ZoneInfo).<br><li>encrypt - Array of String - Optional - Filters by whether a snapshot is created from an encrypted cloud disk. (TRUE: a snapshot of an encrypted cloud disk | FALSE: not a snapshot of an encrypted cloud disk.)
<li>snapshot-type- Array of String - Optional - Filters by the snapshot type specified in `snapshot-type`.
(SHARED_SNAPSHOT: a shared snapshot | PRIVATE_SNAPSHOT: a private snapshot.)\n        :type Filters: list of Filter\n        :param Offset: Offset. Default is 0. For more information on `Offset`, please see relevant sections in API [Introduction](https://intl.cloud.tencent.com/document/product/362/15633?from_cn_redirect=1).\n        :type Offset: int\n        :param Limit: Number of results to be returned. Default is 20. Maximum is 100. For more information on `Limit`, please see relevant sections in API [Introduction](https://intl.cloud.tencent.com/document/product/362/15633?from_cn_redirect=1).\n        :type Limit: int\n        :param Order: Outputs the ordering of the cloud disk list. Value range: <br><li>ASC: Ascending order <br><li>DESC: Descending order.\n        :type Order: str\n        :param OrderField: The field by which the snapshot list is sorted. Value range: <br><li>CREATE_TIME: sorted by the creation time of the snapshots <br>By default, the snapshot list is sorted by the creation time of snapshots.\n        :type OrderField: str\n        """
        self.SnapshotIds = None
        self.Filters = None
        self.Offset = None
        self.Limit = None
        self.Order = None
        self.OrderField = None


    def _deserialize(self, params):
        self.SnapshotIds = params.get("SnapshotIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.Order = params.get("Order")
        self.OrderField = params.get("OrderField")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSnapshotsResponse(AbstractModel):
    """DescribeSnapshots response structure.

    """

    def __init__(self):
        """
        :param TotalCount: Number of snapshots.\n        :type TotalCount: int\n        :param SnapshotSet: List of snapshot details.\n        :type SnapshotSet: list of Snapshot\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.TotalCount = None
        self.SnapshotSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("SnapshotSet") is not None:
            self.SnapshotSet = []
            for item in params.get("SnapshotSet"):
                obj = Snapshot()
                obj._deserialize(item)
                self.SnapshotSet.append(obj)
        self.RequestId = params.get("RequestId")


class DetachDisksRequest(AbstractModel):
    """DetachDisks request structure.

    """

    def __init__(self):
        """
        :param DiskIds: IDs of the cloud disks to be unmounted, which can be queried via the [DescribeDisks](https://intl.cloud.tencent.com/document/product/362/16315?from_cn_redirect=1) API. Up to 10 elastic cloud disks can be unmounted in a single request.\n        :type DiskIds: list of str\n        :param InstanceId: Indicates the CVM from which you want to unmount the disks. This parameter is only available for shared cloud disks.\n        :type InstanceId: str\n        """
        self.DiskIds = None
        self.InstanceId = None


    def _deserialize(self, params):
        self.DiskIds = params.get("DiskIds")
        self.InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DetachDisksResponse(AbstractModel):
    """DetachDisks response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class Disk(AbstractModel):
    """The details of a cloud disk

    """

    def __init__(self):
        """
        :param DeleteWithInstance: Whether the cloud disk terminates along with the instance mounted to it. <br><li>true: Cloud disk will also be terminated when instance terminates, so only hourly postpaid cloud disk are supported.<br><li>false: Cloud disk does not terminate when instance terminates.
Note: This field may return null, indicating that no valid value was found.\n        :type DeleteWithInstance: bool\n        :param RenewFlag: Auto renewal flag. Supported values:<br><li>NOTIFY_AND_AUTO_RENEW: Notify expiry and renew automatically<br><li>NOTIFY_AND_MANUAL_RENEW: Notify expiry but not renew automatically<br><li>DISABLE_NOTIFY_AND_MANUAL_RENEW: Neither notify expiry nor renew automatically.
Note: This field may return null, indicating that no valid value was found.\n        :type RenewFlag: str\n        :param DiskType: Cloud disk media type. Valid values: <br><li>CLOUD_BASIC: HDD cloud disk<br><li>CLOUD_PREMIUM: Premium Cloud Storage<br><li>CLOUD_SSD: SSD<br><li>CLOUD_HSSD: Enhanced SSD<br><li>CLOUD_TSSD: Tremendous SSD\n        :type DiskType: str\n        :param DiskState: The state of the cloud disk. Value range: <br><li>UNATTACHED: Not mounted <br><li>ATTACHING: Mounting <br><li>ATTACHED: Mounted <br><li>DETACHING: Un-mounting <br><li>EXPANDING: Expanding <br><li>ROLLBACKING: Rolling back <br><li>TORECYCE: Pending recycling. <br><li>DUMPING: Copying the hard drive.\n        :type DiskState: str\n        :param SnapshotCount: The total number of snapshots of the cloud disk.\n        :type SnapshotCount: int\n        :param AutoRenewFlagError: Cloud disk already mounted to CVM, and both CVM and cloud disk use monthly subscription.<br><li>true: CVM has auto-renewal flag set up, but cloud disk does not.<br><li>false: Cloud disk auto-renewal flag set up normally.
Note: This field may return null, indicating that no valid value was found.\n        :type AutoRenewFlagError: bool\n        :param Rollbacking: Whether the cloud disk is in the status of snapshot rollback. Value range: <br><li>false: No <br><li>true: Yes\n        :type Rollbacking: bool\n        :param InstanceIdList: For non-shareable cloud disks, this parameter is null. For shareable cloud disks, this parameters indicates this cloud disk's Instance IDs currently mounted to the CVM.\n        :type InstanceIdList: list of str\n        :param Encrypt: Whether the cloud disk is encrypted. Value range: <br><li>false: Not encrypted <br><li>true: Encrypted.\n        :type Encrypt: bool\n        :param DiskName: Cloud disk name.\n        :type DiskName: str\n        :param BackupDisk: Specifies whether to create a snapshot when the cloud disk is terminated due to overdue payment or expiration. `true`: create snapshot; `false`: do not create snapshot.\n        :type BackupDisk: bool\n        :param Tags: The tag bound to the cloud disk. The value Null is used when no tag is bound to the cloud disk.
Note: This field may return null, indicating that no valid value was found.\n        :type Tags: list of Tag\n        :param InstanceId: ID of the CVM to which the cloud disk is mounted.\n        :type InstanceId: str\n        :param AttachMode: Cloud disk mount method. Valid values: <br><li>PF: mount as a PF (Physical Function)<br><li>VF: mount as a VF (Virtual Function)
Note: this field may return `null`, indicating that no valid value is obtained.\n        :type AttachMode: str\n        :param AutoSnapshotPolicyIds: ID of the periodic snapshot associated to the cloud disk. This parameter is returned only if the value of parameter ReturnBindAutoSnapshotPolicy is TRUE when the API DescribeDisks is called.
Note: This field may return null, indicating that no valid value was found.\n        :type AutoSnapshotPolicyIds: list of str\n        :param ThroughputPerformance: Extra performance for a cloud disk, in MB/sec.
Note: this field may return `null`, indicating that no valid values can be obtained.\n        :type ThroughputPerformance: int\n        :param Migrating: Whether cloud disk is in process of type change. Value range: <br><li>false: Cloud disk not in process of type change. <br><li>true: Cloud disk type change has been launched, and migration is in process.
Note: This field may return null, indicating that no valid value was found.\n        :type Migrating: bool\n        :param DiskId: Cloud disk ID.\n        :type DiskId: str\n        :param SnapshotSize: The total capacity of the snapshots of the cloud disk. Unit: MB.\n        :type SnapshotSize: int\n        :param Placement: Location of the cloud disk.\n        :type Placement: :class:`tencentcloud.cbs.v20170312.models.Placement`\n        :param IsReturnable: Determines whether or not prepaid cloud disk supports active return. <br><li>true: Active return supported.<br><li>false: Active return not supported.
Note: This field may return null, indicating that no valid value was found.\n        :type IsReturnable: bool\n        :param DeadlineTime: Expiration time of the cloud disk.\n        :type DeadlineTime: str\n        :param Attached: Whether the cloud disk is mounted to the CVM. Value range: <br><li>false: Unmounted <br><li>true: Mounted.\n        :type Attached: bool\n        :param DiskSize: Cloud disk size (in GB).\n        :type DiskSize: int\n        :param MigratePercent: Migration progress of cloud disk type change, from 0 to 100.
Note: This field may return null, indicating that no valid value was found.\n        :type MigratePercent: int\n        :param DiskUsage: Cloud disk type. Value range:<br><li>SYSTEM_DISK: System disk <br><li>DATA_DISK: Data disk.\n        :type DiskUsage: str\n        :param DiskChargeType: Billing method. Value range: <br><li>PREPAID: Prepaid, that is, monthly subscription<br><li>POSTPAID_BY_HOUR: Postpaid, that is, pay as you go.\n        :type DiskChargeType: str\n        :param Portable: Whether it is an elastic cloud disk. false: Non-elastic cloud disk; true: Elastic cloud disk.\n        :type Portable: bool\n        :param SnapshotAbility: Whether the cloud disk has the capability to create snapshots. Value range: <br><li>false: Cannot create snapshots. true: Can create snapshots.\n        :type SnapshotAbility: bool\n        :param DeadlineError: This field is only applicable when the instance is already mounted to the cloud disk, and both the instance and the cloud disk use monthly subscription. <br><li>true: Expiration time of cloud disk is earlier than that of the instance.<br><li>false:Expiration time of cloud disk is later than that of the instance.
Note: This field may return null, indicating that no valid value was found.\n        :type DeadlineError: bool\n        :param RollbackPercent: Rollback progress of a cloud disk snapshot.\n        :type RollbackPercent: int\n        :param DifferDaysOfDeadline: Number of days from current time until disk expiration (only applicable for prepaid disks).
Note: This field may return null, indicating that no valid value was found.\n        :type DifferDaysOfDeadline: int\n        :param ReturnFailCode: In circumstances where the prepaid cloud disk does not support active return, this parameter indicates the reason that return is not supported. Value range: <br><li>1: The cloud disk has already been returned. <br><li>2: The cloud disk has already expired. <br><li>3: The cloud disk does not support return. <br><li> 8: The limit on the number of returns is exceeded.
Note: This field may return null, indicating that no valid value was found.\n        :type ReturnFailCode: int\n        :param Shareable: Whether or not cloud disk is shareable cloud disk.\n        :type Shareable: bool\n        :param CreateTime: Creation time of the cloud disk.\n        :type CreateTime: str\n        """
        self.DeleteWithInstance = None
        self.RenewFlag = None
        self.DiskType = None
        self.DiskState = None
        self.SnapshotCount = None
        self.AutoRenewFlagError = None
        self.Rollbacking = None
        self.InstanceIdList = None
        self.Encrypt = None
        self.DiskName = None
        self.BackupDisk = None
        self.Tags = None
        self.InstanceId = None
        self.AttachMode = None
        self.AutoSnapshotPolicyIds = None
        self.ThroughputPerformance = None
        self.Migrating = None
        self.DiskId = None
        self.SnapshotSize = None
        self.Placement = None
        self.IsReturnable = None
        self.DeadlineTime = None
        self.Attached = None
        self.DiskSize = None
        self.MigratePercent = None
        self.DiskUsage = None
        self.DiskChargeType = None
        self.Portable = None
        self.SnapshotAbility = None
        self.DeadlineError = None
        self.RollbackPercent = None
        self.DifferDaysOfDeadline = None
        self.ReturnFailCode = None
        self.Shareable = None
        self.CreateTime = None


    def _deserialize(self, params):
        self.DeleteWithInstance = params.get("DeleteWithInstance")
        self.RenewFlag = params.get("RenewFlag")
        self.DiskType = params.get("DiskType")
        self.DiskState = params.get("DiskState")
        self.SnapshotCount = params.get("SnapshotCount")
        self.AutoRenewFlagError = params.get("AutoRenewFlagError")
        self.Rollbacking = params.get("Rollbacking")
        self.InstanceIdList = params.get("InstanceIdList")
        self.Encrypt = params.get("Encrypt")
        self.DiskName = params.get("DiskName")
        self.BackupDisk = params.get("BackupDisk")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.InstanceId = params.get("InstanceId")
        self.AttachMode = params.get("AttachMode")
        self.AutoSnapshotPolicyIds = params.get("AutoSnapshotPolicyIds")
        self.ThroughputPerformance = params.get("ThroughputPerformance")
        self.Migrating = params.get("Migrating")
        self.DiskId = params.get("DiskId")
        self.SnapshotSize = params.get("SnapshotSize")
        if params.get("Placement") is not None:
            self.Placement = Placement()
            self.Placement._deserialize(params.get("Placement"))
        self.IsReturnable = params.get("IsReturnable")
        self.DeadlineTime = params.get("DeadlineTime")
        self.Attached = params.get("Attached")
        self.DiskSize = params.get("DiskSize")
        self.MigratePercent = params.get("MigratePercent")
        self.DiskUsage = params.get("DiskUsage")
        self.DiskChargeType = params.get("DiskChargeType")
        self.Portable = params.get("Portable")
        self.SnapshotAbility = params.get("SnapshotAbility")
        self.DeadlineError = params.get("DeadlineError")
        self.RollbackPercent = params.get("RollbackPercent")
        self.DifferDaysOfDeadline = params.get("DifferDaysOfDeadline")
        self.ReturnFailCode = params.get("ReturnFailCode")
        self.Shareable = params.get("Shareable")
        self.CreateTime = params.get("CreateTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DiskChargePrepaid(AbstractModel):
    """The billing method of an instance

    """

    def __init__(self):
        """
        :param Period: The purchased usage period of a cloud disk (in months). Value range: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 24, 36.\n        :type Period: int\n        :param RenewFlag: Auto Renewal flag. Value range: <br><li>NOTIFY_AND_AUTO_RENEW: Notify expiry and renew automatically <br><li>NOTIFY_AND_MANUAL_RENEW: Notify expiry but do not renew automatically <br><li>DISABLE_NOTIFY_AND_MANUAL_RENEW: Neither notify expiry nor renew automatically <br><br>Default value range: NOTIFY_AND_MANUAL_RENEW: Notify expiry but do not renew automatically.\n        :type RenewFlag: str\n        :param CurInstanceDeadline: This parameter is used when you align the expiration time of the cloud disk with that of the mounted server. It is the current expiration time of the server. In this case, the Period passed represents the renewal period of the server, and the cloud disk will be automatically renewed in alignment with the expiration time of the renewed server. Example value: 2018-03-30 20:15:03.\n        :type CurInstanceDeadline: str\n        """
        self.Period = None
        self.RenewFlag = None
        self.CurInstanceDeadline = None


    def _deserialize(self, params):
        self.Period = params.get("Period")
        self.RenewFlag = params.get("RenewFlag")
        self.CurInstanceDeadline = params.get("CurInstanceDeadline")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DiskConfig(AbstractModel):
    """Cloud disk configuration.

    """

    def __init__(self):
        """
        :param Available: Whether the configuration is available.\n        :type Available: bool\n        :param DiskType: Type of cloud disk medium. Value range: <br><li>CLOUD_BASIC: Ordinary cloud disk <br><li>CLOUD_PREMIUM: Premium cloud storage <br><li>CLOUD_SSD: SSD cloud disk.\n        :type DiskType: str\n        :param DiskUsage: Cloud disk type. Value range: <br><li>SYSTEM_DISK: System disk <br><li>DATA_DISK: Data disk.\n        :type DiskUsage: str\n        :param DiskChargeType: Billing method. Value range: <br><li>PREPAID: Prepaid, that is, monthly subscription<br><li>POSTPAID_BY_HOUR: Postpaid, that is, pay as you go.\n        :type DiskChargeType: str\n        :param MaxDiskSize: The maximum configurable cloud disk size (in GB).\n        :type MaxDiskSize: int\n        :param MinDiskSize: The minimum configurable cloud disk size (in GB).\n        :type MinDiskSize: int\n        :param Zone: The [Availability Region](https://intl.cloud.tencent.com/document/product/213/15753?from_cn_redirect=1#ZoneInfo) of the cloud drive.\n        :type Zone: str\n        :param DeviceClass: Instance model.
Note: This field may return null, indicating that no valid value was found.\n        :type DeviceClass: str\n        :param InstanceFamily: Instance model series. For more information, please see [Instance Models](https://intl.cloud.tencent.com/document/product/213/11518?from_cn_redirect=1)
Note: This field may return null, indicating that no valid value was found.\n        :type InstanceFamily: str\n        """
        self.Available = None
        self.DiskType = None
        self.DiskUsage = None
        self.DiskChargeType = None
        self.MaxDiskSize = None
        self.MinDiskSize = None
        self.Zone = None
        self.DeviceClass = None
        self.InstanceFamily = None


    def _deserialize(self, params):
        self.Available = params.get("Available")
        self.DiskType = params.get("DiskType")
        self.DiskUsage = params.get("DiskUsage")
        self.DiskChargeType = params.get("DiskChargeType")
        self.MaxDiskSize = params.get("MaxDiskSize")
        self.MinDiskSize = params.get("MinDiskSize")
        self.Zone = params.get("Zone")
        self.DeviceClass = params.get("DeviceClass")
        self.InstanceFamily = params.get("InstanceFamily")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DiskOperationLog(AbstractModel):
    """The operation log of the cloud disk.

    """

    def __init__(self):
        """
        :param Operator: UIN of operator.\n        :type Operator: str\n        :param Operation: Operation type. Value range:
CBS_OPERATION_ATTACH: Mount cloud disk
CBS_OPERATION_DETACH: Unmount cloud disk
CBS_OPERATION_RENEW: Renew
CBS_OPERATION_EXPAND: Expand
CBS_OPERATION_CREATE: Create
CBS_OPERATION_ISOLATE: Isolate
CBS_OPERATION_MODIFY: Modify cloud disk attributes
ASP_OPERATION_BIND: Associate scheduled snapshot policy
ASP_OPERATION_UNBIND: Cancel associated scheduled snapshot policy\n        :type Operation: str\n        :param DiskId: Cloud disk ID of operation.\n        :type DiskId: str\n        :param OperationState: Status of operation. Value range:
SUCCESS: Operation successful 
FAILED: Operation failed 
PROCESSING: Operation in process\n        :type OperationState: str\n        :param StartTime: Start time\n        :type StartTime: str\n        :param EndTime: End time\n        :type EndTime: str\n        """
        self.Operator = None
        self.Operation = None
        self.DiskId = None
        self.OperationState = None
        self.StartTime = None
        self.EndTime = None


    def _deserialize(self, params):
        self.Operator = params.get("Operator")
        self.Operation = params.get("Operation")
        self.DiskId = params.get("DiskId")
        self.OperationState = params.get("OperationState")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Filter(AbstractModel):
    """Key-value pair filters for conditional filtering queries.

    """

    def __init__(self):
        """
        :param Name: Name of filter key.\n        :type Name: str\n        :param Values: One or more filter values.\n        :type Values: list of str\n        """
        self.Name = None
        self.Values = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Values = params.get("Values")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GetSnapOverviewRequest(AbstractModel):
    """GetSnapOverview request structure.

    """


class GetSnapOverviewResponse(AbstractModel):
    """GetSnapOverview response structure.

    """

    def __init__(self):
        """
        :param TotalSize: The total snapshot size of the user\n        :type TotalSize: float\n        :param RealTradeSize: The total billed snapshot size of the user\n        :type RealTradeSize: float\n        :param FreeQuota: Free tier of snapshot\n        :type FreeQuota: float\n        :param TotalNums: Total number of snapshots\n        :type TotalNums: int\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.TotalSize = None
        self.RealTradeSize = None
        self.FreeQuota = None
        self.TotalNums = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalSize = params.get("TotalSize")
        self.RealTradeSize = params.get("RealTradeSize")
        self.FreeQuota = params.get("FreeQuota")
        self.TotalNums = params.get("TotalNums")
        self.RequestId = params.get("RequestId")


class Image(AbstractModel):
    """Image

    """

    def __init__(self):
        """
        :param ImageId: Image instance ID.\n        :type ImageId: str\n        :param ImageName: Image name.\n        :type ImageName: str\n        """
        self.ImageId = None
        self.ImageName = None


    def _deserialize(self, params):
        self.ImageId = params.get("ImageId")
        self.ImageName = params.get("ImageName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InquirePriceModifyDiskExtraPerformanceRequest(AbstractModel):
    """InquirePriceModifyDiskExtraPerformance request structure.

    """

    def __init__(self):
        """
        :param DiskId: Cloud disk ID, which can be queried via the [DescribeDisks](https://intl.cloud.tencent.com/document/product/362/16315?from_cn_redirect=1) API.\n        :type DiskId: str\n        :param ThroughputPerformance: The extra throughput to purchase, in MB/s\n        :type ThroughputPerformance: int\n        """
        self.DiskId = None
        self.ThroughputPerformance = None


    def _deserialize(self, params):
        self.DiskId = params.get("DiskId")
        self.ThroughputPerformance = params.get("ThroughputPerformance")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InquirePriceModifyDiskExtraPerformanceResponse(AbstractModel):
    """InquirePriceModifyDiskExtraPerformance response structure.

    """

    def __init__(self):
        """
        :param DiskPrice: Price for purchasing the extra performance\n        :type DiskPrice: :class:`tencentcloud.cbs.v20170312.models.Price`\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.DiskPrice = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DiskPrice") is not None:
            self.DiskPrice = Price()
            self.DiskPrice._deserialize(params.get("DiskPrice"))
        self.RequestId = params.get("RequestId")


class InquiryPriceCreateDisksRequest(AbstractModel):
    """InquiryPriceCreateDisks request structure.

    """

    def __init__(self):
        """
        :param DiskType: Cloud disk media type. Valid values: <br><li>CLOUD_BASIC: HDD cloud disk<br><li>CLOUD_PREMIUM: Premium Cloud Storage<br><li>CLOUD_SSD: SSD<br><li>CLOUD_HSSD: Enhanced SSD<br><li>CLOUD_TSSD: Tremendous SSD.\n        :type DiskType: str\n        :param DiskSize: Cloud disk size (in GB). For the value range of the cloud disk sizes, see cloud disk [Product Types](https://intl.cloud.tencent.com/document/product/362/2353?from_cn_redirect=1).\n        :type DiskSize: int\n        :param DiskChargeType: Cloud disk billing method. <br><li>POSTPAID_BY_HOUR: Pay-as-you-go on an hourly basis\n        :type DiskChargeType: str\n        :param DiskChargePrepaid: Relevant parameter settings for the prepaid mode (i.e., monthly subscription). The monthly subscription cloud disk purchase attributes such as usage period and whether or not auto-renewal is set up can be specified using this parameter. <br>This parameter is required when creating a prepaid cloud disk. This parameter is not required when creating an hourly postpaid cloud disk.\n        :type DiskChargePrepaid: :class:`tencentcloud.cbs.v20170312.models.DiskChargePrepaid`\n        :param DiskCount: Quantity of cloud disks purchased. If left empty, default is 1.\n        :type DiskCount: int\n        :param ProjectId: ID of project the cloud disk belongs to.\n        :type ProjectId: int\n        :param ThroughputPerformance: Extra performance (in MB/sec) purchased for a cloud disk.<br>This parameter is only valid for Enhanced SSD (CLOUD_HSSD) and Tremendous SSD (CLOUD_TSSD).\n        :type ThroughputPerformance: int\n        """
        self.DiskType = None
        self.DiskSize = None
        self.DiskChargeType = None
        self.DiskChargePrepaid = None
        self.DiskCount = None
        self.ProjectId = None
        self.ThroughputPerformance = None


    def _deserialize(self, params):
        self.DiskType = params.get("DiskType")
        self.DiskSize = params.get("DiskSize")
        self.DiskChargeType = params.get("DiskChargeType")
        if params.get("DiskChargePrepaid") is not None:
            self.DiskChargePrepaid = DiskChargePrepaid()
            self.DiskChargePrepaid._deserialize(params.get("DiskChargePrepaid"))
        self.DiskCount = params.get("DiskCount")
        self.ProjectId = params.get("ProjectId")
        self.ThroughputPerformance = params.get("ThroughputPerformance")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InquiryPriceCreateDisksResponse(AbstractModel):
    """InquiryPriceCreateDisks response structure.

    """

    def __init__(self):
        """
        :param DiskPrice: Describes the price of purchasing new cloud disk.\n        :type DiskPrice: :class:`tencentcloud.cbs.v20170312.models.Price`\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.DiskPrice = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DiskPrice") is not None:
            self.DiskPrice = Price()
            self.DiskPrice._deserialize(params.get("DiskPrice"))
        self.RequestId = params.get("RequestId")


class InquiryPriceResizeDiskRequest(AbstractModel):
    """InquiryPriceResizeDisk request structure.

    """

    def __init__(self):
        """
        :param DiskId: ID of the cloud disk, which can be queried via the API [DescribeDisks](https://intl.cloud.tencent.com/document/product/362/16315?from_cn_redirect=1).\n        :type DiskId: str\n        :param DiskSize: Cloud disk size after scale out (in GB). This cannot be smaller than the current size of the cloud disk. For the value range of the cloud disk sizes, see cloud disk [Product Types](https://intl.cloud.tencent.com/document/product/362/2353?from_cn_redirect=1).\n        :type DiskSize: int\n        :param ProjectId: ID of project the cloud disk belongs to. If selected, it can only be used for authentication.\n        :type ProjectId: int\n        """
        self.DiskId = None
        self.DiskSize = None
        self.ProjectId = None


    def _deserialize(self, params):
        self.DiskId = params.get("DiskId")
        self.DiskSize = params.get("DiskSize")
        self.ProjectId = params.get("ProjectId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InquiryPriceResizeDiskResponse(AbstractModel):
    """InquiryPriceResizeDisk response structure.

    """

    def __init__(self):
        """
        :param DiskPrice: Describes the price of expanding the cloud disk.\n        :type DiskPrice: :class:`tencentcloud.cbs.v20170312.models.PrepayPrice`\n        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.DiskPrice = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DiskPrice") is not None:
            self.DiskPrice = PrepayPrice()
            self.DiskPrice._deserialize(params.get("DiskPrice"))
        self.RequestId = params.get("RequestId")


class ModifyAutoSnapshotPolicyAttributeRequest(AbstractModel):
    """ModifyAutoSnapshotPolicyAttribute request structure.

    """

    def __init__(self):
        """
        :param AutoSnapshotPolicyId: Scheduled snapshot policy ID.\n        :type AutoSnapshotPolicyId: str\n        :param Policy: The policy for executing the scheduled snapshot.\n        :type Policy: list of Policy\n        :param AutoSnapshotPolicyName: The name of the scheduled snapshot policy to be created. If it is left empty, the default is 'Not named'. The maximum length cannot exceed 60 bytes.\n        :type AutoSnapshotPolicyName: str\n        :param IsActivated: Whether or not the scheduled snapshot policy is activated. FALSE: Not activated. TRUE: Activated. The default value is TRUE.\n        :type IsActivated: bool\n        :param IsPermanent: Whether the snapshot created by this scheduled snapshot policy is retained permanently. FALSE: Not retained permanently. TRUE: Retained permanently. The default value is FALSE.\n        :type IsPermanent: bool\n        :param RetentionDays: The number of days for which snapshots created by this policy are retained. This parameter cannot clash with `IsPermanent`, which is, if the scheduled snapshot policy is configured to retain permanently, `RetentionDays` must be 0.\n        :type RetentionDays: int\n        """
        self.AutoSnapshotPolicyId = None
        self.Policy = None
        self.AutoSnapshotPolicyName = None
        self.IsActivated = None
        self.IsPermanent = None
        self.RetentionDays = None


    def _deserialize(self, params):
        self.AutoSnapshotPolicyId = params.get("AutoSnapshotPolicyId")
        if params.get("Policy") is not None:
            self.Policy = []
            for item in params.get("Policy"):
                obj = Policy()
                obj._deserialize(item)
                self.Policy.append(obj)
        self.AutoSnapshotPolicyName = params.get("AutoSnapshotPolicyName")
        self.IsActivated = params.get("IsActivated")
        self.IsPermanent = params.get("IsPermanent")
        self.RetentionDays = params.get("RetentionDays")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyAutoSnapshotPolicyAttributeResponse(AbstractModel):
    """ModifyAutoSnapshotPolicyAttribute response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDiskAttributesRequest(AbstractModel):
    """ModifyDiskAttributes request structure.

    """

    def __init__(self):
        """
        :param DiskIds: IDs of one or more cloud disks to be operated. If multiple cloud disk IDs are selected, it only supports modifying all cloud disks with the same attributes.\n        :type DiskIds: list of str\n        :param ProjectId: The new project ID of the cloud disk. Only the project ID of elastic cloud disk can be modified. The available projects and their IDs can be queried via the API [DescribeProject](https://intl.cloud.tencent.com/document/api/378/4400?from_cn_redirect=1).\n        :type ProjectId: int\n        :param DiskName: Name of new cloud disk.\n        :type DiskName: str\n        :param Portable: Whether it is an elastic cloud disk. FALSE: non-elastic cloud disk; TRUE: elastic cloud disk. You can only modify non-elastic cloud disks to elastic cloud disks.\n        :type Portable: bool\n        :param DeleteWithInstance: Whether the cloud disk is terminated with the CVM after it has been successfully mounted. `TRUE` indicates that it is terminated with the CVM. `FALSE` indicates that it is not terminated with the CVM. This is only supported for cloud disks and data disks that are pay-as-you-go.\n        :type DeleteWithInstance: bool\n        :param DiskType: When changing the type of a cloud disk, this parameter can be passed to indicate the desired cloud disk type. Value range: <br><li>CLOUD_PREMIUM: Premium cloud storage.  <br><li>CLOUD_SSD: SSD cloud disk. <br>Currently, batch operations are not supported for changing type. That is, when `DiskType` is passed, only one cloud disk can be passed through `DiskIds`. <br>When the cloud disk type is changed, the changing of other attributes is not supported concurrently.\n        :type DiskType: str\n        """
        self.DiskIds = None
        self.ProjectId = None
        self.DiskName = None
        self.Portable = None
        self.DeleteWithInstance = None
        self.DiskType = None


    def _deserialize(self, params):
        self.DiskIds = params.get("DiskIds")
        self.ProjectId = params.get("ProjectId")
        self.DiskName = params.get("DiskName")
        self.Portable = params.get("Portable")
        self.DeleteWithInstance = params.get("DeleteWithInstance")
        self.DiskType = params.get("DiskType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDiskAttributesResponse(AbstractModel):
    """ModifyDiskAttributes response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDiskExtraPerformanceRequest(AbstractModel):
    """ModifyDiskExtraPerformance request structure.

    """

    def __init__(self):
        """
        :param DiskId: ID of the cloud disk to create a snapshot, which can be obtained via the [DescribeDisks](https://intl.cloud.tencent.com/document/product/362/16315?from_cn_redirect=1) API.\n        :type DiskId: str\n        :param ThroughputPerformance: The extra throughput to purchase, in MB/s\n        :type ThroughputPerformance: int\n        """
        self.DiskId = None
        self.ThroughputPerformance = None


    def _deserialize(self, params):
        self.DiskId = params.get("DiskId")
        self.ThroughputPerformance = params.get("ThroughputPerformance")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDiskExtraPerformanceResponse(AbstractModel):
    """ModifyDiskExtraPerformance response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifySnapshotAttributeRequest(AbstractModel):
    """ModifySnapshotAttribute request structure.

    """

    def __init__(self):
        """
        :param SnapshotId: Snapshot ID, which can be queried via [DescribeSnapshots](https://intl.cloud.tencent.com/document/product/362/15647?from_cn_redirect=1).\n        :type SnapshotId: str\n        :param SnapshotName: Name of new snapshot. Maximum length is 60 bytes.\n        :type SnapshotName: str\n        :param IsPermanent: Snapshot retention mode. Valid values: `FALSE`: non-permanent retention; `TRUE`: permanent retention.\n        :type IsPermanent: bool\n        :param Deadline: Expiration time of the snapshot. Setting this parameter will set the snapshot retention mode to `FALSE` (non-permanent retention) and the snapshot will be automatically deleted upon expiration.\n        :type Deadline: str\n        """
        self.SnapshotId = None
        self.SnapshotName = None
        self.IsPermanent = None
        self.Deadline = None


    def _deserialize(self, params):
        self.SnapshotId = params.get("SnapshotId")
        self.SnapshotName = params.get("SnapshotName")
        self.IsPermanent = params.get("IsPermanent")
        self.Deadline = params.get("Deadline")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifySnapshotAttributeResponse(AbstractModel):
    """ModifySnapshotAttribute response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifySnapshotsSharePermissionRequest(AbstractModel):
    """ModifySnapshotsSharePermission request structure.

    """

    def __init__(self):
        """
        :param AccountIds: List of account IDs with which a snapshot is shared. For the format of array-type parameters, see [API Introduction](https://intl.cloud.tencent.com/document/api/213/568?from_cn_redirect=1). You can find the account ID in [Account Information](https://console.cloud.tencent.com/developer).\n        :type AccountIds: list of str\n        :param Permission: Operations. Valid values: `SHARE`, sharing an image; `CANCEL`, cancelling the sharing of an image.\n        :type Permission: str\n        :param SnapshotIds: The ID of the snapshot. You can obtain this by using [DescribeSnapshots](https://intl.cloud.tencent.com/document/api/362/15647?from_cn_redirect=1).\n        :type SnapshotIds: list of str\n        """
        self.AccountIds = None
        self.Permission = None
        self.SnapshotIds = None


    def _deserialize(self, params):
        self.AccountIds = params.get("AccountIds")
        self.Permission = params.get("Permission")
        self.SnapshotIds = params.get("SnapshotIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifySnapshotsSharePermissionResponse(AbstractModel):
    """ModifySnapshotsSharePermission response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class Placement(AbstractModel):
    """This describes the abstract location of the instance, including the availability zone in which it is located, the projects to which it belongs, and the ID and name of the dedicated clusters to which it belongs.

    """

    def __init__(self):
        """
        :param Zone: The ID of the [Availability Zone](https://intl.cloud.tencent.com/document/product/213/15753?from_cn_redirect=1#ZoneInfo) to which the cloud disk belongs. This parameter can be obtained from the Zone field in the returned values of [DescribeZones](https://intl.cloud.tencent.com/document/product/213/15707?from_cn_redirect=1).\n        :type Zone: str\n        :param CageId: Cage ID. When it is an input parameter, the specified CageID resource is operated, and it can be left blank. When it is an output parameter, it is the ID of the cage the resource belongs to, and it can be left blank.
Note: This field may return null, indicating that no valid value was found.\n        :type CageId: str\n        :param ProjectId: ID of the project to which the instance belongs. This parameter can be obtained from the projectId field in the returned values of [DescribeProject](https://intl.cloud.tencent.com/document/api/378/4400?from_cn_redirect=1). If this is left empty, default project is used.\n        :type ProjectId: int\n        :param CdcName: Dedicated cluster name. When it is an input parameter, it is ignored.  When it is an output parameter, it is the name of the dedicated cluster the cloud disk belongs to, and it can be left blank.
Note: This field may return null, indicating that no valid value was found.\n        :type CdcName: str\n        :param CdcId: ID of dedicated cluster which the instance belongs to. When it is an input parameter, the specified CdcId dedicated cluster resource is operated, and it can be left blank. When it is an output parameter, it is the ID of the dedicated cluster which the resource belongs to, and it can be left blank.
Note: This field may return null, indicating that no valid value was found.\n        :type CdcId: str\n        :param DedicatedClusterId: Dedicated cluster ID\n        :type DedicatedClusterId: str\n        """
        self.Zone = None
        self.CageId = None
        self.ProjectId = None
        self.CdcName = None
        self.CdcId = None
        self.DedicatedClusterId = None


    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.CageId = params.get("CageId")
        self.ProjectId = params.get("ProjectId")
        self.CdcName = params.get("CdcName")
        self.CdcId = params.get("CdcId")
        self.DedicatedClusterId = params.get("DedicatedClusterId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Policy(AbstractModel):
    """Describes the execution policy for scheduled snapshots. This can be understood as that, on the days specified by DayOfWeek, the scheduled snapshot policy is executed at the hour specified by Hour.

    """

    def __init__(self):
        """
        :param DayOfWeek: Specifies the days of the week, from Monday to Sunday, on which a scheduled snapshot will be triggered. Value range: [0, 6]. 0 indicates triggering on Sunday, 1-6 indicate triggering on Monday-Saturday.\n        :type DayOfWeek: list of int non-negative\n        :param Hour: Specifies the time that that the scheduled snapshot policy will be triggered. The unit is hour. The value range is [0-23]. 00:00-23:00 is a total of 24 time points that can be selected. 1 indicates 01:00, and so on.\n        :type Hour: list of int non-negative\n        """
        self.DayOfWeek = None
        self.Hour = None


    def _deserialize(self, params):
        self.DayOfWeek = params.get("DayOfWeek")
        self.Hour = params.get("Hour")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PrepayPrice(AbstractModel):
    """The cost of a prepaid order.

    """

    def __init__(self):
        """
        :param OriginalPrice: Original payment of a monthly-subscribed cloud disk or a snapshot, in USD.\n        :type OriginalPrice: float\n        :param DiscountPrice: Discounted price of a monthly-subscribed cloud disk or a snapshot, in USD.\n        :type DiscountPrice: float\n        :param OriginalPriceHigh: Original payment of a monthly-subscribed cloud disk or a snapshot, in USD, with six decimal places.\n        :type OriginalPriceHigh: str\n        :param DiscountPriceHigh: Discounted price of a monthly-subscribed cloud disk or a snapshot, in USD, with six decimal places.\n        :type DiscountPriceHigh: str\n        :param UnitPrice: Original unit price of a pay-as-you-go cloud disk, in USD.
Note: this field may return `null`, indicating that no valid values can be obtained.\n        :type UnitPrice: float\n        :param ChargeUnit: Billing unit for pay-as-you-go cloud disks. Valid value: <br><li>HOUR: billed hourly.
Note: this field may return `null`, indicating that no valid values can be obtained.\n        :type ChargeUnit: str\n        :param UnitPriceDiscount: Discount unit price of a pay-as-you-go cloud disk, in USD.
Note: this field may return `null`, indicating that no valid values can be obtained.\n        :type UnitPriceDiscount: float\n        :param UnitPriceHigh: Original unit price of a pay-as-you-go cloud disk, in USD, with six decimal places.
Note: this field may return `null`, indicating that no valid values can be obtained.\n        :type UnitPriceHigh: str\n        :param UnitPriceDiscountHigh: Discounted unit price of a pay-as-you-go cloud disk, in USD, with six decimal places.
Note: this field may return `null`, indicating that no valid values can be obtained.\n        :type UnitPriceDiscountHigh: str\n        """
        self.OriginalPrice = None
        self.DiscountPrice = None
        self.OriginalPriceHigh = None
        self.DiscountPriceHigh = None
        self.UnitPrice = None
        self.ChargeUnit = None
        self.UnitPriceDiscount = None
        self.UnitPriceHigh = None
        self.UnitPriceDiscountHigh = None


    def _deserialize(self, params):
        self.OriginalPrice = params.get("OriginalPrice")
        self.DiscountPrice = params.get("DiscountPrice")
        self.OriginalPriceHigh = params.get("OriginalPriceHigh")
        self.DiscountPriceHigh = params.get("DiscountPriceHigh")
        self.UnitPrice = params.get("UnitPrice")
        self.ChargeUnit = params.get("ChargeUnit")
        self.UnitPriceDiscount = params.get("UnitPriceDiscount")
        self.UnitPriceHigh = params.get("UnitPriceHigh")
        self.UnitPriceDiscountHigh = params.get("UnitPriceDiscountHigh")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Price(AbstractModel):
    """Describes the prepaid or postpaid price for the cloud disk.

    """

    def __init__(self):
        """
        :param OriginalPrice: Original price of a monthly-subscribed cloud disk, in USD.
Note: this field may return `null`, indicating that no valid values can be obtained.\n        :type OriginalPrice: float\n        :param DiscountPrice: Discounted price of a monthly-subscribed cloud disk, in USD.
Note: this field may return `null`, indicating that no valid values can be obtained.\n        :type DiscountPrice: float\n        :param UnitPrice: Original unit price of a pay-as-you-go cloud disk, in USD.
Note: this field may return `null`, indicating that no valid values can be obtained.\n        :type UnitPrice: float\n        :param ChargeUnit: Billing unit of a postpaid cloud disk. Value range: <br><li>HOUR: Billed by hour.
Note: This field may return null, indicating that no valid value was found.\n        :type ChargeUnit: str\n        :param UnitPriceDiscount: Discount unit price of a pay-as-you-go cloud disk, in USD.
Note: this field may return `null`, indicating that no valid values can be obtained.\n        :type UnitPriceDiscount: float\n        :param OriginalPriceHigh: Original payment of a monthly-subscribed cloud disk, in USD, with six decimal places.
Note: this field may return `null`, indicating that no valid values can be obtained.\n        :type OriginalPriceHigh: str\n        :param DiscountPriceHigh: Discounted payment price of a monthly-subscribed cloud disk, in USD, with six decimal places.
Note: this field may return `null`, indicating that no valid values can be obtained.\n        :type DiscountPriceHigh: str\n        :param UnitPriceHigh: Original unit price of a pay-as-you-go cloud disk, in USD, with six decimal places.
Note: this field may return `null`, indicating that no valid values can be obtained.\n        :type UnitPriceHigh: str\n        :param UnitPriceDiscountHigh: Discounted unit price of a pay-as-you-go cloud disk, in USD, with six decimal places.
Note: this field may return `null`, indicating that no valid values can be obtained.\n        :type UnitPriceDiscountHigh: str\n        """
        self.OriginalPrice = None
        self.DiscountPrice = None
        self.UnitPrice = None
        self.ChargeUnit = None
        self.UnitPriceDiscount = None
        self.OriginalPriceHigh = None
        self.DiscountPriceHigh = None
        self.UnitPriceHigh = None
        self.UnitPriceDiscountHigh = None


    def _deserialize(self, params):
        self.OriginalPrice = params.get("OriginalPrice")
        self.DiscountPrice = params.get("DiscountPrice")
        self.UnitPrice = params.get("UnitPrice")
        self.ChargeUnit = params.get("ChargeUnit")
        self.UnitPriceDiscount = params.get("UnitPriceDiscount")
        self.OriginalPriceHigh = params.get("OriginalPriceHigh")
        self.DiscountPriceHigh = params.get("DiscountPriceHigh")
        self.UnitPriceHigh = params.get("UnitPriceHigh")
        self.UnitPriceDiscountHigh = params.get("UnitPriceDiscountHigh")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ResizeDiskRequest(AbstractModel):
    """ResizeDisk request structure.

    """

    def __init__(self):
        """
        :param DiskId: ID of the cloud disk, which can be queried via the API [DescribeDisks](https://intl.cloud.tencent.com/document/product/362/16315?from_cn_redirect=1).\n        :type DiskId: str\n        :param DiskSize: Cloud disk size after scale out (in GB). This must be larger than the current size of the cloud disk. For the value range of the cloud disk sizes, see cloud disk [Product Types](https://intl.cloud.tencent.com/document/product/362/2353?from_cn_redirect=1).\n        :type DiskSize: int\n        """
        self.DiskId = None
        self.DiskSize = None


    def _deserialize(self, params):
        self.DiskId = params.get("DiskId")
        self.DiskSize = params.get("DiskSize")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ResizeDiskResponse(AbstractModel):
    """ResizeDisk response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class SharePermission(AbstractModel):
    """Snapshot sharing information set

    """

    def __init__(self):
        """
        :param CreatedTime: Snapshot sharing time\n        :type CreatedTime: str\n        :param AccountId: ID of the shared account\n        :type AccountId: str\n        """
        self.CreatedTime = None
        self.AccountId = None


    def _deserialize(self, params):
        self.CreatedTime = params.get("CreatedTime")
        self.AccountId = params.get("AccountId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Snapshot(AbstractModel):
    """The details of a snapshot

    """

    def __init__(self):
        """
        :param SnapshotId: Snapshot ID.\n        :type SnapshotId: str\n        :param Placement: Location of the snapshot.\n        :type Placement: :class:`tencentcloud.cbs.v20170312.models.Placement`\n        :param DiskUsage: The type of the cloud disk used to create the snapshot. Value range: <br><li>SYSTEM_DISK: System disk <br><li>DATA_DISK: Data disk.\n        :type DiskUsage: str\n        :param DiskId: ID of the cloud disk used to create this snapshot.\n        :type DiskId: str\n        :param DiskSize: Size of the cloud disk used to create this snapshot (in GB).\n        :type DiskSize: int\n        :param SnapshotState: Snapshot status. Valid values: <br><li>NORMAL: normal <br><li>CREATING: creating<br><li>ROLLBACKING: rolling back<br><li>COPYING_FROM_REMOTE: cross-region replicating<li>CHECKING_COPIED: verifying the cross-region replicated data<br><li>TORECYCLE: to be repossessed.\n        :type SnapshotState: str\n        :param SnapshotName: Snapshot name, the user-defined snapshot alias. Call [ModifySnapshotAttribute](https://intl.cloud.tencent.com/document/product/362/15650?from_cn_redirect=1) to modify this field.\n        :type SnapshotName: str\n        :param Percent: The progress percentage for snapshot creation. This field is always 100 after the snapshot is created successfully.\n        :type Percent: int\n        :param CreateTime: Creation time of the snapshot.\n        :type CreateTime: str\n        :param DeadlineTime: The expiration time of the snapshot. If the snapshot is permanently retained, this field is blank.\n        :type DeadlineTime: str\n        :param Encrypt: Whether the snapshot is created from an encrypted disk. Value range: <br><li>true: Yes <br><li>false: No.\n        :type Encrypt: bool\n        :param IsPermanent: Whether it is a permanent snapshot. Value range: <br><li>true: Permanent snapshot <br><li>false: Non-permanent snapshot.\n        :type IsPermanent: bool\n        :param CopyingToRegions: The destination region to which the snapshot is being replicated. Default value is [ ].\n        :type CopyingToRegions: list of str\n        :param CopyFromRemote: Whether the snapshot is replicated across regions. Value range: <br><li>true: Indicates that the snapshot is replicated across regions. <br><li>false: Indicates that the snapshot belongs to the local region.\n        :type CopyFromRemote: bool\n        :param Images: List of images associated with snapshot.\n        :type Images: list of Image\n        :param ImageCount: Number of images associated with snapshot.\n        :type ImageCount: int\n        :param SnapshotType: Snapshot type. This value can currently be either PRIVATE_SNAPSHOT or SHARED_SNAPSHOT.\n        :type SnapshotType: str\n        :param ShareReference: Number of snapshots currently shared\n        :type ShareReference: int\n        :param TimeStartShare: The time when the snapshot sharing starts\n        :type TimeStartShare: str\n        """
        self.SnapshotId = None
        self.Placement = None
        self.DiskUsage = None
        self.DiskId = None
        self.DiskSize = None
        self.SnapshotState = None
        self.SnapshotName = None
        self.Percent = None
        self.CreateTime = None
        self.DeadlineTime = None
        self.Encrypt = None
        self.IsPermanent = None
        self.CopyingToRegions = None
        self.CopyFromRemote = None
        self.Images = None
        self.ImageCount = None
        self.SnapshotType = None
        self.ShareReference = None
        self.TimeStartShare = None


    def _deserialize(self, params):
        self.SnapshotId = params.get("SnapshotId")
        if params.get("Placement") is not None:
            self.Placement = Placement()
            self.Placement._deserialize(params.get("Placement"))
        self.DiskUsage = params.get("DiskUsage")
        self.DiskId = params.get("DiskId")
        self.DiskSize = params.get("DiskSize")
        self.SnapshotState = params.get("SnapshotState")
        self.SnapshotName = params.get("SnapshotName")
        self.Percent = params.get("Percent")
        self.CreateTime = params.get("CreateTime")
        self.DeadlineTime = params.get("DeadlineTime")
        self.Encrypt = params.get("Encrypt")
        self.IsPermanent = params.get("IsPermanent")
        self.CopyingToRegions = params.get("CopyingToRegions")
        self.CopyFromRemote = params.get("CopyFromRemote")
        if params.get("Images") is not None:
            self.Images = []
            for item in params.get("Images"):
                obj = Image()
                obj._deserialize(item)
                self.Images.append(obj)
        self.ImageCount = params.get("ImageCount")
        self.SnapshotType = params.get("SnapshotType")
        self.ShareReference = params.get("ShareReference")
        self.TimeStartShare = params.get("TimeStartShare")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SnapshotOperationLog(AbstractModel):
    """The snapshot operation log.

    """

    def __init__(self):
        """
        :param Operator: UIN of operator.
Note: This field may return null, indicating that no valid value was found.\n        :type Operator: str\n        :param Operation: Operation type. Value range:
SNAP_OPERATION_DELETE: Delete snapshot
SNAP_OPERATION_ROLLBACK: Roll back snapshot
SNAP_OPERATION_MODIFY: Modify snapshot attributes
SNAP_OPERATION_CREATE: Create snapshot
SNAP_OPERATION_COPY: Cross-region replication of snapshot
ASP_OPERATION_CREATE_SNAP: Create snapshot with scheduled snapshot policy
ASP_OPERATION_DELETE_SNAP: Delete snapshot from scheduled snapshot policy\n        :type Operation: str\n        :param SnapshotId: ID of snapshot being operated.\n        :type SnapshotId: str\n        :param OperationState: Status of operation. Value range:
SUCCESS: Operation successful 
FAILED: Operation failed 
PROCESSING: Operation in process\n        :type OperationState: str\n        :param StartTime: Start time\n        :type StartTime: str\n        :param EndTime: End time\n        :type EndTime: str\n        """
        self.Operator = None
        self.Operation = None
        self.SnapshotId = None
        self.OperationState = None
        self.StartTime = None
        self.EndTime = None


    def _deserialize(self, params):
        self.Operator = params.get("Operator")
        self.Operation = params.get("Operation")
        self.SnapshotId = params.get("SnapshotId")
        self.OperationState = params.get("OperationState")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Tag(AbstractModel):
    """Tag.

    """

    def __init__(self):
        """
        :param Key: Tag key.\n        :type Key: str\n        :param Value: Tag value.\n        :type Value: str\n        """
        self.Key = None
        self.Value = None


    def _deserialize(self, params):
        self.Key = params.get("Key")
        self.Value = params.get("Value")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TerminateDisksRequest(AbstractModel):
    """TerminateDisks request structure.

    """

    def __init__(self):
        """
        :param DiskIds: List of cloud disk IDs required to be returned.\n        :type DiskIds: list of str\n        """
        self.DiskIds = None


    def _deserialize(self, params):
        self.DiskIds = params.get("DiskIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TerminateDisksResponse(AbstractModel):
    """TerminateDisks response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UnbindAutoSnapshotPolicyRequest(AbstractModel):
    """UnbindAutoSnapshotPolicy request structure.

    """

    def __init__(self):
        """
        :param DiskIds: List of cloud disk IDs scheduled snapshot policy to be unbound from.\n        :type DiskIds: list of str\n        :param AutoSnapshotPolicyId: ID of scheduled snapshot policy to be unbound.\n        :type AutoSnapshotPolicyId: str\n        """
        self.DiskIds = None
        self.AutoSnapshotPolicyId = None


    def _deserialize(self, params):
        self.DiskIds = params.get("DiskIds")
        self.AutoSnapshotPolicyId = params.get("AutoSnapshotPolicyId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UnbindAutoSnapshotPolicyResponse(AbstractModel):
    """UnbindAutoSnapshotPolicy response structure.

    """

    def __init__(self):
        """
        :param RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")