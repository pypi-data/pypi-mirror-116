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


class AcListsData(AbstractModel):
    """访问控制列表对象

    """

    def __init__(self):
        """
        :param Id: 规则id\n        :type Id: int\n        :param SourceIp: 访问源
注意：此字段可能返回 null，表示取不到有效值。\n        :type SourceIp: str\n        :param TargetIp: 访问目的
注意：此字段可能返回 null，表示取不到有效值。\n        :type TargetIp: str\n        :param Protocol: 协议
注意：此字段可能返回 null，表示取不到有效值。\n        :type Protocol: str\n        :param Port: 端口
注意：此字段可能返回 null，表示取不到有效值。\n        :type Port: str\n        :param Strategy: 策略
注意：此字段可能返回 null，表示取不到有效值。\n        :type Strategy: int\n        :param Detail: 描述
注意：此字段可能返回 null，表示取不到有效值。\n        :type Detail: str\n        :param Count: 命中次数\n        :type Count: int\n        :param OrderIndex: 执行顺序\n        :type OrderIndex: int\n        :param LogId: 告警规则id
注意：此字段可能返回 null，表示取不到有效值。\n        :type LogId: str\n        """
        self.Id = None
        self.SourceIp = None
        self.TargetIp = None
        self.Protocol = None
        self.Port = None
        self.Strategy = None
        self.Detail = None
        self.Count = None
        self.OrderIndex = None
        self.LogId = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.SourceIp = params.get("SourceIp")
        self.TargetIp = params.get("TargetIp")
        self.Protocol = params.get("Protocol")
        self.Port = params.get("Port")
        self.Strategy = params.get("Strategy")
        self.Detail = params.get("Detail")
        self.Count = params.get("Count")
        self.OrderIndex = params.get("OrderIndex")
        self.LogId = params.get("LogId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AssetZone(AbstractModel):
    """AssetZone

    """

    def __init__(self):
        """
        :param Zone: 地域\n        :type Zone: str\n        :param ZoneEng: 地域英文\n        :type ZoneEng: str\n        """
        self.Zone = None
        self.ZoneEng = None


    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.ZoneEng = params.get("ZoneEng")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AssociatedInstanceInfo(AbstractModel):
    """企业安全组关联实例信息

    """

    def __init__(self):
        """
        :param InstanceId: 实例ID
注意：此字段可能返回 null，表示取不到有效值。\n        :type InstanceId: str\n        :param InstanceName: 实例名称
注意：此字段可能返回 null，表示取不到有效值。\n        :type InstanceName: str\n        :param Type: 实例类型，3是cvm实例,4是clb实例,5是eni实例,6是云数据库
注意：此字段可能返回 null，表示取不到有效值。\n        :type Type: int\n        :param VpcId: 私有网络ID
注意：此字段可能返回 null，表示取不到有效值。\n        :type VpcId: str\n        :param VpcName: 私有网络名称
注意：此字段可能返回 null，表示取不到有效值。\n        :type VpcName: str\n        :param PublicIp: 公网IP
注意：此字段可能返回 null，表示取不到有效值。\n        :type PublicIp: str\n        :param Ip: 内网IP
注意：此字段可能返回 null，表示取不到有效值。\n        :type Ip: str\n        :param SecurityGroupCount: 关联安全组数量
注意：此字段可能返回 null，表示取不到有效值。\n        :type SecurityGroupCount: int\n        """
        self.InstanceId = None
        self.InstanceName = None
        self.Type = None
        self.VpcId = None
        self.VpcName = None
        self.PublicIp = None
        self.Ip = None
        self.SecurityGroupCount = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        self.Type = params.get("Type")
        self.VpcId = params.get("VpcId")
        self.VpcName = params.get("VpcName")
        self.PublicIp = params.get("PublicIp")
        self.Ip = params.get("Ip")
        self.SecurityGroupCount = params.get("SecurityGroupCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CfwNatDnatRule(AbstractModel):
    """NAT防火墙Dnat规则

    """

    def __init__(self):
        """
        :param IpProtocol: 网络协议，可选值：TCP、UDP。\n        :type IpProtocol: str\n        :param PublicIpAddress: 弹性IP。\n        :type PublicIpAddress: str\n        :param PublicPort: 公网端口。\n        :type PublicPort: int\n        :param PrivateIpAddress: 内网地址。\n        :type PrivateIpAddress: str\n        :param PrivatePort: 内网端口。\n        :type PrivatePort: int\n        :param Description: NAT防火墙转发规则描述。\n        :type Description: str\n        """
        self.IpProtocol = None
        self.PublicIpAddress = None
        self.PublicPort = None
        self.PrivateIpAddress = None
        self.PrivatePort = None
        self.Description = None


    def _deserialize(self, params):
        self.IpProtocol = params.get("IpProtocol")
        self.PublicIpAddress = params.get("PublicIpAddress")
        self.PublicPort = params.get("PublicPort")
        self.PrivateIpAddress = params.get("PrivateIpAddress")
        self.PrivatePort = params.get("PrivatePort")
        self.Description = params.get("Description")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateAcRulesRequest(AbstractModel):
    """CreateAcRules请求参数结构体

    """

    def __init__(self):
        """
        :param Data: 创建规则数据\n        :type Data: list of RuleInfoData\n        :param Type: 0：添加（默认），1：插入\n        :type Type: int\n        :param EdgeId: 边id\n        :type EdgeId: str\n        :param Enable: 访问控制规则状态\n        :type Enable: int\n        :param Overwrite: 0：添加，1：覆盖\n        :type Overwrite: int\n        :param InstanceId: NAT实例ID, 参数Area存在的时候这个必传\n        :type InstanceId: str\n        :param From: portScan: 来自于端口扫描, patchImport: 来自于批量导入\n        :type From: str\n        :param Area: NAT地域\n        :type Area: str\n        """
        self.Data = None
        self.Type = None
        self.EdgeId = None
        self.Enable = None
        self.Overwrite = None
        self.InstanceId = None
        self.From = None
        self.Area = None


    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = RuleInfoData()
                obj._deserialize(item)
                self.Data.append(obj)
        self.Type = params.get("Type")
        self.EdgeId = params.get("EdgeId")
        self.Enable = params.get("Enable")
        self.Overwrite = params.get("Overwrite")
        self.InstanceId = params.get("InstanceId")
        self.From = params.get("From")
        self.Area = params.get("Area")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateAcRulesResponse(AbstractModel):
    """CreateAcRules返回参数结构体

    """

    def __init__(self):
        """
        :param Status: 状态值，0:操作成功\n        :type Status: int\n        :param Info: 返回多余的信息
注意：此字段可能返回 null，表示取不到有效值。\n        :type Info: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Status = None
        self.Info = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.Info = params.get("Info")
        self.RequestId = params.get("RequestId")


class CreateChooseVpcsRequest(AbstractModel):
    """CreateChooseVpcs请求参数结构体

    """

    def __init__(self):
        """
        :param VpcList: vpc列表\n        :type VpcList: list of str\n        :param AllZoneList: zone列表\n        :type AllZoneList: list of VpcZoneData\n        """
        self.VpcList = None
        self.AllZoneList = None


    def _deserialize(self, params):
        self.VpcList = params.get("VpcList")
        if params.get("AllZoneList") is not None:
            self.AllZoneList = []
            for item in params.get("AllZoneList"):
                obj = VpcZoneData()
                obj._deserialize(item)
                self.AllZoneList.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateChooseVpcsResponse(AbstractModel):
    """CreateChooseVpcs返回参数结构体

    """

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateNatFwInstanceRequest(AbstractModel):
    """CreateNatFwInstance请求参数结构体

    """

    def __init__(self):
        """
        :param Name: 防火墙实例名称\n        :type Name: str\n        :param Width: 带宽\n        :type Width: int\n        :param Mode: 模式 1：接入模式；0：新增模式\n        :type Mode: int\n        :param NewModeItems: 新增模式传递参数，其中NewModeItems和NatgwList至少传递一种。\n        :type NewModeItems: :class:`tencentcloud.cfw.v20190904.models.NewModeItems`\n        :param NatGwList: 接入模式接入的nat网关列表，其中NewModeItems和NatgwList至少传递一种。\n        :type NatGwList: list of str\n        :param Zone: 主可用区，为空则选择默认可用区\n        :type Zone: str\n        :param ZoneBak: 备可用区，为空则选择默认可用区\n        :type ZoneBak: str\n        :param CrossAZone: 异地灾备 1：使用异地灾备；0：不使用异地灾备\n        :type CrossAZone: int\n        """
        self.Name = None
        self.Width = None
        self.Mode = None
        self.NewModeItems = None
        self.NatGwList = None
        self.Zone = None
        self.ZoneBak = None
        self.CrossAZone = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Width = params.get("Width")
        self.Mode = params.get("Mode")
        if params.get("NewModeItems") is not None:
            self.NewModeItems = NewModeItems()
            self.NewModeItems._deserialize(params.get("NewModeItems"))
        self.NatGwList = params.get("NatGwList")
        self.Zone = params.get("Zone")
        self.ZoneBak = params.get("ZoneBak")
        self.CrossAZone = params.get("CrossAZone")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateNatFwInstanceResponse(AbstractModel):
    """CreateNatFwInstance返回参数结构体

    """

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateSecurityGroupApiRulesRequest(AbstractModel):
    """CreateSecurityGroupApiRules请求参数结构体

    """

    def __init__(self):
        """
        :param Data: 创建规则数据\n        :type Data: list of SecurityGroupApiRuleData\n        :param Direction: 方向，0：出站，1：入站\n        :type Direction: int\n        :param Type: 插入类型，0：后插，1：前插，2：中插\n        :type Type: int\n        :param Area: 腾讯云地域的英文简写\n        :type Area: str\n        """
        self.Data = None
        self.Direction = None
        self.Type = None
        self.Area = None


    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = SecurityGroupApiRuleData()
                obj._deserialize(item)
                self.Data.append(obj)
        self.Direction = params.get("Direction")
        self.Type = params.get("Type")
        self.Area = params.get("Area")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateSecurityGroupApiRulesResponse(AbstractModel):
    """CreateSecurityGroupApiRules返回参数结构体

    """

    def __init__(self):
        """
        :param Status: 状态值，0:添加成功，非0：添加失败\n        :type Status: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class CreateSecurityGroupRulesRequest(AbstractModel):
    """CreateSecurityGroupRules请求参数结构体

    """

    def __init__(self):
        """
        :param Data: 添加的企业安全组规则数据\n        :type Data: list of SecurityGroupListData\n        :param Direction: 方向，0：出站，1：入站，默认1\n        :type Direction: int\n        :param Type: 0：后插，1：前插，2：中插，默认0\n        :type Type: int\n        :param Enable: 添加后是否启用规则，0：不启用，1：启用，默认1\n        :type Enable: int\n        """
        self.Data = None
        self.Direction = None
        self.Type = None
        self.Enable = None


    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = SecurityGroupListData()
                obj._deserialize(item)
                self.Data.append(obj)
        self.Direction = params.get("Direction")
        self.Type = params.get("Type")
        self.Enable = params.get("Enable")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateSecurityGroupRulesResponse(AbstractModel):
    """CreateSecurityGroupRules返回参数结构体

    """

    def __init__(self):
        """
        :param Status: 状态值，0：添加成功，非0：添加失败\n        :type Status: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class DeleteAcRuleRequest(AbstractModel):
    """DeleteAcRule请求参数结构体

    """

    def __init__(self):
        """
        :param Id: 删除规则对应的id值, 对应获取规则列表接口的Id 值\n        :type Id: int\n        :param Direction: 方向，0：出站，1：入站\n        :type Direction: int\n        :param EdgeId: EdgeId值两个vpc间的边id\n        :type EdgeId: str\n        :param Area: NAT地域， 如ap-shanghai/ap-guangzhou/ap-chongqing等\n        :type Area: str\n        """
        self.Id = None
        self.Direction = None
        self.EdgeId = None
        self.Area = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Direction = params.get("Direction")
        self.EdgeId = params.get("EdgeId")
        self.Area = params.get("Area")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteAcRuleResponse(AbstractModel):
    """DeleteAcRule返回参数结构体

    """

    def __init__(self):
        """
        :param Status: 状态值 0: 删除成功, !0: 删除失败\n        :type Status: int\n        :param Info: 返回多余的信息
注意：此字段可能返回 null，表示取不到有效值。\n        :type Info: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Status = None
        self.Info = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.Info = params.get("Info")
        self.RequestId = params.get("RequestId")


class DeleteAllAccessControlRuleRequest(AbstractModel):
    """DeleteAllAccessControlRule请求参数结构体

    """

    def __init__(self):
        """
        :param Direction: 方向，0：出站，1：入站  默认值是 0\n        :type Direction: int\n        :param EdgeId: VPC间防火墙开关ID  全部删除 EdgeId和Area只填写一个，不填写则不删除vpc间防火墙开关 ，默认值为‘’\n        :type EdgeId: str\n        :param Area: nat地域 全部删除 EdgeId和Area只填写一个，不填写则不删除nat防火墙开关 默认值为‘’\n        :type Area: str\n        """
        self.Direction = None
        self.EdgeId = None
        self.Area = None


    def _deserialize(self, params):
        self.Direction = params.get("Direction")
        self.EdgeId = params.get("EdgeId")
        self.Area = params.get("Area")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteAllAccessControlRuleResponse(AbstractModel):
    """DeleteAllAccessControlRule返回参数结构体

    """

    def __init__(self):
        """
        :param Status: 状态值 0: 修改成功, !0: 修改失败\n        :type Status: int\n        :param Info: 删除了几条访问控制规则
注意：此字段可能返回 null，表示取不到有效值。\n        :type Info: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Status = None
        self.Info = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.Info = params.get("Info")
        self.RequestId = params.get("RequestId")


class DeleteNatFwInstanceRequest(AbstractModel):
    """DeleteNatFwInstance请求参数结构体

    """

    def __init__(self):
        """
        :param CfwInstance: 防火墙实例id\n        :type CfwInstance: str\n        """
        self.CfwInstance = None


    def _deserialize(self, params):
        self.CfwInstance = params.get("CfwInstance")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteNatFwInstanceResponse(AbstractModel):
    """DeleteNatFwInstance返回参数结构体

    """

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteResourceGroupRequest(AbstractModel):
    """DeleteResourceGroup请求参数结构体

    """

    def __init__(self):
        """
        :param GroupId: 组id\n        :type GroupId: str\n        """
        self.GroupId = None


    def _deserialize(self, params):
        self.GroupId = params.get("GroupId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteResourceGroupResponse(AbstractModel):
    """DeleteResourceGroup返回参数结构体

    """

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteSecurityGroupAllRuleRequest(AbstractModel):
    """DeleteSecurityGroupAllRule请求参数结构体

    """

    def __init__(self):
        """
        :param Direction: 方向，0：出站，1：入站\n        :type Direction: int\n        :param Area: 腾讯云地域的英文简写\n        :type Area: str\n        """
        self.Direction = None
        self.Area = None


    def _deserialize(self, params):
        self.Direction = params.get("Direction")
        self.Area = params.get("Area")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteSecurityGroupAllRuleResponse(AbstractModel):
    """DeleteSecurityGroupAllRule返回参数结构体

    """

    def __init__(self):
        """
        :param Status: 0: 操作成功，非0：操作失败\n        :type Status: int\n        :param Info: 返回数据的json字符串
注意：此字段可能返回 null，表示取不到有效值。\n        :type Info: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Status = None
        self.Info = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.Info = params.get("Info")
        self.RequestId = params.get("RequestId")


class DeleteSecurityGroupRuleRequest(AbstractModel):
    """DeleteSecurityGroupRule请求参数结构体

    """

    def __init__(self):
        """
        :param Id: 所需要删除规则的ID\n        :type Id: int\n        :param Area: 腾讯云地域的英文简写\n        :type Area: str\n        :param Direction: 方向，0：出站，1：入站\n        :type Direction: int\n        :param IsDelReverse: 是否删除反向规则，0：否，1：是\n        :type IsDelReverse: int\n        """
        self.Id = None
        self.Area = None
        self.Direction = None
        self.IsDelReverse = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Area = params.get("Area")
        self.Direction = params.get("Direction")
        self.IsDelReverse = params.get("IsDelReverse")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteSecurityGroupRuleResponse(AbstractModel):
    """DeleteSecurityGroupRule返回参数结构体

    """

    def __init__(self):
        """
        :param Status: 状态值，0：成功，非0：失败\n        :type Status: int\n        :param Info: 返回多余的信息
注意：此字段可能返回 null，表示取不到有效值。\n        :type Info: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Status = None
        self.Info = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.Info = params.get("Info")
        self.RequestId = params.get("RequestId")


class DeleteVpcInstanceRequest(AbstractModel):
    """DeleteVpcInstance请求参数结构体

    """


class DeleteVpcInstanceResponse(AbstractModel):
    """DeleteVpcInstance返回参数结构体

    """

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeAcListsRequest(AbstractModel):
    """DescribeAcLists请求参数结构体

    """

    def __init__(self):
        """
        :param Protocol: 协议\n        :type Protocol: str\n        :param Strategy: 策略\n        :type Strategy: str\n        :param SearchValue: 搜索值\n        :type SearchValue: str\n        :param Limit: 每页条数\n        :type Limit: int\n        :param Offset: 偏移值\n        :type Offset: int\n        :param Direction: 出站还是入站，0：入站，1：出站\n        :type Direction: int\n        :param EdgeId: EdgeId值\n        :type EdgeId: str\n        :param Status: 规则是否开启，'0': 未开启，'1': 开启, 默认为'0'\n        :type Status: str\n        :param Area: 地域\n        :type Area: str\n        :param InstanceId: 实例ID\n        :type InstanceId: str\n        """
        self.Protocol = None
        self.Strategy = None
        self.SearchValue = None
        self.Limit = None
        self.Offset = None
        self.Direction = None
        self.EdgeId = None
        self.Status = None
        self.Area = None
        self.InstanceId = None


    def _deserialize(self, params):
        self.Protocol = params.get("Protocol")
        self.Strategy = params.get("Strategy")
        self.SearchValue = params.get("SearchValue")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.Direction = params.get("Direction")
        self.EdgeId = params.get("EdgeId")
        self.Status = params.get("Status")
        self.Area = params.get("Area")
        self.InstanceId = params.get("InstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAcListsResponse(AbstractModel):
    """DescribeAcLists返回参数结构体

    """

    def __init__(self):
        """
        :param Total: 总条数\n        :type Total: int\n        :param Data: 访问控制列表数据\n        :type Data: list of AcListsData\n        :param AllTotal: 不算筛选条数的总条数\n        :type AllTotal: int\n        :param Enable: 访问控制规则全部启用/全部停用
注意：此字段可能返回 null，表示取不到有效值。\n        :type Enable: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Total = None
        self.Data = None
        self.AllTotal = None
        self.Enable = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = AcListsData()
                obj._deserialize(item)
                self.Data.append(obj)
        self.AllTotal = params.get("AllTotal")
        self.Enable = params.get("Enable")
        self.RequestId = params.get("RequestId")


class DescribeAssociatedInstanceListRequest(AbstractModel):
    """DescribeAssociatedInstanceList请求参数结构体

    """

    def __init__(self):
        """
        :param Offset: 列表偏移量\n        :type Offset: int\n        :param Limit: 每页记录条数\n        :type Limit: int\n        :param Area: 地域代码（例：ap-guangzhou）,支持腾讯云全地域\n        :type Area: str\n        :param SearchValue: 额外检索条件（JSON字符串）\n        :type SearchValue: str\n        :param By: 排序字段\n        :type By: str\n        :param Order: 排序方式（asc:升序,desc:降序）\n        :type Order: str\n        :param SecurityGroupId: 安全组ID\n        :type SecurityGroupId: str\n        :param Type: 实例类型,'3'是cvm实例,'4'是clb实例,'5'是eni实例,'6'是云数据库\n        :type Type: str\n        """
        self.Offset = None
        self.Limit = None
        self.Area = None
        self.SearchValue = None
        self.By = None
        self.Order = None
        self.SecurityGroupId = None
        self.Type = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.Area = params.get("Area")
        self.SearchValue = params.get("SearchValue")
        self.By = params.get("By")
        self.Order = params.get("Order")
        self.SecurityGroupId = params.get("SecurityGroupId")
        self.Type = params.get("Type")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAssociatedInstanceListResponse(AbstractModel):
    """DescribeAssociatedInstanceList返回参数结构体

    """

    def __init__(self):
        """
        :param Total: 实例数量
注意：此字段可能返回 null，表示取不到有效值。\n        :type Total: int\n        :param Data: 实例列表
注意：此字段可能返回 null，表示取不到有效值。\n        :type Data: list of AssociatedInstanceInfo\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Total = None
        self.Data = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = AssociatedInstanceInfo()
                obj._deserialize(item)
                self.Data.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeBlockByIpTimesListRequest(AbstractModel):
    """DescribeBlockByIpTimesList请求参数结构体

    """

    def __init__(self):
        """
        :param StartTime: 开始时间\n        :type StartTime: str\n        :param EndTime: 结束时间\n        :type EndTime: str\n        :param Ip: ip查询条件\n        :type Ip: str\n        :param Zone: 地域\n        :type Zone: str\n        :param Direction: 方向\n        :type Direction: str\n        :param Source: 来源\n        :type Source: str\n        """
        self.StartTime = None
        self.EndTime = None
        self.Ip = None
        self.Zone = None
        self.Direction = None
        self.Source = None


    def _deserialize(self, params):
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Ip = params.get("Ip")
        self.Zone = params.get("Zone")
        self.Direction = params.get("Direction")
        self.Source = params.get("Source")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBlockByIpTimesListResponse(AbstractModel):
    """DescribeBlockByIpTimesList返回参数结构体

    """

    def __init__(self):
        """
        :param Data: 返回数据\n        :type Data: list of IpStatic\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Data = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = IpStatic()
                obj._deserialize(item)
                self.Data.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeBlockStaticListRequest(AbstractModel):
    """DescribeBlockStaticList请求参数结构体

    """

    def __init__(self):
        """
        :param StartTime: 开始时间\n        :type StartTime: str\n        :param EndTime: 结束时间\n        :type EndTime: str\n        :param QueryType: 类型\n        :type QueryType: str\n        :param Top: top数\n        :type Top: int\n        :param SearchValue: 查询条件\n        :type SearchValue: str\n        """
        self.StartTime = None
        self.EndTime = None
        self.QueryType = None
        self.Top = None
        self.SearchValue = None


    def _deserialize(self, params):
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.QueryType = params.get("QueryType")
        self.Top = params.get("Top")
        self.SearchValue = params.get("SearchValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBlockStaticListResponse(AbstractModel):
    """DescribeBlockStaticList返回参数结构体

    """

    def __init__(self):
        """
        :param Data: 无\n        :type Data: list of StaticInfo\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Data = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = StaticInfo()
                obj._deserialize(item)
                self.Data.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeCfwEipsRequest(AbstractModel):
    """DescribeCfwEips请求参数结构体

    """

    def __init__(self):
        """
        :param Mode: 0：cfw新增模式，1：cfw接入模式\n        :type Mode: int\n        :param NatGatewayId: ALL：查询所有弹性公网ip; nat-xxxxx：接入模式场景指定网关的弹性公网ip\n        :type NatGatewayId: str\n        :param CfwInstance: 防火墙实例id\n        :type CfwInstance: str\n        """
        self.Mode = None
        self.NatGatewayId = None
        self.CfwInstance = None


    def _deserialize(self, params):
        self.Mode = params.get("Mode")
        self.NatGatewayId = params.get("NatGatewayId")
        self.CfwInstance = params.get("CfwInstance")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeCfwEipsResponse(AbstractModel):
    """DescribeCfwEips返回参数结构体

    """

    def __init__(self):
        """
        :param NatFwEipList: 返回值信息\n        :type NatFwEipList: list of NatFwEipsInfo\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.NatFwEipList = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("NatFwEipList") is not None:
            self.NatFwEipList = []
            for item in params.get("NatFwEipList"):
                obj = NatFwEipsInfo()
                obj._deserialize(item)
                self.NatFwEipList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeGuideScanInfoRequest(AbstractModel):
    """DescribeGuideScanInfo请求参数结构体

    """


class DescribeGuideScanInfoResponse(AbstractModel):
    """DescribeGuideScanInfo返回参数结构体

    """

    def __init__(self):
        """
        :param Data: 扫描信息\n        :type Data: :class:`tencentcloud.cfw.v20190904.models.ScanInfo`\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Data = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = ScanInfo()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeNatFwInfoCountRequest(AbstractModel):
    """DescribeNatFwInfoCount请求参数结构体

    """


class DescribeNatFwInfoCountResponse(AbstractModel):
    """DescribeNatFwInfoCount返回参数结构体

    """

    def __init__(self):
        """
        :param ReturnMsg: 返回参数
注意：此字段可能返回 null，表示取不到有效值。\n        :type ReturnMsg: str\n        :param NatFwInsCount: 当前租户的nat实例个数
注意：此字段可能返回 null，表示取不到有效值。\n        :type NatFwInsCount: int\n        :param SubnetCount: 当前租户接入子网个数
注意：此字段可能返回 null，表示取不到有效值。\n        :type SubnetCount: int\n        :param OpenSwitchCount: 打开开关个数
注意：此字段可能返回 null，表示取不到有效值。\n        :type OpenSwitchCount: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.ReturnMsg = None
        self.NatFwInsCount = None
        self.SubnetCount = None
        self.OpenSwitchCount = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ReturnMsg = params.get("ReturnMsg")
        self.NatFwInsCount = params.get("NatFwInsCount")
        self.SubnetCount = params.get("SubnetCount")
        self.OpenSwitchCount = params.get("OpenSwitchCount")
        self.RequestId = params.get("RequestId")


class DescribeNatFwInstanceRequest(AbstractModel):
    """DescribeNatFwInstance请求参数结构体

    """


class DescribeNatFwInstanceResponse(AbstractModel):
    """DescribeNatFwInstance返回参数结构体

    """

    def __init__(self):
        """
        :param NatinsLst: 实例数组\n        :type NatinsLst: list of NatFwInstance\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.NatinsLst = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("NatinsLst") is not None:
            self.NatinsLst = []
            for item in params.get("NatinsLst"):
                obj = NatFwInstance()
                obj._deserialize(item)
                self.NatinsLst.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeNatFwInstanceWithRegionRequest(AbstractModel):
    """DescribeNatFwInstanceWithRegion请求参数结构体

    """


class DescribeNatFwInstanceWithRegionResponse(AbstractModel):
    """DescribeNatFwInstanceWithRegion返回参数结构体

    """

    def __init__(self):
        """
        :param NatinsLst: 实例数组
注意：此字段可能返回 null，表示取不到有效值。\n        :type NatinsLst: list of NatFwInstance\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.NatinsLst = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("NatinsLst") is not None:
            self.NatinsLst = []
            for item in params.get("NatinsLst"):
                obj = NatFwInstance()
                obj._deserialize(item)
                self.NatinsLst.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeNatFwInstancesInfoRequest(AbstractModel):
    """DescribeNatFwInstancesInfo请求参数结构体

    """

    def __init__(self):
        """
        :param Filter: 获取实例列表过滤字段\n        :type Filter: list of NatFwFilter\n        :param Offset: 第几页\n        :type Offset: int\n        :param Limit: 每页长度\n        :type Limit: int\n        """
        self.Filter = None
        self.Offset = None
        self.Limit = None


    def _deserialize(self, params):
        if params.get("Filter") is not None:
            self.Filter = []
            for item in params.get("Filter"):
                obj = NatFwFilter()
                obj._deserialize(item)
                self.Filter.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeNatFwInstancesInfoResponse(AbstractModel):
    """DescribeNatFwInstancesInfo返回参数结构体

    """

    def __init__(self):
        """
        :param NatinsLst: 实例卡片信息数组
注意：此字段可能返回 null，表示取不到有效值。\n        :type NatinsLst: list of NatInstanceInfo\n        :param Total: 总共多少条数
注意：此字段可能返回 null，表示取不到有效值。\n        :type Total: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.NatinsLst = None
        self.Total = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("NatinsLst") is not None:
            self.NatinsLst = []
            for item in params.get("NatinsLst"):
                obj = NatInstanceInfo()
                obj._deserialize(item)
                self.NatinsLst.append(obj)
        self.Total = params.get("Total")
        self.RequestId = params.get("RequestId")


class DescribeNatFwVpcDnsLstRequest(AbstractModel):
    """DescribeNatFwVpcDnsLst请求参数结构体

    """

    def __init__(self):
        """
        :param NatFwInsId: natfw 防火墙实例id\n        :type NatFwInsId: str\n        :param NatInsIdFilter: natfw 过滤，以','分隔\n        :type NatInsIdFilter: str\n        :param Offset: 分页页数\n        :type Offset: int\n        :param Limit: 每页最多个数\n        :type Limit: int\n        """
        self.NatFwInsId = None
        self.NatInsIdFilter = None
        self.Offset = None
        self.Limit = None


    def _deserialize(self, params):
        self.NatFwInsId = params.get("NatFwInsId")
        self.NatInsIdFilter = params.get("NatInsIdFilter")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeNatFwVpcDnsLstResponse(AbstractModel):
    """DescribeNatFwVpcDnsLst返回参数结构体

    """

    def __init__(self):
        """
        :param VpcDnsSwitchLst: nat防火墙vpc dns 信息数组
注意：此字段可能返回 null，表示取不到有效值。\n        :type VpcDnsSwitchLst: list of VpcDnsInfo\n        :param ReturnMsg: 返回参数
注意：此字段可能返回 null，表示取不到有效值。\n        :type ReturnMsg: str\n        :param Total: 开关总条数
注意：此字段可能返回 null，表示取不到有效值。\n        :type Total: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.VpcDnsSwitchLst = None
        self.ReturnMsg = None
        self.Total = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("VpcDnsSwitchLst") is not None:
            self.VpcDnsSwitchLst = []
            for item in params.get("VpcDnsSwitchLst"):
                obj = VpcDnsInfo()
                obj._deserialize(item)
                self.VpcDnsSwitchLst.append(obj)
        self.ReturnMsg = params.get("ReturnMsg")
        self.Total = params.get("Total")
        self.RequestId = params.get("RequestId")


class DescribeNatRuleOverviewRequest(AbstractModel):
    """DescribeNatRuleOverview请求参数结构体

    """

    def __init__(self):
        """
        :param Direction: 方向，0：出站，1：入站 默认值：0\n        :type Direction: int\n        :param Area: NAT地域  这个是必填项，填入相关的英文，'ap-beijing-fsi': '北京金融',
        'ap-beijing': '北京',
        'ap-changsha-ec': '长沙EC',
        'ap-chengdu': '成都',
        'ap-chongqing': '重庆',
        'ap-fuzhou-ec': '福州EC',
        'ap-guangzhou-open': '广州Open',
        'ap-guangzhou': '广州',
        'ap-hangzhou-ec': '杭州EC',
        'ap-jinan-ec': '济南EC',
        'ap-nanjing': '南京',
        'ap-shanghai-fsi': '上海金融',
        'ap-shanghai': '上海',
        'ap-shenzhen-fsi': '深圳金融',
        'ap-shenzhen': '深圳',
        'ap-wuhan-ec': '武汉EC'\n        :type Area: str\n        """
        self.Direction = None
        self.Area = None


    def _deserialize(self, params):
        self.Direction = params.get("Direction")
        self.Area = params.get("Area")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeNatRuleOverviewResponse(AbstractModel):
    """DescribeNatRuleOverview返回参数结构体

    """

    def __init__(self):
        """
        :param InstanceId: 实例ID\n        :type InstanceId: str\n        :param InstanceName: 实例名称\n        :type InstanceName: str\n        :param EipList: 弹性IP列表\n        :type EipList: list of str\n        :param DnatNum: 端口转发规则数量\n        :type DnatNum: int\n        :param TotalNum: 访问控制规则总数\n        :type TotalNum: int\n        :param RemainNum: 访问控制规则剩余配额\n        :type RemainNum: int\n        :param BlockNum: 阻断规则条数\n        :type BlockNum: int\n        :param EnableNum: 启用规则条数\n        :type EnableNum: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.InstanceId = None
        self.InstanceName = None
        self.EipList = None
        self.DnatNum = None
        self.TotalNum = None
        self.RemainNum = None
        self.BlockNum = None
        self.EnableNum = None
        self.RequestId = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        self.EipList = params.get("EipList")
        self.DnatNum = params.get("DnatNum")
        self.TotalNum = params.get("TotalNum")
        self.RemainNum = params.get("RemainNum")
        self.BlockNum = params.get("BlockNum")
        self.EnableNum = params.get("EnableNum")
        self.RequestId = params.get("RequestId")


class DescribeResourceGroupRequest(AbstractModel):
    """DescribeResourceGroup请求参数结构体

    """

    def __init__(self):
        """
        :param QueryType: 查询类型 网络结构 vpc，业务识别- resource ，资源标签-tag\n        :type QueryType: str\n        :param GroupId: 资产组id  全部传0\n        :type GroupId: str\n        """
        self.QueryType = None
        self.GroupId = None


    def _deserialize(self, params):
        self.QueryType = params.get("QueryType")
        self.GroupId = params.get("GroupId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeResourceGroupResponse(AbstractModel):
    """DescribeResourceGroup返回参数结构体

    """

    def __init__(self):
        """
        :param Data: 返回树形结构\n        :type Data: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Data = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Data = params.get("Data")
        self.RequestId = params.get("RequestId")


class DescribeRuleOverviewRequest(AbstractModel):
    """DescribeRuleOverview请求参数结构体

    """

    def __init__(self):
        """
        :param Direction: 方向，0：出站，1：入站\n        :type Direction: int\n        """
        self.Direction = None


    def _deserialize(self, params):
        self.Direction = params.get("Direction")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeRuleOverviewResponse(AbstractModel):
    """DescribeRuleOverview返回参数结构体

    """

    def __init__(self):
        """
        :param AllTotal: 规则总数
注意：此字段可能返回 null，表示取不到有效值。\n        :type AllTotal: int\n        :param StrategyNum: 阻断策略规则数量
注意：此字段可能返回 null，表示取不到有效值。\n        :type StrategyNum: int\n        :param StartRuleNum: 启用规则数量
注意：此字段可能返回 null，表示取不到有效值。\n        :type StartRuleNum: int\n        :param StopRuleNum: 停用规则数量
注意：此字段可能返回 null，表示取不到有效值。\n        :type StopRuleNum: int\n        :param RemainingNum: 剩余配额
注意：此字段可能返回 null，表示取不到有效值。\n        :type RemainingNum: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.AllTotal = None
        self.StrategyNum = None
        self.StartRuleNum = None
        self.StopRuleNum = None
        self.RemainingNum = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AllTotal = params.get("AllTotal")
        self.StrategyNum = params.get("StrategyNum")
        self.StartRuleNum = params.get("StartRuleNum")
        self.StopRuleNum = params.get("StopRuleNum")
        self.RemainingNum = params.get("RemainingNum")
        self.RequestId = params.get("RequestId")


class DescribeSecurityGroupListRequest(AbstractModel):
    """DescribeSecurityGroupList请求参数结构体

    """

    def __init__(self):
        """
        :param Direction: 0: 出站规则，1：入站规则\n        :type Direction: int\n        :param Area: 地域代码（例: ap-guangzhou),支持腾讯云全部地域\n        :type Area: str\n        :param SearchValue: 搜索值\n        :type SearchValue: str\n        :param Limit: 每页条数，默认为10\n        :type Limit: int\n        :param Offset: 偏移值，默认为0\n        :type Offset: int\n        :param Status: 状态，'': 全部，'0'：筛选停用规则，'1'：筛选启用规则\n        :type Status: str\n        :param Filter: 0: 不过滤，1：过滤掉正常规则，保留下发异常规则\n        :type Filter: int\n        """
        self.Direction = None
        self.Area = None
        self.SearchValue = None
        self.Limit = None
        self.Offset = None
        self.Status = None
        self.Filter = None


    def _deserialize(self, params):
        self.Direction = params.get("Direction")
        self.Area = params.get("Area")
        self.SearchValue = params.get("SearchValue")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.Status = params.get("Status")
        self.Filter = params.get("Filter")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSecurityGroupListResponse(AbstractModel):
    """DescribeSecurityGroupList返回参数结构体

    """

    def __init__(self):
        """
        :param Total: 列表当前规则总条数\n        :type Total: int\n        :param Data: 安全组规则列表数据\n        :type Data: list of SecurityGroupListData\n        :param AllTotal: 不算筛选条数的总条数\n        :type AllTotal: int\n        :param Enable: 访问控制规则全部启用/全部停用
注意：此字段可能返回 null，表示取不到有效值。\n        :type Enable: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Total = None
        self.Data = None
        self.AllTotal = None
        self.Enable = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = SecurityGroupListData()
                obj._deserialize(item)
                self.Data.append(obj)
        self.AllTotal = params.get("AllTotal")
        self.Enable = params.get("Enable")
        self.RequestId = params.get("RequestId")


class DescribeSourceAssetRequest(AbstractModel):
    """DescribeSourceAsset请求参数结构体

    """

    def __init__(self):
        """
        :param FuzzySearch: 模糊查询\n        :type FuzzySearch: str\n        :param InsType: 资产类型 1公网 2内网\n        :type InsType: str\n        :param ChooseType: 是否未分组 1是\n        :type ChooseType: str\n        :param Zone: 地域\n        :type Zone: str\n        :param Limit: 页大小\n        :type Limit: int\n        :param Offset: 偏移量\n        :type Offset: int\n        """
        self.FuzzySearch = None
        self.InsType = None
        self.ChooseType = None
        self.Zone = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.FuzzySearch = params.get("FuzzySearch")
        self.InsType = params.get("InsType")
        self.ChooseType = params.get("ChooseType")
        self.Zone = params.get("Zone")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSourceAssetResponse(AbstractModel):
    """DescribeSourceAsset返回参数结构体

    """

    def __init__(self):
        """
        :param ZoneList: 地域集合\n        :type ZoneList: list of AssetZone\n        :param Data: 数据\n        :type Data: list of InstanceInfo\n        :param Total: 10\n        :type Total: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.ZoneList = None
        self.Data = None
        self.Total = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ZoneList") is not None:
            self.ZoneList = []
            for item in params.get("ZoneList"):
                obj = AssetZone()
                obj._deserialize(item)
                self.ZoneList.append(obj)
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = InstanceInfo()
                obj._deserialize(item)
                self.Data.append(obj)
        self.Total = params.get("Total")
        self.RequestId = params.get("RequestId")


class DescribeSwitchListsRequest(AbstractModel):
    """DescribeSwitchLists请求参数结构体

    """

    def __init__(self):
        """
        :param Status: 防火墙状态  0: 关闭，1：开启\n        :type Status: int\n        :param Type: 资产类型 CVM/NAT/VPN/CLB/其它\n        :type Type: str\n        :param Area: 地域 上海/重庆/广州，等等\n        :type Area: str\n        :param SearchValue: 搜索值  例子："{"common":"106.54.189.45"}"\n        :type SearchValue: str\n        :param Limit: 条数  默认值:10\n        :type Limit: int\n        :param Offset: 偏移值 默认值: 0\n        :type Offset: int\n        :param Order: 排序，desc：降序，asc：升序\n        :type Order: str\n        :param By: 排序字段 PortTimes(风险端口数)\n        :type By: str\n        """
        self.Status = None
        self.Type = None
        self.Area = None
        self.SearchValue = None
        self.Limit = None
        self.Offset = None
        self.Order = None
        self.By = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.Type = params.get("Type")
        self.Area = params.get("Area")
        self.SearchValue = params.get("SearchValue")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.Order = params.get("Order")
        self.By = params.get("By")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSwitchListsResponse(AbstractModel):
    """DescribeSwitchLists返回参数结构体

    """

    def __init__(self):
        """
        :param Total: 总条数\n        :type Total: int\n        :param Data: 列表数据\n        :type Data: list of SwitchListsData\n        :param AreaLists: 区域列表\n        :type AreaLists: list of str\n        :param OnNum: 打开个数
注意：此字段可能返回 null，表示取不到有效值。\n        :type OnNum: int\n        :param OffNum: 关闭个数
注意：此字段可能返回 null，表示取不到有效值。\n        :type OffNum: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Total = None
        self.Data = None
        self.AreaLists = None
        self.OnNum = None
        self.OffNum = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = SwitchListsData()
                obj._deserialize(item)
                self.Data.append(obj)
        self.AreaLists = params.get("AreaLists")
        self.OnNum = params.get("OnNum")
        self.OffNum = params.get("OffNum")
        self.RequestId = params.get("RequestId")


class DescribeSyncAssetStatusRequest(AbstractModel):
    """DescribeSyncAssetStatus请求参数结构体

    """

    def __init__(self):
        """
        :param Type: 0: 互联网防火墙开关，1：vpc 防火墙开关\n        :type Type: int\n        """
        self.Type = None


    def _deserialize(self, params):
        self.Type = params.get("Type")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSyncAssetStatusResponse(AbstractModel):
    """DescribeSyncAssetStatus返回参数结构体

    """

    def __init__(self):
        """
        :param Status: 1-更新中 2-更新完成 3、4-更新失败\n        :type Status: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class DescribeTLogInfoRequest(AbstractModel):
    """DescribeTLogInfo请求参数结构体

    """

    def __init__(self):
        """
        :param StartTime: 开始时间\n        :type StartTime: str\n        :param EndTime: 结束时间\n        :type EndTime: str\n        :param QueryType: 类型 1 告警 2阻断\n        :type QueryType: str\n        :param SearchValue: 查询条件\n        :type SearchValue: str\n        """
        self.StartTime = None
        self.EndTime = None
        self.QueryType = None
        self.SearchValue = None


    def _deserialize(self, params):
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.QueryType = params.get("QueryType")
        self.SearchValue = params.get("SearchValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTLogInfoResponse(AbstractModel):
    """DescribeTLogInfo返回参数结构体

    """

    def __init__(self):
        """
        :param Data: 无\n        :type Data: :class:`tencentcloud.cfw.v20190904.models.TLogInfo`\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Data = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = TLogInfo()
            self.Data._deserialize(params.get("Data"))
        self.RequestId = params.get("RequestId")


class DescribeTLogIpListRequest(AbstractModel):
    """DescribeTLogIpList请求参数结构体

    """

    def __init__(self):
        """
        :param StartTime: 开始时间\n        :type StartTime: str\n        :param EndTime: 结束时间\n        :type EndTime: str\n        :param QueryType: 类型 1 告警 2阻断\n        :type QueryType: str\n        :param Top: top数\n        :type Top: int\n        :param SearchValue: 查询条件\n        :type SearchValue: str\n        """
        self.StartTime = None
        self.EndTime = None
        self.QueryType = None
        self.Top = None
        self.SearchValue = None


    def _deserialize(self, params):
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.QueryType = params.get("QueryType")
        self.Top = params.get("Top")
        self.SearchValue = params.get("SearchValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTLogIpListResponse(AbstractModel):
    """DescribeTLogIpList返回参数结构体

    """

    def __init__(self):
        """
        :param Data: 数据集合\n        :type Data: list of StaticInfo\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Data = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = StaticInfo()
                obj._deserialize(item)
                self.Data.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeTableStatusRequest(AbstractModel):
    """DescribeTableStatus请求参数结构体

    """

    def __init__(self):
        """
        :param EdgeId: EdgeId值两个vpc间的边id vpc填Edgeid，不要填Area；\n        :type EdgeId: str\n        :param Status: 状态值，0：检查表的状态 确实只有一个默认值\n        :type Status: int\n        :param Area: Nat所在地域 NAT填Area，不要填Edgeid；\n        :type Area: str\n        :param Direction: 方向，0：出站，1：入站 默认值为 0\n        :type Direction: int\n        """
        self.EdgeId = None
        self.Status = None
        self.Area = None
        self.Direction = None


    def _deserialize(self, params):
        self.EdgeId = params.get("EdgeId")
        self.Status = params.get("Status")
        self.Area = params.get("Area")
        self.Direction = params.get("Direction")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTableStatusResponse(AbstractModel):
    """DescribeTableStatus返回参数结构体

    """

    def __init__(self):
        """
        :param Status: 0：正常，其它：不正常
注意：此字段可能返回 null，表示取不到有效值。\n        :type Status: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class DescribeUnHandleEventTabListRequest(AbstractModel):
    """DescribeUnHandleEventTabList请求参数结构体

    """

    def __init__(self):
        """
        :param StartTime: 开始时间\n        :type StartTime: str\n        :param EndTime: 结束时间\n        :type EndTime: str\n        :param AssetID: 查询示例ID\n        :type AssetID: str\n        """
        self.StartTime = None
        self.EndTime = None
        self.AssetID = None


    def _deserialize(self, params):
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.AssetID = params.get("AssetID")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeUnHandleEventTabListResponse(AbstractModel):
    """DescribeUnHandleEventTabList返回参数结构体

    """

    def __init__(self):
        """
        :param Data: 租户伪攻击链未处置事件
注意：此字段可能返回 null，表示取不到有效值。\n        :type Data: :class:`tencentcloud.cfw.v20190904.models.UnHandleEvent`\n        :param ReturnCode: 错误码，0成功 非0错误\n        :type ReturnCode: int\n        :param ReturnMsg: 返回信息 success成功\n        :type ReturnMsg: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Data = None
        self.ReturnCode = None
        self.ReturnMsg = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = UnHandleEvent()
            self.Data._deserialize(params.get("Data"))
        self.ReturnCode = params.get("ReturnCode")
        self.ReturnMsg = params.get("ReturnMsg")
        self.RequestId = params.get("RequestId")


class DescribeVpcRuleOverviewRequest(AbstractModel):
    """DescribeVpcRuleOverview请求参数结构体

    """

    def __init__(self):
        """
        :param EdgeId: EdgeId值两个vpc间的边id  不是必填项可以为空，就是所有vpc间的访问控制规则\n        :type EdgeId: str\n        """
        self.EdgeId = None


    def _deserialize(self, params):
        self.EdgeId = params.get("EdgeId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeVpcRuleOverviewResponse(AbstractModel):
    """DescribeVpcRuleOverview返回参数结构体

    """

    def __init__(self):
        """
        :param StrategyNum: 阻断策略规则数量
注意：此字段可能返回 null，表示取不到有效值。\n        :type StrategyNum: int\n        :param StartRuleNum: 启用规则数量
注意：此字段可能返回 null，表示取不到有效值。\n        :type StartRuleNum: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.StrategyNum = None
        self.StartRuleNum = None
        self.RequestId = None


    def _deserialize(self, params):
        self.StrategyNum = params.get("StrategyNum")
        self.StartRuleNum = params.get("StartRuleNum")
        self.RequestId = params.get("RequestId")


class DnsVpcSwitch(AbstractModel):
    """设置nat防火墙的vpc dns 接入开关

    """

    def __init__(self):
        """
        :param VpcId: vpc id\n        :type VpcId: str\n        :param Status: 0：设置为关闭 1:设置为打开\n        :type Status: int\n        """
        self.VpcId = None
        self.Status = None


    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.Status = params.get("Status")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ExpandCfwVerticalRequest(AbstractModel):
    """ExpandCfwVertical请求参数结构体

    """

    def __init__(self):
        """
        :param FwType: nat：nat防火墙，ew：东西向防火墙\n        :type FwType: str\n        :param Width: 带宽值\n        :type Width: int\n        :param CfwInstance: 防火墙实例id\n        :type CfwInstance: str\n        """
        self.FwType = None
        self.Width = None
        self.CfwInstance = None


    def _deserialize(self, params):
        self.FwType = params.get("FwType")
        self.Width = params.get("Width")
        self.CfwInstance = params.get("CfwInstance")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ExpandCfwVerticalResponse(AbstractModel):
    """ExpandCfwVertical返回参数结构体

    """

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class InstanceInfo(AbstractModel):
    """// InstanceInfo 实例详情结果
    type InstanceInfo struct {
    	AppID        string `json:"AppId" gorm:"column:appid"`
    	Region       string `json:"Region" gorm:"column:region"`
    	VPCID        string `json:"VpcId" gorm:"column:vpc_id"`
    	SubNetID     string `json:"SubnetId" gorm:"column:subnet_id"`
    	InstanceID   string `json:"InstanceId" gorm:"column:instance_id"`
    	InstanceName string `json:"InstanceName" gorm:"column:instance_name"`
    	//InsType common.CVM 3是cvm实例,4是clb实例,5是eni实例,6是mysql,7是redis,8是NAT,9是VPN,10是ES,11是MARIADB,12是KAFKA
    	InsType   int    `json:"InsType" gorm:"column:instance_type"`
    	PublicIP  string `json:"PublicIp" gorm:"column:public_ip"`
    	PrivateIP string `json:"PrivateIp" gorm:"column:ip"`

    	//规则下发无需管，前端展示用
    	PortNum          string `json:"PortNum" gorm:"column:port_num"`
    	LeakNum          string `json:"LeakNum" gorm:"column:leak_num"`
    	ResourceGroupNum int    `json:"ResourceGroupNum"`
    	VPCName          string `json:"VPCName" gorm:"column:VPCName"`
    }

    """

    def __init__(self):
        """
        :param AppId: appid信息\n        :type AppId: str\n        :param Region: 地域\n        :type Region: str\n        :param VpcId: vpcid信息\n        :type VpcId: str\n        :param VPCName: vpc名称\n        :type VPCName: str\n        :param SubnetId: 子网id\n        :type SubnetId: str\n        :param InstanceId: 资产id\n        :type InstanceId: str\n        :param InstanceName: 资产名\n        :type InstanceName: str\n        :param InsType: 资产类型
 3是cvm实例,4是clb实例,5是eni实例,6是mysql,7是redis,8是NAT,9是VPN,10是ES,11是MARIADB,12是KAFKA 13 NATFW\n        :type InsType: int\n        :param PublicIp: 公网ip\n        :type PublicIp: str\n        :param PrivateIp: 内网ip\n        :type PrivateIp: str\n        :param PortNum: 端口数\n        :type PortNum: str\n        :param LeakNum: 漏洞数\n        :type LeakNum: str\n        :param InsSource: 1，公网 2内网\n        :type InsSource: str\n        :param ResourcePath: [a,b]
注意：此字段可能返回 null，表示取不到有效值。\n        :type ResourcePath: list of str\n        """
        self.AppId = None
        self.Region = None
        self.VpcId = None
        self.VPCName = None
        self.SubnetId = None
        self.InstanceId = None
        self.InstanceName = None
        self.InsType = None
        self.PublicIp = None
        self.PrivateIp = None
        self.PortNum = None
        self.LeakNum = None
        self.InsSource = None
        self.ResourcePath = None


    def _deserialize(self, params):
        self.AppId = params.get("AppId")
        self.Region = params.get("Region")
        self.VpcId = params.get("VpcId")
        self.VPCName = params.get("VPCName")
        self.SubnetId = params.get("SubnetId")
        self.InstanceId = params.get("InstanceId")
        self.InstanceName = params.get("InstanceName")
        self.InsType = params.get("InsType")
        self.PublicIp = params.get("PublicIp")
        self.PrivateIp = params.get("PrivateIp")
        self.PortNum = params.get("PortNum")
        self.LeakNum = params.get("LeakNum")
        self.InsSource = params.get("InsSource")
        self.ResourcePath = params.get("ResourcePath")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class IocListData(AbstractModel):
    """黑白名单IOC列表

    """

    def __init__(self):
        """
        :param IP: 待处置IP地址，IP/Domain字段二选一\n        :type IP: str\n        :param Direction: 只能为0或者1   0代表出站 1代表入站\n        :type Direction: int\n        :param Domain: 待处置域名，IP/Domain字段二选一\n        :type Domain: str\n        """
        self.IP = None
        self.Direction = None
        self.Domain = None


    def _deserialize(self, params):
        self.IP = params.get("IP")
        self.Direction = params.get("Direction")
        self.Domain = params.get("Domain")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class IpStatic(AbstractModel):
    """统计折线图通用结构体

    """

    def __init__(self):
        """
        :param Num: 值\n        :type Num: int\n        :param StatTime: 折线图横坐标时间\n        :type StatTime: str\n        """
        self.Num = None
        self.StatTime = None


    def _deserialize(self, params):
        self.Num = params.get("Num")
        self.StatTime = params.get("StatTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyAcRuleRequest(AbstractModel):
    """ModifyAcRule请求参数结构体

    """

    def __init__(self):
        """
        :param Data: 规则数组\n        :type Data: list of RuleInfoData\n        :param EdgeId: EdgeId值\n        :type EdgeId: str\n        :param Enable: 访问规则状态\n        :type Enable: int\n        :param Area: NAT地域\n        :type Area: str\n        """
        self.Data = None
        self.EdgeId = None
        self.Enable = None
        self.Area = None


    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = RuleInfoData()
                obj._deserialize(item)
                self.Data.append(obj)
        self.EdgeId = params.get("EdgeId")
        self.Enable = params.get("Enable")
        self.Area = params.get("Area")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyAcRuleResponse(AbstractModel):
    """ModifyAcRule返回参数结构体

    """

    def __init__(self):
        """
        :param Status: 状态值，0:操作成功，非0：操作失败\n        :type Status: int\n        :param Info: 返回多余的信息
注意：此字段可能返回 null，表示取不到有效值。\n        :type Info: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Status = None
        self.Info = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.Info = params.get("Info")
        self.RequestId = params.get("RequestId")


class ModifyAllPublicIPSwitchStatusRequest(AbstractModel):
    """ModifyAllPublicIPSwitchStatus请求参数结构体

    """

    def __init__(self):
        """
        :param Status: 状态，0：关闭，1：开启\n        :type Status: int\n        :param FireWallPublicIPs: 选中的防火墙开关Id\n        :type FireWallPublicIPs: list of str\n        """
        self.Status = None
        self.FireWallPublicIPs = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.FireWallPublicIPs = params.get("FireWallPublicIPs")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyAllPublicIPSwitchStatusResponse(AbstractModel):
    """ModifyAllPublicIPSwitchStatus返回参数结构体

    """

    def __init__(self):
        """
        :param ReturnMsg: 接口返回信息
注意：此字段可能返回 null，表示取不到有效值。\n        :type ReturnMsg: str\n        :param ReturnCode: 接口返回错误码，0请求成功  非0失败
注意：此字段可能返回 null，表示取不到有效值。\n        :type ReturnCode: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.ReturnMsg = None
        self.ReturnCode = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ReturnMsg = params.get("ReturnMsg")
        self.ReturnCode = params.get("ReturnCode")
        self.RequestId = params.get("RequestId")


class ModifyAllRuleStatusRequest(AbstractModel):
    """ModifyAllRuleStatus请求参数结构体

    """

    def __init__(self):
        """
        :param Status: 状态，0：全部停用，1：全部启用\n        :type Status: int\n        :param Direction: 方向，0：出站，1：入站\n        :type Direction: int\n        :param EdgeId: Edge ID值\n        :type EdgeId: str\n        :param Area: NAT地域\n        :type Area: str\n        """
        self.Status = None
        self.Direction = None
        self.EdgeId = None
        self.Area = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.Direction = params.get("Direction")
        self.EdgeId = params.get("EdgeId")
        self.Area = params.get("Area")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyAllRuleStatusResponse(AbstractModel):
    """ModifyAllRuleStatus返回参数结构体

    """

    def __init__(self):
        """
        :param Status: 0: 修改成功, 其他: 修改失败
注意：此字段可能返回 null，表示取不到有效值。\n        :type Status: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class ModifyAllSwitchStatusRequest(AbstractModel):
    """ModifyAllSwitchStatus请求参数结构体

    """

    def __init__(self):
        """
        :param Status: 状态，0：关闭，1：开启\n        :type Status: int\n        :param Type: 0: 互联网边界防火墙开关，1：vpc防火墙开关\n        :type Type: int\n        :param Ids: 选中的防火墙开关Id\n        :type Ids: list of str\n        :param ChangeType: NAT开关切换类型，1,单个子网，2，同开同关，3，全部\n        :type ChangeType: int\n        :param Area: NAT实例所在地域\n        :type Area: str\n        """
        self.Status = None
        self.Type = None
        self.Ids = None
        self.ChangeType = None
        self.Area = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.Type = params.get("Type")
        self.Ids = params.get("Ids")
        self.ChangeType = params.get("ChangeType")
        self.Area = params.get("Area")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyAllSwitchStatusResponse(AbstractModel):
    """ModifyAllSwitchStatus返回参数结构体

    """

    def __init__(self):
        """
        :param Status: 修改成功与否的状态值 0：修改成功，非 0：修改失败\n        :type Status: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class ModifyAllVPCSwitchStatusRequest(AbstractModel):
    """ModifyAllVPCSwitchStatus请求参数结构体

    """

    def __init__(self):
        """
        :param Status: 状态，0：关闭，1：开启\n        :type Status: int\n        :param FireWallVpcIds: 选中的防火墙开关Id\n        :type FireWallVpcIds: list of str\n        """
        self.Status = None
        self.FireWallVpcIds = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.FireWallVpcIds = params.get("FireWallVpcIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyAllVPCSwitchStatusResponse(AbstractModel):
    """ModifyAllVPCSwitchStatus返回参数结构体

    """

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyAssetScanRequest(AbstractModel):
    """ModifyAssetScan请求参数结构体

    """

    def __init__(self):
        """
        :param ScanRange: 扫描范围：1端口, 2端口+漏扫\n        :type ScanRange: int\n        :param ScanDeep: 扫描深度：'heavy', 'medium', 'light'\n        :type ScanDeep: str\n        :param RangeType: 扫描类型：1立即扫描 2 周期任务\n        :type RangeType: int\n        :param ScanPeriod: RangeType为2 是必须添加，定时任务时间\n        :type ScanPeriod: str\n        :param ScanFilterIp: 立即扫描这个字段传过滤的扫描集合\n        :type ScanFilterIp: list of str\n        :param ScanType: 1全量2单个\n        :type ScanType: int\n        """
        self.ScanRange = None
        self.ScanDeep = None
        self.RangeType = None
        self.ScanPeriod = None
        self.ScanFilterIp = None
        self.ScanType = None


    def _deserialize(self, params):
        self.ScanRange = params.get("ScanRange")
        self.ScanDeep = params.get("ScanDeep")
        self.RangeType = params.get("RangeType")
        self.ScanPeriod = params.get("ScanPeriod")
        self.ScanFilterIp = params.get("ScanFilterIp")
        self.ScanType = params.get("ScanType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyAssetScanResponse(AbstractModel):
    """ModifyAssetScan返回参数结构体

    """

    def __init__(self):
        """
        :param ReturnMsg: 接口返回信息
注意：此字段可能返回 null，表示取不到有效值。\n        :type ReturnMsg: str\n        :param ReturnCode: 接口返回错误码，0请求成功  非0失败
注意：此字段可能返回 null，表示取不到有效值。\n        :type ReturnCode: int\n        :param Status: 状态值 0：成功，1 执行扫描中,其他：失败\n        :type Status: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.ReturnMsg = None
        self.ReturnCode = None
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ReturnMsg = params.get("ReturnMsg")
        self.ReturnCode = params.get("ReturnCode")
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class ModifyBlockIgnoreListRequest(AbstractModel):
    """ModifyBlockIgnoreList请求参数结构体

    """

    def __init__(self):
        """
        :param RuleType: 1拦截列表 2 忽略列表\n        :type RuleType: int\n        :param IOC: IP、Domain二选一，不能同时为空\n        :type IOC: list of IocListData\n        :param IocAction: 可选值：delete（删除）、edit（编辑）、add（添加）  其他值无效\n        :type IocAction: str\n        :param StartTime: 时间格式：yyyy-MM-dd HH:mm:ss\n        :type StartTime: str\n        :param EndTime: 时间格式：yyyy-MM-dd HH:mm:ss\n        :type EndTime: str\n        """
        self.RuleType = None
        self.IOC = None
        self.IocAction = None
        self.StartTime = None
        self.EndTime = None


    def _deserialize(self, params):
        self.RuleType = params.get("RuleType")
        if params.get("IOC") is not None:
            self.IOC = []
            for item in params.get("IOC"):
                obj = IocListData()
                obj._deserialize(item)
                self.IOC.append(obj)
        self.IocAction = params.get("IocAction")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyBlockIgnoreListResponse(AbstractModel):
    """ModifyBlockIgnoreList返回参数结构体

    """

    def __init__(self):
        """
        :param ReturnMsg: 接口返回信息\n        :type ReturnMsg: str\n        :param ReturnCode: 接口返回错误码，0请求成功  非0失败\n        :type ReturnCode: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.ReturnMsg = None
        self.ReturnCode = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ReturnMsg = params.get("ReturnMsg")
        self.ReturnCode = params.get("ReturnCode")
        self.RequestId = params.get("RequestId")


class ModifyBlockTopRequest(AbstractModel):
    """ModifyBlockTop请求参数结构体

    """

    def __init__(self):
        """
        :param UniqueId: 记录id\n        :type UniqueId: str\n        :param OpeType: 操作类型 1 置顶 0取消\n        :type OpeType: str\n        """
        self.UniqueId = None
        self.OpeType = None


    def _deserialize(self, params):
        self.UniqueId = params.get("UniqueId")
        self.OpeType = params.get("OpeType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyBlockTopResponse(AbstractModel):
    """ModifyBlockTop返回参数结构体

    """

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyItemSwitchStatusRequest(AbstractModel):
    """ModifyItemSwitchStatus请求参数结构体

    """

    def __init__(self):
        """
        :param Id: id值\n        :type Id: int\n        :param Status: 状态值，0: 关闭 ,1:开启\n        :type Status: int\n        :param Type: 0: 互联网边界边界防火墙开关，1：vpc防火墙开关\n        :type Type: int\n        """
        self.Id = None
        self.Status = None
        self.Type = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Status = params.get("Status")
        self.Type = params.get("Type")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyItemSwitchStatusResponse(AbstractModel):
    """ModifyItemSwitchStatus返回参数结构体

    """

    def __init__(self):
        """
        :param Status: 修改成功与否状态值 0：修改成功，非 0：修改失败\n        :type Status: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class ModifyNatFwReSelectRequest(AbstractModel):
    """ModifyNatFwReSelect请求参数结构体

    """

    def __init__(self):
        """
        :param Mode: 模式 1：接入模式；0：新增模式\n        :type Mode: int\n        :param CfwInstance: 防火墙实例id\n        :type CfwInstance: str\n        :param NatGwList: 接入模式重新接入的nat网关列表，其中NatGwList和VpcList只能传递一个。\n        :type NatGwList: list of str\n        :param VpcList: 新增模式重新接入的vpc列表，其中NatGwList和NatgwList只能传递一个。\n        :type VpcList: list of str\n        """
        self.Mode = None
        self.CfwInstance = None
        self.NatGwList = None
        self.VpcList = None


    def _deserialize(self, params):
        self.Mode = params.get("Mode")
        self.CfwInstance = params.get("CfwInstance")
        self.NatGwList = params.get("NatGwList")
        self.VpcList = params.get("VpcList")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyNatFwReSelectResponse(AbstractModel):
    """ModifyNatFwReSelect返回参数结构体

    """

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyNatFwSwitchRequest(AbstractModel):
    """ModifyNatFwSwitch请求参数结构体

    """

    def __init__(self):
        """
        :param Enable: 开关，0：关闭，1：开启\n        :type Enable: int\n        :param CfwInsIdList: 防火墙实例id列表，其中CfwInsIdList，SubnetIdList和RouteTableIdList只能传递一种。\n        :type CfwInsIdList: list of str\n        :param SubnetIdList: 子网id列表，其中CfwInsIdList，SubnetIdList和RouteTableIdList只能传递一种。\n        :type SubnetIdList: list of str\n        :param RouteTableIdList: 路由表id列表，其中CfwInsIdList，SubnetIdList和RouteTableIdList只能传递一种。\n        :type RouteTableIdList: list of str\n        """
        self.Enable = None
        self.CfwInsIdList = None
        self.SubnetIdList = None
        self.RouteTableIdList = None


    def _deserialize(self, params):
        self.Enable = params.get("Enable")
        self.CfwInsIdList = params.get("CfwInsIdList")
        self.SubnetIdList = params.get("SubnetIdList")
        self.RouteTableIdList = params.get("RouteTableIdList")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyNatFwSwitchResponse(AbstractModel):
    """ModifyNatFwSwitch返回参数结构体

    """

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyNatFwVpcDnsSwitchRequest(AbstractModel):
    """ModifyNatFwVpcDnsSwitch请求参数结构体

    """

    def __init__(self):
        """
        :param NatFwInsId: nat 防火墙 id\n        :type NatFwInsId: str\n        :param DnsVpcSwitchLst: DNS 开关切换列表\n        :type DnsVpcSwitchLst: list of DnsVpcSwitch\n        """
        self.NatFwInsId = None
        self.DnsVpcSwitchLst = None


    def _deserialize(self, params):
        self.NatFwInsId = params.get("NatFwInsId")
        if params.get("DnsVpcSwitchLst") is not None:
            self.DnsVpcSwitchLst = []
            for item in params.get("DnsVpcSwitchLst"):
                obj = DnsVpcSwitch()
                obj._deserialize(item)
                self.DnsVpcSwitchLst.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyNatFwVpcDnsSwitchResponse(AbstractModel):
    """ModifyNatFwVpcDnsSwitch返回参数结构体

    """

    def __init__(self):
        """
        :param ReturnMsg: 修改成功
注意：此字段可能返回 null，表示取不到有效值。\n        :type ReturnMsg: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.ReturnMsg = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ReturnMsg = params.get("ReturnMsg")
        self.RequestId = params.get("RequestId")


class ModifyPublicIPSwitchStatusRequest(AbstractModel):
    """ModifyPublicIPSwitchStatus请求参数结构体

    """

    def __init__(self):
        """
        :param FireWallPublicIP: 公网IP\n        :type FireWallPublicIP: str\n        :param Status: 状态值，0: 关闭 ,1:开启\n        :type Status: int\n        """
        self.FireWallPublicIP = None
        self.Status = None


    def _deserialize(self, params):
        self.FireWallPublicIP = params.get("FireWallPublicIP")
        self.Status = params.get("Status")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyPublicIPSwitchStatusResponse(AbstractModel):
    """ModifyPublicIPSwitchStatus返回参数结构体

    """

    def __init__(self):
        """
        :param ReturnMsg: 接口返回信息
注意：此字段可能返回 null，表示取不到有效值。\n        :type ReturnMsg: str\n        :param ReturnCode: 接口返回错误码，0请求成功  非0失败\n        :type ReturnCode: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.ReturnMsg = None
        self.ReturnCode = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ReturnMsg = params.get("ReturnMsg")
        self.ReturnCode = params.get("ReturnCode")
        self.RequestId = params.get("RequestId")


class ModifyResourceGroupRequest(AbstractModel):
    """ModifyResourceGroup请求参数结构体

    """

    def __init__(self):
        """
        :param GroupId: 组id\n        :type GroupId: str\n        :param GroupName: 组名称\n        :type GroupName: str\n        :param ParentId: 上级组id\n        :type ParentId: str\n        """
        self.GroupId = None
        self.GroupName = None
        self.ParentId = None


    def _deserialize(self, params):
        self.GroupId = params.get("GroupId")
        self.GroupName = params.get("GroupName")
        self.ParentId = params.get("ParentId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyResourceGroupResponse(AbstractModel):
    """ModifyResourceGroup返回参数结构体

    """

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifySecurityGroupAllRuleStatusRequest(AbstractModel):
    """ModifySecurityGroupAllRuleStatus请求参数结构体

    """

    def __init__(self):
        """
        :param Status: 列表规则状态，0：全部停用，1：全部启用\n        :type Status: int\n        :param Direction: 方向，0：出站，1：入站\n        :type Direction: int\n        :param EdgeId: Edge ID值\n        :type EdgeId: str\n        :param Area: NAT地域, 腾讯云地域的英文简写\n        :type Area: str\n        """
        self.Status = None
        self.Direction = None
        self.EdgeId = None
        self.Area = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.Direction = params.get("Direction")
        self.EdgeId = params.get("EdgeId")
        self.Area = params.get("Area")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifySecurityGroupAllRuleStatusResponse(AbstractModel):
    """ModifySecurityGroupAllRuleStatus返回参数结构体

    """

    def __init__(self):
        """
        :param Status: 0: 修改成功, 其他: 修改失败
注意：此字段可能返回 null，表示取不到有效值。\n        :type Status: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class ModifySecurityGroupItemRuleStatusRequest(AbstractModel):
    """ModifySecurityGroupItemRuleStatus请求参数结构体

    """

    def __init__(self):
        """
        :param Direction: 方向，0：出站，1：入站，默认1\n        :type Direction: int\n        :param Status: 是否开关开启，0：未开启，1：开启\n        :type Status: int\n        :param RuleSequence: 更改的企业安全组规则的执行顺序\n        :type RuleSequence: int\n        """
        self.Direction = None
        self.Status = None
        self.RuleSequence = None


    def _deserialize(self, params):
        self.Direction = params.get("Direction")
        self.Status = params.get("Status")
        self.RuleSequence = params.get("RuleSequence")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifySecurityGroupItemRuleStatusResponse(AbstractModel):
    """ModifySecurityGroupItemRuleStatus返回参数结构体

    """

    def __init__(self):
        """
        :param Status: 状态值，0：修改成功，非0：修改失败\n        :type Status: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class ModifySecurityGroupRuleRequest(AbstractModel):
    """ModifySecurityGroupRule请求参数结构体

    """

    def __init__(self):
        """
        :param Direction: 方向，0：出站，1：入站，默认1\n        :type Direction: int\n        :param Enable: 编辑后是否启用规则，0：不启用，1：启用，默认1\n        :type Enable: int\n        :param Data: 编辑的企业安全组规则数据\n        :type Data: list of SecurityGroupListData\n        :param SgRuleOriginSequence: 编辑的企业安全组规则的原始执行顺序\n        :type SgRuleOriginSequence: int\n        """
        self.Direction = None
        self.Enable = None
        self.Data = None
        self.SgRuleOriginSequence = None


    def _deserialize(self, params):
        self.Direction = params.get("Direction")
        self.Enable = params.get("Enable")
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = SecurityGroupListData()
                obj._deserialize(item)
                self.Data.append(obj)
        self.SgRuleOriginSequence = params.get("SgRuleOriginSequence")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifySecurityGroupRuleResponse(AbstractModel):
    """ModifySecurityGroupRule返回参数结构体

    """

    def __init__(self):
        """
        :param Status: 状态值，0：编辑成功，非0：编辑失败\n        :type Status: int\n        :param NewRuleId: 编辑后新生成规则的Id\n        :type NewRuleId: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Status = None
        self.NewRuleId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.NewRuleId = params.get("NewRuleId")
        self.RequestId = params.get("RequestId")


class ModifySecurityGroupSequenceRulesRequest(AbstractModel):
    """ModifySecurityGroupSequenceRules请求参数结构体

    """

    def __init__(self):
        """
        :param Direction: 方向，0：出站，1：入站，默认1\n        :type Direction: int\n        :param Data: 企业安全组规则快速排序数据\n        :type Data: list of SecurityGroupOrderIndexData\n        """
        self.Direction = None
        self.Data = None


    def _deserialize(self, params):
        self.Direction = params.get("Direction")
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = SecurityGroupOrderIndexData()
                obj._deserialize(item)
                self.Data.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifySecurityGroupSequenceRulesResponse(AbstractModel):
    """ModifySecurityGroupSequenceRules返回参数结构体

    """

    def __init__(self):
        """
        :param Status: 状态值，0：修改成功，非0：修改失败\n        :type Status: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class ModifySequenceRulesRequest(AbstractModel):
    """ModifySequenceRules请求参数结构体

    """

    def __init__(self):
        """
        :param EdgeId: 边Id值\n        :type EdgeId: str\n        :param Data: 修改数据\n        :type Data: list of SequenceData\n        :param Area: NAT地域\n        :type Area: str\n        :param Direction: 方向，0：出向，1：入向\n        :type Direction: int\n        """
        self.EdgeId = None
        self.Data = None
        self.Area = None
        self.Direction = None


    def _deserialize(self, params):
        self.EdgeId = params.get("EdgeId")
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = SequenceData()
                obj._deserialize(item)
                self.Data.append(obj)
        self.Area = params.get("Area")
        self.Direction = params.get("Direction")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifySequenceRulesResponse(AbstractModel):
    """ModifySequenceRules返回参数结构体

    """

    def __init__(self):
        """
        :param Status: 0: 修改成功, 非0: 修改失败
注意：此字段可能返回 null，表示取不到有效值。\n        :type Status: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class ModifyTableStatusRequest(AbstractModel):
    """ModifyTableStatus请求参数结构体

    """

    def __init__(self):
        """
        :param EdgeId: EdgeId值两个vpc间的边id\n        :type EdgeId: str\n        :param Status: 状态值，1：锁表，2：解锁表\n        :type Status: int\n        :param Area: Nat所在地域\n        :type Area: str\n        :param Direction: 0： 出向，1：入向\n        :type Direction: int\n        """
        self.EdgeId = None
        self.Status = None
        self.Area = None
        self.Direction = None


    def _deserialize(self, params):
        self.EdgeId = params.get("EdgeId")
        self.Status = params.get("Status")
        self.Area = params.get("Area")
        self.Direction = params.get("Direction")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyTableStatusResponse(AbstractModel):
    """ModifyTableStatus返回参数结构体

    """

    def __init__(self):
        """
        :param Status: 0：正常，-1：不正常
注意：此字段可能返回 null，表示取不到有效值。\n        :type Status: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class ModifyVPCSwitchStatusRequest(AbstractModel):
    """ModifyVPCSwitchStatus请求参数结构体

    """

    def __init__(self):
        """
        :param FirewallVpcId: 公网IP\n        :type FirewallVpcId: str\n        :param Status: 状态值，0: 关闭 ,1:开启\n        :type Status: int\n        """
        self.FirewallVpcId = None
        self.Status = None


    def _deserialize(self, params):
        self.FirewallVpcId = params.get("FirewallVpcId")
        self.Status = params.get("Status")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyVPCSwitchStatusResponse(AbstractModel):
    """ModifyVPCSwitchStatus返回参数结构体

    """

    def __init__(self):
        """
        :param ReturnMsg: 接口返回信息
注意：此字段可能返回 null，表示取不到有效值。\n        :type ReturnMsg: str\n        :param ReturnCode: 接口返回错误码，0请求成功  非0失败\n        :type ReturnCode: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.ReturnMsg = None
        self.ReturnCode = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ReturnMsg = params.get("ReturnMsg")
        self.ReturnCode = params.get("ReturnCode")
        self.RequestId = params.get("RequestId")


class NatFwEipsInfo(AbstractModel):
    """Nat防火墙弹性公网ip列表

    """

    def __init__(self):
        """
        :param Eip: 弹性公网ip\n        :type Eip: str\n        :param NatGatewayId: 所属的Nat网关Id
注意：此字段可能返回 null，表示取不到有效值。\n        :type NatGatewayId: str\n        :param NatGatewayName: Nat网关名称
注意：此字段可能返回 null，表示取不到有效值。\n        :type NatGatewayName: str\n        """
        self.Eip = None
        self.NatGatewayId = None
        self.NatGatewayName = None


    def _deserialize(self, params):
        self.Eip = params.get("Eip")
        self.NatGatewayId = params.get("NatGatewayId")
        self.NatGatewayName = params.get("NatGatewayName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NatFwFilter(AbstractModel):
    """nat fw 实例展示的过滤列表

    """

    def __init__(self):
        """
        :param FilterType: 过滤的类型，例如实例id\n        :type FilterType: str\n        :param FilterContent: 过滤的内容，以',' 分隔\n        :type FilterContent: str\n        """
        self.FilterType = None
        self.FilterContent = None


    def _deserialize(self, params):
        self.FilterType = params.get("FilterType")
        self.FilterContent = params.get("FilterContent")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NatFwInstance(AbstractModel):
    """Nat实例类型

    """

    def __init__(self):
        """
        :param NatinsId: nat实例id\n        :type NatinsId: str\n        :param NatinsName: nat实例名称\n        :type NatinsName: str\n        :param Region: 实例所在地域
注意：此字段可能返回 null，表示取不到有效值。\n        :type Region: str\n        :param FwMode: 0:新增模式，1:接入模式
注意：此字段可能返回 null，表示取不到有效值。\n        :type FwMode: int\n        :param Status: 0:正常状态， 1: 正在创建
注意：此字段可能返回 null，表示取不到有效值。\n        :type Status: int\n        """
        self.NatinsId = None
        self.NatinsName = None
        self.Region = None
        self.FwMode = None
        self.Status = None


    def _deserialize(self, params):
        self.NatinsId = params.get("NatinsId")
        self.NatinsName = params.get("NatinsName")
        self.Region = params.get("Region")
        self.FwMode = params.get("FwMode")
        self.Status = params.get("Status")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NatInstanceInfo(AbstractModel):
    """Nat实例卡片详细信息

    """

    def __init__(self):
        """
        :param NatinsId: nat实例id\n        :type NatinsId: str\n        :param NatinsName: nat实例名称\n        :type NatinsName: str\n        :param Region: 实例所在地域\n        :type Region: str\n        :param FwMode: 0: 新增模式，1:接入模式\n        :type FwMode: int\n        :param BandWidth: 实例带宽大小 Mbps\n        :type BandWidth: int\n        :param InFlowMax: 入向带宽峰值 bps\n        :type InFlowMax: int\n        :param OutFlowMax: 出向带宽峰值 bps\n        :type OutFlowMax: int\n        :param RegionZh: 地域中文信息\n        :type RegionZh: str\n        :param EipAddress: 公网ip数组
注意：此字段可能返回 null，表示取不到有效值。\n        :type EipAddress: list of str\n        :param VpcIp: 内外使用ip数组
注意：此字段可能返回 null，表示取不到有效值。\n        :type VpcIp: list of str\n        :param Subnets: 实例关联子网数组
注意：此字段可能返回 null，表示取不到有效值。\n        :type Subnets: list of str\n        :param Status: 0 :正常 1：正在初始化
注意：此字段可能返回 null，表示取不到有效值。\n        :type Status: int\n        """
        self.NatinsId = None
        self.NatinsName = None
        self.Region = None
        self.FwMode = None
        self.BandWidth = None
        self.InFlowMax = None
        self.OutFlowMax = None
        self.RegionZh = None
        self.EipAddress = None
        self.VpcIp = None
        self.Subnets = None
        self.Status = None


    def _deserialize(self, params):
        self.NatinsId = params.get("NatinsId")
        self.NatinsName = params.get("NatinsName")
        self.Region = params.get("Region")
        self.FwMode = params.get("FwMode")
        self.BandWidth = params.get("BandWidth")
        self.InFlowMax = params.get("InFlowMax")
        self.OutFlowMax = params.get("OutFlowMax")
        self.RegionZh = params.get("RegionZh")
        self.EipAddress = params.get("EipAddress")
        self.VpcIp = params.get("VpcIp")
        self.Subnets = params.get("Subnets")
        self.Status = params.get("Status")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NewModeItems(AbstractModel):
    """新增模式传递参数

    """

    def __init__(self):
        """
        :param VpcList: 新增模式下接入的vpc列表\n        :type VpcList: list of str\n        :param Eips: 新增模式下绑定的出口弹性公网ip列表，其中Eips和AddCount至少传递一个。\n        :type Eips: list of str\n        :param AddCount: 新增模式下新增绑定的出口弹性公网ip个数，其中Eips和AddCount至少传递一个。\n        :type AddCount: int\n        """
        self.VpcList = None
        self.Eips = None
        self.AddCount = None


    def _deserialize(self, params):
        self.VpcList = params.get("VpcList")
        self.Eips = params.get("Eips")
        self.AddCount = params.get("AddCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RuleInfoData(AbstractModel):
    """规则输入对象

    """

    def __init__(self):
        """
        :param OrderIndex: 执行顺序\n        :type OrderIndex: int\n        :param SourceIp: 访问源\n        :type SourceIp: str\n        :param TargetIp: 访问目的\n        :type TargetIp: str\n        :param Protocol: 协议\n        :type Protocol: str\n        :param Strategy: 策略\n        :type Strategy: str\n        :param SourceType: 访问源类型，1是IP，3是域名，4是IP地址模版，5是域名地址模版\n        :type SourceType: int\n        :param Direction: 方向，0：出站，1：入站\n        :type Direction: int\n        :param Detail: 描述\n        :type Detail: str\n        :param TargetType: 访问目的类型，1是IP，3是域名，4是IP地址模版，5是域名地址模版\n        :type TargetType: int\n        :param Port: 端口\n        :type Port: str\n        :param Id: id值\n        :type Id: int\n        :param LogId: 日志id，从告警处创建必传，其它为空\n        :type LogId: str\n        :param City: 城市Code\n        :type City: int\n        :param Country: 国家Code\n        :type Country: int\n        :param CloudCode: 云厂商，支持多个，以逗号分隔， 1:腾讯云（仅中国香港及海外）,2:阿里云,3:亚马逊云,4:华为云,5:微软云\n        :type CloudCode: str\n        :param IsRegion: 是否为地域\n        :type IsRegion: int\n        :param CityName: 城市名\n        :type CityName: str\n        :param CountryName: 国家名\n        :type CountryName: str\n        """
        self.OrderIndex = None
        self.SourceIp = None
        self.TargetIp = None
        self.Protocol = None
        self.Strategy = None
        self.SourceType = None
        self.Direction = None
        self.Detail = None
        self.TargetType = None
        self.Port = None
        self.Id = None
        self.LogId = None
        self.City = None
        self.Country = None
        self.CloudCode = None
        self.IsRegion = None
        self.CityName = None
        self.CountryName = None


    def _deserialize(self, params):
        self.OrderIndex = params.get("OrderIndex")
        self.SourceIp = params.get("SourceIp")
        self.TargetIp = params.get("TargetIp")
        self.Protocol = params.get("Protocol")
        self.Strategy = params.get("Strategy")
        self.SourceType = params.get("SourceType")
        self.Direction = params.get("Direction")
        self.Detail = params.get("Detail")
        self.TargetType = params.get("TargetType")
        self.Port = params.get("Port")
        self.Id = params.get("Id")
        self.LogId = params.get("LogId")
        self.City = params.get("City")
        self.Country = params.get("Country")
        self.CloudCode = params.get("CloudCode")
        self.IsRegion = params.get("IsRegion")
        self.CityName = params.get("CityName")
        self.CountryName = params.get("CountryName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RunSyncAssetRequest(AbstractModel):
    """RunSyncAsset请求参数结构体

    """

    def __init__(self):
        """
        :param Type: 0: 互联网防火墙开关，1：vpc 防火墙开关\n        :type Type: int\n        """
        self.Type = None


    def _deserialize(self, params):
        self.Type = params.get("Type")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RunSyncAssetResponse(AbstractModel):
    """RunSyncAsset返回参数结构体

    """

    def __init__(self):
        """
        :param Status: 0：同步成功，1：资产更新中，2：后台同步调用失败\n        :type Status: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class ScanInfo(AbstractModel):
    """新手引导扫描信息

    """

    def __init__(self):
        """
        :param ScanResultInfo: 扫描结果信息\n        :type ScanResultInfo: :class:`tencentcloud.cfw.v20190904.models.ScanResultInfo`\n        :param ScanStatus: 扫描状态 0扫描中 1完成   2没赠送过扫描显示开启界面\n        :type ScanStatus: int\n        :param ScanPercent: 进度\n        :type ScanPercent: float\n        :param ScanTime: 预计完成时间\n        :type ScanTime: str\n        """
        self.ScanResultInfo = None
        self.ScanStatus = None
        self.ScanPercent = None
        self.ScanTime = None


    def _deserialize(self, params):
        if params.get("ScanResultInfo") is not None:
            self.ScanResultInfo = ScanResultInfo()
            self.ScanResultInfo._deserialize(params.get("ScanResultInfo"))
        self.ScanStatus = params.get("ScanStatus")
        self.ScanPercent = params.get("ScanPercent")
        self.ScanTime = params.get("ScanTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ScanResultInfo(AbstractModel):
    """新手引导扫描结果信息PortNum   int
    	LeakNum   int
    	IPNum     int
    	IPStatus  bool
    	IdpStatus bool
    	BanStatus bool

    """

    def __init__(self):
        """
        :param LeakNum: 暴漏漏洞数量\n        :type LeakNum: int\n        :param IPNum: 防护ip数量\n        :type IPNum: int\n        :param PortNum: 暴漏端口数量\n        :type PortNum: int\n        :param IPStatus: 是否开启防护\n        :type IPStatus: bool\n        :param IdpStatus: 是否拦截攻击\n        :type IdpStatus: bool\n        :param BanStatus: 是否禁封端口\n        :type BanStatus: bool\n        """
        self.LeakNum = None
        self.IPNum = None
        self.PortNum = None
        self.IPStatus = None
        self.IdpStatus = None
        self.BanStatus = None


    def _deserialize(self, params):
        self.LeakNum = params.get("LeakNum")
        self.IPNum = params.get("IPNum")
        self.PortNum = params.get("PortNum")
        self.IPStatus = params.get("IPStatus")
        self.IdpStatus = params.get("IdpStatus")
        self.BanStatus = params.get("BanStatus")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SecurityGroupApiRuleData(AbstractModel):
    """添加安全组Api规则对象

    """

    def __init__(self):
        """
        :param SourceId: 访问源，入站时为Ip/Cidr，默认为0.0.0.0/0； 出站时当RuleType为1时，支持内网Ip/Cidr, 当RuleType为2时，填实例ID\n        :type SourceId: str\n        :param TargetId: 访问目的，出站时为Ip/Cidr，默认为0.0.0.0/0；入站时当RuleType为1时，支持内网Ip/Cidr, 当RuleType为2时，填实例ID\n        :type TargetId: str\n        :param Protocol: 协议，支持ANY/TCP/UDP/ICMP\n        :type Protocol: str\n        :param Port: 端口, 当Protocol为ANY或ICMP时，Port为-1/-1\n        :type Port: str\n        :param Strategy: 策略, 1：阻断，2：放行\n        :type Strategy: str\n        :param Detail: 描述\n        :type Detail: str\n        :param RuleType: 规则类型，1：VpcId+Ip/Cidr, 2: 实例ID，入站时为访问目的类型，出站时为访问源类型\n        :type RuleType: int\n        :param OrderIndex: 执行顺序，中间插入必传，前插、后插非必传\n        :type OrderIndex: int\n        :param VpcId: 私有网络ID，当RuleType为1时必传\n        :type VpcId: str\n        """
        self.SourceId = None
        self.TargetId = None
        self.Protocol = None
        self.Port = None
        self.Strategy = None
        self.Detail = None
        self.RuleType = None
        self.OrderIndex = None
        self.VpcId = None


    def _deserialize(self, params):
        self.SourceId = params.get("SourceId")
        self.TargetId = params.get("TargetId")
        self.Protocol = params.get("Protocol")
        self.Port = params.get("Port")
        self.Strategy = params.get("Strategy")
        self.Detail = params.get("Detail")
        self.RuleType = params.get("RuleType")
        self.OrderIndex = params.get("OrderIndex")
        self.VpcId = params.get("VpcId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SecurityGroupBothWayInfo(AbstractModel):
    """双向下发的企业安全组规则

    """

    def __init__(self):
        """
        :param OrderIndex: 执行顺序
注意：此字段可能返回 null，表示取不到有效值。\n        :type OrderIndex: int\n        :param SourceId: 访问源
注意：此字段可能返回 null，表示取不到有效值。\n        :type SourceId: str\n        :param SourceType: 访问源类型，默认为0，1: VPC, 2: SUBNET, 3: CVM, 4: CLB, 5: ENI, 6: CDB, 100:资源组
注意：此字段可能返回 null，表示取不到有效值。\n        :type SourceType: int\n        :param TargetId: 访问目的
注意：此字段可能返回 null，表示取不到有效值。\n        :type TargetId: str\n        :param TargetType: 访问目的类型，默认为0，1: VPC, 2: SUBNET, 3: CVM, 4: CLB, 5: ENI, 6: CDB, 100:资源组
注意：此字段可能返回 null，表示取不到有效值。\n        :type TargetType: int\n        :param Protocol: 协议
注意：此字段可能返回 null，表示取不到有效值。\n        :type Protocol: str\n        :param Port: 目的端口
注意：此字段可能返回 null，表示取不到有效值。\n        :type Port: str\n        :param Strategy: 策略, 1：阻断，2：放行
注意：此字段可能返回 null，表示取不到有效值。\n        :type Strategy: int\n        :param Direction: 方向，0：出站，1：入站，默认1
注意：此字段可能返回 null，表示取不到有效值。\n        :type Direction: int\n        :param Region: 地域\n        :type Region: str\n        :param Detail: 描述
注意：此字段可能返回 null，表示取不到有效值。\n        :type Detail: str\n        :param Status: 是否开关开启，0：未开启，1：开启
注意：此字段可能返回 null，表示取不到有效值。\n        :type Status: int\n        :param IsNew: 是否是正常规则，0：正常，1：异常
注意：此字段可能返回 null，表示取不到有效值。\n        :type IsNew: int\n        :param BothWay: 单/双向下发，0:单向下发，1：双向下发
注意：此字段可能返回 null，表示取不到有效值。\n        :type BothWay: int\n        :param VpcId: 私有网络ID
注意：此字段可能返回 null，表示取不到有效值。\n        :type VpcId: str\n        :param SubnetId: 子网ID
注意：此字段可能返回 null，表示取不到有效值。\n        :type SubnetId: str\n        :param InstanceName: 子网ID
注意：此字段可能返回 null，表示取不到有效值。\n        :type InstanceName: str\n        :param PublicIp: 公网IP，多个以英文逗号分隔
注意：此字段可能返回 null，表示取不到有效值。\n        :type PublicIp: str\n        :param PrivateIp: 内网IP，多个以英文逗号分隔
注意：此字段可能返回 null，表示取不到有效值。\n        :type PrivateIp: str\n        :param Cidr: 掩码地址，多个以英文逗号分隔
注意：此字段可能返回 null，表示取不到有效值。\n        :type Cidr: str\n        :param ServiceTemplateId: 端口协议类型参数模板id
注意：此字段可能返回 null，表示取不到有效值。\n        :type ServiceTemplateId: str\n        """
        self.OrderIndex = None
        self.SourceId = None
        self.SourceType = None
        self.TargetId = None
        self.TargetType = None
        self.Protocol = None
        self.Port = None
        self.Strategy = None
        self.Direction = None
        self.Region = None
        self.Detail = None
        self.Status = None
        self.IsNew = None
        self.BothWay = None
        self.VpcId = None
        self.SubnetId = None
        self.InstanceName = None
        self.PublicIp = None
        self.PrivateIp = None
        self.Cidr = None
        self.ServiceTemplateId = None


    def _deserialize(self, params):
        self.OrderIndex = params.get("OrderIndex")
        self.SourceId = params.get("SourceId")
        self.SourceType = params.get("SourceType")
        self.TargetId = params.get("TargetId")
        self.TargetType = params.get("TargetType")
        self.Protocol = params.get("Protocol")
        self.Port = params.get("Port")
        self.Strategy = params.get("Strategy")
        self.Direction = params.get("Direction")
        self.Region = params.get("Region")
        self.Detail = params.get("Detail")
        self.Status = params.get("Status")
        self.IsNew = params.get("IsNew")
        self.BothWay = params.get("BothWay")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.InstanceName = params.get("InstanceName")
        self.PublicIp = params.get("PublicIp")
        self.PrivateIp = params.get("PrivateIp")
        self.Cidr = params.get("Cidr")
        self.ServiceTemplateId = params.get("ServiceTemplateId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SecurityGroupListData(AbstractModel):
    """安全组列表数据

    """

    def __init__(self):
        """
        :param OrderIndex: 执行顺序\n        :type OrderIndex: int\n        :param SourceId: 访问源\n        :type SourceId: str\n        :param SourceType: 访问源类型，默认为0，1: VPC, 2: SUBNET, 3: CVM, 4: CLB, 5: ENI, 6: CDB, 100:资源组\n        :type SourceType: int\n        :param TargetId: 访问目的\n        :type TargetId: str\n        :param TargetType: 访问目的类型，默认为0，1: VPC, 2: SUBNET, 3: CVM, 4: CLB, 5: ENI, 6: CDB, 100:资源组\n        :type TargetType: int\n        :param Protocol: 协议\n        :type Protocol: str\n        :param Port: 目的端口\n        :type Port: str\n        :param Strategy: 策略, 1：阻断，2：放行\n        :type Strategy: int\n        :param Detail: 描述\n        :type Detail: str\n        :param BothWay: 单/双向下发，0:单向下发，1：双向下发\n        :type BothWay: int\n        :param Id: 规则ID\n        :type Id: int\n        :param Status: 是否开关开启，0：未开启，1：开启\n        :type Status: int\n        :param IsNew: 是否是正常规则，0：正常，1：异常\n        :type IsNew: int\n        :param VpcId: 私有网络ID
注意：此字段可能返回 null，表示取不到有效值。\n        :type VpcId: str\n        :param SubnetId: 子网ID
注意：此字段可能返回 null，表示取不到有效值。\n        :type SubnetId: str\n        :param InstanceName: 实例名称
注意：此字段可能返回 null，表示取不到有效值。\n        :type InstanceName: str\n        :param PublicIp: 公网IP，多个以英文逗号分隔
注意：此字段可能返回 null，表示取不到有效值。\n        :type PublicIp: str\n        :param PrivateIp: 内网IP，多个以英文逗号分隔
注意：此字段可能返回 null，表示取不到有效值。\n        :type PrivateIp: str\n        :param Cidr: 掩码地址，多个以英文逗号分隔
注意：此字段可能返回 null，表示取不到有效值。\n        :type Cidr: str\n        :param ServiceTemplateId: 端口协议类型参数模板id
注意：此字段可能返回 null，表示取不到有效值。\n        :type ServiceTemplateId: str\n        :param BothWayInfo: 当BothWay为0的时候，填空，当BothWay为1的时候，为JSON字符串，数据来源于DescribeBothWayInstanceListByIp个接口，如果该接口返回数据为空，则不支持双向下发
注意：此字段可能返回 null，表示取不到有效值。\n        :type BothWayInfo: list of SecurityGroupBothWayInfo\n        :param Direction: 方向，0：出站，1：入站，默认1\n        :type Direction: int\n        """
        self.OrderIndex = None
        self.SourceId = None
        self.SourceType = None
        self.TargetId = None
        self.TargetType = None
        self.Protocol = None
        self.Port = None
        self.Strategy = None
        self.Detail = None
        self.BothWay = None
        self.Id = None
        self.Status = None
        self.IsNew = None
        self.VpcId = None
        self.SubnetId = None
        self.InstanceName = None
        self.PublicIp = None
        self.PrivateIp = None
        self.Cidr = None
        self.ServiceTemplateId = None
        self.BothWayInfo = None
        self.Direction = None


    def _deserialize(self, params):
        self.OrderIndex = params.get("OrderIndex")
        self.SourceId = params.get("SourceId")
        self.SourceType = params.get("SourceType")
        self.TargetId = params.get("TargetId")
        self.TargetType = params.get("TargetType")
        self.Protocol = params.get("Protocol")
        self.Port = params.get("Port")
        self.Strategy = params.get("Strategy")
        self.Detail = params.get("Detail")
        self.BothWay = params.get("BothWay")
        self.Id = params.get("Id")
        self.Status = params.get("Status")
        self.IsNew = params.get("IsNew")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.InstanceName = params.get("InstanceName")
        self.PublicIp = params.get("PublicIp")
        self.PrivateIp = params.get("PrivateIp")
        self.Cidr = params.get("Cidr")
        self.ServiceTemplateId = params.get("ServiceTemplateId")
        if params.get("BothWayInfo") is not None:
            self.BothWayInfo = []
            for item in params.get("BothWayInfo"):
                obj = SecurityGroupBothWayInfo()
                obj._deserialize(item)
                self.BothWayInfo.append(obj)
        self.Direction = params.get("Direction")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SecurityGroupOrderIndexData(AbstractModel):
    """企业安全组规则执行顺序修改对象

    """

    def __init__(self):
        """
        :param OrderIndex: 企业安全组规则当前执行顺序\n        :type OrderIndex: int\n        :param NewOrderIndex: 企业安全组规则更新目标执行顺序\n        :type NewOrderIndex: int\n        """
        self.OrderIndex = None
        self.NewOrderIndex = None


    def _deserialize(self, params):
        self.OrderIndex = params.get("OrderIndex")
        self.NewOrderIndex = params.get("NewOrderIndex")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SequenceData(AbstractModel):
    """执行顺序对象

    """

    def __init__(self):
        """
        :param Id: 规则Id值\n        :type Id: int\n        :param OrderIndex: 修改前执行顺序\n        :type OrderIndex: int\n        :param NewOrderIndex: 修改后执行顺序\n        :type NewOrderIndex: int\n        """
        self.Id = None
        self.OrderIndex = None
        self.NewOrderIndex = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.OrderIndex = params.get("OrderIndex")
        self.NewOrderIndex = params.get("NewOrderIndex")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SetNatFwDnatRuleRequest(AbstractModel):
    """SetNatFwDnatRule请求参数结构体

    """

    def __init__(self):
        """
        :param Mode: 0：cfw新增模式，1：cfw接入模式。\n        :type Mode: int\n        :param OperationType: 操作类型，可选值：add，del，modify。\n        :type OperationType: str\n        :param CfwInstance: 防火墙实例id，该字段必须传递。\n        :type CfwInstance: str\n        :param AddOrDelDnatRules: 添加或删除操作的Dnat规则列表。\n        :type AddOrDelDnatRules: list of CfwNatDnatRule\n        :param OriginDnat: 修改操作的原始Dnat规则\n        :type OriginDnat: :class:`tencentcloud.cfw.v20190904.models.CfwNatDnatRule`\n        :param NewDnat: 修改操作的新的Dnat规则\n        :type NewDnat: :class:`tencentcloud.cfw.v20190904.models.CfwNatDnatRule`\n        """
        self.Mode = None
        self.OperationType = None
        self.CfwInstance = None
        self.AddOrDelDnatRules = None
        self.OriginDnat = None
        self.NewDnat = None


    def _deserialize(self, params):
        self.Mode = params.get("Mode")
        self.OperationType = params.get("OperationType")
        self.CfwInstance = params.get("CfwInstance")
        if params.get("AddOrDelDnatRules") is not None:
            self.AddOrDelDnatRules = []
            for item in params.get("AddOrDelDnatRules"):
                obj = CfwNatDnatRule()
                obj._deserialize(item)
                self.AddOrDelDnatRules.append(obj)
        if params.get("OriginDnat") is not None:
            self.OriginDnat = CfwNatDnatRule()
            self.OriginDnat._deserialize(params.get("OriginDnat"))
        if params.get("NewDnat") is not None:
            self.NewDnat = CfwNatDnatRule()
            self.NewDnat._deserialize(params.get("NewDnat"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SetNatFwDnatRuleResponse(AbstractModel):
    """SetNatFwDnatRule返回参数结构体

    """

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class SetNatFwEipRequest(AbstractModel):
    """SetNatFwEip请求参数结构体

    """

    def __init__(self):
        """
        :param OperationType: bind：绑定eip；unbind：解绑eip；newAdd：新增防火墙弹性公网ip\n        :type OperationType: str\n        :param CfwInstance: 防火墙实例id\n        :type CfwInstance: str\n        :param EipList: 当OperationType 为bind或unbind操作时，使用该字段。\n        :type EipList: list of str\n        """
        self.OperationType = None
        self.CfwInstance = None
        self.EipList = None


    def _deserialize(self, params):
        self.OperationType = params.get("OperationType")
        self.CfwInstance = params.get("CfwInstance")
        self.EipList = params.get("EipList")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SetNatFwEipResponse(AbstractModel):
    """SetNatFwEip返回参数结构体

    """

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class StaticInfo(AbstractModel):
    """StaticInfo 告警柱形图统计信息


    """

    def __init__(self):
        """
        :param Num: 数\n        :type Num: int\n        :param Port: 端口\n        :type Port: str\n        :param Ip: ip信息\n        :type Ip: str\n        :param Address: 地址\n        :type Address: str\n        :param InsID: 资产id\n        :type InsID: str\n        :param InsName: 资产名称\n        :type InsName: str\n        """
        self.Num = None
        self.Port = None
        self.Ip = None
        self.Address = None
        self.InsID = None
        self.InsName = None


    def _deserialize(self, params):
        self.Num = params.get("Num")
        self.Port = params.get("Port")
        self.Ip = params.get("Ip")
        self.Address = params.get("Address")
        self.InsID = params.get("InsID")
        self.InsName = params.get("InsName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StopSecurityGroupRuleDispatchRequest(AbstractModel):
    """StopSecurityGroupRuleDispatch请求参数结构体

    """


class StopSecurityGroupRuleDispatchResponse(AbstractModel):
    """StopSecurityGroupRuleDispatch返回参数结构体

    """

    def __init__(self):
        """
        :param Status: true代表成功，false代表错误
注意：此字段可能返回 null，表示取不到有效值。\n        :type Status: bool\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Status = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Status = params.get("Status")
        self.RequestId = params.get("RequestId")


class SwitchListsData(AbstractModel):
    """防火墙开关列表对象

    """

    def __init__(self):
        """
        :param PublicIp: 公网IP
注意：此字段可能返回 null，表示取不到有效值。\n        :type PublicIp: str\n        :param IntranetIp: 内网IP
注意：此字段可能返回 null，表示取不到有效值。\n        :type IntranetIp: str\n        :param InstanceName: 实例名
注意：此字段可能返回 null，表示取不到有效值。\n        :type InstanceName: str\n        :param InstanceId: 实例ID
注意：此字段可能返回 null，表示取不到有效值。\n        :type InstanceId: str\n        :param AssetType: 资产类型\n        :type AssetType: str\n        :param Area: 地域
注意：此字段可能返回 null，表示取不到有效值。\n        :type Area: str\n        :param Switch: 防火墙开关\n        :type Switch: int\n        :param Id: id值\n        :type Id: int\n        :param PublicIpType: 公网 IP 类型
注意：此字段可能返回 null，表示取不到有效值。\n        :type PublicIpType: int\n        :param PortTimes: 风险端口数
注意：此字段可能返回 null，表示取不到有效值。\n        :type PortTimes: int\n        :param LastTime: 最近扫描时间
注意：此字段可能返回 null，表示取不到有效值。\n        :type LastTime: str\n        :param ScanMode: 扫描深度
注意：此字段可能返回 null，表示取不到有效值。\n        :type ScanMode: str\n        :param ScanStatus: 扫描状态
注意：此字段可能返回 null，表示取不到有效值。\n        :type ScanStatus: int\n        """
        self.PublicIp = None
        self.IntranetIp = None
        self.InstanceName = None
        self.InstanceId = None
        self.AssetType = None
        self.Area = None
        self.Switch = None
        self.Id = None
        self.PublicIpType = None
        self.PortTimes = None
        self.LastTime = None
        self.ScanMode = None
        self.ScanStatus = None


    def _deserialize(self, params):
        self.PublicIp = params.get("PublicIp")
        self.IntranetIp = params.get("IntranetIp")
        self.InstanceName = params.get("InstanceName")
        self.InstanceId = params.get("InstanceId")
        self.AssetType = params.get("AssetType")
        self.Area = params.get("Area")
        self.Switch = params.get("Switch")
        self.Id = params.get("Id")
        self.PublicIpType = params.get("PublicIpType")
        self.PortTimes = params.get("PortTimes")
        self.LastTime = params.get("LastTime")
        self.ScanMode = params.get("ScanMode")
        self.ScanStatus = params.get("ScanStatus")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TLogInfo(AbstractModel):
    """告警中心概览数据

    """

    def __init__(self):
        """
        :param OutNum: 失陷主机\n        :type OutNum: int\n        :param HandleNum: 待处置告警\n        :type HandleNum: int\n        :param VulNum: 漏洞攻击\n        :type VulNum: int\n        :param NetworkNum: 网络探测\n        :type NetworkNum: int\n        :param BanNum: 封禁列表\n        :type BanNum: int\n        :param BruteForceNum: 暴力破解\n        :type BruteForceNum: int\n        """
        self.OutNum = None
        self.HandleNum = None
        self.VulNum = None
        self.NetworkNum = None
        self.BanNum = None
        self.BruteForceNum = None


    def _deserialize(self, params):
        self.OutNum = params.get("OutNum")
        self.HandleNum = params.get("HandleNum")
        self.VulNum = params.get("VulNum")
        self.NetworkNum = params.get("NetworkNum")
        self.BanNum = params.get("BanNum")
        self.BruteForceNum = params.get("BruteForceNum")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UnHandleEvent(AbstractModel):
    """未处置事件详情

    """

    def __init__(self):
        """
        :param EventTableListStruct: 伪攻击链类型\n        :type EventTableListStruct: list of UnHandleEventDetail\n        :param BaseLineUser: 1 是  0否\n        :type BaseLineUser: int\n        :param BaseLineInSwitch: 1 打开 0 关闭\n        :type BaseLineInSwitch: int\n        :param BaseLineOutSwitch: 1 打开 0 关闭\n        :type BaseLineOutSwitch: int\n        """
        self.EventTableListStruct = None
        self.BaseLineUser = None
        self.BaseLineInSwitch = None
        self.BaseLineOutSwitch = None


    def _deserialize(self, params):
        if params.get("EventTableListStruct") is not None:
            self.EventTableListStruct = []
            for item in params.get("EventTableListStruct"):
                obj = UnHandleEventDetail()
                obj._deserialize(item)
                self.EventTableListStruct.append(obj)
        self.BaseLineUser = params.get("BaseLineUser")
        self.BaseLineInSwitch = params.get("BaseLineInSwitch")
        self.BaseLineOutSwitch = params.get("BaseLineOutSwitch")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UnHandleEventDetail(AbstractModel):
    """未处置事件信息汇总

    """

    def __init__(self):
        """
        :param EventName: 安全事件名称\n        :type EventName: str\n        :param Total: 未处置事件数量\n        :type Total: int\n        """
        self.EventName = None
        self.Total = None


    def _deserialize(self, params):
        self.EventName = params.get("EventName")
        self.Total = params.get("Total")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class VpcDnsInfo(AbstractModel):
    """nat防火墙 vpc dns 开关信息

    """

    def __init__(self):
        """
        :param VpcId: vpc id\n        :type VpcId: str\n        :param VpcName: vpc 名称\n        :type VpcName: str\n        :param FwMode: nat 防火墙模式 0：新增模式， 1: 接入模式\n        :type FwMode: int\n        :param VpcIpv4Cidr: vpc ipv4网段范围 CIDR（Classless Inter-Domain Routing，无类域间路由选择）\n        :type VpcIpv4Cidr: str\n        :param DNSEip: 外网弹性ip，防火墙 dns解析地址\n        :type DNSEip: str\n        :param NatInsId: nat网关id
注意：此字段可能返回 null，表示取不到有效值。\n        :type NatInsId: str\n        :param NatInsName: nat网关名称
注意：此字段可能返回 null，表示取不到有效值。\n        :type NatInsName: str\n        :param SwitchStatus: 0：开关关闭 ， 1: 开关打开\n        :type SwitchStatus: int\n        """
        self.VpcId = None
        self.VpcName = None
        self.FwMode = None
        self.VpcIpv4Cidr = None
        self.DNSEip = None
        self.NatInsId = None
        self.NatInsName = None
        self.SwitchStatus = None


    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.VpcName = params.get("VpcName")
        self.FwMode = params.get("FwMode")
        self.VpcIpv4Cidr = params.get("VpcIpv4Cidr")
        self.DNSEip = params.get("DNSEip")
        self.NatInsId = params.get("NatInsId")
        self.NatInsName = params.get("NatInsName")
        self.SwitchStatus = params.get("SwitchStatus")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class VpcZoneData(AbstractModel):
    """vpc区域数据详情

    """

    def __init__(self):
        """
        :param Zone: 可用区\n        :type Zone: str\n        :param Region: vpc节点地域\n        :type Region: str\n        """
        self.Zone = None
        self.Region = None


    def _deserialize(self, params):
        self.Zone = params.get("Zone")
        self.Region = params.get("Region")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        