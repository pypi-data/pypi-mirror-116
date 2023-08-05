#  The MIT License (MIT)
#
#  Copyright (c) 2021. Scott Lau
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import logging
import os

import numpy as np
import pandas as pd
from pandas import ExcelWriter

from .utils import ConfigUtils


class DiffAnalyzer:

    def __init__(self):
        # 是否包含年初数据
        self._contains_yearly_base_data = False
        self._yearly_base_data = pd.DataFrame()
        # 是否包含季度初数据
        self._contains_seasonal_base_data = False
        self._seasonal_base_data = pd.DataFrame()
        # 是否包含月初数据
        self._contains_monthly_base_data = False
        self._monthly_base_data = pd.DataFrame()
        # 是否包含上周数据
        self._contains_last_week_data = False
        self._last_week_data = pd.DataFrame()
        # 是否包含昨日数据
        self._contains_yesterday_data = False
        self._yesterday_data = pd.DataFrame()
        # 是否包含当日数据
        self._contains_current_day_data = False
        self._current_day_data = pd.DataFrame()
        self._read_config()

    def _read_config(self):
        """
        读取配置，初始化相关变量
        """
        config = ConfigUtils.get_config()

        # 年初分析结果文件路径
        self._yearly_base_file_path = config.get("diff.yearly_base_file_path")
        # 季度初分析结果文件路径
        self._seasonal_base_file_path = config.get("diff.seasonal_base_file_path")
        # 月初分析结果文件路径
        self._monthly_base_file_path = config.get("diff.monthly_base_file_path")
        # 上周分析结果文件路径
        self._last_week_file_path = config.get("diff.last_week_file_path")
        # 昨日分析结果文件路径
        self._yesterday_file_path = config.get("diff.yesterday_file_path")
        # 当日分析结果文件路径
        self._current_day_file_path = config.get("diff.current_day_file_path")

        # 生成的目标Excel文件存放路径
        self._target_directory = config.get("diff.target_directory")
        # 目标文件名称
        self._target_filename = config.get("diff.target_filename")
        # 生成的Excel中Sheet的名称
        self._target_sheet_name = config.get("diff.target_sheet_name")

        # 比较类型列名称
        self._target_compare_type_column_name = config.get("diff.target_compare_type_column_name")
        # 较年初分析结果列名称
        self._target_yearly_base_compare_column_name = config.get("diff.target_yearly_base_compare_column_name")
        # 较季初分析结果列名称
        self._target_seasonal_base_compare_column_name = config.get("diff.target_seasonal_base_compare_column_name")
        # 较月初分析结果列名称
        self._target_monthly_base_compare_column_name = config.get("diff.target_monthly_base_compare_column_name")
        # 较上周分析结果列名称
        self._target_last_week_compare_column_name = config.get("diff.target_last_week_compare_column_name")
        # 较昨日分析结果列名称
        self._target_yesterday_compare_column_name = config.get("diff.target_yesterday_compare_column_name")
        # 当前日期分析结果列名称
        self._target_current_day_column_name = config.get("diff.target_current_day_column_name")

        # Sheet名称
        self._sheet_name = config.get("diff.sheet_name")
        # 表头行索引
        self._header_row = config.get("diff.header_row")
        # 所属机构列名称（Excel中列名必须唯一）
        self._branch_column_name = config.get("diff.branch_column_name")
        # 待分析差异列名称列表（Excel中列名必须唯一）
        self._diff_column_list = config.get("diff.diff_column_list")
        # 比较项目的排序规则，按配置文件配置的先后顺序进行排序
        self._diff_column_order = dict()
        index = 1
        for column in self._diff_column_list:
            self._diff_column_order[column] = index
            index = index + 1
        # 选中需要处理的机构清单
        self._branch_selected_list = config.get("branch.selected_list")

    def analysis(self):
        logging.getLogger(__name__).info("开始进行报表阶段性差异分析...")
        self._contains_current_day_data, self._current_day_data = self._read_src_file(self._current_day_file_path)
        if not self._contains_current_day_data:
            logging.getLogger(__name__).error("未找到当日数据，程序退出。")
            return 1
        self._contains_yesterday_data, self._yesterday_data = self._read_src_file(self._yesterday_file_path)
        if not self._contains_yesterday_data:
            logging.getLogger(__name__).warning("未找到昨日数据")
        self._contains_last_week_data, self._last_week_data = self._read_src_file(self._last_week_file_path)
        if not self._contains_last_week_data:
            logging.getLogger(__name__).warning("未找到上周数据")
        self._contains_monthly_base_data, self._monthly_base_data = self._read_src_file(self._monthly_base_file_path)
        if not self._contains_monthly_base_data:
            logging.getLogger(__name__).warning("未找到月初数据")
        self._contains_seasonal_base_data, self._seasonal_base_data = self._read_src_file(self._seasonal_base_file_path)
        if not self._contains_seasonal_base_data:
            logging.getLogger(__name__).warning("未找到季度初数据")
        self._contains_yearly_base_data, self._yearly_base_data = self._read_src_file(self._yearly_base_file_path)
        if not self._contains_yearly_base_data:
            logging.getLogger(__name__).warning("未找到年初数据")
        if (not self._contains_yesterday_data) \
                and (not self._contains_last_week_data) \
                and (not self._contains_monthly_base_data) \
                and (not self._contains_seasonal_base_data) \
                and (not self._contains_yearly_base_data):
            logging.getLogger(__name__).error("未找到可对比数据，程序退出。")
            return 2

        diff = self._calculate_difference(
            current_day_data=self._current_day_data,
            yesterday_data=self._yesterday_data,
            last_week_data=self._last_week_data,
            monthly_base_data=self._monthly_base_data,
            seasonal_base_data=self._seasonal_base_data,
            yearly_base_data=self._yearly_base_data,
        )
        result = self._write_diff_result(diff=diff)
        logging.getLogger(__name__).info("结束报表阶段性差异分析，结果：{}".format(result))
        return result

    def _read_src_file(self,
                       source_file_path: str,
                       ) -> (bool, pd.DataFrame):
        """
        读取原始数据，获取DataFrame

        :param source_file_path: 源文件路径
        :return: (bool, pd.DataFrame), 1、是否包含数据，2、读取的数据
        """
        logging.getLogger(__name__).info("读取源文件：{}".format(source_file_path))
        try:
            data = pd.read_excel(source_file_path, sheet_name=self._sheet_name, header=self._header_row)
            # 筛选指定部门，删除合计行
            data = data[data[self._branch_column_name].isin(self._branch_selected_list)]
            # 按机构排序
            data = data.sort_values(
                by=[self._branch_column_name],
                ascending=True
            )
            return True, data
        except Exception as e:
            logging.getLogger(__name__).error("读取文件失败：{}".format(e))
            return False, pd.DataFrame()

    def _calculate_difference(self, *,
                              current_day_data: pd.DataFrame,
                              yesterday_data: pd.DataFrame,
                              last_week_data: pd.DataFrame,
                              monthly_base_data: pd.DataFrame,
                              seasonal_base_data: pd.DataFrame,
                              yearly_base_data: pd.DataFrame,
                              ) -> pd.DataFrame:
        """
        差异分析
        :rtype: pd.DataFrame
        :param current_day_data: 当日数据
        :param yesterday_data: 昨日数据
        :param last_week_data: 上周数据
        :param monthly_base_data: 月初数据
        :param seasonal_base_data: 季度初数据
        :param yearly_base_data: 年初数据
        :return: 差异分析结果
        """
        # 所有列
        all_columns = list()
        all_columns.append(self._branch_column_name)
        all_columns.append(self._target_compare_type_column_name)
        all_columns.extend(self._diff_column_list)
        result = pd.DataFrame(columns=all_columns)
        # 所有部门
        all_branches = list(current_day_data[self._branch_column_name].values)

        compare_types = list()
        manager_order = dict()
        if self._contains_current_day_data:
            compare_types.append(self._target_current_day_column_name)
            manager_order[self._target_current_day_column_name] = 0
        if self._contains_yearly_base_data:
            compare_types.append(self._target_yearly_base_compare_column_name)
            manager_order[self._target_yearly_base_compare_column_name] = 0
        if self._contains_seasonal_base_data:
            compare_types.append(self._target_seasonal_base_compare_column_name)
            manager_order[self._target_seasonal_base_compare_column_name] = 0
        if self._contains_monthly_base_data:
            compare_types.append(self._target_monthly_base_compare_column_name)
            manager_order[self._target_monthly_base_compare_column_name] = 0
        if self._contains_last_week_data:
            compare_types.append(self._target_last_week_compare_column_name)
            manager_order[self._target_last_week_compare_column_name] = 0
        if self._contains_yesterday_data:
            compare_types.append(self._target_yesterday_compare_column_name)
            manager_order[self._target_yesterday_compare_column_name] = 0

        logging.getLogger(__name__).info("before init %s", result)
        # 初始化基础数据
        for branch in all_branches:
            for key in compare_types:
                result = result.append({
                    self._branch_column_name: branch,
                    self._target_compare_type_column_name: key,
                }, ignore_index=True)
        logging.getLogger(__name__).info("initialize %s", result)
        # 分析较年初
        self._calculate_diff_according_to_type(
            result=result,
            contains_data=self._contains_yearly_base_data,
            current_day_data=current_day_data,
            compare_type=self._target_yearly_base_compare_column_name,
            compare_data=yearly_base_data,
        )
        logging.getLogger(__name__).info("yearly %s", result)
        # 分析较季度初
        self._calculate_diff_according_to_type(
            result=result,
            contains_data=self._contains_seasonal_base_data,
            current_day_data=current_day_data,
            compare_type=self._target_seasonal_base_compare_column_name,
            compare_data=seasonal_base_data,
        )
        logging.getLogger(__name__).info("yesterday %s", result)
        # 分析较月初
        self._calculate_diff_according_to_type(
            result=result,
            contains_data=self._contains_monthly_base_data,
            current_day_data=current_day_data,
            compare_type=self._target_monthly_base_compare_column_name,
            compare_data=monthly_base_data,
        )
        logging.getLogger(__name__).info("monthly %s", result)
        # 分析较上周
        self._calculate_diff_according_to_type(
            result=result,
            contains_data=self._contains_last_week_data,
            current_day_data=current_day_data,
            compare_type=self._target_last_week_compare_column_name,
            compare_data=last_week_data,
        )
        logging.getLogger(__name__).info("weekly %s", result)
        # 分析较昨日
        self._calculate_diff_according_to_type(
            result=result,
            contains_data=self._contains_yesterday_data,
            current_day_data=current_day_data,
            compare_type=self._target_yesterday_compare_column_name,
            compare_data=yesterday_data,
        )
        logging.getLogger(__name__).info("yesterday %s", result)
        # 当前时点数
        self._deal_with_current_data(result, current_day_data)
        logging.getLogger(__name__).info("current %s", result)
        # 没有的数据填充"-"
        result.fillna("-", inplace=True)
        # 处理比较类型的排序
        result[self._target_compare_type_column_name] = pd.Categorical(
            result[self._target_compare_type_column_name],
            manager_order.keys()
        )
        logging.getLogger(__name__).info("before pivot %s", result)

        # 按待分析差异、按比较类型归类
        result = pd.pivot_table(
            result,
            values=self._diff_column_list,
            columns=[self._target_compare_type_column_name],
            index=[self._branch_column_name],
            aggfunc=np.sum,
            fill_value=0,
        )
        logging.getLogger(__name__).info("after pivot %s", result)
        # 添加机构合计行
        result.loc["合计"] = result.apply(lambda x: x.sum())
        logging.getLogger(__name__).info("add sum %s", result)
        # 调整比较项目（待分析差异列）的排序
        result.sort_index(
            axis=1,
            level=[0, 1],
            key=self._sort_compare_item_and_type,
            inplace=True,
        )
        logging.getLogger(__name__).info("sort index %s", result)
        return result

    def _sort_compare_item_and_type(self, columns):
        # 如果是待分析差异项排序，则使用自定义的排序规则
        if self._diff_column_order.get(columns[0]) is not None:
            return columns.map(self._diff_column_order)
        else:
            # 如果是比较类型的排序，使用原有的Categorical进行排序
            return columns

    def _deal_with_current_data(self,
                                result: pd.DataFrame,
                                current_day_data: pd.DataFrame,
                                ):
        for row_i, row in result.iterrows():
            branch = row[self._branch_column_name]
            target_cmp_type = row[self._target_compare_type_column_name]
            if target_cmp_type != self._target_current_day_column_name:
                continue
            for column in self._diff_column_list:
                if column not in current_day_data.columns.values:
                    continue
                # 查找指标对应的值
                criterion1 = current_day_data[self._branch_column_name].map(lambda x: x == branch)
                value = current_day_data.loc[criterion1, column]
                if value.empty:
                    continue
                result.at[row_i, column] = value.values[0]

    def _calculate_diff_according_to_type(self,
                                          result: pd.DataFrame,
                                          contains_data: bool,
                                          current_day_data: pd.DataFrame,
                                          compare_type: str,
                                          compare_data: pd.DataFrame,
                                          ):
        """
        根据比较类型计算差异
        :param result: 差异分析结果
        :param contains_data: 是否包含待比较数据，如果没有，则直接返回
        :param current_day_data: 当前时点数
        :param compare_type: 比数类型：较年初、季初、月初、上周、昨日
        :param compare_data: 待比较分析
        :return:
        """
        if not contains_data:
            return
        compare_result = current_day_data.merge(
            compare_data,
            how="left",
            on=self._branch_column_name,
            suffixes=["_1", "_2"],
        )
        compare_result.fillna(0, inplace=True)
        compare_result[self._target_compare_type_column_name] = compare_type
        # 按机构计算两次数据的差异
        existed_columns = list()
        existed_columns_plus_index_column = list([self._branch_column_name, self._target_compare_type_column_name])
        for column in self._diff_column_list:
            if column in current_day_data.columns.values and column in compare_data.columns.values:
                compare_result[column] = compare_result[column + "_1"] - compare_result[column + "_2"]
                existed_columns_plus_index_column.append(column)
                existed_columns.append(column)
        compare_result = compare_result[existed_columns_plus_index_column]
        for row_i, row in result.iterrows():
            branch = row[self._branch_column_name]
            target_cmp_type = row[self._target_compare_type_column_name]
            for column in existed_columns:
                # 查找指标对应的值
                criterion1 = compare_result[self._branch_column_name].map(lambda x: x == branch)
                criterion2 = compare_result[self._target_compare_type_column_name].map(lambda x: x == target_cmp_type)
                value = compare_result.loc[criterion1 & criterion2, column]
                if value.empty:
                    continue
                result.at[row_i, column] = value.values[0]

    def _write_diff_result(self, *, diff: pd.DataFrame) -> int:
        target_filename_full_path = os.path.join(self._target_directory, self._target_filename)
        logging.getLogger(__name__).info("输出文件：{} ".format(target_filename_full_path))
        with ExcelWriter(target_filename_full_path) as excel_writer:
            for name, data in dict({
                self._target_current_day_column_name: self._current_day_data,
                self._target_yearly_base_compare_column_name: self._yearly_base_data,
                self._target_seasonal_base_compare_column_name: self._seasonal_base_data,
                self._target_monthly_base_compare_column_name: self._monthly_base_data,
                self._target_last_week_compare_column_name: self._last_week_data,
                self._target_yesterday_compare_column_name: self._yesterday_data,
            }).items():
                if data.empty:
                    continue
                # 添加机构合计行
                data.set_index(self._branch_column_name, inplace=True)
                data.loc["合计"] = data.apply(lambda x: x.sum())
                data.reset_index(inplace=True)
                data.to_excel(
                    excel_writer=excel_writer,
                    index=False,
                    sheet_name=name.replace("较", ""),
                )

            diff.to_excel(
                excel_writer=excel_writer,
                sheet_name=self._target_sheet_name,
            )
        return 0
