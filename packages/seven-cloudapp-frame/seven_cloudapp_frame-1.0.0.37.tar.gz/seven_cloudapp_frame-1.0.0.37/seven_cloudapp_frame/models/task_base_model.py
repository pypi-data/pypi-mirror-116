# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-10 10:41:13
@LastEditTime: 2021-08-12 11:46:35
@LastEditors: HuangJianYi
@Description: 
"""
from seven_cloudapp_frame.models.enum import *
from seven_cloudapp_frame.models.seven_model import *
from seven_cloudapp_frame.models.frame_base_model import *
from seven_cloudapp_frame.models.asset_base_model import *
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.models.act_base_model import *
from seven_cloudapp_frame.models.db_models.task.task_info_model import *
from seven_cloudapp_frame.models.db_models.task.task_count_model import *

class TaskBaseModel(FrameBaseModel):
    """
    :description: 任务基类
    """
    def __init__(self, context):
        self.context = context
        super(TaskBaseModel,self).__init__(context)

    def _delete_task_info_dependency_key(self,act_id,task_id):
        """
        :description: 删除任务依赖建
        :param act_id: 活动标识
        :param task_id: 任务标识
        :return: 
        :last_editors: HuangJianYi
        """
        try:
            redis_init = SevenHelper.redis_init()
            if task_id:
                redis_init.delete(f"task_info:taskid_{task_id}")
            if act_id:
                redis_init.delete(f"task_info_list:actid_{act_id}")
        except Exception as ex:
            pass

    def get_task_info_list(self,app_id,act_id,module_id,is_release,is_cache=True):
        """
        :description: 获取任务列表
        :param app_id: 应用标识
        :param act_id: 活动标识
        :param module_id: 活动模块标识
        :param is_release: 是否发布
        :param is_cache: 是否缓存
        :return: 
        :last_editors: HuangJianYi
        """
        order_by = "sort_index desc,id asc"
        condition = "app_id=%s and act_id=%s"
        params = [app_id,act_id]
        if is_release !=-1:
            condition += " and is_release=%s"
            params.append(is_release)
        if module_id !=-1:
            condition += " and module_id=%s"
            params.append(module_id)
        task_info_model = TaskInfoModel(context=self.context)
        if is_cache:
            dict_list = task_info_model.get_cache_dict_list(condition, group_by="", order_by=order_by, params=params,dependency_key=f"task_info_list:actid_{act_id}")
        else:
            dict_list = task_info_model.get_dict_list(condition, group_by="", order_by=order_by, params=params)
        for task_info in dict_list:
            task_info["task_config"] = SevenHelper.json_loads(task_info["task_config"]) if task_info["task_config"] else {}   
        return dict_list
    
    def get_task_info_dict(self,task_id,is_cache=True,is_filter=True):
        """
        :description: 获取任务信息
        :param task_id: 任务标识
        :param is_cache: 是否缓存
        :param is_filter: 是否过滤未发布的数据
        :return: 
        :last_editors: HuangJianYi
        """
        task_info_model = TaskInfoModel(context=self.context)
        task_info_dict = None
        if is_cache:
            task_info_dict = task_info_model.get_cache_dict_by_id(task_id,dependency_key=f"task_info:taskid_{task_id}")
        else:
            task_info_dict = task_info_model.get_dict_by_id(task_id)
        if is_filter == True:
            if not task_info_dict or task_info_dict["is_release"] == 0:
                return None
        return task_info_dict
    
    def get_task_asset_type(self, task_asset_type_json, task_type):
        """
        :description: 获取任务奖励资产类型
        :param task_asset_type:任务资产类型配置  key:1次数2积分3价格档位9999其他（混合搭配）
        :param task_type:任务类型
        :return 任务奖励资产类型
        :last_editors: HuangJianYi
        """
        asset_type = 2
        if task_asset_type_json == "":
            return asset_type
        task_asset_type_dict = SevenHelper.json_loads(task_asset_type_json)
        if not task_asset_type_dict:
            return asset_type
        if int(task_asset_type_dict["key"]) != 9999:
            asset_type = int(task_asset_type_dict["key"])
            return asset_type
        value_dict = task_asset_type_dict["value"]
        if not value_dict:
            return asset_type
        if str(task_type) in value_dict.keys():
            asset_type = value_dict[str(task_type)]
        return asset_type

    def _get_task_count_id(self,act_id,module_id,task_type,task_sub_type,user_id):
        """
        :description: 获取任务计数标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param task_type:任务类型
        :param task_sub_type:任务子类型
        :param user_id:用户标识
        :return 获取任务计数标识
        :last_editors: HuangJianYi
        """
        if not act_id or not task_type or not user_id:
            return 0
        return CryptoHelper.md5_encrypt_int(f"{act_id}_{module_id}_{task_type}_{task_sub_type}_{user_id}")

    def check_task_info(self,act_id,module_id,task_type):
        """
        :description: 校验任务信息
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param task_type:任务类型
        :return 
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            task_info_model = TaskInfoModel(context=self.context)
            task_info_dict = task_info_model.get_cache_dict("act_id=%s and module_id=%s and task_type=%s",params=[act_id,module_id,task_type],dependency_key=f"task_info_list:actid_{act_id}")
            if not task_info_dict or task_info_dict["is_release"] == 0:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "任务信息不存在"
                return invoke_result_data
            task_config = SevenHelper.json_loads(task_info_dict["task_config"])
            if not task_config:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "任务信息配置不存在"
                return invoke_result_data
            task_info_dict["task_config"] = task_config
            invoke_result_data.data = task_info_dict
        except Exception as ex:
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "任务信息不存在"
            return invoke_result_data
        return invoke_result_data
    
    def get_only_id(self,complete_type,task_type,task_sub_type="",complete_count=1):
        """
        :description: 获取only_id
        :param complete_type:完成类型(1每日任务2每周任务3持久任务)
        :param task_type:任务类型
        :param task_sub_type:任务子类型
        :param complete_count:完成次数
        :return only_id
        :last_editors: HuangJianYi
        """
        only_id = f"task_{task_type}_{task_sub_type}"
        if complete_type == 1:
            only_id += f"_{SevenHelper.get_now_day_int()}"
        elif complete_type == 2:
            only_id += f"_{str(datetime.datetime.year)+str(datetime.datetime.now().isocalendar()[1])}"
        else:
            only_id += f"_0"
        only_id += f"_{complete_count}"
            
    def process_free_gift(self,app_id,act_id,module_id,user_id,login_token,handler_name,request_id,check_new_user=False,check_user_nick=True,continue_request_expire=5,asset_sub_table=None):
        """
        :description: 处理掌柜有礼、新人有礼、免费领取等相似任务
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_id:用户标识
        :param login_token:访问令牌
        :param handler_name:接口名称
        :param request_id:请求标识
        :param check_new_user:是否新用户才能领取 1是0否
        :param check_user_nick:是否校验昵称为空
        :param continue_request_expire:连续请求过期时间，为0不进行校验，单位秒
        :param asset_sub_table:资产分表名称
        :return 
        :last_editors: HuangJianYi
        """
        acquire_lock_name = f"process_free_gift:{act_id}_{module_id}_{user_id}"
        identifier = ""
        task_type = TaskType.free_gift.value
        try:
            invoke_result_data = self.business_process_executing(app_id,act_id,module_id,user_id,login_token,handler_name,check_new_user,check_user_nick,continue_request_expire,acquire_lock_name)
            if invoke_result_data.success == True:
                task_invoke_result_data = self.check_task_info(act_id,module_id,task_type)
                if task_invoke_result_data.success == True:
                    task_info_dict = task_invoke_result_data.data
                    task_config = task_info_dict["task_config"]
                    reward_value = int(task_config["reward_value"]) if task_config.__contains__("reward_value") else 0
                    act_info_dict = invoke_result_data.data["act_info_dict"]
                    act_module_dict = invoke_result_data.data["act_module_dict"]
                    user_info_dict = invoke_result_data.data["user_info_dict"]
                    identifier = invoke_result_data.data["identifier"]
                    task_count_model = TaskCountModel(context=self.context)
                    task_count_id = self._get_task_count_id(act_id,module_id,task_info_dict["task_type"],"",user_id)
                    task_count_total = task_count_model.get_total(where="id=%s",params=[task_count_id])
                    if task_count_total > 0:
                        invoke_result_data.success = False
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = "已经领取过"
                    else:
                        if reward_value > 0:
                            only_id = self.get_only_id(task_info_dict["complete_type"],task_type)
                            asset_type = self.get_task_asset_type(act_info_dict["task_asset_type_json"],task_type)
                            asset_base_model = AssetBaseModel(context=self.context)
                            asset_invoke_result_data = asset_base_model.update_user_asset(app_id,act_id,module_id,user_id,user_info_dict["open_id"],user_info_dict["user_nick"],asset_type,reward_value,"",2,task_type,task_info_dict["task_name"],task_type,"",only_id,handler_name,request_id,info_json={},sub_table=asset_sub_table)
                            if asset_invoke_result_data.success == False:
                                reward_value = 0
                            task_count = TaskCount()
                            task_count.id = task_count_id
                            task_count.app_id = app_id
                            task_count.act_id = act_id
                            task_count.module_id = module_id
                            task_count.user_id = user_id
                            task_count.open_id = user_info_dict["open_id"]
                            task_count.task_type = task_type
                            task_count.task_sub_type = ""
                            task_count.complete_count = 1
                            task_count.now_count = 1
                            task_count.create_date = SevenHelper.get_now_datetime()
                            task_count.modify_date = SevenHelper.get_now_datetime()
                            task_count.modify_day = SevenHelper.get_now_day_int()
                            task_count_model.add_update_entity(task_count)

                            invoke_result_data.data = reward_value

        except Exception as ex:
            self.context.logging_link_error("【掌柜有礼】" + str(ex))
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"    
        finally:
            self.business_process_executed(act_id,module_id,user_id,handler_name,acquire_lock_name,identifier)

        return invoke_result_data
        
        