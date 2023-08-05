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


class AIAssistantRequest(AbstractModel):
    """AIAssistant请求参数结构体

    """

    def __init__(self):
        """
        :param FileContent: 输入分析对象内容，输入数据格式参考FileType参数释义\n        :type FileContent: str\n        :param FileType: 输入分析对象类型，picture_url:图片地址，vod_url:视频地址，live_url：直播地址，audio_url: 音频文件，picture：图片二进制数据的BASE64编码\n        :type FileType: str\n        :param Lang: 音频源的语言，默认0为英文，1为中文\n        :type Lang: int\n        :param LibrarySet: 查询人员库列表\n        :type LibrarySet: list of str\n        :param MaxVideoDuration: 视频评估时间，单位秒，点播场景默认值为2小时（无法探测长度时）或完整视频，直播场景默认值为10分钟或直播提前结束\n        :type MaxVideoDuration: int\n        :param Template: 标准化模板选择：0：AI助教基础版本，1：AI评教基础版本，2：AI评教标准版本。AI 助教基础版本功能包括：人脸检索、人脸检测、人脸表情识别、学生动作选项，音频信息分析，微笑识别。AI 评教基础版本功能包括：人脸检索、人脸检测、人脸表情识别、音频信息分析。AI 评教标准版功能包括人脸检索、人脸检测、人脸表情识别、手势识别、音频信息分析、音频关键词分析、视频精彩集锦分析。\n        :type Template: int\n        :param VocabLibNameList: 识别词库名列表，评估过程使用这些词汇库中的词汇进行词汇使用行为分析\n        :type VocabLibNameList: list of str\n        :param VoiceEncodeType: 语音编码类型 1:pcm\n        :type VoiceEncodeType: int\n        :param VoiceFileType: 语音文件类型 1:raw, 2:wav, 3:mp3，10:视频（三种音频格式目前仅支持16k采样率16bit）\n        :type VoiceFileType: int\n        """
        self.FileContent = None
        self.FileType = None
        self.Lang = None
        self.LibrarySet = None
        self.MaxVideoDuration = None
        self.Template = None
        self.VocabLibNameList = None
        self.VoiceEncodeType = None
        self.VoiceFileType = None


    def _deserialize(self, params):
        self.FileContent = params.get("FileContent")
        self.FileType = params.get("FileType")
        self.Lang = params.get("Lang")
        self.LibrarySet = params.get("LibrarySet")
        self.MaxVideoDuration = params.get("MaxVideoDuration")
        self.Template = params.get("Template")
        self.VocabLibNameList = params.get("VocabLibNameList")
        self.VoiceEncodeType = params.get("VoiceEncodeType")
        self.VoiceFileType = params.get("VoiceFileType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AIAssistantResponse(AbstractModel):
    """AIAssistant返回参数结构体

    """

    def __init__(self):
        """
        :param ImageResults: 图像任务直接返回结果\n        :type ImageResults: list of ImageTaskResult\n        :param TaskId: 任务ID\n        :type TaskId: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.ImageResults = None
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ImageResults") is not None:
            self.ImageResults = []
            for item in params.get("ImageResults"):
                obj = ImageTaskResult()
                obj._deserialize(item)
                self.ImageResults.append(obj)
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class ASRStat(AbstractModel):
    """当前音频的统计结果

    """

    def __init__(self):
        """
        :param AvgSpeed: 当前音频的平均语速\n        :type AvgSpeed: float\n        :param AvgVolume: Vad的平均音量\n        :type AvgVolume: float\n        :param MaxVolume: Vad的最大音量\n        :type MaxVolume: float\n        :param MinVolume: Vad的最小音量\n        :type MinVolume: float\n        :param MuteDuration: 当前音频的非发音时长\n        :type MuteDuration: int\n        :param SoundDuration: 当前音频的发音时长\n        :type SoundDuration: int\n        :param TotalDuration: 当前音频的总时长\n        :type TotalDuration: int\n        :param VadNum: 当前音频的句子总数\n        :type VadNum: int\n        :param WordNum: 当前音频的单词总数\n        :type WordNum: int\n        """
        self.AvgSpeed = None
        self.AvgVolume = None
        self.MaxVolume = None
        self.MinVolume = None
        self.MuteDuration = None
        self.SoundDuration = None
        self.TotalDuration = None
        self.VadNum = None
        self.WordNum = None


    def _deserialize(self, params):
        self.AvgSpeed = params.get("AvgSpeed")
        self.AvgVolume = params.get("AvgVolume")
        self.MaxVolume = params.get("MaxVolume")
        self.MinVolume = params.get("MinVolume")
        self.MuteDuration = params.get("MuteDuration")
        self.SoundDuration = params.get("SoundDuration")
        self.TotalDuration = params.get("TotalDuration")
        self.VadNum = params.get("VadNum")
        self.WordNum = params.get("WordNum")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AbsenceInfo(AbstractModel):
    """缺勤人员信息

    """

    def __init__(self):
        """
        :param LibraryIds: 识别到的人员所在的库id\n        :type LibraryIds: str\n        :param PersonId: 识别到的人员id\n        :type PersonId: str\n        """
        self.LibraryIds = None
        self.PersonId = None


    def _deserialize(self, params):
        self.LibraryIds = params.get("LibraryIds")
        self.PersonId = params.get("PersonId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ActionCountStatistic(AbstractModel):
    """数量统计结果

    """

    def __init__(self):
        """
        :param Count: 数量\n        :type Count: int\n        :param Name: 名称\n        :type Name: str\n        """
        self.Count = None
        self.Name = None


    def _deserialize(self, params):
        self.Count = params.get("Count")
        self.Name = params.get("Name")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ActionDurationRatioStatistic(AbstractModel):
    """时长占比统计结果

    """

    def __init__(self):
        """
        :param Name: 名称\n        :type Name: str\n        :param Ratio: 比例\n        :type Ratio: float\n        """
        self.Name = None
        self.Ratio = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Ratio = params.get("Ratio")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ActionDurationStatistic(AbstractModel):
    """时长统计结果

    """

    def __init__(self):
        """
        :param Duration: 时长\n        :type Duration: int\n        :param Name: 名称\n        :type Name: str\n        """
        self.Duration = None
        self.Name = None


    def _deserialize(self, params):
        self.Duration = params.get("Duration")
        self.Name = params.get("Name")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ActionInfo(AbstractModel):
    """大教室场景肢体动作识别信息

    """

    def __init__(self):
        """
        :param BodyPosture: 躯体动作识别结果，包含坐着（sit）、站立（stand）和趴睡（sleep）\n        :type BodyPosture: :class:`tencentcloud.tci.v20190318.models.ActionType`\n        :param Handup: 举手识别结果，包含举手（hand）和未检测到举手（nothand）\n        :type Handup: :class:`tencentcloud.tci.v20190318.models.ActionType`\n        :param LookHead: 是否低头识别结果，包含抬头（lookingahead）和未检测到抬头（notlookingahead）\n        :type LookHead: :class:`tencentcloud.tci.v20190318.models.ActionType`\n        :param Writing: 是否写字识别结果，包含写字（write）和未检测到写字（notlookingahead）\n        :type Writing: :class:`tencentcloud.tci.v20190318.models.ActionType`\n        :param Height: 动作图像高度\n        :type Height: int\n        :param Left: 动作出现图像的左侧起始坐标位置\n        :type Left: int\n        :param Top: 动作出现图像的上侧起始侧坐标位置\n        :type Top: int\n        :param Width: 动作图像宽度\n        :type Width: int\n        """
        self.BodyPosture = None
        self.Handup = None
        self.LookHead = None
        self.Writing = None
        self.Height = None
        self.Left = None
        self.Top = None
        self.Width = None


    def _deserialize(self, params):
        if params.get("BodyPosture") is not None:
            self.BodyPosture = ActionType()
            self.BodyPosture._deserialize(params.get("BodyPosture"))
        if params.get("Handup") is not None:
            self.Handup = ActionType()
            self.Handup._deserialize(params.get("Handup"))
        if params.get("LookHead") is not None:
            self.LookHead = ActionType()
            self.LookHead._deserialize(params.get("LookHead"))
        if params.get("Writing") is not None:
            self.Writing = ActionType()
            self.Writing._deserialize(params.get("Writing"))
        self.Height = params.get("Height")
        self.Left = params.get("Left")
        self.Top = params.get("Top")
        self.Width = params.get("Width")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ActionStatistic(AbstractModel):
    """统计结果

    """

    def __init__(self):
        """
        :param ActionCount: 数量统计\n        :type ActionCount: list of ActionCountStatistic\n        :param ActionDuration: 时长统计\n        :type ActionDuration: list of ActionDurationStatistic\n        :param ActionDurationRatio: 时长比例统计\n        :type ActionDurationRatio: list of ActionDurationRatioStatistic\n        """
        self.ActionCount = None
        self.ActionDuration = None
        self.ActionDurationRatio = None


    def _deserialize(self, params):
        if params.get("ActionCount") is not None:
            self.ActionCount = []
            for item in params.get("ActionCount"):
                obj = ActionCountStatistic()
                obj._deserialize(item)
                self.ActionCount.append(obj)
        if params.get("ActionDuration") is not None:
            self.ActionDuration = []
            for item in params.get("ActionDuration"):
                obj = ActionDurationStatistic()
                obj._deserialize(item)
                self.ActionDuration.append(obj)
        if params.get("ActionDurationRatio") is not None:
            self.ActionDurationRatio = []
            for item in params.get("ActionDurationRatio"):
                obj = ActionDurationRatioStatistic()
                obj._deserialize(item)
                self.ActionDurationRatio.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ActionType(AbstractModel):
    """动作行为子类型

    """

    def __init__(self):
        """
        :param Confidence: 置信度\n        :type Confidence: float\n        :param Type: 动作类别\n        :type Type: str\n        """
        self.Confidence = None
        self.Type = None


    def _deserialize(self, params):
        self.Confidence = params.get("Confidence")
        self.Type = params.get("Type")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AllMuteSlice(AbstractModel):
    """如果请求中开启了静音检测开关，则会返回所有的静音片段（静音时长超过阈值的片段）。

    """

    def __init__(self):
        """
        :param MuteSlice: 所有静音片段。\n        :type MuteSlice: list of MuteSlice\n        :param MuteRatio: 静音时长占比。\n        :type MuteRatio: float\n        :param TotalMuteDuration: 静音总时长。\n        :type TotalMuteDuration: int\n        """
        self.MuteSlice = None
        self.MuteRatio = None
        self.TotalMuteDuration = None


    def _deserialize(self, params):
        if params.get("MuteSlice") is not None:
            self.MuteSlice = []
            for item in params.get("MuteSlice"):
                obj = MuteSlice()
                obj._deserialize(item)
                self.MuteSlice.append(obj)
        self.MuteRatio = params.get("MuteRatio")
        self.TotalMuteDuration = params.get("TotalMuteDuration")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AttendanceInfo(AbstractModel):
    """识别到的人员信息

    """

    def __init__(self):
        """
        :param Face: 识别到的人员信息\n        :type Face: :class:`tencentcloud.tci.v20190318.models.FrameInfo`\n        :param PersonId: 识别到的人员id\n        :type PersonId: str\n        """
        self.Face = None
        self.PersonId = None


    def _deserialize(self, params):
        if params.get("Face") is not None:
            self.Face = FrameInfo()
            self.Face._deserialize(params.get("Face"))
        self.PersonId = params.get("PersonId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BodyMovementResult(AbstractModel):
    """老师肢体动作识别结果

    """

    def __init__(self):
        """
        :param Confidence: 置信度\n        :type Confidence: float\n        :param Height: 识别结果高度\n        :type Height: int\n        :param Left: 识别结果左坐标\n        :type Left: int\n        :param Movements: 老师动作识别结果，包含
1、teach_on_positive_attitude 正面讲解
2、point_to_the_blackboard 指黑板
3、writing_blackboard 写板书
4、other 其他\n        :type Movements: str\n        :param Top: 识别结果顶坐标\n        :type Top: int\n        :param Width: 识别结果宽度\n        :type Width: int\n        """
        self.Confidence = None
        self.Height = None
        self.Left = None
        self.Movements = None
        self.Top = None
        self.Width = None


    def _deserialize(self, params):
        self.Confidence = params.get("Confidence")
        self.Height = params.get("Height")
        self.Left = params.get("Left")
        self.Movements = params.get("Movements")
        self.Top = params.get("Top")
        self.Width = params.get("Width")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CancelTaskRequest(AbstractModel):
    """CancelTask请求参数结构体

    """

    def __init__(self):
        """
        :param JobId: 待取消任务标志符。\n        :type JobId: int\n        """
        self.JobId = None


    def _deserialize(self, params):
        self.JobId = params.get("JobId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CancelTaskResponse(AbstractModel):
    """CancelTask返回参数结构体

    """

    def __init__(self):
        """
        :param JobId: 取消任务标志符。\n        :type JobId: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.JobId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.JobId = params.get("JobId")
        self.RequestId = params.get("RequestId")


class CheckFacePhotoRequest(AbstractModel):
    """CheckFacePhoto请求参数结构体

    """

    def __init__(self):
        """
        :param FileContent: 输入分析对象内容\n        :type FileContent: str\n        :param FileType: 输入分析对象类型，picture_url:图片地址\n        :type FileType: str\n        """
        self.FileContent = None
        self.FileType = None


    def _deserialize(self, params):
        self.FileContent = params.get("FileContent")
        self.FileType = params.get("FileType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckFacePhotoResponse(AbstractModel):
    """CheckFacePhoto返回参数结构体

    """

    def __init__(self):
        """
        :param CheckResult: 人脸检查结果，0：通过检查，1：图片模糊\n        :type CheckResult: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.CheckResult = None
        self.RequestId = None


    def _deserialize(self, params):
        self.CheckResult = params.get("CheckResult")
        self.RequestId = params.get("RequestId")


class CreateFaceRequest(AbstractModel):
    """CreateFace请求参数结构体

    """

    def __init__(self):
        """
        :param PersonId: 人员唯一标识符\n        :type PersonId: str\n        :param Images: 图片数据 base64 字符串，与 Urls 参数选择一个输入\n        :type Images: list of str\n        :param LibraryId: 人员库唯一标识符\n        :type LibraryId: str\n        :param Urls: 图片下载地址，与 Images 参数选择一个输入\n        :type Urls: list of str\n        """
        self.PersonId = None
        self.Images = None
        self.LibraryId = None
        self.Urls = None


    def _deserialize(self, params):
        self.PersonId = params.get("PersonId")
        self.Images = params.get("Images")
        self.LibraryId = params.get("LibraryId")
        self.Urls = params.get("Urls")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateFaceResponse(AbstractModel):
    """CreateFace返回参数结构体

    """

    def __init__(self):
        """
        :param FaceInfoSet: 人脸操作结果信息\n        :type FaceInfoSet: list of FaceInfo\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.FaceInfoSet = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("FaceInfoSet") is not None:
            self.FaceInfoSet = []
            for item in params.get("FaceInfoSet"):
                obj = FaceInfo()
                obj._deserialize(item)
                self.FaceInfoSet.append(obj)
        self.RequestId = params.get("RequestId")


class CreateLibraryRequest(AbstractModel):
    """CreateLibrary请求参数结构体

    """

    def __init__(self):
        """
        :param LibraryName: 人员库名称\n        :type LibraryName: str\n        :param LibraryId: 人员库唯一标志符，为空则系统自动生成。\n        :type LibraryId: str\n        """
        self.LibraryName = None
        self.LibraryId = None


    def _deserialize(self, params):
        self.LibraryName = params.get("LibraryName")
        self.LibraryId = params.get("LibraryId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateLibraryResponse(AbstractModel):
    """CreateLibrary返回参数结构体

    """

    def __init__(self):
        """
        :param LibraryId: 人员库唯一标识符\n        :type LibraryId: str\n        :param LibraryName: 人员库名称\n        :type LibraryName: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.LibraryId = None
        self.LibraryName = None
        self.RequestId = None


    def _deserialize(self, params):
        self.LibraryId = params.get("LibraryId")
        self.LibraryName = params.get("LibraryName")
        self.RequestId = params.get("RequestId")


class CreatePersonRequest(AbstractModel):
    """CreatePerson请求参数结构体

    """

    def __init__(self):
        """
        :param LibraryId: 人员库唯一标识符\n        :type LibraryId: str\n        :param PersonName: 人员名称\n        :type PersonName: str\n        :param Images: 图片数据 base64 字符串，与 Urls 参数选择一个输入\n        :type Images: list of str\n        :param JobNumber: 人员工作号码\n        :type JobNumber: str\n        :param Mail: 人员邮箱\n        :type Mail: str\n        :param Male: 人员性别，0：未知 1：男性，2：女性\n        :type Male: int\n        :param PersonId: 自定义人员 ID，注意不能使用 tci_person_ 前缀\n        :type PersonId: str\n        :param PhoneNumber: 人员电话号码\n        :type PhoneNumber: str\n        :param StudentNumber: 人员学生号码\n        :type StudentNumber: str\n        :param Urls: 图片下载地址，与 Images 参数选择一个输入\n        :type Urls: list of str\n        """
        self.LibraryId = None
        self.PersonName = None
        self.Images = None
        self.JobNumber = None
        self.Mail = None
        self.Male = None
        self.PersonId = None
        self.PhoneNumber = None
        self.StudentNumber = None
        self.Urls = None


    def _deserialize(self, params):
        self.LibraryId = params.get("LibraryId")
        self.PersonName = params.get("PersonName")
        self.Images = params.get("Images")
        self.JobNumber = params.get("JobNumber")
        self.Mail = params.get("Mail")
        self.Male = params.get("Male")
        self.PersonId = params.get("PersonId")
        self.PhoneNumber = params.get("PhoneNumber")
        self.StudentNumber = params.get("StudentNumber")
        self.Urls = params.get("Urls")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreatePersonResponse(AbstractModel):
    """CreatePerson返回参数结构体

    """

    def __init__(self):
        """
        :param FaceInfoSet: 人脸操作结果信息\n        :type FaceInfoSet: list of FaceInfo\n        :param LibraryId: 人员库唯一标识符\n        :type LibraryId: str\n        :param PersonId: 人员唯一标识符\n        :type PersonId: str\n        :param PersonName: 人员名称\n        :type PersonName: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.FaceInfoSet = None
        self.LibraryId = None
        self.PersonId = None
        self.PersonName = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("FaceInfoSet") is not None:
            self.FaceInfoSet = []
            for item in params.get("FaceInfoSet"):
                obj = FaceInfo()
                obj._deserialize(item)
                self.FaceInfoSet.append(obj)
        self.LibraryId = params.get("LibraryId")
        self.PersonId = params.get("PersonId")
        self.PersonName = params.get("PersonName")
        self.RequestId = params.get("RequestId")


class CreateVocabLibRequest(AbstractModel):
    """CreateVocabLib请求参数结构体

    """

    def __init__(self):
        """
        :param VocabLibName: 词汇库名称\n        :type VocabLibName: str\n        """
        self.VocabLibName = None


    def _deserialize(self, params):
        self.VocabLibName = params.get("VocabLibName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateVocabLibResponse(AbstractModel):
    """CreateVocabLib返回参数结构体

    """

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateVocabRequest(AbstractModel):
    """CreateVocab请求参数结构体

    """

    def __init__(self):
        """
        :param VocabLibName: 要添加词汇的词汇库名\n        :type VocabLibName: str\n        :param VocabList: 要添加的词汇列表\n        :type VocabList: list of str\n        """
        self.VocabLibName = None
        self.VocabList = None


    def _deserialize(self, params):
        self.VocabLibName = params.get("VocabLibName")
        self.VocabList = params.get("VocabList")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateVocabResponse(AbstractModel):
    """CreateVocab返回参数结构体

    """

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteFaceRequest(AbstractModel):
    """DeleteFace请求参数结构体

    """

    def __init__(self):
        """
        :param FaceIdSet: 人脸标识符数组\n        :type FaceIdSet: list of str\n        :param PersonId: 人员唯一标识符\n        :type PersonId: str\n        :param LibraryId: 人员库唯一标识符\n        :type LibraryId: str\n        """
        self.FaceIdSet = None
        self.PersonId = None
        self.LibraryId = None


    def _deserialize(self, params):
        self.FaceIdSet = params.get("FaceIdSet")
        self.PersonId = params.get("PersonId")
        self.LibraryId = params.get("LibraryId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteFaceResponse(AbstractModel):
    """DeleteFace返回参数结构体

    """

    def __init__(self):
        """
        :param FaceInfoSet: 人脸操作结果\n        :type FaceInfoSet: list of FaceInfo\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.FaceInfoSet = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("FaceInfoSet") is not None:
            self.FaceInfoSet = []
            for item in params.get("FaceInfoSet"):
                obj = FaceInfo()
                obj._deserialize(item)
                self.FaceInfoSet.append(obj)
        self.RequestId = params.get("RequestId")


class DeleteLibraryRequest(AbstractModel):
    """DeleteLibrary请求参数结构体

    """

    def __init__(self):
        """
        :param LibraryId: 人员库唯一标识符\n        :type LibraryId: str\n        """
        self.LibraryId = None


    def _deserialize(self, params):
        self.LibraryId = params.get("LibraryId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteLibraryResponse(AbstractModel):
    """DeleteLibrary返回参数结构体

    """

    def __init__(self):
        """
        :param LibraryId: 人员库唯一标识符\n        :type LibraryId: str\n        :param LibraryName: 人员库名称\n        :type LibraryName: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.LibraryId = None
        self.LibraryName = None
        self.RequestId = None


    def _deserialize(self, params):
        self.LibraryId = params.get("LibraryId")
        self.LibraryName = params.get("LibraryName")
        self.RequestId = params.get("RequestId")


class DeletePersonRequest(AbstractModel):
    """DeletePerson请求参数结构体

    """

    def __init__(self):
        """
        :param LibraryId: 人员库唯一标识符\n        :type LibraryId: str\n        :param PersonId: 人员唯一标识符\n        :type PersonId: str\n        """
        self.LibraryId = None
        self.PersonId = None


    def _deserialize(self, params):
        self.LibraryId = params.get("LibraryId")
        self.PersonId = params.get("PersonId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeletePersonResponse(AbstractModel):
    """DeletePerson返回参数结构体

    """

    def __init__(self):
        """
        :param FaceInfoSet: 人脸信息\n        :type FaceInfoSet: list of FaceInfo\n        :param LibraryId: 人员库唯一标识符\n        :type LibraryId: str\n        :param PersonId: 人员唯一标识符\n        :type PersonId: str\n        :param PersonName: 人员名称\n        :type PersonName: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.FaceInfoSet = None
        self.LibraryId = None
        self.PersonId = None
        self.PersonName = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("FaceInfoSet") is not None:
            self.FaceInfoSet = []
            for item in params.get("FaceInfoSet"):
                obj = FaceInfo()
                obj._deserialize(item)
                self.FaceInfoSet.append(obj)
        self.LibraryId = params.get("LibraryId")
        self.PersonId = params.get("PersonId")
        self.PersonName = params.get("PersonName")
        self.RequestId = params.get("RequestId")


class DeleteVocabLibRequest(AbstractModel):
    """DeleteVocabLib请求参数结构体

    """

    def __init__(self):
        """
        :param VocabLibName: 词汇库名称\n        :type VocabLibName: str\n        """
        self.VocabLibName = None


    def _deserialize(self, params):
        self.VocabLibName = params.get("VocabLibName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteVocabLibResponse(AbstractModel):
    """DeleteVocabLib返回参数结构体

    """

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteVocabRequest(AbstractModel):
    """DeleteVocab请求参数结构体

    """

    def __init__(self):
        """
        :param VocabLibName: 要删除词汇的词汇库名\n        :type VocabLibName: str\n        :param VocabList: 要删除的词汇列表\n        :type VocabList: list of str\n        """
        self.VocabLibName = None
        self.VocabList = None


    def _deserialize(self, params):
        self.VocabLibName = params.get("VocabLibName")
        self.VocabList = params.get("VocabList")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteVocabResponse(AbstractModel):
    """DeleteVocab返回参数结构体

    """

    def __init__(self):
        """
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DescribeAITaskResultRequest(AbstractModel):
    """DescribeAITaskResult请求参数结构体

    """

    def __init__(self):
        """
        :param TaskId: 任务唯一标识符。在URL方式时提交请求后会返回一个任务标识符，后续查询该url的结果时使用这个标识符进行查询。\n        :type TaskId: int\n        :param Limit: 限制数目\n        :type Limit: int\n        :param Offset: 偏移量\n        :type Offset: int\n        """
        self.TaskId = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAITaskResultResponse(AbstractModel):
    """DescribeAITaskResult返回参数结构体

    """

    def __init__(self):
        """
        :param AudioResult: 音频分析结果\n        :type AudioResult: :class:`tencentcloud.tci.v20190318.models.StandardAudioResult`\n        :param ImageResult: 图像分析结果\n        :type ImageResult: :class:`tencentcloud.tci.v20190318.models.StandardImageResult`\n        :param VideoResult: 视频分析结果\n        :type VideoResult: :class:`tencentcloud.tci.v20190318.models.StandardVideoResult`\n        :param Status: 任务状态\n        :type Status: str\n        :param TaskId: 任务唯一id。在URL方式时提交请求后会返回一个jobid，后续查询该url的结果时使用这个jobid进行查询。\n        :type TaskId: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.AudioResult = None
        self.ImageResult = None
        self.VideoResult = None
        self.Status = None
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("AudioResult") is not None:
            self.AudioResult = StandardAudioResult()
            self.AudioResult._deserialize(params.get("AudioResult"))
        if params.get("ImageResult") is not None:
            self.ImageResult = StandardImageResult()
            self.ImageResult._deserialize(params.get("ImageResult"))
        if params.get("VideoResult") is not None:
            self.VideoResult = StandardVideoResult()
            self.VideoResult._deserialize(params.get("VideoResult"))
        self.Status = params.get("Status")
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class DescribeAttendanceResultRequest(AbstractModel):
    """DescribeAttendanceResult请求参数结构体

    """

    def __init__(self):
        """
        :param JobId: 任务唯一标识符\n        :type JobId: int\n        """
        self.JobId = None


    def _deserialize(self, params):
        self.JobId = params.get("JobId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAttendanceResultResponse(AbstractModel):
    """DescribeAttendanceResult返回参数结构体

    """

    def __init__(self):
        """
        :param AbsenceSetInLibs: 缺失人员的ID列表(只针对请求中的libids字段)\n        :type AbsenceSetInLibs: list of AbsenceInfo\n        :param AttendanceSet: 确定出勤人员列表\n        :type AttendanceSet: list of AttendanceInfo\n        :param SuspectedSet: 疑似出勤人员列表\n        :type SuspectedSet: list of SuspectedInfo\n        :param AbsenceSet: 缺失人员的ID列表(只针对请求中的personids字段)\n        :type AbsenceSet: list of str\n        :param Progress: 请求处理进度\n        :type Progress: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.AbsenceSetInLibs = None
        self.AttendanceSet = None
        self.SuspectedSet = None
        self.AbsenceSet = None
        self.Progress = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("AbsenceSetInLibs") is not None:
            self.AbsenceSetInLibs = []
            for item in params.get("AbsenceSetInLibs"):
                obj = AbsenceInfo()
                obj._deserialize(item)
                self.AbsenceSetInLibs.append(obj)
        if params.get("AttendanceSet") is not None:
            self.AttendanceSet = []
            for item in params.get("AttendanceSet"):
                obj = AttendanceInfo()
                obj._deserialize(item)
                self.AttendanceSet.append(obj)
        if params.get("SuspectedSet") is not None:
            self.SuspectedSet = []
            for item in params.get("SuspectedSet"):
                obj = SuspectedInfo()
                obj._deserialize(item)
                self.SuspectedSet.append(obj)
        self.AbsenceSet = params.get("AbsenceSet")
        self.Progress = params.get("Progress")
        self.RequestId = params.get("RequestId")


class DescribeAudioTaskRequest(AbstractModel):
    """DescribeAudioTask请求参数结构体

    """

    def __init__(self):
        """
        :param JobId: 音频任务唯一id。在URL方式时提交请求后会返回一个jobid，后续查询该url的结果时使用这个jobid进行查询。\n        :type JobId: int\n        :param Limit: 限制数目\n        :type Limit: int\n        :param Offset: 偏移量\n        :type Offset: int\n        """
        self.JobId = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.JobId = params.get("JobId")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAudioTaskResponse(AbstractModel):
    """DescribeAudioTask返回参数结构体

    """

    def __init__(self):
        """
        :param AllMuteSlice: 如果请求中开启了静音检测开关，则会返回所有的静音片段（静音时长超过阈值的片段）。\n        :type AllMuteSlice: :class:`tencentcloud.tci.v20190318.models.AllMuteSlice`\n        :param AsrStat: 返回的当前音频的统计信息。当进度为100时返回。\n        :type AsrStat: :class:`tencentcloud.tci.v20190318.models.ASRStat`\n        :param Texts: 返回当前音频流的详细信息，如果是流模式，返回的是对应流的详细信息，如果是 URL模式，返回的是查询的那一段seq对应的音频的详细信息。\n        :type Texts: list of WholeTextItem\n        :param VocabAnalysisDetailInfo: 返回词汇库中的单词出现的详细时间信息。\n        :type VocabAnalysisDetailInfo: list of VocabDetailInfomation\n        :param VocabAnalysisStatInfo: 返回词汇库中的单词出现的次数信息。\n        :type VocabAnalysisStatInfo: list of VocabStatInfomation\n        :param AllTexts: 返回音频全部文本。\n        :type AllTexts: str\n        :param JobId: 音频任务唯一id。在URL方式时提交请求后会返回一个jobid，后续查询该url的结果时使用这个jobid进行查询。\n        :type JobId: int\n        :param Progress: 返回的当前处理进度。\n        :type Progress: float\n        :param TotalCount: 结果总数\n        :type TotalCount: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.AllMuteSlice = None
        self.AsrStat = None
        self.Texts = None
        self.VocabAnalysisDetailInfo = None
        self.VocabAnalysisStatInfo = None
        self.AllTexts = None
        self.JobId = None
        self.Progress = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("AllMuteSlice") is not None:
            self.AllMuteSlice = AllMuteSlice()
            self.AllMuteSlice._deserialize(params.get("AllMuteSlice"))
        if params.get("AsrStat") is not None:
            self.AsrStat = ASRStat()
            self.AsrStat._deserialize(params.get("AsrStat"))
        if params.get("Texts") is not None:
            self.Texts = []
            for item in params.get("Texts"):
                obj = WholeTextItem()
                obj._deserialize(item)
                self.Texts.append(obj)
        if params.get("VocabAnalysisDetailInfo") is not None:
            self.VocabAnalysisDetailInfo = []
            for item in params.get("VocabAnalysisDetailInfo"):
                obj = VocabDetailInfomation()
                obj._deserialize(item)
                self.VocabAnalysisDetailInfo.append(obj)
        if params.get("VocabAnalysisStatInfo") is not None:
            self.VocabAnalysisStatInfo = []
            for item in params.get("VocabAnalysisStatInfo"):
                obj = VocabStatInfomation()
                obj._deserialize(item)
                self.VocabAnalysisStatInfo.append(obj)
        self.AllTexts = params.get("AllTexts")
        self.JobId = params.get("JobId")
        self.Progress = params.get("Progress")
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeConversationTaskRequest(AbstractModel):
    """DescribeConversationTask请求参数结构体

    """

    def __init__(self):
        """
        :param JobId: 音频任务唯一id。在URL方式时提交请求后会返回一个jobid，后续查询该url的结果时使用这个jobid进行查询。\n        :type JobId: int\n        :param Identity: 要查询明细的流的身份，1 老师 2 学生\n        :type Identity: int\n        :param Limit: 限制数目\n        :type Limit: int\n        :param Offset: 偏移量\n        :type Offset: int\n        """
        self.JobId = None
        self.Identity = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.JobId = params.get("JobId")
        self.Identity = params.get("Identity")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeConversationTaskResponse(AbstractModel):
    """DescribeConversationTask返回参数结构体

    """

    def __init__(self):
        """
        :param AsrStat: 返回的当前音频的统计信息。当进度为100时返回。\n        :type AsrStat: :class:`tencentcloud.tci.v20190318.models.ASRStat`\n        :param Texts: 返回当前音频流的详细信息，如果是流模式，返回的是对应流的详细信息，如果是 URL模式，返回的是查询的那一段seq对应的音频的详细信息。\n        :type Texts: list of WholeTextItem\n        :param VocabAnalysisDetailInfo: 返回词汇库中的单词出现的详细时间信息。\n        :type VocabAnalysisDetailInfo: list of VocabDetailInfomation\n        :param VocabAnalysisStatInfo: 返回词汇库中的单词出现的次数信息。\n        :type VocabAnalysisStatInfo: list of VocabStatInfomation\n        :param AllTexts: 整个音频流的全部文本\n        :type AllTexts: str\n        :param JobId: 音频任务唯一id。在URL方式时提交请求后会返回一个jobid，后续查询该url的结果时使用这个jobid进行查询。\n        :type JobId: int\n        :param Progress: 返回的当前处理进度。\n        :type Progress: float\n        :param TotalCount: 结果总数\n        :type TotalCount: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.AsrStat = None
        self.Texts = None
        self.VocabAnalysisDetailInfo = None
        self.VocabAnalysisStatInfo = None
        self.AllTexts = None
        self.JobId = None
        self.Progress = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("AsrStat") is not None:
            self.AsrStat = ASRStat()
            self.AsrStat._deserialize(params.get("AsrStat"))
        if params.get("Texts") is not None:
            self.Texts = []
            for item in params.get("Texts"):
                obj = WholeTextItem()
                obj._deserialize(item)
                self.Texts.append(obj)
        if params.get("VocabAnalysisDetailInfo") is not None:
            self.VocabAnalysisDetailInfo = []
            for item in params.get("VocabAnalysisDetailInfo"):
                obj = VocabDetailInfomation()
                obj._deserialize(item)
                self.VocabAnalysisDetailInfo.append(obj)
        if params.get("VocabAnalysisStatInfo") is not None:
            self.VocabAnalysisStatInfo = []
            for item in params.get("VocabAnalysisStatInfo"):
                obj = VocabStatInfomation()
                obj._deserialize(item)
                self.VocabAnalysisStatInfo.append(obj)
        self.AllTexts = params.get("AllTexts")
        self.JobId = params.get("JobId")
        self.Progress = params.get("Progress")
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeHighlightResultRequest(AbstractModel):
    """DescribeHighlightResult请求参数结构体

    """

    def __init__(self):
        """
        :param JobId: 精彩集锦任务唯一id。在URL方式时提交请求后会返回一个JobId，后续查询该url的结果时使用这个JobId进行查询。\n        :type JobId: int\n        """
        self.JobId = None


    def _deserialize(self, params):
        self.JobId = params.get("JobId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeHighlightResultResponse(AbstractModel):
    """DescribeHighlightResult返回参数结构体

    """

    def __init__(self):
        """
        :param HighlightsInfo: 精彩集锦详细信息。\n        :type HighlightsInfo: list of HighlightsInfomation\n        :param JobId: 精彩集锦任务唯一id。在URL方式时提交请求后会返回一个JobId，后续查询该url的结果时使用这个JobId进行查询。\n        :type JobId: int\n        :param Progress: 任务的进度百分比，100表示任务已完成。\n        :type Progress: float\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.HighlightsInfo = None
        self.JobId = None
        self.Progress = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("HighlightsInfo") is not None:
            self.HighlightsInfo = []
            for item in params.get("HighlightsInfo"):
                obj = HighlightsInfomation()
                obj._deserialize(item)
                self.HighlightsInfo.append(obj)
        self.JobId = params.get("JobId")
        self.Progress = params.get("Progress")
        self.RequestId = params.get("RequestId")


class DescribeImageTaskRequest(AbstractModel):
    """DescribeImageTask请求参数结构体

    """

    def __init__(self):
        """
        :param JobId: 任务标识符\n        :type JobId: int\n        :param Limit: 限制数目\n        :type Limit: int\n        :param Offset: 偏移量\n        :type Offset: int\n        """
        self.JobId = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.JobId = params.get("JobId")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeImageTaskResponse(AbstractModel):
    """DescribeImageTask返回参数结构体

    """

    def __init__(self):
        """
        :param ResultSet: 任务处理结果\n        :type ResultSet: list of ImageTaskResult\n        :param JobId: 任务唯一标识\n        :type JobId: int\n        :param Progress: 任务执行进度\n        :type Progress: int\n        :param TotalCount: 任务结果数目\n        :type TotalCount: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.ResultSet = None
        self.JobId = None
        self.Progress = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ResultSet") is not None:
            self.ResultSet = []
            for item in params.get("ResultSet"):
                obj = ImageTaskResult()
                obj._deserialize(item)
                self.ResultSet.append(obj)
        self.JobId = params.get("JobId")
        self.Progress = params.get("Progress")
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeImageTaskStatisticRequest(AbstractModel):
    """DescribeImageTaskStatistic请求参数结构体

    """

    def __init__(self):
        """
        :param JobId: 图像任务标识符\n        :type JobId: int\n        """
        self.JobId = None


    def _deserialize(self, params):
        self.JobId = params.get("JobId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeImageTaskStatisticResponse(AbstractModel):
    """DescribeImageTaskStatistic返回参数结构体

    """

    def __init__(self):
        """
        :param Statistic: 任务统计信息\n        :type Statistic: :class:`tencentcloud.tci.v20190318.models.ImageTaskStatistic`\n        :param JobId: 图像任务唯一标识符\n        :type JobId: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.Statistic = None
        self.JobId = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Statistic") is not None:
            self.Statistic = ImageTaskStatistic()
            self.Statistic._deserialize(params.get("Statistic"))
        self.JobId = params.get("JobId")
        self.RequestId = params.get("RequestId")


class DescribeLibrariesRequest(AbstractModel):
    """DescribeLibraries请求参数结构体

    """


class DescribeLibrariesResponse(AbstractModel):
    """DescribeLibraries返回参数结构体

    """

    def __init__(self):
        """
        :param LibrarySet: 人员库列表\n        :type LibrarySet: list of Library\n        :param TotalCount: 人员库总数量\n        :type TotalCount: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.LibrarySet = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("LibrarySet") is not None:
            self.LibrarySet = []
            for item in params.get("LibrarySet"):
                obj = Library()
                obj._deserialize(item)
                self.LibrarySet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribePersonRequest(AbstractModel):
    """DescribePerson请求参数结构体

    """

    def __init__(self):
        """
        :param LibraryId: 人员库唯一标识符\n        :type LibraryId: str\n        :param PersonId: 人员唯一标识符\n        :type PersonId: str\n        """
        self.LibraryId = None
        self.PersonId = None


    def _deserialize(self, params):
        self.LibraryId = params.get("LibraryId")
        self.PersonId = params.get("PersonId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribePersonResponse(AbstractModel):
    """DescribePerson返回参数结构体

    """

    def __init__(self):
        """
        :param FaceSet: 人员人脸列表\n        :type FaceSet: list of Face\n        :param CreateTime: 创建时间\n        :type CreateTime: str\n        :param JobNumber: 工作号码\n        :type JobNumber: str\n        :param LibraryId: 人员库唯一标识符\n        :type LibraryId: str\n        :param Mail: 邮箱\n        :type Mail: str\n        :param Male: 性别\n        :type Male: int\n        :param PersonId: 人员唯一标识符\n        :type PersonId: str\n        :param PersonName: 人员名称\n        :type PersonName: str\n        :param PhoneNumber: 电话号码\n        :type PhoneNumber: str\n        :param StudentNumber: 学生号码\n        :type StudentNumber: str\n        :param UpdateTime: 修改时间\n        :type UpdateTime: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.FaceSet = None
        self.CreateTime = None
        self.JobNumber = None
        self.LibraryId = None
        self.Mail = None
        self.Male = None
        self.PersonId = None
        self.PersonName = None
        self.PhoneNumber = None
        self.StudentNumber = None
        self.UpdateTime = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("FaceSet") is not None:
            self.FaceSet = []
            for item in params.get("FaceSet"):
                obj = Face()
                obj._deserialize(item)
                self.FaceSet.append(obj)
        self.CreateTime = params.get("CreateTime")
        self.JobNumber = params.get("JobNumber")
        self.LibraryId = params.get("LibraryId")
        self.Mail = params.get("Mail")
        self.Male = params.get("Male")
        self.PersonId = params.get("PersonId")
        self.PersonName = params.get("PersonName")
        self.PhoneNumber = params.get("PhoneNumber")
        self.StudentNumber = params.get("StudentNumber")
        self.UpdateTime = params.get("UpdateTime")
        self.RequestId = params.get("RequestId")


class DescribePersonsRequest(AbstractModel):
    """DescribePersons请求参数结构体

    """

    def __init__(self):
        """
        :param LibraryId: 人员库唯一标识符\n        :type LibraryId: str\n        :param Limit: 限制数目\n        :type Limit: int\n        :param Offset: 偏移量\n        :type Offset: int\n        """
        self.LibraryId = None
        self.Limit = None
        self.Offset = None


    def _deserialize(self, params):
        self.LibraryId = params.get("LibraryId")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribePersonsResponse(AbstractModel):
    """DescribePersons返回参数结构体

    """

    def __init__(self):
        """
        :param PersonSet: 人员列表\n        :type PersonSet: list of Person\n        :param TotalCount: 人员总数\n        :type TotalCount: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.PersonSet = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("PersonSet") is not None:
            self.PersonSet = []
            for item in params.get("PersonSet"):
                obj = Person()
                obj._deserialize(item)
                self.PersonSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeVocabLibRequest(AbstractModel):
    """DescribeVocabLib请求参数结构体

    """


class DescribeVocabLibResponse(AbstractModel):
    """DescribeVocabLib返回参数结构体

    """

    def __init__(self):
        """
        :param VocabLibNameSet: 返回该appid下的所有词汇库名\n        :type VocabLibNameSet: list of str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.VocabLibNameSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.VocabLibNameSet = params.get("VocabLibNameSet")
        self.RequestId = params.get("RequestId")


class DescribeVocabRequest(AbstractModel):
    """DescribeVocab请求参数结构体

    """

    def __init__(self):
        """
        :param VocabLibName: 要查询词汇的词汇库名\n        :type VocabLibName: str\n        """
        self.VocabLibName = None


    def _deserialize(self, params):
        self.VocabLibName = params.get("VocabLibName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeVocabResponse(AbstractModel):
    """DescribeVocab返回参数结构体

    """

    def __init__(self):
        """
        :param VocabNameSet: 词汇列表\n        :type VocabNameSet: list of str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.VocabNameSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.VocabNameSet = params.get("VocabNameSet")
        self.RequestId = params.get("RequestId")


class DetailInfo(AbstractModel):
    """单词出现的那个句子的起始时间和结束时间信息

    """

    def __init__(self):
        """
        :param Value: 单词出现在该音频中的那个句子的时间戳，出现了几次， 就返回对应次数的起始和结束时间戳\n        :type Value: list of WordTimePair\n        :param Keyword: 词汇库中的单词\n        :type Keyword: str\n        """
        self.Value = None
        self.Keyword = None


    def _deserialize(self, params):
        if params.get("Value") is not None:
            self.Value = []
            for item in params.get("Value"):
                obj = WordTimePair()
                obj._deserialize(item)
                self.Value.append(obj)
        self.Keyword = params.get("Keyword")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DoubleVideoFunction(AbstractModel):
    """双路混流视频集锦开关项

    """

    def __init__(self):
        """
        :param EnableCoverPictures: 片头片尾增加图片开关\n        :type EnableCoverPictures: bool\n        """
        self.EnableCoverPictures = None


    def _deserialize(self, params):
        self.EnableCoverPictures = params.get("EnableCoverPictures")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ExpressRatioStatistic(AbstractModel):
    """表情比例统计

    """

    def __init__(self):
        """
        :param Count: 出现次数\n        :type Count: int\n        :param Express: 表情\n        :type Express: str\n        :param Ratio: 该表情时长占所有表情时长的比例\n        :type Ratio: float\n        :param RatioUseDuration: 该表情时长占视频总时长的比例\n        :type RatioUseDuration: float\n        """
        self.Count = None
        self.Express = None
        self.Ratio = None
        self.RatioUseDuration = None


    def _deserialize(self, params):
        self.Count = params.get("Count")
        self.Express = params.get("Express")
        self.Ratio = params.get("Ratio")
        self.RatioUseDuration = params.get("RatioUseDuration")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Face(AbstractModel):
    """人脸描述

    """

    def __init__(self):
        """
        :param FaceId: 人脸唯一标识符\n        :type FaceId: str\n        :param FaceUrl: 人脸图片 URL\n        :type FaceUrl: str\n        :param PersonId: 人员唯一标识符\n        :type PersonId: str\n        """
        self.FaceId = None
        self.FaceUrl = None
        self.PersonId = None


    def _deserialize(self, params):
        self.FaceId = params.get("FaceId")
        self.FaceUrl = params.get("FaceUrl")
        self.PersonId = params.get("PersonId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class FaceAttrResult(AbstractModel):
    """FaceAttrResult

    """

    def __init__(self):
        """
        :param Age: 年龄\n        :type Age: int\n        :param Sex: 性别\n        :type Sex: str\n        """
        self.Age = None
        self.Sex = None


    def _deserialize(self, params):
        self.Age = params.get("Age")
        self.Sex = params.get("Sex")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class FaceDetectStatistic(AbstractModel):
    """人脸监测统计信息

    """

    def __init__(self):
        """
        :param FaceSizeRatio: 人脸大小占画面平均占比\n        :type FaceSizeRatio: float\n        :param FrontalFaceCount: 检测到正脸次数\n        :type FrontalFaceCount: int\n        :param FrontalFaceRatio: 正脸时长占比\n        :type FrontalFaceRatio: float\n        :param FrontalFaceRealRatio: 正脸时长在总出现时常占比\n        :type FrontalFaceRealRatio: float\n        :param PersonId: 人员唯一标识符\n        :type PersonId: str\n        :param SideFaceCount: 检测到侧脸次数\n        :type SideFaceCount: int\n        :param SideFaceRatio: 侧脸时长占比\n        :type SideFaceRatio: float\n        :param SideFaceRealRatio: 侧脸时长在总出现时常占比\n        :type SideFaceRealRatio: float\n        """
        self.FaceSizeRatio = None
        self.FrontalFaceCount = None
        self.FrontalFaceRatio = None
        self.FrontalFaceRealRatio = None
        self.PersonId = None
        self.SideFaceCount = None
        self.SideFaceRatio = None
        self.SideFaceRealRatio = None


    def _deserialize(self, params):
        self.FaceSizeRatio = params.get("FaceSizeRatio")
        self.FrontalFaceCount = params.get("FrontalFaceCount")
        self.FrontalFaceRatio = params.get("FrontalFaceRatio")
        self.FrontalFaceRealRatio = params.get("FrontalFaceRealRatio")
        self.PersonId = params.get("PersonId")
        self.SideFaceCount = params.get("SideFaceCount")
        self.SideFaceRatio = params.get("SideFaceRatio")
        self.SideFaceRealRatio = params.get("SideFaceRealRatio")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class FaceExpressStatistic(AbstractModel):
    """人脸表情统计结果

    """

    def __init__(self):
        """
        :param PersonId: 人员唯一标识符\n        :type PersonId: str\n        :param ExpressRatio: 表情统计结果\n        :type ExpressRatio: list of ExpressRatioStatistic\n        """
        self.PersonId = None
        self.ExpressRatio = None


    def _deserialize(self, params):
        self.PersonId = params.get("PersonId")
        if params.get("ExpressRatio") is not None:
            self.ExpressRatio = []
            for item in params.get("ExpressRatio"):
                obj = ExpressRatioStatistic()
                obj._deserialize(item)
                self.ExpressRatio.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class FaceExpressionResult(AbstractModel):
    """FaceExpressionResult

    """

    def __init__(self):
        """
        :param Confidence: 表情置信度\n        :type Confidence: float\n        :param Expression: 表情识别结果，包括"neutral":中性,"happiness":开心，"angry":"生气"，"disgust":厌恶，"fear":"恐惧"，"sadness":"悲伤"，"surprise":"惊讶"，"contempt":"蔑视"\n        :type Expression: str\n        """
        self.Confidence = None
        self.Expression = None


    def _deserialize(self, params):
        self.Confidence = params.get("Confidence")
        self.Expression = params.get("Expression")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class FaceIdentifyResult(AbstractModel):
    """FaceIdentifyResult

    """

    def __init__(self):
        """
        :param FaceId: 人脸标识符\n        :type FaceId: str\n        :param LibraryId: 人员库标识符\n        :type LibraryId: str\n        :param PersonId: 人员标识符\n        :type PersonId: str\n        :param Similarity: 相似度\n        :type Similarity: float\n        """
        self.FaceId = None
        self.LibraryId = None
        self.PersonId = None
        self.Similarity = None


    def _deserialize(self, params):
        self.FaceId = params.get("FaceId")
        self.LibraryId = params.get("LibraryId")
        self.PersonId = params.get("PersonId")
        self.Similarity = params.get("Similarity")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class FaceIdentifyStatistic(AbstractModel):
    """人员检索统计结果

    """

    def __init__(self):
        """
        :param Duration: 持续时间\n        :type Duration: int\n        :param EndTs: 结束时间\n        :type EndTs: int\n        :param PersonId: 人员唯一标识符\n        :type PersonId: str\n        :param Similarity: 相似度\n        :type Similarity: float\n        :param StartTs: 开始时间\n        :type StartTs: int\n        """
        self.Duration = None
        self.EndTs = None
        self.PersonId = None
        self.Similarity = None
        self.StartTs = None


    def _deserialize(self, params):
        self.Duration = params.get("Duration")
        self.EndTs = params.get("EndTs")
        self.PersonId = params.get("PersonId")
        self.Similarity = params.get("Similarity")
        self.StartTs = params.get("StartTs")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class FaceInfo(AbstractModel):
    """人脸操作信息

    """

    def __init__(self):
        """
        :param ErrorCode: 人脸操作错误码\n        :type ErrorCode: str\n        :param ErrorMsg: 人脸操作结果信息\n        :type ErrorMsg: str\n        :param FaceId: 人脸唯一标识符\n        :type FaceId: str\n        :param FaceUrl: 人脸保存地址\n        :type FaceUrl: str\n        :param PersonId: 人员唯一标识\n        :type PersonId: str\n        """
        self.ErrorCode = None
        self.ErrorMsg = None
        self.FaceId = None
        self.FaceUrl = None
        self.PersonId = None


    def _deserialize(self, params):
        self.ErrorCode = params.get("ErrorCode")
        self.ErrorMsg = params.get("ErrorMsg")
        self.FaceId = params.get("FaceId")
        self.FaceUrl = params.get("FaceUrl")
        self.PersonId = params.get("PersonId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class FaceInfoResult(AbstractModel):
    """FaceInfoResult

    """

    def __init__(self):
        """
        :param FaceRatio: 人脸尺寸的占比\n        :type FaceRatio: float\n        :param FrameHeight: 帧高度\n        :type FrameHeight: int\n        :param FrameWidth: 帧宽度\n        :type FrameWidth: int\n        :param Height: 人脸高度\n        :type Height: int\n        :param Left: 人脸左坐标\n        :type Left: int\n        :param Top: 人脸顶坐标\n        :type Top: int\n        :param Width: 人脸宽度\n        :type Width: int\n        """
        self.FaceRatio = None
        self.FrameHeight = None
        self.FrameWidth = None
        self.Height = None
        self.Left = None
        self.Top = None
        self.Width = None


    def _deserialize(self, params):
        self.FaceRatio = params.get("FaceRatio")
        self.FrameHeight = params.get("FrameHeight")
        self.FrameWidth = params.get("FrameWidth")
        self.Height = params.get("Height")
        self.Left = params.get("Left")
        self.Top = params.get("Top")
        self.Width = params.get("Width")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class FacePoseResult(AbstractModel):
    """FacePoseResult

    """

    def __init__(self):
        """
        :param Direction: 正脸或侧脸的消息\n        :type Direction: str\n        :param Pitch: 围绕Z轴旋转角度，俯仰角\n        :type Pitch: float\n        :param Roll: 围绕X轴旋转角度，翻滚角\n        :type Roll: float\n        :param Yaw: 围绕Y轴旋转角度，偏航角\n        :type Yaw: float\n        """
        self.Direction = None
        self.Pitch = None
        self.Roll = None
        self.Yaw = None


    def _deserialize(self, params):
        self.Direction = params.get("Direction")
        self.Pitch = params.get("Pitch")
        self.Roll = params.get("Roll")
        self.Yaw = params.get("Yaw")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class FrameInfo(AbstractModel):
    """人员信息

    """

    def __init__(self):
        """
        :param Similarity: 相似度\n        :type Similarity: float\n        :param SnapshotUrl: 截图的存储地址\n        :type SnapshotUrl: str\n        :param Ts: 相对于视频起始时间的时间戳，单位秒\n        :type Ts: int\n        """
        self.Similarity = None
        self.SnapshotUrl = None
        self.Ts = None


    def _deserialize(self, params):
        self.Similarity = params.get("Similarity")
        self.SnapshotUrl = params.get("SnapshotUrl")
        self.Ts = params.get("Ts")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Function(AbstractModel):
    """功能开关列表，表示是否需要打开相应的功能，返回相应的信息

    """

    def __init__(self):
        """
        :param EnableAllText: 输出全部文本标识，当该值设置为true时，会输出当前音频的全部文本\n        :type EnableAllText: bool\n        :param EnableKeyword: 输出关键词信息标识，当该值设置为true时，会输出当前音频的关键词信息。\n        :type EnableKeyword: bool\n        :param EnableMuteDetect: 静音检测标识，当设置为 true 时，需要设置静音时间阈值字段mute_threshold，统计结果中会返回静音片段。\n        :type EnableMuteDetect: bool\n        :param EnableVadInfo: 输出音频统计信息标识，当设置为 true 时，任务查询结果会输出音频的统计信息（AsrStat）\n        :type EnableVadInfo: bool\n        :param EnableVolume: 输出音频音量信息标识，当设置为 true 时，会输出当前音频音量信息。\n        :type EnableVolume: bool\n        """
        self.EnableAllText = None
        self.EnableKeyword = None
        self.EnableMuteDetect = None
        self.EnableVadInfo = None
        self.EnableVolume = None


    def _deserialize(self, params):
        self.EnableAllText = params.get("EnableAllText")
        self.EnableKeyword = params.get("EnableKeyword")
        self.EnableMuteDetect = params.get("EnableMuteDetect")
        self.EnableVadInfo = params.get("EnableVadInfo")
        self.EnableVolume = params.get("EnableVolume")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GestureResult(AbstractModel):
    """GestureResult

    """

    def __init__(self):
        """
        :param Class: 识别结果，包含"USPEAK":听你说，"LISTEN":听我说，"GOOD":GOOD，"TOOLS":拿教具，"OTHERS":其他\n        :type Class: str\n        :param Confidence: 置信度\n        :type Confidence: float\n        :param Height: 识别结果高度\n        :type Height: int\n        :param Left: 识别结果左坐标\n        :type Left: int\n        :param Top: 识别结果顶坐标\n        :type Top: int\n        :param Width: 识别结果宽度\n        :type Width: int\n        """
        self.Class = None
        self.Confidence = None
        self.Height = None
        self.Left = None
        self.Top = None
        self.Width = None


    def _deserialize(self, params):
        self.Class = params.get("Class")
        self.Confidence = params.get("Confidence")
        self.Height = params.get("Height")
        self.Left = params.get("Left")
        self.Top = params.get("Top")
        self.Width = params.get("Width")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class HLFunction(AbstractModel):
    """检索配置开关项

    """

    def __init__(self):
        """
        :param EnableFaceDetect: 是否开启人脸检测\n        :type EnableFaceDetect: bool\n        :param EnableFaceExpression: 是否开启表情识别\n        :type EnableFaceExpression: bool\n        :param EnableFaceIdent: 是否开启人脸检索\n        :type EnableFaceIdent: bool\n        :param EnableKeywordWonderfulTime: 是否开启视频集锦-老师关键字识别\n        :type EnableKeywordWonderfulTime: bool\n        :param EnableSmileWonderfulTime: 是否开启视频集锦-微笑识别\n        :type EnableSmileWonderfulTime: bool\n        """
        self.EnableFaceDetect = None
        self.EnableFaceExpression = None
        self.EnableFaceIdent = None
        self.EnableKeywordWonderfulTime = None
        self.EnableSmileWonderfulTime = None


    def _deserialize(self, params):
        self.EnableFaceDetect = params.get("EnableFaceDetect")
        self.EnableFaceExpression = params.get("EnableFaceExpression")
        self.EnableFaceIdent = params.get("EnableFaceIdent")
        self.EnableKeywordWonderfulTime = params.get("EnableKeywordWonderfulTime")
        self.EnableSmileWonderfulTime = params.get("EnableSmileWonderfulTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class HandTrackingResult(AbstractModel):
    """HandTrackingResult

    """

    def __init__(self):
        """
        :param Class: 识别结果\n        :type Class: str\n        :param Confidence: 置信度\n        :type Confidence: float\n        :param Height: 识别结果高度\n        :type Height: int\n        :param Left: 识别结果左坐标\n        :type Left: int\n        :param Top: 识别结果顶坐标\n        :type Top: int\n        :param Width: 识别结果宽度\n        :type Width: int\n        """
        self.Class = None
        self.Confidence = None
        self.Height = None
        self.Left = None
        self.Top = None
        self.Width = None


    def _deserialize(self, params):
        self.Class = params.get("Class")
        self.Confidence = params.get("Confidence")
        self.Height = params.get("Height")
        self.Left = params.get("Left")
        self.Top = params.get("Top")
        self.Width = params.get("Width")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class HighlightsInfomation(AbstractModel):
    """精彩集锦信息

    """

    def __init__(self):
        """
        :param Concentration: 专注的起始与终止时间信息。\n        :type Concentration: list of TimeType\n        :param Smile: 微笑的起始与终止时间信息。\n        :type Smile: list of TimeType\n        :param HighlightsUrl: 高光集锦视频地址，保存剪辑好的视频地址。\n        :type HighlightsUrl: str\n        :param PersonId: 片段中识别出来的人脸ID。\n        :type PersonId: str\n        """
        self.Concentration = None
        self.Smile = None
        self.HighlightsUrl = None
        self.PersonId = None


    def _deserialize(self, params):
        if params.get("Concentration") is not None:
            self.Concentration = []
            for item in params.get("Concentration"):
                obj = TimeType()
                obj._deserialize(item)
                self.Concentration.append(obj)
        if params.get("Smile") is not None:
            self.Smile = []
            for item in params.get("Smile"):
                obj = TimeType()
                obj._deserialize(item)
                self.Smile.append(obj)
        self.HighlightsUrl = params.get("HighlightsUrl")
        self.PersonId = params.get("PersonId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ImageTaskFunction(AbstractModel):
    """图像任务控制选项

    """

    def __init__(self):
        """
        :param EnableActionClass: 大教室场景学生肢体动作识别选项\n        :type EnableActionClass: bool\n        :param EnableFaceDetect: 人脸检测选项（默认为true，目前不可编辑）\n        :type EnableFaceDetect: bool\n        :param EnableFaceExpression: 人脸表情识别选项\n        :type EnableFaceExpression: bool\n        :param EnableFaceIdentify: 人脸检索选项（默认为true，目前不可编辑）\n        :type EnableFaceIdentify: bool\n        :param EnableGesture: 手势选项\n        :type EnableGesture: bool\n        :param EnableHandTracking: 优图手势选项（该功能尚未支持）\n        :type EnableHandTracking: bool\n        :param EnableLightJudge: 光照选项\n        :type EnableLightJudge: bool\n        :param EnableStudentBodyMovements: 小班课场景学生肢体动作识别选项\n        :type EnableStudentBodyMovements: bool\n        :param EnableTeacherBodyMovements: 教师动作选项（该功能尚未支持）\n        :type EnableTeacherBodyMovements: bool\n        :param EnableTeacherOutScreen: 判断老师是否在屏幕中（该功能尚未支持）\n        :type EnableTeacherOutScreen: bool\n        """
        self.EnableActionClass = None
        self.EnableFaceDetect = None
        self.EnableFaceExpression = None
        self.EnableFaceIdentify = None
        self.EnableGesture = None
        self.EnableHandTracking = None
        self.EnableLightJudge = None
        self.EnableStudentBodyMovements = None
        self.EnableTeacherBodyMovements = None
        self.EnableTeacherOutScreen = None


    def _deserialize(self, params):
        self.EnableActionClass = params.get("EnableActionClass")
        self.EnableFaceDetect = params.get("EnableFaceDetect")
        self.EnableFaceExpression = params.get("EnableFaceExpression")
        self.EnableFaceIdentify = params.get("EnableFaceIdentify")
        self.EnableGesture = params.get("EnableGesture")
        self.EnableHandTracking = params.get("EnableHandTracking")
        self.EnableLightJudge = params.get("EnableLightJudge")
        self.EnableStudentBodyMovements = params.get("EnableStudentBodyMovements")
        self.EnableTeacherBodyMovements = params.get("EnableTeacherBodyMovements")
        self.EnableTeacherOutScreen = params.get("EnableTeacherOutScreen")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ImageTaskResult(AbstractModel):
    """图像任务结果

    """

    def __init__(self):
        """
        :param ActionInfo: 大教室场景学生肢体动作识别信息\n        :type ActionInfo: :class:`tencentcloud.tci.v20190318.models.ActionInfo`\n        :param FaceAttr: 属性识别结果\n        :type FaceAttr: :class:`tencentcloud.tci.v20190318.models.FaceAttrResult`\n        :param FaceExpression: 表情识别结果\n        :type FaceExpression: :class:`tencentcloud.tci.v20190318.models.FaceExpressionResult`\n        :param FaceIdentify: 人脸检索结果\n        :type FaceIdentify: :class:`tencentcloud.tci.v20190318.models.FaceIdentifyResult`\n        :param FaceInfo: 人脸检测结果\n        :type FaceInfo: :class:`tencentcloud.tci.v20190318.models.FaceInfoResult`\n        :param FacePose: 姿势识别结果\n        :type FacePose: :class:`tencentcloud.tci.v20190318.models.FacePoseResult`\n        :param Gesture: 动作分类结果\n        :type Gesture: :class:`tencentcloud.tci.v20190318.models.GestureResult`\n        :param HandTracking: 手势分类结果\n        :type HandTracking: :class:`tencentcloud.tci.v20190318.models.HandTrackingResult`\n        :param Light: 光照识别结果\n        :type Light: :class:`tencentcloud.tci.v20190318.models.LightResult`\n        :param StudentBodyMovement: 学生肢体动作识别结果\n        :type StudentBodyMovement: :class:`tencentcloud.tci.v20190318.models.StudentBodyMovementResult`\n        :param TeacherBodyMovement: 老师肢体动作识别结果\n        :type TeacherBodyMovement: :class:`tencentcloud.tci.v20190318.models.BodyMovementResult`\n        :param TeacherOutScreen: 教师是否在屏幕内判断结果\n        :type TeacherOutScreen: :class:`tencentcloud.tci.v20190318.models.TeacherOutScreenResult`\n        :param TimeInfo: 时间统计结果\n        :type TimeInfo: :class:`tencentcloud.tci.v20190318.models.TimeInfoResult`\n        """
        self.ActionInfo = None
        self.FaceAttr = None
        self.FaceExpression = None
        self.FaceIdentify = None
        self.FaceInfo = None
        self.FacePose = None
        self.Gesture = None
        self.HandTracking = None
        self.Light = None
        self.StudentBodyMovement = None
        self.TeacherBodyMovement = None
        self.TeacherOutScreen = None
        self.TimeInfo = None


    def _deserialize(self, params):
        if params.get("ActionInfo") is not None:
            self.ActionInfo = ActionInfo()
            self.ActionInfo._deserialize(params.get("ActionInfo"))
        if params.get("FaceAttr") is not None:
            self.FaceAttr = FaceAttrResult()
            self.FaceAttr._deserialize(params.get("FaceAttr"))
        if params.get("FaceExpression") is not None:
            self.FaceExpression = FaceExpressionResult()
            self.FaceExpression._deserialize(params.get("FaceExpression"))
        if params.get("FaceIdentify") is not None:
            self.FaceIdentify = FaceIdentifyResult()
            self.FaceIdentify._deserialize(params.get("FaceIdentify"))
        if params.get("FaceInfo") is not None:
            self.FaceInfo = FaceInfoResult()
            self.FaceInfo._deserialize(params.get("FaceInfo"))
        if params.get("FacePose") is not None:
            self.FacePose = FacePoseResult()
            self.FacePose._deserialize(params.get("FacePose"))
        if params.get("Gesture") is not None:
            self.Gesture = GestureResult()
            self.Gesture._deserialize(params.get("Gesture"))
        if params.get("HandTracking") is not None:
            self.HandTracking = HandTrackingResult()
            self.HandTracking._deserialize(params.get("HandTracking"))
        if params.get("Light") is not None:
            self.Light = LightResult()
            self.Light._deserialize(params.get("Light"))
        if params.get("StudentBodyMovement") is not None:
            self.StudentBodyMovement = StudentBodyMovementResult()
            self.StudentBodyMovement._deserialize(params.get("StudentBodyMovement"))
        if params.get("TeacherBodyMovement") is not None:
            self.TeacherBodyMovement = BodyMovementResult()
            self.TeacherBodyMovement._deserialize(params.get("TeacherBodyMovement"))
        if params.get("TeacherOutScreen") is not None:
            self.TeacherOutScreen = TeacherOutScreenResult()
            self.TeacherOutScreen._deserialize(params.get("TeacherOutScreen"))
        if params.get("TimeInfo") is not None:
            self.TimeInfo = TimeInfoResult()
            self.TimeInfo._deserialize(params.get("TimeInfo"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ImageTaskStatistic(AbstractModel):
    """图像任务统计结果

    """

    def __init__(self):
        """
        :param FaceDetect: 人员检测统计信息\n        :type FaceDetect: list of FaceDetectStatistic\n        :param FaceExpression: 人脸表情统计信息\n        :type FaceExpression: list of FaceExpressStatistic\n        :param FaceIdentify: 人脸检索统计信息\n        :type FaceIdentify: list of FaceIdentifyStatistic\n        :param Gesture: 姿势识别统计信息\n        :type Gesture: :class:`tencentcloud.tci.v20190318.models.ActionStatistic`\n        :param Handtracking: 手势识别统计信息\n        :type Handtracking: :class:`tencentcloud.tci.v20190318.models.ActionStatistic`\n        :param Light: 光照统计信息\n        :type Light: :class:`tencentcloud.tci.v20190318.models.LightStatistic`\n        :param StudentMovement: 学生动作统计信息\n        :type StudentMovement: :class:`tencentcloud.tci.v20190318.models.ActionStatistic`\n        :param TeacherMovement: 教师动作统计信息\n        :type TeacherMovement: :class:`tencentcloud.tci.v20190318.models.ActionStatistic`\n        """
        self.FaceDetect = None
        self.FaceExpression = None
        self.FaceIdentify = None
        self.Gesture = None
        self.Handtracking = None
        self.Light = None
        self.StudentMovement = None
        self.TeacherMovement = None


    def _deserialize(self, params):
        if params.get("FaceDetect") is not None:
            self.FaceDetect = []
            for item in params.get("FaceDetect"):
                obj = FaceDetectStatistic()
                obj._deserialize(item)
                self.FaceDetect.append(obj)
        if params.get("FaceExpression") is not None:
            self.FaceExpression = []
            for item in params.get("FaceExpression"):
                obj = FaceExpressStatistic()
                obj._deserialize(item)
                self.FaceExpression.append(obj)
        if params.get("FaceIdentify") is not None:
            self.FaceIdentify = []
            for item in params.get("FaceIdentify"):
                obj = FaceIdentifyStatistic()
                obj._deserialize(item)
                self.FaceIdentify.append(obj)
        if params.get("Gesture") is not None:
            self.Gesture = ActionStatistic()
            self.Gesture._deserialize(params.get("Gesture"))
        if params.get("Handtracking") is not None:
            self.Handtracking = ActionStatistic()
            self.Handtracking._deserialize(params.get("Handtracking"))
        if params.get("Light") is not None:
            self.Light = LightStatistic()
            self.Light._deserialize(params.get("Light"))
        if params.get("StudentMovement") is not None:
            self.StudentMovement = ActionStatistic()
            self.StudentMovement._deserialize(params.get("StudentMovement"))
        if params.get("TeacherMovement") is not None:
            self.TeacherMovement = ActionStatistic()
            self.TeacherMovement._deserialize(params.get("TeacherMovement"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Library(AbstractModel):
    """人员库描述

    """

    def __init__(self):
        """
        :param CreateTime: 人员库创建时间\n        :type CreateTime: str\n        :param LibraryId: 人员库唯一标识符\n        :type LibraryId: str\n        :param LibraryName: 人员库名称\n        :type LibraryName: str\n        :param PersonCount: 人员库人员数量\n        :type PersonCount: int\n        :param UpdateTime: 人员库修改时间\n        :type UpdateTime: str\n        """
        self.CreateTime = None
        self.LibraryId = None
        self.LibraryName = None
        self.PersonCount = None
        self.UpdateTime = None


    def _deserialize(self, params):
        self.CreateTime = params.get("CreateTime")
        self.LibraryId = params.get("LibraryId")
        self.LibraryName = params.get("LibraryName")
        self.PersonCount = params.get("PersonCount")
        self.UpdateTime = params.get("UpdateTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class LightDistributionStatistic(AbstractModel):
    """光照强度统计结果

    """

    def __init__(self):
        """
        :param Time: 时间点\n        :type Time: int\n        :param Value: 光线值\n        :type Value: int\n        """
        self.Time = None
        self.Value = None


    def _deserialize(self, params):
        self.Time = params.get("Time")
        self.Value = params.get("Value")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class LightLevelRatioStatistic(AbstractModel):
    """光照强度比例统计结果

    """

    def __init__(self):
        """
        :param Level: 名称\n        :type Level: str\n        :param Ratio: 比例\n        :type Ratio: float\n        """
        self.Level = None
        self.Ratio = None


    def _deserialize(self, params):
        self.Level = params.get("Level")
        self.Ratio = params.get("Ratio")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class LightResult(AbstractModel):
    """LightResult

    """

    def __init__(self):
        """
        :param LightLevel: 光照程度，参考提交任务时的LightStandard指定的Name参数\n        :type LightLevel: str\n        :param LightValue: 光照亮度\n        :type LightValue: float\n        """
        self.LightLevel = None
        self.LightValue = None


    def _deserialize(self, params):
        self.LightLevel = params.get("LightLevel")
        self.LightValue = params.get("LightValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class LightStandard(AbstractModel):
    """光照标准，结构的相关示例为：
    {
        "Name":"dark"，
        "Range":[0,30]
    }
    当光照的区间落入在0到30的范围时，就会命中dark的光照标准

    """

    def __init__(self):
        """
        :param Name: 光照名称\n        :type Name: str\n        :param Range: 范围\n        :type Range: list of float\n        """
        self.Name = None
        self.Range = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Range = params.get("Range")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class LightStatistic(AbstractModel):
    """光照统计结果

    """

    def __init__(self):
        """
        :param LightDistribution: 各个时间点的光线值\n        :type LightDistribution: list of LightDistributionStatistic\n        :param LightLevelRatio: 光照程度比例统计结果\n        :type LightLevelRatio: list of LightLevelRatioStatistic\n        """
        self.LightDistribution = None
        self.LightLevelRatio = None


    def _deserialize(self, params):
        if params.get("LightDistribution") is not None:
            self.LightDistribution = []
            for item in params.get("LightDistribution"):
                obj = LightDistributionStatistic()
                obj._deserialize(item)
                self.LightDistribution.append(obj)
        if params.get("LightLevelRatio") is not None:
            self.LightLevelRatio = []
            for item in params.get("LightLevelRatio"):
                obj = LightLevelRatioStatistic()
                obj._deserialize(item)
                self.LightLevelRatio.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyLibraryRequest(AbstractModel):
    """ModifyLibrary请求参数结构体

    """

    def __init__(self):
        """
        :param LibraryId: 人员库唯一标识符\n        :type LibraryId: str\n        :param LibraryName: 人员库名称\n        :type LibraryName: str\n        """
        self.LibraryId = None
        self.LibraryName = None


    def _deserialize(self, params):
        self.LibraryId = params.get("LibraryId")
        self.LibraryName = params.get("LibraryName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyLibraryResponse(AbstractModel):
    """ModifyLibrary返回参数结构体

    """

    def __init__(self):
        """
        :param LibraryId: 人员库唯一标识符\n        :type LibraryId: str\n        :param LibraryName: 人员库名称\n        :type LibraryName: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.LibraryId = None
        self.LibraryName = None
        self.RequestId = None


    def _deserialize(self, params):
        self.LibraryId = params.get("LibraryId")
        self.LibraryName = params.get("LibraryName")
        self.RequestId = params.get("RequestId")


class ModifyPersonRequest(AbstractModel):
    """ModifyPerson请求参数结构体

    """

    def __init__(self):
        """
        :param LibraryId: 人员库唯一标识符\n        :type LibraryId: str\n        :param PersonId: 人员唯一标识符\n        :type PersonId: str\n        :param JobNumber: 人员工作号码\n        :type JobNumber: str\n        :param Mail: 人员邮箱\n        :type Mail: str\n        :param Male: 人员性别\n        :type Male: int\n        :param PersonName: 人员名称\n        :type PersonName: str\n        :param PhoneNumber: 人员电话号码\n        :type PhoneNumber: str\n        :param StudentNumber: 人员学生号码\n        :type StudentNumber: str\n        """
        self.LibraryId = None
        self.PersonId = None
        self.JobNumber = None
        self.Mail = None
        self.Male = None
        self.PersonName = None
        self.PhoneNumber = None
        self.StudentNumber = None


    def _deserialize(self, params):
        self.LibraryId = params.get("LibraryId")
        self.PersonId = params.get("PersonId")
        self.JobNumber = params.get("JobNumber")
        self.Mail = params.get("Mail")
        self.Male = params.get("Male")
        self.PersonName = params.get("PersonName")
        self.PhoneNumber = params.get("PhoneNumber")
        self.StudentNumber = params.get("StudentNumber")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyPersonResponse(AbstractModel):
    """ModifyPerson返回参数结构体

    """

    def __init__(self):
        """
        :param FaceInfoSet: 人脸信息\n        :type FaceInfoSet: list of FaceInfo\n        :param LibraryId: 人员所属人员库标识符\n        :type LibraryId: str\n        :param PersonId: 人员唯一标识符\n        :type PersonId: str\n        :param PersonName: 人员名称\n        :type PersonName: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.FaceInfoSet = None
        self.LibraryId = None
        self.PersonId = None
        self.PersonName = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("FaceInfoSet") is not None:
            self.FaceInfoSet = []
            for item in params.get("FaceInfoSet"):
                obj = FaceInfo()
                obj._deserialize(item)
                self.FaceInfoSet.append(obj)
        self.LibraryId = params.get("LibraryId")
        self.PersonId = params.get("PersonId")
        self.PersonName = params.get("PersonName")
        self.RequestId = params.get("RequestId")


class MuteSlice(AbstractModel):
    """所有静音片段。

    """

    def __init__(self):
        """
        :param MuteBtm: 起始时间。\n        :type MuteBtm: int\n        :param MuteEtm: 终止时间。\n        :type MuteEtm: int\n        """
        self.MuteBtm = None
        self.MuteEtm = None


    def _deserialize(self, params):
        self.MuteBtm = params.get("MuteBtm")
        self.MuteEtm = params.get("MuteEtm")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Person(AbstractModel):
    """人员描述

    """

    def __init__(self):
        """
        :param LibraryId: 人员库唯一标识符\n        :type LibraryId: str\n        :param PersonId: 人员唯一标识符\n        :type PersonId: str\n        :param PersonName: 人员名称\n        :type PersonName: str\n        :param CreateTime: 创建时间\n        :type CreateTime: str\n        :param JobNumber: 工作号码\n        :type JobNumber: str\n        :param Mail: 邮箱\n        :type Mail: str\n        :param Male: 性别\n        :type Male: int\n        :param PhoneNumber: 电话号码\n        :type PhoneNumber: str\n        :param StudentNumber: 学生号码\n        :type StudentNumber: str\n        :param UpdateTime: 修改时间\n        :type UpdateTime: str\n        """
        self.LibraryId = None
        self.PersonId = None
        self.PersonName = None
        self.CreateTime = None
        self.JobNumber = None
        self.Mail = None
        self.Male = None
        self.PhoneNumber = None
        self.StudentNumber = None
        self.UpdateTime = None


    def _deserialize(self, params):
        self.LibraryId = params.get("LibraryId")
        self.PersonId = params.get("PersonId")
        self.PersonName = params.get("PersonName")
        self.CreateTime = params.get("CreateTime")
        self.JobNumber = params.get("JobNumber")
        self.Mail = params.get("Mail")
        self.Male = params.get("Male")
        self.PhoneNumber = params.get("PhoneNumber")
        self.StudentNumber = params.get("StudentNumber")
        self.UpdateTime = params.get("UpdateTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PersonInfo(AbstractModel):
    """人员信息

    """

    def __init__(self):
        """
        :param PersonId: 需要匹配的人员的ID列表。\n        :type PersonId: str\n        :param CoverBeginUrl: 视频集锦开始封面照片。\n        :type CoverBeginUrl: str\n        :param CoverEndUrl: 视频集锦结束封面照片。\n        :type CoverEndUrl: str\n        """
        self.PersonId = None
        self.CoverBeginUrl = None
        self.CoverEndUrl = None


    def _deserialize(self, params):
        self.PersonId = params.get("PersonId")
        self.CoverBeginUrl = params.get("CoverBeginUrl")
        self.CoverEndUrl = params.get("CoverEndUrl")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StandardAudioResult(AbstractModel):
    """标准化接口图像分析结果

    """

    def __init__(self):
        """
        :param AsrStat: 返回的当前音频的统计信息。当进度为100时返回。\n        :type AsrStat: :class:`tencentcloud.tci.v20190318.models.ASRStat`\n        :param Texts: 返回当前音频流的详细信息，如果是流模式，返回的是对应流的详细信息，如果是 URL模式，返回的是查询的那一段seq对应的音频的详细信息。\n        :type Texts: list of WholeTextItem\n        :param VocabAnalysisDetailInfo: 返回词汇库中的单词出现的详细时间信息。\n        :type VocabAnalysisDetailInfo: list of VocabDetailInfomation\n        :param VocabAnalysisStatInfo: 返回词汇库中的单词出现的次数信息。\n        :type VocabAnalysisStatInfo: list of VocabStatInfomation\n        :param Message: 状态描述\n        :type Message: str\n        :param Status: 任务状态\n        :type Status: str\n        :param TotalCount: 结果数量\n        :type TotalCount: int\n        """
        self.AsrStat = None
        self.Texts = None
        self.VocabAnalysisDetailInfo = None
        self.VocabAnalysisStatInfo = None
        self.Message = None
        self.Status = None
        self.TotalCount = None


    def _deserialize(self, params):
        if params.get("AsrStat") is not None:
            self.AsrStat = ASRStat()
            self.AsrStat._deserialize(params.get("AsrStat"))
        if params.get("Texts") is not None:
            self.Texts = []
            for item in params.get("Texts"):
                obj = WholeTextItem()
                obj._deserialize(item)
                self.Texts.append(obj)
        if params.get("VocabAnalysisDetailInfo") is not None:
            self.VocabAnalysisDetailInfo = []
            for item in params.get("VocabAnalysisDetailInfo"):
                obj = VocabDetailInfomation()
                obj._deserialize(item)
                self.VocabAnalysisDetailInfo.append(obj)
        if params.get("VocabAnalysisStatInfo") is not None:
            self.VocabAnalysisStatInfo = []
            for item in params.get("VocabAnalysisStatInfo"):
                obj = VocabStatInfomation()
                obj._deserialize(item)
                self.VocabAnalysisStatInfo.append(obj)
        self.Message = params.get("Message")
        self.Status = params.get("Status")
        self.TotalCount = params.get("TotalCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StandardImageResult(AbstractModel):
    """标准化接口图像分析结果

    """

    def __init__(self):
        """
        :param ResultSet: 详细结果\n        :type ResultSet: list of ImageTaskResult\n        :param Statistic: 分析完成后的统计结果\n        :type Statistic: :class:`tencentcloud.tci.v20190318.models.ImageTaskStatistic`\n        :param Message: 状态描述\n        :type Message: str\n        :param Status: 任务状态\n        :type Status: str\n        :param TotalCount: 结果总数\n        :type TotalCount: int\n        """
        self.ResultSet = None
        self.Statistic = None
        self.Message = None
        self.Status = None
        self.TotalCount = None


    def _deserialize(self, params):
        if params.get("ResultSet") is not None:
            self.ResultSet = []
            for item in params.get("ResultSet"):
                obj = ImageTaskResult()
                obj._deserialize(item)
                self.ResultSet.append(obj)
        if params.get("Statistic") is not None:
            self.Statistic = ImageTaskStatistic()
            self.Statistic._deserialize(params.get("Statistic"))
        self.Message = params.get("Message")
        self.Status = params.get("Status")
        self.TotalCount = params.get("TotalCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StandardVideoResult(AbstractModel):
    """标准化接口图像分析结果

    """

    def __init__(self):
        """
        :param HighlightsInfo: 分析完成后的统计结果\n        :type HighlightsInfo: list of HighlightsInfomation\n        :param Message: 状态描述\n        :type Message: str\n        :param Status: 任务状态\n        :type Status: str\n        """
        self.HighlightsInfo = None
        self.Message = None
        self.Status = None


    def _deserialize(self, params):
        if params.get("HighlightsInfo") is not None:
            self.HighlightsInfo = []
            for item in params.get("HighlightsInfo"):
                obj = HighlightsInfomation()
                obj._deserialize(item)
                self.HighlightsInfo.append(obj)
        self.Message = params.get("Message")
        self.Status = params.get("Status")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StatInfo(AbstractModel):
    """单词出现的次数信息

    """

    def __init__(self):
        """
        :param Keyword: 词汇库中的单词\n        :type Keyword: str\n        :param Value: 单词出现在该音频中总次数\n        :type Value: int\n        """
        self.Keyword = None
        self.Value = None


    def _deserialize(self, params):
        self.Keyword = params.get("Keyword")
        self.Value = params.get("Value")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StudentBodyMovementResult(AbstractModel):
    """学生肢体动作结果

    """

    def __init__(self):
        """
        :param Confidence: 置信度（已废弃）\n        :type Confidence: float\n        :param HandupConfidence: 举手识别结果置信度\n        :type HandupConfidence: float\n        :param HandupStatus: 举手识别结果，包含举手（handup）和未举手（nothandup）\n        :type HandupStatus: str\n        :param Height: 识别结果高度\n        :type Height: int\n        :param Left: 识别结果左坐标\n        :type Left: int\n        :param Movements: 动作识别结果（已废弃）\n        :type Movements: str\n        :param StandConfidence: 站立识别结果置信度\n        :type StandConfidence: float\n        :param StandStatus: 站立识别结果，包含站立（stand）和坐着（sit）\n        :type StandStatus: str\n        :param Top: 识别结果顶坐标\n        :type Top: int\n        :param Width: 识别结果宽度\n        :type Width: int\n        """
        self.Confidence = None
        self.HandupConfidence = None
        self.HandupStatus = None
        self.Height = None
        self.Left = None
        self.Movements = None
        self.StandConfidence = None
        self.StandStatus = None
        self.Top = None
        self.Width = None


    def _deserialize(self, params):
        self.Confidence = params.get("Confidence")
        self.HandupConfidence = params.get("HandupConfidence")
        self.HandupStatus = params.get("HandupStatus")
        self.Height = params.get("Height")
        self.Left = params.get("Left")
        self.Movements = params.get("Movements")
        self.StandConfidence = params.get("StandConfidence")
        self.StandStatus = params.get("StandStatus")
        self.Top = params.get("Top")
        self.Width = params.get("Width")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SubmitAudioTaskRequest(AbstractModel):
    """SubmitAudioTask请求参数结构体

    """

    def __init__(self):
        """
        :param Lang: 音频源的语言，默认0为英文，1为中文\n        :type Lang: int\n        :param Url: 音频URL。客户请求为URL方式时必须带此字段指名音频的url。\n        :type Url: str\n        :param VoiceEncodeType: 语音编码类型 1:pcm\n        :type VoiceEncodeType: int\n        :param VoiceFileType: 语音文件类型 1:raw, 2:wav, 3:mp3，10:视频（三种音频格式目前仅支持16k采样率16bit）\n        :type VoiceFileType: int\n        :param Functions: 功能开关列表，表示是否需要打开相应的功能，返回相应的信息\n        :type Functions: :class:`tencentcloud.tci.v20190318.models.Function`\n        :param FileType: 视频文件类型，默认点播，直播填 live_url\n        :type FileType: str\n        :param MuteThreshold: 静音阈值设置，如果静音检测开关开启，则静音时间超过这个阈值认为是静音片段，在结果中会返回, 没给的话默认值为3s\n        :type MuteThreshold: int\n        :param VocabLibNameList: 识别词库名列表，评估过程使用这些词汇库中的词汇进行词汇使用行为分析\n        :type VocabLibNameList: list of str\n        """
        self.Lang = None
        self.Url = None
        self.VoiceEncodeType = None
        self.VoiceFileType = None
        self.Functions = None
        self.FileType = None
        self.MuteThreshold = None
        self.VocabLibNameList = None


    def _deserialize(self, params):
        self.Lang = params.get("Lang")
        self.Url = params.get("Url")
        self.VoiceEncodeType = params.get("VoiceEncodeType")
        self.VoiceFileType = params.get("VoiceFileType")
        if params.get("Functions") is not None:
            self.Functions = Function()
            self.Functions._deserialize(params.get("Functions"))
        self.FileType = params.get("FileType")
        self.MuteThreshold = params.get("MuteThreshold")
        self.VocabLibNameList = params.get("VocabLibNameList")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SubmitAudioTaskResponse(AbstractModel):
    """SubmitAudioTask返回参数结构体

    """

    def __init__(self):
        """
        :param JobId: 	查询结果时指名的jobid。在URL方式时提交请求后会返回一个jobid，后续查询该url的结果时使用这个jobid进行查询。\n        :type JobId: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.JobId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.JobId = params.get("JobId")
        self.RequestId = params.get("RequestId")


class SubmitCheckAttendanceTaskPlusRequest(AbstractModel):
    """SubmitCheckAttendanceTaskPlus请求参数结构体

    """

    def __init__(self):
        """
        :param FileContent: 输入数据\n        :type FileContent: list of str\n        :param FileType: 视频流类型，vod_url表示点播URL，live_url表示直播URL，默认vod_url\n        :type FileType: str\n        :param LibraryIds: 人员库 ID列表\n        :type LibraryIds: list of str\n        :param AttendanceThreshold: 确定出勤阈值；默认为0.92\n        :type AttendanceThreshold: float\n        :param EnableStranger: 是否开启陌生人模式，陌生人模式是指在任务中发现的非注册人脸库中的人脸也返回相关统计信息，默认不开启\n        :type EnableStranger: bool\n        :param EndTime: 考勤结束时间（到视频的第几秒结束考勤），单位秒；默认为900 
对于直播场景，使用绝对时间戳，单位秒，默认当前时间往后12小时\n        :type EndTime: int\n        :param NoticeUrl: 通知回调地址，要求方法为post，application/json格式\n        :type NoticeUrl: str\n        :param StartTime: 考勤开始时间（从视频的第几秒开始考勤），单位秒；默认为0 
对于直播场景，使用绝对时间戳，单位秒，默认当前时间\n        :type StartTime: int\n        :param Threshold: 识别阈值；默认为0.8\n        :type Threshold: float\n        """
        self.FileContent = None
        self.FileType = None
        self.LibraryIds = None
        self.AttendanceThreshold = None
        self.EnableStranger = None
        self.EndTime = None
        self.NoticeUrl = None
        self.StartTime = None
        self.Threshold = None


    def _deserialize(self, params):
        self.FileContent = params.get("FileContent")
        self.FileType = params.get("FileType")
        self.LibraryIds = params.get("LibraryIds")
        self.AttendanceThreshold = params.get("AttendanceThreshold")
        self.EnableStranger = params.get("EnableStranger")
        self.EndTime = params.get("EndTime")
        self.NoticeUrl = params.get("NoticeUrl")
        self.StartTime = params.get("StartTime")
        self.Threshold = params.get("Threshold")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SubmitCheckAttendanceTaskPlusResponse(AbstractModel):
    """SubmitCheckAttendanceTaskPlus返回参数结构体

    """

    def __init__(self):
        """
        :param JobId: 任务标识符\n        :type JobId: int\n        :param NotRegisteredSet: 没有注册的人的ID列表\n        :type NotRegisteredSet: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.JobId = None
        self.NotRegisteredSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.JobId = params.get("JobId")
        self.NotRegisteredSet = params.get("NotRegisteredSet")
        self.RequestId = params.get("RequestId")


class SubmitCheckAttendanceTaskRequest(AbstractModel):
    """SubmitCheckAttendanceTask请求参数结构体

    """

    def __init__(self):
        """
        :param FileContent: 输入数据\n        :type FileContent: str\n        :param FileType: 视频流类型，vod_url表示点播URL，live_url表示直播URL，默认vod_url\n        :type FileType: str\n        :param LibraryIds: 人员库 ID列表\n        :type LibraryIds: list of str\n        :param AttendanceThreshold: 确定出勤阈值；默认为0.92\n        :type AttendanceThreshold: float\n        :param EnableStranger: 是否开启陌生人模式，陌生人模式是指在任务中发现的非注册人脸库中的人脸也返回相关统计信息，默认不开启\n        :type EnableStranger: bool\n        :param EndTime: 考勤结束时间（到视频的第几秒结束考勤），单位秒；默认为900 
对于直播场景，使用绝对时间戳，单位秒，默认当前时间往后12小时\n        :type EndTime: int\n        :param NoticeUrl: 通知回调地址，要求方法为post，application/json格式\n        :type NoticeUrl: str\n        :param StartTime: 考勤开始时间（从视频的第几秒开始考勤），单位秒；默认为0 
对于直播场景，使用绝对时间戳，单位秒，默认当前时间\n        :type StartTime: int\n        :param Threshold: 识别阈值；默认为0.8\n        :type Threshold: float\n        """
        self.FileContent = None
        self.FileType = None
        self.LibraryIds = None
        self.AttendanceThreshold = None
        self.EnableStranger = None
        self.EndTime = None
        self.NoticeUrl = None
        self.StartTime = None
        self.Threshold = None


    def _deserialize(self, params):
        self.FileContent = params.get("FileContent")
        self.FileType = params.get("FileType")
        self.LibraryIds = params.get("LibraryIds")
        self.AttendanceThreshold = params.get("AttendanceThreshold")
        self.EnableStranger = params.get("EnableStranger")
        self.EndTime = params.get("EndTime")
        self.NoticeUrl = params.get("NoticeUrl")
        self.StartTime = params.get("StartTime")
        self.Threshold = params.get("Threshold")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SubmitCheckAttendanceTaskResponse(AbstractModel):
    """SubmitCheckAttendanceTask返回参数结构体

    """

    def __init__(self):
        """
        :param JobId: 任务标识符\n        :type JobId: int\n        :param NotRegisteredSet: 没有注册的人的ID列表\n        :type NotRegisteredSet: list of str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.JobId = None
        self.NotRegisteredSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.JobId = params.get("JobId")
        self.NotRegisteredSet = params.get("NotRegisteredSet")
        self.RequestId = params.get("RequestId")


class SubmitConversationTaskRequest(AbstractModel):
    """SubmitConversationTask请求参数结构体

    """

    def __init__(self):
        """
        :param Lang: 音频源的语言，默认0为英文，1为中文\n        :type Lang: int\n        :param StudentUrl: 学生音频流\n        :type StudentUrl: str\n        :param TeacherUrl: 教师音频流\n        :type TeacherUrl: str\n        :param VoiceEncodeType: 语音编码类型 1:pcm\n        :type VoiceEncodeType: int\n        :param VoiceFileType: 语音文件类型 1:raw, 2:wav, 3:mp3（三种格式目前仅支持16k采样率16bit）\n        :type VoiceFileType: int\n        :param Functions: 功能开关列表，表示是否需要打开相应的功能，返回相应的信息\n        :type Functions: :class:`tencentcloud.tci.v20190318.models.Function`\n        :param VocabLibNameList: 识别词库名列表，评估过程使用这些词汇库中的词汇进行词汇使用行为分析\n        :type VocabLibNameList: list of str\n        """
        self.Lang = None
        self.StudentUrl = None
        self.TeacherUrl = None
        self.VoiceEncodeType = None
        self.VoiceFileType = None
        self.Functions = None
        self.VocabLibNameList = None


    def _deserialize(self, params):
        self.Lang = params.get("Lang")
        self.StudentUrl = params.get("StudentUrl")
        self.TeacherUrl = params.get("TeacherUrl")
        self.VoiceEncodeType = params.get("VoiceEncodeType")
        self.VoiceFileType = params.get("VoiceFileType")
        if params.get("Functions") is not None:
            self.Functions = Function()
            self.Functions._deserialize(params.get("Functions"))
        self.VocabLibNameList = params.get("VocabLibNameList")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SubmitConversationTaskResponse(AbstractModel):
    """SubmitConversationTask返回参数结构体

    """

    def __init__(self):
        """
        :param JobId: 	查询结果时指名的jobid。在URL方式时提交请求后会返回一个jobid，后续查询该url的结果时使用这个jobid进行查询。\n        :type JobId: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.JobId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.JobId = params.get("JobId")
        self.RequestId = params.get("RequestId")


class SubmitDoubleVideoHighlightsRequest(AbstractModel):
    """SubmitDoubleVideoHighlights请求参数结构体

    """

    def __init__(self):
        """
        :param FileContent: 学生视频url\n        :type FileContent: str\n        :param LibIds: 需要检索的人脸合集库，不在库中的人脸将不参与精彩集锦；目前仅支持输入一个人脸库。\n        :type LibIds: list of str\n        :param Functions: 详细功能开关配置项\n        :type Functions: :class:`tencentcloud.tci.v20190318.models.DoubleVideoFunction`\n        :param PersonInfoList: 需要匹配的人员信息列表。\n        :type PersonInfoList: list of PersonInfo\n        :param FrameInterval: 视频处理的抽帧间隔，单位毫秒。建议留空。\n        :type FrameInterval: int\n        :param PersonIds: 旧版本需要匹配的人员信息列表。\n        :type PersonIds: list of str\n        :param SimThreshold: 人脸检索的相似度阈值，默认值0.89。建议留空。\n        :type SimThreshold: float\n        :param TeacherFileContent: 老师视频url\n        :type TeacherFileContent: str\n        """
        self.FileContent = None
        self.LibIds = None
        self.Functions = None
        self.PersonInfoList = None
        self.FrameInterval = None
        self.PersonIds = None
        self.SimThreshold = None
        self.TeacherFileContent = None


    def _deserialize(self, params):
        self.FileContent = params.get("FileContent")
        self.LibIds = params.get("LibIds")
        if params.get("Functions") is not None:
            self.Functions = DoubleVideoFunction()
            self.Functions._deserialize(params.get("Functions"))
        if params.get("PersonInfoList") is not None:
            self.PersonInfoList = []
            for item in params.get("PersonInfoList"):
                obj = PersonInfo()
                obj._deserialize(item)
                self.PersonInfoList.append(obj)
        self.FrameInterval = params.get("FrameInterval")
        self.PersonIds = params.get("PersonIds")
        self.SimThreshold = params.get("SimThreshold")
        self.TeacherFileContent = params.get("TeacherFileContent")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SubmitDoubleVideoHighlightsResponse(AbstractModel):
    """SubmitDoubleVideoHighlights返回参数结构体

    """

    def __init__(self):
        """
        :param JobId: 视频拆条任务ID，用来唯一标识视频拆条任务。\n        :type JobId: int\n        :param NotRegistered: 未注册的人员ID列表。若出现此项，代表评估出现了问题，输入的PersonId中有不在库中的人员ID。\n        :type NotRegistered: list of str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.JobId = None
        self.NotRegistered = None
        self.RequestId = None


    def _deserialize(self, params):
        self.JobId = params.get("JobId")
        self.NotRegistered = params.get("NotRegistered")
        self.RequestId = params.get("RequestId")


class SubmitFullBodyClassTaskRequest(AbstractModel):
    """SubmitFullBodyClassTask请求参数结构体

    """

    def __init__(self):
        """
        :param FileContent: 输入分析对象内容，输入数据格式参考FileType参数释义\n        :type FileContent: str\n        :param FileType: 输入分析对象类型，picture_url:图片地址，vod_url:视频地址，live_url：直播地址，picture: 图片二进制数据的BASE64编码\n        :type FileType: str\n        :param Lang: 音频源的语言，默认0为英文，1为中文\n        :type Lang: int\n        :param LibrarySet: 查询人员库列表，可填写老师的注册照所在人员库\n        :type LibrarySet: list of str\n        :param MaxVideoDuration: 视频评估时间，单位秒，点播场景默认值为2小时（无法探测长度时）或完整视频，直播场景默认值为10分钟或直播提前结束\n        :type MaxVideoDuration: int\n        :param VocabLibNameList: 识别词库名列表，这些词汇库用来维护关键词，评估老师授课过程中，对这些关键词的使用情况\n        :type VocabLibNameList: list of str\n        :param VoiceEncodeType: 语音编码类型 1:pcm，当FileType为vod_url或live_url时为必填\n        :type VoiceEncodeType: int\n        :param VoiceFileType: 语音文件类型 10:视频（三种音频格式目前仅支持16k采样率16bit），当FileType为vod_url或live_url时为必填\n        :type VoiceFileType: int\n        """
        self.FileContent = None
        self.FileType = None
        self.Lang = None
        self.LibrarySet = None
        self.MaxVideoDuration = None
        self.VocabLibNameList = None
        self.VoiceEncodeType = None
        self.VoiceFileType = None


    def _deserialize(self, params):
        self.FileContent = params.get("FileContent")
        self.FileType = params.get("FileType")
        self.Lang = params.get("Lang")
        self.LibrarySet = params.get("LibrarySet")
        self.MaxVideoDuration = params.get("MaxVideoDuration")
        self.VocabLibNameList = params.get("VocabLibNameList")
        self.VoiceEncodeType = params.get("VoiceEncodeType")
        self.VoiceFileType = params.get("VoiceFileType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SubmitFullBodyClassTaskResponse(AbstractModel):
    """SubmitFullBodyClassTask返回参数结构体

    """

    def __init__(self):
        """
        :param ImageResults: 图像任务直接返回结果，包括： FaceAttr、 FaceExpression、 FaceIdentify、 FaceInfo、 FacePose、 TeacherBodyMovement、TimeInfo\n        :type ImageResults: list of ImageTaskResult\n        :param TaskId: 任务ID\n        :type TaskId: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.ImageResults = None
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ImageResults") is not None:
            self.ImageResults = []
            for item in params.get("ImageResults"):
                obj = ImageTaskResult()
                obj._deserialize(item)
                self.ImageResults.append(obj)
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class SubmitHighlightsRequest(AbstractModel):
    """SubmitHighlights请求参数结构体

    """

    def __init__(self):
        """
        :param Functions: 表情配置开关项。\n        :type Functions: :class:`tencentcloud.tci.v20190318.models.HLFunction`\n        :param FileContent: 视频url。\n        :type FileContent: str\n        :param FileType: 视频类型及来源，目前只支持点播类型："vod_url"。\n        :type FileType: str\n        :param LibIds: 需要检索的人脸合集库，不在库中的人脸将不参与精彩集锦。\n        :type LibIds: list of str\n        :param FrameInterval: 视频处理的抽帧间隔，单位毫秒。建议留空。\n        :type FrameInterval: int\n        :param KeywordsLanguage: 关键词语言类型，0为英文，1为中文。\n        :type KeywordsLanguage: int\n        :param KeywordsStrings: 关键词数组，当且仅当Funtions中的EnableKeywordWonderfulTime为true时有意义，匹配相应的关键字。\n        :type KeywordsStrings: list of str\n        :param MaxVideoDuration: 处理视频的总时长，单位毫秒。该值为0或未设置时，默认值两小时生效；当该值大于视频实际时长时，视频实际时长生效；当该值小于视频实际时长时，该值生效；当获取视频实际时长失败时，若该值设置则生效，否则默认值生效。建议留空。\n        :type MaxVideoDuration: int\n        :param SimThreshold: 人脸检索的相似度阈值，默认值0.89。建议留空。\n        :type SimThreshold: float\n        """
        self.Functions = None
        self.FileContent = None
        self.FileType = None
        self.LibIds = None
        self.FrameInterval = None
        self.KeywordsLanguage = None
        self.KeywordsStrings = None
        self.MaxVideoDuration = None
        self.SimThreshold = None


    def _deserialize(self, params):
        if params.get("Functions") is not None:
            self.Functions = HLFunction()
            self.Functions._deserialize(params.get("Functions"))
        self.FileContent = params.get("FileContent")
        self.FileType = params.get("FileType")
        self.LibIds = params.get("LibIds")
        self.FrameInterval = params.get("FrameInterval")
        self.KeywordsLanguage = params.get("KeywordsLanguage")
        self.KeywordsStrings = params.get("KeywordsStrings")
        self.MaxVideoDuration = params.get("MaxVideoDuration")
        self.SimThreshold = params.get("SimThreshold")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SubmitHighlightsResponse(AbstractModel):
    """SubmitHighlights返回参数结构体

    """

    def __init__(self):
        """
        :param JobId: 视频拆条任务ID，用来唯一标识视频拆条任务。\n        :type JobId: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.JobId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.JobId = params.get("JobId")
        self.RequestId = params.get("RequestId")


class SubmitImageTaskPlusRequest(AbstractModel):
    """SubmitImageTaskPlus请求参数结构体

    """

    def __init__(self):
        """
        :param FileContent: 输入分析对象内容，输入数据格式参考FileType参数释义\n        :type FileContent: list of str\n        :param FileType: 输入分析对象类型，picture：二进制图片的 base64 编码字符串，picture_url:图片地址，vod_url：视频地址，live_url：直播地址\n        :type FileType: str\n        :param Functions: 任务控制选项\n        :type Functions: :class:`tencentcloud.tci.v20190318.models.ImageTaskFunction`\n        :param LightStandardSet: 光照标准列表\n        :type LightStandardSet: list of LightStandard\n        :param FrameInterval: 抽帧的时间间隔，单位毫秒，默认值1000，保留字段，当前不支持填写。\n        :type FrameInterval: int\n        :param LibrarySet: 查询人员库列表\n        :type LibrarySet: list of str\n        :param MaxVideoDuration: 视频评估时间，单位秒，点播场景默认值为2小时（无法探测长度时）或完整视频，直播场景默认值为10分钟或直播提前结束\n        :type MaxVideoDuration: int\n        :param SimThreshold: 人脸识别中的相似度阈值，默认值为0.89，保留字段，当前不支持填写。\n        :type SimThreshold: float\n        """
        self.FileContent = None
        self.FileType = None
        self.Functions = None
        self.LightStandardSet = None
        self.FrameInterval = None
        self.LibrarySet = None
        self.MaxVideoDuration = None
        self.SimThreshold = None


    def _deserialize(self, params):
        self.FileContent = params.get("FileContent")
        self.FileType = params.get("FileType")
        if params.get("Functions") is not None:
            self.Functions = ImageTaskFunction()
            self.Functions._deserialize(params.get("Functions"))
        if params.get("LightStandardSet") is not None:
            self.LightStandardSet = []
            for item in params.get("LightStandardSet"):
                obj = LightStandard()
                obj._deserialize(item)
                self.LightStandardSet.append(obj)
        self.FrameInterval = params.get("FrameInterval")
        self.LibrarySet = params.get("LibrarySet")
        self.MaxVideoDuration = params.get("MaxVideoDuration")
        self.SimThreshold = params.get("SimThreshold")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SubmitImageTaskPlusResponse(AbstractModel):
    """SubmitImageTaskPlus返回参数结构体

    """

    def __init__(self):
        """
        :param ResultSet: 识别结果\n        :type ResultSet: list of ImageTaskResult\n        :param JobId: 任务标识符\n        :type JobId: int\n        :param Progress: 任务进度\n        :type Progress: int\n        :param TotalCount: 结果总数目\n        :type TotalCount: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.ResultSet = None
        self.JobId = None
        self.Progress = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ResultSet") is not None:
            self.ResultSet = []
            for item in params.get("ResultSet"):
                obj = ImageTaskResult()
                obj._deserialize(item)
                self.ResultSet.append(obj)
        self.JobId = params.get("JobId")
        self.Progress = params.get("Progress")
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class SubmitImageTaskRequest(AbstractModel):
    """SubmitImageTask请求参数结构体

    """

    def __init__(self):
        """
        :param FileContent: 输入分析对象内容，输入数据格式参考FileType参数释义\n        :type FileContent: str\n        :param FileType: 输入分析对象类型，picture：二进制图片的 base64 编码字符串，picture_url:图片地址，vod_url：视频地址，live_url：直播地址\n        :type FileType: str\n        :param Functions: 任务控制选项\n        :type Functions: :class:`tencentcloud.tci.v20190318.models.ImageTaskFunction`\n        :param LightStandardSet: 光照标准列表\n        :type LightStandardSet: list of LightStandard\n        :param EventsCallBack: 结果更新回调地址。\n        :type EventsCallBack: str\n        :param FrameInterval: 抽帧的时间间隔，单位毫秒，默认值1000，保留字段，当前不支持填写。\n        :type FrameInterval: int\n        :param LibrarySet: 查询人员库列表\n        :type LibrarySet: list of str\n        :param MaxVideoDuration: 视频评估时间，单位秒，点播场景默认值为2小时（无法探测长度时）或完整视频，直播场景默认值为10分钟或直播提前结束\n        :type MaxVideoDuration: int\n        :param SimThreshold: 人脸识别中的相似度阈值，默认值为0.89，保留字段，当前不支持填写。\n        :type SimThreshold: float\n        """
        self.FileContent = None
        self.FileType = None
        self.Functions = None
        self.LightStandardSet = None
        self.EventsCallBack = None
        self.FrameInterval = None
        self.LibrarySet = None
        self.MaxVideoDuration = None
        self.SimThreshold = None


    def _deserialize(self, params):
        self.FileContent = params.get("FileContent")
        self.FileType = params.get("FileType")
        if params.get("Functions") is not None:
            self.Functions = ImageTaskFunction()
            self.Functions._deserialize(params.get("Functions"))
        if params.get("LightStandardSet") is not None:
            self.LightStandardSet = []
            for item in params.get("LightStandardSet"):
                obj = LightStandard()
                obj._deserialize(item)
                self.LightStandardSet.append(obj)
        self.EventsCallBack = params.get("EventsCallBack")
        self.FrameInterval = params.get("FrameInterval")
        self.LibrarySet = params.get("LibrarySet")
        self.MaxVideoDuration = params.get("MaxVideoDuration")
        self.SimThreshold = params.get("SimThreshold")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SubmitImageTaskResponse(AbstractModel):
    """SubmitImageTask返回参数结构体

    """

    def __init__(self):
        """
        :param ResultSet: 识别结果\n        :type ResultSet: list of ImageTaskResult\n        :param JobId: 任务标识符\n        :type JobId: int\n        :param Progress: 任务进度\n        :type Progress: int\n        :param TotalCount: 结果总数目\n        :type TotalCount: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.ResultSet = None
        self.JobId = None
        self.Progress = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ResultSet") is not None:
            self.ResultSet = []
            for item in params.get("ResultSet"):
                obj = ImageTaskResult()
                obj._deserialize(item)
                self.ResultSet.append(obj)
        self.JobId = params.get("JobId")
        self.Progress = params.get("Progress")
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class SubmitOneByOneClassTaskRequest(AbstractModel):
    """SubmitOneByOneClassTask请求参数结构体

    """

    def __init__(self):
        """
        :param FileContent: 输入分析对象内容，输入数据格式参考FileType参数释义\n        :type FileContent: str\n        :param FileType: 输入分析对象类型，picture_url:图片地址，vod_url:视频地址，live_url：直播地址，picture: 图片二进制数据的BASE64编码\n        :type FileType: str\n        :param Lang: 音频源的语言，默认0为英文，1为中文 \n        :type Lang: int\n        :param LibrarySet: 查询人员库列表，可填写学生的注册照所在人员库\n        :type LibrarySet: list of str\n        :param MaxVideoDuration: 视频评估时间，单位秒，点播场景默认值为2小时（无法探测长度时）或完整视频，直播场景默认值为10分钟或直播提前结束\n        :type MaxVideoDuration: int\n        :param VocabLibNameList: 识别词库名列表，这些词汇库用来维护关键词，评估学生对这些关键词的使用情况\n        :type VocabLibNameList: list of str\n        :param VoiceEncodeType: 语音编码类型 1:pcm，当FileType为vod_url或live_url时为必填\n        :type VoiceEncodeType: int\n        :param VoiceFileType: 语音文件类型10:视频（三种音频格式目前仅支持16k采样率16bit），当FileType为vod_url或live_url时为必填\n        :type VoiceFileType: int\n        """
        self.FileContent = None
        self.FileType = None
        self.Lang = None
        self.LibrarySet = None
        self.MaxVideoDuration = None
        self.VocabLibNameList = None
        self.VoiceEncodeType = None
        self.VoiceFileType = None


    def _deserialize(self, params):
        self.FileContent = params.get("FileContent")
        self.FileType = params.get("FileType")
        self.Lang = params.get("Lang")
        self.LibrarySet = params.get("LibrarySet")
        self.MaxVideoDuration = params.get("MaxVideoDuration")
        self.VocabLibNameList = params.get("VocabLibNameList")
        self.VoiceEncodeType = params.get("VoiceEncodeType")
        self.VoiceFileType = params.get("VoiceFileType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SubmitOneByOneClassTaskResponse(AbstractModel):
    """SubmitOneByOneClassTask返回参数结构体

    """

    def __init__(self):
        """
        :param ImageResults: 图像任务直接返回结果，包括：FaceAttr、 FaceExpression、 FaceIdentify、 FaceInfo、 FacePose、TimeInfo\n        :type ImageResults: list of ImageTaskResult\n        :param TaskId: 任务ID\n        :type TaskId: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.ImageResults = None
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ImageResults") is not None:
            self.ImageResults = []
            for item in params.get("ImageResults"):
                obj = ImageTaskResult()
                obj._deserialize(item)
                self.ImageResults.append(obj)
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class SubmitOpenClassTaskRequest(AbstractModel):
    """SubmitOpenClassTask请求参数结构体

    """

    def __init__(self):
        """
        :param FileContent: 输入分析对象内容，输入数据格式参考FileType参数释义\n        :type FileContent: str\n        :param FileType: 输入分析对象类型，picture_url:图片地址，vod_url:视频地址，live_url：直播地址,picture: 图片二进制数据的BASE64编码\n        :type FileType: str\n        :param LibrarySet: 查询人员库列表，可填写学生们的注册照所在人员库\n        :type LibrarySet: list of str\n        :param MaxVideoDuration: 视频评估时间，单位秒，点播场景默认值为2小时（无法探测长度时）或完整视频，直播场景默认值为10分钟或直播提前结束\n        :type MaxVideoDuration: int\n        """
        self.FileContent = None
        self.FileType = None
        self.LibrarySet = None
        self.MaxVideoDuration = None


    def _deserialize(self, params):
        self.FileContent = params.get("FileContent")
        self.FileType = params.get("FileType")
        self.LibrarySet = params.get("LibrarySet")
        self.MaxVideoDuration = params.get("MaxVideoDuration")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SubmitOpenClassTaskResponse(AbstractModel):
    """SubmitOpenClassTask返回参数结构体

    """

    def __init__(self):
        """
        :param ImageResults: 图像任务直接返回结果，包括：FaceAttr、 FaceExpression、 FaceIdentify、 FaceInfo、 FacePose、 StudentBodyMovement、TimeInfo\n        :type ImageResults: list of ImageTaskResult\n        :param TaskId: 任务ID\n        :type TaskId: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.ImageResults = None
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ImageResults") is not None:
            self.ImageResults = []
            for item in params.get("ImageResults"):
                obj = ImageTaskResult()
                obj._deserialize(item)
                self.ImageResults.append(obj)
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class SubmitPartialBodyClassTaskRequest(AbstractModel):
    """SubmitPartialBodyClassTask请求参数结构体

    """

    def __init__(self):
        """
        :param FileContent: 输入分析对象内容，输入数据格式参考FileType参数释义\n        :type FileContent: str\n        :param FileType: 输入分析对象类型，picture_url:图片地址，vod_url:视频地址，live_url：直播地址，picture: 图片二进制数据的BASE64编码\n        :type FileType: str\n        :param Lang: 音频源的语言，默认0为英文，1为中文\n        :type Lang: int\n        :param LibrarySet: 查询人员库列表，可填写老师的注册照所在人员库\n        :type LibrarySet: list of str\n        :param MaxVideoDuration: 视频评估时间，单位秒，点播场景默认值为2小时（无法探测长度时）或完整视频，直播场景默认值为10分钟或直播提前结束\n        :type MaxVideoDuration: int\n        :param VocabLibNameList: 识别词库名列表，这些词汇库用来维护关键词，评估老师授课过程中，对这些关键词的使用情况\n        :type VocabLibNameList: list of str\n        :param VoiceEncodeType: 语音编码类型 1:pcm，当FileType为vod_url或live_url时为必填\n        :type VoiceEncodeType: int\n        :param VoiceFileType: 语音文件类型 10:视频（三种音频格式目前仅支持16k采样率16bit），当FileType为vod_url或live_url时为必填\n        :type VoiceFileType: int\n        """
        self.FileContent = None
        self.FileType = None
        self.Lang = None
        self.LibrarySet = None
        self.MaxVideoDuration = None
        self.VocabLibNameList = None
        self.VoiceEncodeType = None
        self.VoiceFileType = None


    def _deserialize(self, params):
        self.FileContent = params.get("FileContent")
        self.FileType = params.get("FileType")
        self.Lang = params.get("Lang")
        self.LibrarySet = params.get("LibrarySet")
        self.MaxVideoDuration = params.get("MaxVideoDuration")
        self.VocabLibNameList = params.get("VocabLibNameList")
        self.VoiceEncodeType = params.get("VoiceEncodeType")
        self.VoiceFileType = params.get("VoiceFileType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SubmitPartialBodyClassTaskResponse(AbstractModel):
    """SubmitPartialBodyClassTask返回参数结构体

    """

    def __init__(self):
        """
        :param ImageResults: 图像任务直接返回结果，包括： FaceAttr、 FaceExpression、 FaceIdentify、 FaceInfo、 FacePose、 Gesture 、 Light、 TimeInfo\n        :type ImageResults: list of ImageTaskResult\n        :param TaskId: 任务ID\n        :type TaskId: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.ImageResults = None
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ImageResults") is not None:
            self.ImageResults = []
            for item in params.get("ImageResults"):
                obj = ImageTaskResult()
                obj._deserialize(item)
                self.ImageResults.append(obj)
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class SubmitTraditionalClassTaskRequest(AbstractModel):
    """SubmitTraditionalClassTask请求参数结构体

    """

    def __init__(self):
        """
        :param FileContent: 输入分析对象内容，输入数据格式参考FileType参数释义\n        :type FileContent: str\n        :param FileType: 输入分析对象类型，picture_url:图片地址，vod_url:视频地址，live_url：直播地址，picture：图片二进制数据的BASE64编码\n        :type FileType: str\n        :param LibrarySet: 查询人员库列表，可填写学生们的注册照所在人员库\n        :type LibrarySet: list of str\n        :param MaxVideoDuration: 视频评估时间，单位秒，点播场景默认值为2小时（无法探测长度时）或完整视频，直播场景默认值为10分钟或直播提前结束\n        :type MaxVideoDuration: int\n        """
        self.FileContent = None
        self.FileType = None
        self.LibrarySet = None
        self.MaxVideoDuration = None


    def _deserialize(self, params):
        self.FileContent = params.get("FileContent")
        self.FileType = params.get("FileType")
        self.LibrarySet = params.get("LibrarySet")
        self.MaxVideoDuration = params.get("MaxVideoDuration")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SubmitTraditionalClassTaskResponse(AbstractModel):
    """SubmitTraditionalClassTask返回参数结构体

    """

    def __init__(self):
        """
        :param ImageResults: 图像任务直接返回结果，包括： ActionInfo、FaceAttr、 FaceExpression、 FaceIdentify、 FaceInfo、 FacePose、 TimeInfo\n        :type ImageResults: list of ImageTaskResult\n        :param TaskId: 任务ID\n        :type TaskId: int\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.ImageResults = None
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ImageResults") is not None:
            self.ImageResults = []
            for item in params.get("ImageResults"):
                obj = ImageTaskResult()
                obj._deserialize(item)
                self.ImageResults.append(obj)
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class SuspectedInfo(AbstractModel):
    """疑似出席人员

    """

    def __init__(self):
        """
        :param FaceSet: TopN匹配信息列表\n        :type FaceSet: list of FrameInfo\n        :param PersonId: 识别到的人员id\n        :type PersonId: str\n        """
        self.FaceSet = None
        self.PersonId = None


    def _deserialize(self, params):
        if params.get("FaceSet") is not None:
            self.FaceSet = []
            for item in params.get("FaceSet"):
                obj = FrameInfo()
                obj._deserialize(item)
                self.FaceSet.append(obj)
        self.PersonId = params.get("PersonId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TeacherOutScreenResult(AbstractModel):
    """教师是否在屏幕内判断结果

    """

    def __init__(self):
        """
        :param Class: 动作识别结果，InScreen：在屏幕内
OutScreen：不在屏幕内\n        :type Class: str\n        :param Height: 识别结果高度\n        :type Height: int\n        :param Left: 识别结果左坐标\n        :type Left: int\n        :param Top: 识别结果顶坐标\n        :type Top: int\n        :param Width: 识别结果宽度\n        :type Width: int\n        """
        self.Class = None
        self.Height = None
        self.Left = None
        self.Top = None
        self.Width = None


    def _deserialize(self, params):
        self.Class = params.get("Class")
        self.Height = params.get("Height")
        self.Left = params.get("Left")
        self.Top = params.get("Top")
        self.Width = params.get("Width")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TextItem(AbstractModel):
    """当前句子的信息

    """

    def __init__(self):
        """
        :param Words: 当前句子包含的所有单词信息\n        :type Words: list of Word\n        :param Confidence: 当前句子的置信度\n        :type Confidence: float\n        :param Mbtm: 当前句子语音的起始时间点，单位为ms\n        :type Mbtm: int\n        :param Metm: 当前句子语音的终止时间点，单位为ms\n        :type Metm: int\n        :param Tag: 保留参数，暂无意义\n        :type Tag: int\n        :param Text: 当前句子\n        :type Text: str\n        :param TextSize: 当前句子的字节数\n        :type TextSize: int\n        """
        self.Words = None
        self.Confidence = None
        self.Mbtm = None
        self.Metm = None
        self.Tag = None
        self.Text = None
        self.TextSize = None


    def _deserialize(self, params):
        if params.get("Words") is not None:
            self.Words = []
            for item in params.get("Words"):
                obj = Word()
                obj._deserialize(item)
                self.Words.append(obj)
        self.Confidence = params.get("Confidence")
        self.Mbtm = params.get("Mbtm")
        self.Metm = params.get("Metm")
        self.Tag = params.get("Tag")
        self.Text = params.get("Text")
        self.TextSize = params.get("TextSize")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TimeInfoResult(AbstractModel):
    """TimeInfoResult

    """

    def __init__(self):
        """
        :param Duration: 持续时间，单位毫秒\n        :type Duration: int\n        :param EndTs: 结束时间戳，单位毫秒\n        :type EndTs: int\n        :param StartTs: 开始时间戳，单位毫秒\n        :type StartTs: int\n        """
        self.Duration = None
        self.EndTs = None
        self.StartTs = None


    def _deserialize(self, params):
        self.Duration = params.get("Duration")
        self.EndTs = params.get("EndTs")
        self.StartTs = params.get("StartTs")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TimeType(AbstractModel):
    """起止时间

    """

    def __init__(self):
        """
        :param EndTime: 结束时间戳\n        :type EndTime: int\n        :param StartTime: 起始时间戳\n        :type StartTime: int\n        """
        self.EndTime = None
        self.StartTime = None


    def _deserialize(self, params):
        self.EndTime = params.get("EndTime")
        self.StartTime = params.get("StartTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TransmitAudioStreamRequest(AbstractModel):
    """TransmitAudioStream请求参数结构体

    """

    def __init__(self):
        """
        :param Functions: 功能开关列表，表示是否需要打开相应的功能，返回相应的信息\n        :type Functions: :class:`tencentcloud.tci.v20190318.models.Function`\n        :param SeqId: 流式数据包的序号，从1开始，当IsEnd字段为1后后续序号无意义。\n        :type SeqId: int\n        :param SessionId: 语音段唯一标识，一个完整语音一个SessionId。\n        :type SessionId: str\n        :param UserVoiceData: 当前数据包数据, 流式模式下数据包大小可以按需设置，在网络良好的情况下，建议设置为0.5k，且必须保证分片帧完整（16bit的数据必须保证音频长度为偶数），编码格式要求为BASE64。\n        :type UserVoiceData: str\n        :param VoiceEncodeType: 语音编码类型 1:pcm。\n        :type VoiceEncodeType: int\n        :param VoiceFileType: 语音文件类型 	1: raw, 2: wav, 3: mp3 (语言文件格式目前仅支持 16k 采样率 16bit 编码单声道，如有不一致可能导致评估不准确或失败)。\n        :type VoiceFileType: int\n        :param IsEnd: 是否传输完毕标志，若为0表示未完毕，若为1则传输完毕开始评估，非流式模式下无意义。\n        :type IsEnd: int\n        :param Lang: 音频源的语言，默认0为英文，1为中文\n        :type Lang: int\n        :param StorageMode: 是否临时保存 音频链接\n        :type StorageMode: int\n        :param VocabLibNameList: 识别词库名列表，评估过程使用这些词汇库中的词汇进行词汇使用行为分析\n        :type VocabLibNameList: list of str\n        """
        self.Functions = None
        self.SeqId = None
        self.SessionId = None
        self.UserVoiceData = None
        self.VoiceEncodeType = None
        self.VoiceFileType = None
        self.IsEnd = None
        self.Lang = None
        self.StorageMode = None
        self.VocabLibNameList = None


    def _deserialize(self, params):
        if params.get("Functions") is not None:
            self.Functions = Function()
            self.Functions._deserialize(params.get("Functions"))
        self.SeqId = params.get("SeqId")
        self.SessionId = params.get("SessionId")
        self.UserVoiceData = params.get("UserVoiceData")
        self.VoiceEncodeType = params.get("VoiceEncodeType")
        self.VoiceFileType = params.get("VoiceFileType")
        self.IsEnd = params.get("IsEnd")
        self.Lang = params.get("Lang")
        self.StorageMode = params.get("StorageMode")
        self.VocabLibNameList = params.get("VocabLibNameList")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TransmitAudioStreamResponse(AbstractModel):
    """TransmitAudioStream返回参数结构体

    """

    def __init__(self):
        """
        :param AsrStat: 返回的当前音频的统计信息。当进度为100时返回。\n        :type AsrStat: :class:`tencentcloud.tci.v20190318.models.ASRStat`\n        :param Texts: 返回当前音频流的详细信息，如果是流模式，返回的是对应流的详细信息，如果是 URL模式，返回的是查询的那一段seq对应的音频的详细信息。\n        :type Texts: list of WholeTextItem\n        :param VocabAnalysisDetailInfo: 返回词汇库中的单词出现的详细时间信息。\n        :type VocabAnalysisDetailInfo: list of VocabDetailInfomation\n        :param VocabAnalysisStatInfo: 返回词汇库中的单词出现的次数信息。\n        :type VocabAnalysisStatInfo: list of VocabStatInfomation\n        :param AllTexts: 音频全部文本。\n        :type AllTexts: str\n        :param AudioUrl: 临时保存的音频链接\n        :type AudioUrl: str\n        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。\n        :type RequestId: str\n        """
        self.AsrStat = None
        self.Texts = None
        self.VocabAnalysisDetailInfo = None
        self.VocabAnalysisStatInfo = None
        self.AllTexts = None
        self.AudioUrl = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("AsrStat") is not None:
            self.AsrStat = ASRStat()
            self.AsrStat._deserialize(params.get("AsrStat"))
        if params.get("Texts") is not None:
            self.Texts = []
            for item in params.get("Texts"):
                obj = WholeTextItem()
                obj._deserialize(item)
                self.Texts.append(obj)
        if params.get("VocabAnalysisDetailInfo") is not None:
            self.VocabAnalysisDetailInfo = []
            for item in params.get("VocabAnalysisDetailInfo"):
                obj = VocabDetailInfomation()
                obj._deserialize(item)
                self.VocabAnalysisDetailInfo.append(obj)
        if params.get("VocabAnalysisStatInfo") is not None:
            self.VocabAnalysisStatInfo = []
            for item in params.get("VocabAnalysisStatInfo"):
                obj = VocabStatInfomation()
                obj._deserialize(item)
                self.VocabAnalysisStatInfo.append(obj)
        self.AllTexts = params.get("AllTexts")
        self.AudioUrl = params.get("AudioUrl")
        self.RequestId = params.get("RequestId")


class VocabDetailInfomation(AbstractModel):
    """词汇库中的单词出现在音频中的那个句子的起始时间和结束时间信息

    """

    def __init__(self):
        """
        :param VocabDetailInfo: 词汇库中的单词出现在该音频中的那个句子的时间戳，出现了几次，就返回对应次数的起始和结束时间戳\n        :type VocabDetailInfo: list of DetailInfo\n        :param VocabLibName: 词汇库名\n        :type VocabLibName: str\n        """
        self.VocabDetailInfo = None
        self.VocabLibName = None


    def _deserialize(self, params):
        if params.get("VocabDetailInfo") is not None:
            self.VocabDetailInfo = []
            for item in params.get("VocabDetailInfo"):
                obj = DetailInfo()
                obj._deserialize(item)
                self.VocabDetailInfo.append(obj)
        self.VocabLibName = params.get("VocabLibName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class VocabStatInfomation(AbstractModel):
    """词汇库中的单词出现在音频中的总次数信息

    """

    def __init__(self):
        """
        :param VocabDetailInfo: 单词出现在该音频中总次数\n        :type VocabDetailInfo: list of StatInfo\n        :param VocabLibName: 词汇库名称\n        :type VocabLibName: str\n        """
        self.VocabDetailInfo = None
        self.VocabLibName = None


    def _deserialize(self, params):
        if params.get("VocabDetailInfo") is not None:
            self.VocabDetailInfo = []
            for item in params.get("VocabDetailInfo"):
                obj = StatInfo()
                obj._deserialize(item)
                self.VocabDetailInfo.append(obj)
        self.VocabLibName = params.get("VocabLibName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class WholeTextItem(AbstractModel):
    """含有语速的句子信息

    """

    def __init__(self):
        """
        :param TextItem: 当前句子的信息\n        :type TextItem: :class:`tencentcloud.tci.v20190318.models.TextItem`\n        :param AvgVolume: Vad的平均音量\n        :type AvgVolume: float\n        :param MaxVolume: Vad的最大音量\n        :type MaxVolume: float\n        :param MinVolume: Vad的最小音量\n        :type MinVolume: float\n        :param Speed: 当前句子的语速\n        :type Speed: float\n        """
        self.TextItem = None
        self.AvgVolume = None
        self.MaxVolume = None
        self.MinVolume = None
        self.Speed = None


    def _deserialize(self, params):
        if params.get("TextItem") is not None:
            self.TextItem = TextItem()
            self.TextItem._deserialize(params.get("TextItem"))
        self.AvgVolume = params.get("AvgVolume")
        self.MaxVolume = params.get("MaxVolume")
        self.MinVolume = params.get("MinVolume")
        self.Speed = params.get("Speed")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Word(AbstractModel):
    """当前句子包含的所有单词信息

    """

    def __init__(self):
        """
        :param Confidence: 当前词的置信度\n        :type Confidence: float\n        :param Mbtm: 当前单词语音的起始时间点，单位为ms\n        :type Mbtm: int\n        :param Metm: 当前单词语音的终止时间点，单位为ms\n        :type Metm: int\n        :param Text: 当前词\n        :type Text: str\n        :param Wsize: 当前词的字节数\n        :type Wsize: int\n        """
        self.Confidence = None
        self.Mbtm = None
        self.Metm = None
        self.Text = None
        self.Wsize = None


    def _deserialize(self, params):
        self.Confidence = params.get("Confidence")
        self.Mbtm = params.get("Mbtm")
        self.Metm = params.get("Metm")
        self.Text = params.get("Text")
        self.Wsize = params.get("Wsize")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class WordTimePair(AbstractModel):
    """单词出现的那个句子的起始时间和结束时间信息

    """

    def __init__(self):
        """
        :param Mbtm: 单词出现的那个句子的起始时间\n        :type Mbtm: int\n        :param Metm: 	单词出现的那个句子的结束时间\n        :type Metm: int\n        """
        self.Mbtm = None
        self.Metm = None


    def _deserialize(self, params):
        self.Mbtm = params.get("Mbtm")
        self.Metm = params.get("Metm")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        