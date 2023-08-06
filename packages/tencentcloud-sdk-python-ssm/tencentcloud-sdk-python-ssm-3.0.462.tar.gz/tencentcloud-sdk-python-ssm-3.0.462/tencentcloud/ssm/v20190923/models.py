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


class CreateProductSecretRequest(AbstractModel):
    """CreateProductSecret请求参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 凭据名称，同一region内不可重复，最长128字节，使用字母、数字或者 - _ 的组合，第一个字符必须为字母或者数字。\n        :type SecretName: str\n        :param UserNamePrefix: 用户账号名前缀，由用户自行指定，长度限定在8个字符以内，
可选字符集包括：
数字字符：[0, 9]，
小写字符：[a, z]，
大写字符：[A, Z]，
特殊字符(全英文符号)：下划线(_)，
前缀必须以大写或小写字母开头。\n        :type UserNamePrefix: str\n        :param ProductName: 凭据所绑定的云产品名称，如Mysql，可以通过DescribeSupportedProducts接口获取所支持的云产品名称。\n        :type ProductName: str\n        :param InstanceID: 云产品实例ID。\n        :type InstanceID: str\n        :param Domains: 账号的域名，IP形式，支持填入%。\n        :type Domains: list of str\n        :param PrivilegesList: 将凭据与云产品实例绑定时，需要授予的权限列表。\n        :type PrivilegesList: list of ProductPrivilegeUnit\n        :param Description: 描述信息，用于详细描述用途等，最大支持2048字节。\n        :type Description: str\n        :param KmsKeyId: 指定对凭据进行加密的KMS CMK。
如果为空则表示使用Secrets Manager为您默认创建的CMK进行加密。
您也可以指定在同region 下自行创建的KMS CMK进行加密。\n        :type KmsKeyId: str\n        :param Tags: 标签列表。\n        :type Tags: list of Tag\n        :param RotationBeginTime: 用户自定义的开始轮转时间，格式：2006-01-02 15:04:05。
当EnableRotation为True时，此参数必填。\n        :type RotationBeginTime: str\n        :param EnableRotation: 是否开启轮转
True -- 开启
False -- 不开启
如果不指定，默认为False。\n        :type EnableRotation: bool\n        :param RotationFrequency: 轮转周期，以天为单位，默认为1天。\n        :type RotationFrequency: int\n        """
        self.SecretName = None
        self.UserNamePrefix = None
        self.ProductName = None
        self.InstanceID = None
        self.Domains = None
        self.PrivilegesList = None
        self.Description = None
        self.KmsKeyId = None
        self.Tags = None
        self.RotationBeginTime = None
        self.EnableRotation = None
        self.RotationFrequency = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        self.UserNamePrefix = params.get("UserNamePrefix")
        self.ProductName = params.get("ProductName")
        self.InstanceID = params.get("InstanceID")
        self.Domains = params.get("Domains")
        if params.get("PrivilegesList") is not None:
            self.PrivilegesList = []
            for item in params.get("PrivilegesList"):
                obj = ProductPrivilegeUnit()
                obj._deserialize(item)
                self.PrivilegesList.append(obj)
        self.Description = params.get("Description")
        self.KmsKeyId = params.get("KmsKeyId")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.RotationBeginTime = params.get("RotationBeginTime")
        self.EnableRotation = params.get("EnableRotation")
        self.RotationFrequency = params.get("RotationFrequency")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateProductSecretResponse(AbstractModel):
    """CreateProductSecret返回参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 创建的凭据名称。\n        :type SecretName: str\n        :param TagCode: 标签操作的返回码. 0: 成功；1: 内部错误；2: 业务处理错误。
注意：此字段可能返回 null，表示取不到有效值。
注意：此字段可能返回 null，表示取不到有效值。\n        :type TagCode: int\n        :param TagMsg: 标签操作的返回信息。
注意：此字段可能返回 null，表示取不到有效值。\n        :type TagMsg: str\n        :param FlowID: 创建云产品凭据异步任务ID号。\n        :type FlowID: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.SecretName = None
        self.TagCode = None
        self.TagMsg = None
        self.FlowID = None
        self.RequestId = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        self.TagCode = params.get("TagCode")
        self.TagMsg = params.get("TagMsg")
        self.FlowID = params.get("FlowID")
        self.RequestId = params.get("RequestId")


class CreateSecretRequest(AbstractModel):
    """CreateSecret请求参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 凭据名称，同一region内不可重复，最长128字节，使用字母、数字或者 - _ 的组合，第一个字符必须为字母或者数字。\n        :type SecretName: str\n        :param VersionId: 凭据版本，查询凭据信息时需要根据SecretName 和 VersionId进行查询，最长64 字节，使用字母、数字或者 - _ . 的组合并且以字母或数字开头。\n        :type VersionId: str\n        :param Description: 描述信息，用于详细描述用途等，最大支持2048字节。\n        :type Description: str\n        :param KmsKeyId: 指定对凭据进行加密的KMS CMK。如果为空则表示使用Secrets Manager为您默认创建的CMK进行加密。您也可以指定在同region 下自行创建的KMS CMK进行加密。\n        :type KmsKeyId: str\n        :param SecretBinary: 二进制凭据信息base64编码后的明文。SecretBinary 和 SecretString 必须且只能设置一个，最大支持4096字节。\n        :type SecretBinary: str\n        :param SecretString: 文本类型凭据信息明文（不需要进行base64编码）。SecretBinary 和 SecretString 必须且只能设置一个，，最大支持4096字节。\n        :type SecretString: str\n        :param Tags: 标签列表\n        :type Tags: list of Tag\n        """
        self.SecretName = None
        self.VersionId = None
        self.Description = None
        self.KmsKeyId = None
        self.SecretBinary = None
        self.SecretString = None
        self.Tags = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        self.VersionId = params.get("VersionId")
        self.Description = params.get("Description")
        self.KmsKeyId = params.get("KmsKeyId")
        self.SecretBinary = params.get("SecretBinary")
        self.SecretString = params.get("SecretString")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateSecretResponse(AbstractModel):
    """CreateSecret返回参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 新创建的凭据名称。\n        :type SecretName: str\n        :param VersionId: 新创建的凭据版本。\n        :type VersionId: str\n        :param TagCode: 标签操作的返回码. 0: 成功；1: 内部错误；2: 业务处理错误
注意：此字段可能返回 null，表示取不到有效值。\n        :type TagCode: int\n        :param TagMsg: 标签操作的返回信息
注意：此字段可能返回 null，表示取不到有效值。\n        :type TagMsg: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.SecretName = None
        self.VersionId = None
        self.TagCode = None
        self.TagMsg = None
        self.RequestId = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        self.VersionId = params.get("VersionId")
        self.TagCode = params.get("TagCode")
        self.TagMsg = params.get("TagMsg")
        self.RequestId = params.get("RequestId")


class DeleteSecretRequest(AbstractModel):
    """DeleteSecret请求参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 指定需要删除的凭据名称。\n        :type SecretName: str\n        :param RecoveryWindowInDays: 指定计划删除日期，单位（天），0（默认）表示立即删除， 1-30 表示预留的天数，超出该日期之后彻底删除。\n        :type RecoveryWindowInDays: int\n        """
        self.SecretName = None
        self.RecoveryWindowInDays = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        self.RecoveryWindowInDays = params.get("RecoveryWindowInDays")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteSecretResponse(AbstractModel):
    """DeleteSecret返回参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 指定删除的凭据名称。\n        :type SecretName: str\n        :param DeleteTime: 凭据删除的日期，unix时间戳。\n        :type DeleteTime: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.SecretName = None
        self.DeleteTime = None
        self.RequestId = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        self.DeleteTime = params.get("DeleteTime")
        self.RequestId = params.get("RequestId")


class DeleteSecretVersionRequest(AbstractModel):
    """DeleteSecretVersion请求参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 指定凭据名称。\n        :type SecretName: str\n        :param VersionId: 指定该名称下需要删除的凭据的版本号。\n        :type VersionId: str\n        """
        self.SecretName = None
        self.VersionId = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        self.VersionId = params.get("VersionId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteSecretVersionResponse(AbstractModel):
    """DeleteSecretVersion返回参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 凭据名称。\n        :type SecretName: str\n        :param VersionId: 凭据版本号。\n        :type VersionId: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.SecretName = None
        self.VersionId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        self.VersionId = params.get("VersionId")
        self.RequestId = params.get("RequestId")


class DescribeAsyncRequestInfoRequest(AbstractModel):
    """DescribeAsyncRequestInfo请求参数结构体

    """

    def __init__(self):
        """
        :param FlowID: 异步任务ID号。\n        :type FlowID: int\n        """
        self.FlowID = None


    def _deserialize(self, params):
        self.FlowID = params.get("FlowID")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAsyncRequestInfoResponse(AbstractModel):
    """DescribeAsyncRequestInfo返回参数结构体

    """

    def __init__(self):
        """
        :param TaskStatus: 0:处理中，1:处理成功，2:处理失败\n        :type TaskStatus: int\n        :param Description: 任务描述信息。\n        :type Description: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.TaskStatus = None
        self.Description = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TaskStatus = params.get("TaskStatus")
        self.Description = params.get("Description")
        self.RequestId = params.get("RequestId")


class DescribeRotationDetailRequest(AbstractModel):
    """DescribeRotationDetail请求参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 指定需要获取凭据轮转详细信息的凭据名称。\n        :type SecretName: str\n        """
        self.SecretName = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeRotationDetailResponse(AbstractModel):
    """DescribeRotationDetail返回参数结构体

    """

    def __init__(self):
        """
        :param EnableRotation: 否允许轮转，True表示开启轮转，False表示禁止轮转。\n        :type EnableRotation: bool\n        :param Frequency: 轮转的频率，以天为单位，默认为1天。
注意：此字段可能返回 null，表示取不到有效值。\n        :type Frequency: int\n        :param LatestRotateTime: 最近一次轮转的时间，显式可见的时间字符串，格式 2006-01-02 15:04:05。
注意：此字段可能返回 null，表示取不到有效值。\n        :type LatestRotateTime: str\n        :param NextRotateBeginTime: 下一次开始轮转的时间，显式可见的时间字符串，格式 2006-01-02 15:04:05。
注意：此字段可能返回 null，表示取不到有效值。\n        :type NextRotateBeginTime: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.EnableRotation = None
        self.Frequency = None
        self.LatestRotateTime = None
        self.NextRotateBeginTime = None
        self.RequestId = None


    def _deserialize(self, params):
        self.EnableRotation = params.get("EnableRotation")
        self.Frequency = params.get("Frequency")
        self.LatestRotateTime = params.get("LatestRotateTime")
        self.NextRotateBeginTime = params.get("NextRotateBeginTime")
        self.RequestId = params.get("RequestId")


class DescribeRotationHistoryRequest(AbstractModel):
    """DescribeRotationHistory请求参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 指定需要获取凭据轮转历史的凭据名称。\n        :type SecretName: str\n        """
        self.SecretName = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeRotationHistoryResponse(AbstractModel):
    """DescribeRotationHistory返回参数结构体

    """

    def __init__(self):
        """
        :param VersionIDs: 版本号列表。\n        :type VersionIDs: list of str\n        :param TotalCount: 版本号个数，可以给用户展示的版本号个数上限为10个。\n        :type TotalCount: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.VersionIDs = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        self.VersionIDs = params.get("VersionIDs")
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeSecretRequest(AbstractModel):
    """DescribeSecret请求参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 指定需要获取凭据详细信息的凭据名称。\n        :type SecretName: str\n        """
        self.SecretName = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSecretResponse(AbstractModel):
    """DescribeSecret返回参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 凭据名称。\n        :type SecretName: str\n        :param Description: 凭据描述信息。\n        :type Description: str\n        :param KmsKeyId: 用于加密的KMS CMK ID。\n        :type KmsKeyId: str\n        :param CreateUin: 创建者UIN。\n        :type CreateUin: int\n        :param Status: 凭据状态：Enabled、Disabled、PendingDelete, Creating, Failed。\n        :type Status: str\n        :param DeleteTime: 删除日期，uinx 时间戳，非计划删除状态的凭据为0。\n        :type DeleteTime: int\n        :param CreateTime: 创建日期。\n        :type CreateTime: int\n        :param SecretType: 0 --  用户自定义凭据类型；1 -- 云产品凭据类型。
注意：此字段可能返回 null，表示取不到有效值。\n        :type SecretType: int\n        :param ProductName: 云产品名称。
注意：此字段可能返回 null，表示取不到有效值。\n        :type ProductName: str\n        :param ResourceID: 云产品实例ID。
注意：此字段可能返回 null，表示取不到有效值。\n        :type ResourceID: str\n        :param RotationStatus: 是否开启轮转：True -- 开启轮转；False -- 禁止轮转。
注意：此字段可能返回 null，表示取不到有效值。\n        :type RotationStatus: bool\n        :param RotationFrequency: 轮转周期，默认以天为单位。
注意：此字段可能返回 null，表示取不到有效值。\n        :type RotationFrequency: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.SecretName = None
        self.Description = None
        self.KmsKeyId = None
        self.CreateUin = None
        self.Status = None
        self.DeleteTime = None
        self.CreateTime = None
        self.SecretType = None
        self.ProductName = None
        self.ResourceID = None
        self.RotationStatus = None
        self.RotationFrequency = None
        self.RequestId = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        self.Description = params.get("Description")
        self.KmsKeyId = params.get("KmsKeyId")
        self.CreateUin = params.get("CreateUin")
        self.Status = params.get("Status")
        self.DeleteTime = params.get("DeleteTime")
        self.CreateTime = params.get("CreateTime")
        self.SecretType = params.get("SecretType")
        self.ProductName = params.get("ProductName")
        self.ResourceID = params.get("ResourceID")
        self.RotationStatus = params.get("RotationStatus")
        self.RotationFrequency = params.get("RotationFrequency")
        self.RequestId = params.get("RequestId")


class DescribeSupportedProductsRequest(AbstractModel):
    """DescribeSupportedProducts请求参数结构体

    """


class DescribeSupportedProductsResponse(AbstractModel):
    """DescribeSupportedProducts返回参数结构体

    """

    def __init__(self):
        """
        :param Products: 支持的产品列表。\n        :type Products: list of str\n        :param TotalCount: 支持的产品个数\n        :type TotalCount: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Products = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Products = params.get("Products")
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DisableSecretRequest(AbstractModel):
    """DisableSecret请求参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 指定停用的凭据名称。\n        :type SecretName: str\n        """
        self.SecretName = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DisableSecretResponse(AbstractModel):
    """DisableSecret返回参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 停用的凭据名称。\n        :type SecretName: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.SecretName = None
        self.RequestId = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        self.RequestId = params.get("RequestId")


class EnableSecretRequest(AbstractModel):
    """EnableSecret请求参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 指定启用凭据的名称。\n        :type SecretName: str\n        """
        self.SecretName = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EnableSecretResponse(AbstractModel):
    """EnableSecret返回参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 启用的凭据名称。\n        :type SecretName: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.SecretName = None
        self.RequestId = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        self.RequestId = params.get("RequestId")


class GetRegionsRequest(AbstractModel):
    """GetRegions请求参数结构体

    """


class GetRegionsResponse(AbstractModel):
    """GetRegions返回参数结构体

    """

    def __init__(self):
        """
        :param Regions: region列表。\n        :type Regions: list of str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Regions = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Regions = params.get("Regions")
        self.RequestId = params.get("RequestId")


class GetSecretValueRequest(AbstractModel):
    """GetSecretValue请求参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 指定凭据的名称。\n        :type SecretName: str\n        :param VersionId: 指定对应凭据的版本号。
对于云产品凭据如Mysql凭据，通过指定凭据名称和历史版本号来获取历史轮转凭据的明文信息，如果要获取当前正在使用的凭据版本的明文，需要将版本号指定为：SSM_Current。\n        :type VersionId: str\n        """
        self.SecretName = None
        self.VersionId = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        self.VersionId = params.get("VersionId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GetSecretValueResponse(AbstractModel):
    """GetSecretValue返回参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 凭据的名称。\n        :type SecretName: str\n        :param VersionId: 该凭据对应的版本号。\n        :type VersionId: str\n        :param SecretBinary: 在创建凭据(CreateSecret)时，如果指定的是二进制数据，则该字段为返回结果，并且使用base64进行编码，应用方需要进行base64解码后获取原始数据。
SecretBinary和SecretString只有一个不为空。\n        :type SecretBinary: str\n        :param SecretString: 在创建凭据(CreateSecret)时，如果指定的是普通文本数据，则该字段为返回结果。
SecretBinary和SecretString只有一个不为空。\n        :type SecretString: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.SecretName = None
        self.VersionId = None
        self.SecretBinary = None
        self.SecretString = None
        self.RequestId = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        self.VersionId = params.get("VersionId")
        self.SecretBinary = params.get("SecretBinary")
        self.SecretString = params.get("SecretString")
        self.RequestId = params.get("RequestId")


class GetServiceStatusRequest(AbstractModel):
    """GetServiceStatus请求参数结构体

    """


class GetServiceStatusResponse(AbstractModel):
    """GetServiceStatus返回参数结构体

    """

    def __init__(self):
        """
        :param ServiceEnabled: true表示服务已开通，false 表示服务尚未开通。\n        :type ServiceEnabled: bool\n        :param InvalidType: 服务不可用类型： 0-未购买，1-正常， 2-欠费停服， 3-资源释放。\n        :type InvalidType: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.ServiceEnabled = None
        self.InvalidType = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ServiceEnabled = params.get("ServiceEnabled")
        self.InvalidType = params.get("InvalidType")
        self.RequestId = params.get("RequestId")


class ListSecretVersionIdsRequest(AbstractModel):
    """ListSecretVersionIds请求参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 凭据名称。\n        :type SecretName: str\n        """
        self.SecretName = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ListSecretVersionIdsResponse(AbstractModel):
    """ListSecretVersionIds返回参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 凭据名称。\n        :type SecretName: str\n        :param Versions: VersionId列表。
注意：此字段可能返回 null，表示取不到有效值。\n        :type Versions: list of VersionInfo\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.SecretName = None
        self.Versions = None
        self.RequestId = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        if params.get("Versions") is not None:
            self.Versions = []
            for item in params.get("Versions"):
                obj = VersionInfo()
                obj._deserialize(item)
                self.Versions.append(obj)
        self.RequestId = params.get("RequestId")


class ListSecretsRequest(AbstractModel):
    """ListSecrets请求参数结构体

    """

    def __init__(self):
        """
        :param Offset: 查询列表的起始位置，以0开始，不设置默认为0。\n        :type Offset: int\n        :param Limit: 单次查询返回的最大数量，0或不设置则使用默认值 20。\n        :type Limit: int\n        :param OrderType: 根据创建时间的排序方式，0或者不设置则使用降序排序， 1 表示升序排序。\n        :type OrderType: int\n        :param State: 根据凭据状态进行过滤。
默认为0表示查询全部。
1 --  表示查询Enabled 凭据列表。
2 --  表示查询Disabled 凭据列表。
3 --  表示查询PendingDelete 凭据列表。
4 --  表示PendingCreate。
5 --  表示CreateFailed。
其中状态PendingCreate和CreateFailed只有在SecretType为云产品凭据时生效\n        :type State: int\n        :param SearchSecretName: 根据凭据名称进行过滤，为空表示不过滤。\n        :type SearchSecretName: str\n        :param TagFilters: 标签过滤条件。\n        :type TagFilters: list of TagFilter\n        :param SecretType: 0  -- 表示用户自定义凭据，默认为0。
1  -- 表示用户云产品凭据。
这个参数只能在云产品凭据(1)和用户自定义凭据(0)中二选一。\n        :type SecretType: int\n        """
        self.Offset = None
        self.Limit = None
        self.OrderType = None
        self.State = None
        self.SearchSecretName = None
        self.TagFilters = None
        self.SecretType = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.OrderType = params.get("OrderType")
        self.State = params.get("State")
        self.SearchSecretName = params.get("SearchSecretName")
        if params.get("TagFilters") is not None:
            self.TagFilters = []
            for item in params.get("TagFilters"):
                obj = TagFilter()
                obj._deserialize(item)
                self.TagFilters.append(obj)
        self.SecretType = params.get("SecretType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ListSecretsResponse(AbstractModel):
    """ListSecrets返回参数结构体

    """

    def __init__(self):
        """
        :param TotalCount: 根据State和SearchSecretName 筛选的凭据总数。\n        :type TotalCount: int\n        :param SecretMetadatas: 返回凭据信息列表。\n        :type SecretMetadatas: list of SecretMetadata\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.TotalCount = None
        self.SecretMetadatas = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("SecretMetadatas") is not None:
            self.SecretMetadatas = []
            for item in params.get("SecretMetadatas"):
                obj = SecretMetadata()
                obj._deserialize(item)
                self.SecretMetadatas.append(obj)
        self.RequestId = params.get("RequestId")


class ProductPrivilegeUnit(AbstractModel):
    """凭据关联产品时被赋予的权限

    """

    def __init__(self):
        """
        :param PrivilegeName: 权限名称，当前可选：
GlobalPrivileges
DatabasePrivileges
TablePrivileges
ColumnPrivileges

当权限为DatabasePrivileges时，必须通过参数Database指定数据库名；

当权限为TablePrivileges时，必须通过参数Database和TableName指定数据库名以及数据库中的表名；

当权限为ColumnPrivileges时，必须通过参数Database、TableName和CoulmnName指定数据库、数据库中的表名以及表中的列名。\n        :type PrivilegeName: str\n        :param Privileges: 权限列表。
对于Mysql产品来说，可选权限值为：

1. GlobalPrivileges 中权限的可选值为："SELECT","INSERT","UPDATE","DELETE","CREATE", "PROCESS", "DROP","REFERENCES","INDEX","ALTER","SHOW DATABASES","CREATE TEMPORARY TABLES","LOCK TABLES","EXECUTE","CREATE VIEW","SHOW VIEW","CREATE ROUTINE","ALTER ROUTINE","EVENT","TRIGGER"。
注意，不传该参数表示清除该权限。

2. DatabasePrivileges 权限的可选值为："SELECT","INSERT","UPDATE","DELETE","CREATE", "DROP","REFERENCES","INDEX","ALTER","CREATE TEMPORARY TABLES","LOCK TABLES","EXECUTE","CREATE VIEW","SHOW VIEW","CREATE ROUTINE","ALTER ROUTINE","EVENT","TRIGGER"。
注意，不传该参数表示清除该权限。

3. TablePrivileges 权限的可选值为：权限的可选值为："SELECT","INSERT","UPDATE","DELETE","CREATE", "DROP","REFERENCES","INDEX","ALTER","CREATE VIEW","SHOW VIEW", "TRIGGER"。
注意，不传该参数表示清除该权限。

4. ColumnPrivileges 权限的可选值为："SELECT","INSERT","UPDATE","REFERENCES"。
注意，不传该参数表示清除该权限。\n        :type Privileges: list of str\n        :param Database: 仅当PrivilegeName为DatabasePrivileges时这个值才有效。\n        :type Database: str\n        :param TableName: 仅当PrivilegeName为TablePrivileges时这个值才有效，并且此时需要填充Database显式指明所在的数据库实例。\n        :type TableName: str\n        :param ColumnName: 仅当PrivilegeName为ColumnPrivileges时这个值才生效，并且此时必须填充：
Database - 显式指明所在的数据库实例。
TableName - 显式指明所在表\n        :type ColumnName: str\n        """
        self.PrivilegeName = None
        self.Privileges = None
        self.Database = None
        self.TableName = None
        self.ColumnName = None


    def _deserialize(self, params):
        self.PrivilegeName = params.get("PrivilegeName")
        self.Privileges = params.get("Privileges")
        self.Database = params.get("Database")
        self.TableName = params.get("TableName")
        self.ColumnName = params.get("ColumnName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PutSecretValueRequest(AbstractModel):
    """PutSecretValue请求参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 指定需要增加版本的凭据名称。\n        :type SecretName: str\n        :param VersionId: 指定新增加的版本号，最长64 字节，使用字母、数字或者 - _ . 的组合并且以字母或数字开头。\n        :type VersionId: str\n        :param SecretBinary: 二进制凭据信息，使用base64编码。
SecretBinary 和 SecretString 必须且只能设置一个。\n        :type SecretBinary: str\n        :param SecretString: 文本类型凭据信息明文（不需要进行base64编码），SecretBinary 和 SecretString 必须且只能设置一个。\n        :type SecretString: str\n        """
        self.SecretName = None
        self.VersionId = None
        self.SecretBinary = None
        self.SecretString = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        self.VersionId = params.get("VersionId")
        self.SecretBinary = params.get("SecretBinary")
        self.SecretString = params.get("SecretString")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PutSecretValueResponse(AbstractModel):
    """PutSecretValue返回参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 凭据名称。\n        :type SecretName: str\n        :param VersionId: 新增加的版本号。\n        :type VersionId: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.SecretName = None
        self.VersionId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        self.VersionId = params.get("VersionId")
        self.RequestId = params.get("RequestId")


class RestoreSecretRequest(AbstractModel):
    """RestoreSecret请求参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 指定需要恢复的凭据名称。\n        :type SecretName: str\n        """
        self.SecretName = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RestoreSecretResponse(AbstractModel):
    """RestoreSecret返回参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 凭据名称。\n        :type SecretName: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.SecretName = None
        self.RequestId = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        self.RequestId = params.get("RequestId")


class RotateProductSecretRequest(AbstractModel):
    """RotateProductSecret请求参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 需要轮转的凭据名。\n        :type SecretName: str\n        """
        self.SecretName = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RotateProductSecretResponse(AbstractModel):
    """RotateProductSecret返回参数结构体

    """

    def __init__(self):
        """
        :param FlowID: 轮转异步任务ID号。\n        :type FlowID: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.FlowID = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FlowID = params.get("FlowID")
        self.RequestId = params.get("RequestId")


class SecretMetadata(AbstractModel):
    """凭据的基础信息

    """

    def __init__(self):
        """
        :param SecretName: 凭据名称\n        :type SecretName: str\n        :param Description: 凭据的描述信息\n        :type Description: str\n        :param KmsKeyId: 用于加密凭据的KMS KeyId\n        :type KmsKeyId: str\n        :param CreateUin: 创建者UIN\n        :type CreateUin: int\n        :param Status: 凭据状态：Enabled、Disabled、PendingDelete、Creating、Failed\n        :type Status: str\n        :param DeleteTime: 凭据删除日期，对于status为PendingDelete 的有效，unix时间戳\n        :type DeleteTime: int\n        :param CreateTime: 凭据创建时间，unix时间戳\n        :type CreateTime: int\n        :param KmsKeyType: 用于加密凭据的KMS CMK类型，DEFAULT 表示SecretsManager 创建的默认密钥， CUSTOMER 表示用户指定的密钥\n        :type KmsKeyType: str\n        :param RotationStatus: 1:--开启轮转；0--禁止轮转
注意：此字段可能返回 null，表示取不到有效值。\n        :type RotationStatus: int\n        :param NextRotationTime: 下一次轮转开始时间，uinx 时间戳
注意：此字段可能返回 null，表示取不到有效值。\n        :type NextRotationTime: int\n        :param SecretType: 0 -- 用户自定义凭据；1 -- 云产品凭据
注意：此字段可能返回 null，表示取不到有效值。\n        :type SecretType: int\n        :param ProductName: 云产品名称，仅在SecretType为1，即凭据类型为云产品凭据时生效
注意：此字段可能返回 null，表示取不到有效值。\n        :type ProductName: str\n        """
        self.SecretName = None
        self.Description = None
        self.KmsKeyId = None
        self.CreateUin = None
        self.Status = None
        self.DeleteTime = None
        self.CreateTime = None
        self.KmsKeyType = None
        self.RotationStatus = None
        self.NextRotationTime = None
        self.SecretType = None
        self.ProductName = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        self.Description = params.get("Description")
        self.KmsKeyId = params.get("KmsKeyId")
        self.CreateUin = params.get("CreateUin")
        self.Status = params.get("Status")
        self.DeleteTime = params.get("DeleteTime")
        self.CreateTime = params.get("CreateTime")
        self.KmsKeyType = params.get("KmsKeyType")
        self.RotationStatus = params.get("RotationStatus")
        self.NextRotationTime = params.get("NextRotationTime")
        self.SecretType = params.get("SecretType")
        self.ProductName = params.get("ProductName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Tag(AbstractModel):
    """标签键和标签值

    """

    def __init__(self):
        """
        :param TagKey: 标签键\n        :type TagKey: str\n        :param TagValue: 标签值\n        :type TagValue: str\n        """
        self.TagKey = None
        self.TagValue = None


    def _deserialize(self, params):
        self.TagKey = params.get("TagKey")
        self.TagValue = params.get("TagValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TagFilter(AbstractModel):
    """标签过滤器

    """

    def __init__(self):
        """
        :param TagKey: 标签键\n        :type TagKey: str\n        :param TagValue: 标签值\n        :type TagValue: list of str\n        """
        self.TagKey = None
        self.TagValue = None


    def _deserialize(self, params):
        self.TagKey = params.get("TagKey")
        self.TagValue = params.get("TagValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateDescriptionRequest(AbstractModel):
    """UpdateDescription请求参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 指定需要更新描述信息的凭据名。\n        :type SecretName: str\n        :param Description: 新的描述信息，最大长度2048个字节。\n        :type Description: str\n        """
        self.SecretName = None
        self.Description = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        self.Description = params.get("Description")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateDescriptionResponse(AbstractModel):
    """UpdateDescription返回参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 凭据名称。\n        :type SecretName: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.SecretName = None
        self.RequestId = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        self.RequestId = params.get("RequestId")


class UpdateRotationStatusRequest(AbstractModel):
    """UpdateRotationStatus请求参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 云产品凭据名称。\n        :type SecretName: str\n        :param EnableRotation: 是否开启轮转。
True -- 开启轮转；
False -- 禁止轮转。\n        :type EnableRotation: bool\n        :param Frequency: 轮转周期，以天为单位，最小为30天，最大为365天。\n        :type Frequency: int\n        :param RotationBeginTime: 用户设置的期望开始轮转时间，格式为：2006-01-02 15:04:05。
当EnableRotation为True时，如果不填RotationBeginTime，则默认填充为当前时间。\n        :type RotationBeginTime: str\n        """
        self.SecretName = None
        self.EnableRotation = None
        self.Frequency = None
        self.RotationBeginTime = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        self.EnableRotation = params.get("EnableRotation")
        self.Frequency = params.get("Frequency")
        self.RotationBeginTime = params.get("RotationBeginTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateRotationStatusResponse(AbstractModel):
    """UpdateRotationStatus返回参数结构体

    """

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class UpdateSecretRequest(AbstractModel):
    """UpdateSecret请求参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 指定需要更新凭据内容的名称。\n        :type SecretName: str\n        :param VersionId: 指定需要更新凭据内容的版本号。\n        :type VersionId: str\n        :param SecretBinary: 新的凭据内容为二进制的场景使用该字段，并使用base64进行编码。
SecretBinary 和 SecretString 只能一个不为空。\n        :type SecretBinary: str\n        :param SecretString: 新的凭据内容为文本的场景使用该字段，不需要base64编码SecretBinary 和 SecretString 只能一个不为空。\n        :type SecretString: str\n        """
        self.SecretName = None
        self.VersionId = None
        self.SecretBinary = None
        self.SecretString = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        self.VersionId = params.get("VersionId")
        self.SecretBinary = params.get("SecretBinary")
        self.SecretString = params.get("SecretString")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateSecretResponse(AbstractModel):
    """UpdateSecret返回参数结构体

    """

    def __init__(self):
        """
        :param SecretName: 凭据名称。\n        :type SecretName: str\n        :param VersionId: 凭据版本号。\n        :type VersionId: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.SecretName = None
        self.VersionId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.SecretName = params.get("SecretName")
        self.VersionId = params.get("VersionId")
        self.RequestId = params.get("RequestId")


class VersionInfo(AbstractModel):
    """凭据版本号列表信息

    """

    def __init__(self):
        """
        :param VersionId: 版本号。\n        :type VersionId: str\n        :param CreateTime: 创建时间，unix时间戳。\n        :type CreateTime: int\n        """
        self.VersionId = None
        self.CreateTime = None


    def _deserialize(self, params):
        self.VersionId = params.get("VersionId")
        self.CreateTime = params.get("CreateTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        