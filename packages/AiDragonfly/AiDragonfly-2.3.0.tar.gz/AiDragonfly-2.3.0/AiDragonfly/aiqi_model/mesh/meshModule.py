#! /usr/bin/env python
# -*- coding: utf-8 -*-


import AiDragonfly.aiqi_model.ble_cc.constantModule as constantModule
import AiDragonfly.aiqi_main as df

import asyncio
import csv
import time
# mesh设备的使用大体分为三步，第一步：用户输入直连设备，当多于一个设备时 需要输入配置设备
# 第二步：调用配置函数 当多于一个mesh设备时
# 第三步：调用控制函数
from AiDragonfly.aiqi_bluetooth_save_json import Read_Local_Onebot_Device
from AiDragonfly.common.onebot_common_function import Aiqi_Print_HEX

mesh_super_conf_name_list = ["OneBot_XL_M", "OneBot_St_M", "OneBot_BL_M"]
mesh_super_conf_dev_list = []

__log_title = 'mesh_model '

'''
speed -100 至 100
'''


def _speed_to_xl_speed(speed):
    re_spd = 0
    spd = speed
    if spd > 100:
        spd = 100
    elif spd < -100:
        spd = -100

    if spd >= 0:
        re_spd = spd
    else:
        re_spd = 100 - spd
    if re_spd == 100:
        re_spd = 99

    return re_spd


'''
speed -100 至 100
'''


def _speed_to_bl_speed(speed):
    re_spd = 0
    spd = speed
    if spd > 100:
        spd = 100
    elif spd < -100:
        spd = -100
    re_spd = spd

    return re_spd


'''
speed -150 至 150
'''


def _speed_to_st_speed(speed):
    zero_angle = 173
    re_spd = 0
    spd = speed
    if spd > 150:
        spd = 150
    elif spd < -150:
        spd = -150
    re_spd = zero_angle + spd
    return re_spd


'''
速度buff ,如 speed_buff=[100,-100]
+100，对应xl 电机、平衡电机，速度正传100，
+100 对应舵机，左转100度
max value  100 电机
max value  150 舵机
min value -100 电机
min value -150 舵机
'''


def mesh_super_ctrl(speed_buff):
    if len(speed_buff) == 0:
        print('please check speed_buff')
        return
    dev_len = len(mesh_super_conf_dev_list)
    dev_list = mesh_super_conf_dev_list

    tx_buf = bytearray(2+dev_len * 2)
    for i in tx_buf:
        i = 0
    tx_buf[0] = dev_len * 2
    tx_buf[1] = 122
    index = 0
    x = 0
    for spd in speed_buff:
        v1 = 0
        if dev_list[x].name == "OneBot_XL_M":
            v1 = _speed_to_xl_speed(spd)
        elif dev_list[x].name == "OneBot_BL_M":
            v1 = _speed_to_bl_speed(spd)
        elif dev_list[x].name == "OneBot_St_M":
            v1 = _speed_to_st_speed(spd)
        else:
            print('speed analy err')
            break
        tx_buf[2 + index] = v1 >> 8
        tx_buf[2 + index + 1] = v1 & 0xff
        index += 2
        x += 1
        if x > dev_len-1:
            break

    df.Aiqi_Bluetooth_Send(tx_buf)
    time.sleep(0.05)


'''
目前只支持配置 "OneBot_XL_M","OneBot_St_M","OneBot_BL_M"
配置时，会默认自动从列表中配置查找并配置，不支持的设备会自动跳过
默认直连扫到的第一个设备

'''


def mesh_super_configure():
    global mesh_super_conf_dev_list
    local_dev = Read_Local_Onebot_Device()
    conf_item = []
    for localitem in local_dev:  # 读取需要配置设备mesh addr
        if localitem.name in mesh_super_conf_name_list:
            conf_item.append(localitem)
    mesh_super_conf_dev_list = conf_item[:]

    del conf_item[0]  # 删除第一个，默认直连第一个
    dev_len = len(conf_item)

    if dev_len == 0 or dev_len > 6:
        # print('dev num is ' + str(dev_len) + ',不需要super配置')
        return
    tx_buf = bytearray(5 + dev_len * 2)

    tx_buf[0] = 3 + dev_len * 2

    tx_buf[1] = 121
    # Aiqi_Print_HEX(tx_buf)
    dev_mes = [0, 0, 0, 0, 0, 0]  # 配置设备类型属性
    dev_mes_index = 0
    for item in conf_item:
        if item.name == 'OneBot_XL_M' or item.name == 'OneBot_BL_M':
            dev_mes[dev_mes_index] = 1
        elif item.name == 'OneBot_St_M':
            dev_mes[dev_mes_index] = 2
        tx_buf[5 + dev_mes_index] = item.mesh_addr >> 8
        tx_buf[5 + dev_mes_index + 1] = item.mesh_addr & 0xff
        dev_mes_index += 1

    tx_buf[2] = dev_mes[0] << 4 + dev_mes[1]
    tx_buf[3] = dev_mes[2] << 4 + dev_mes[3]
    tx_buf[4] = dev_mes[4] << 4 + dev_mes[5]
    try:
        df.Aiqi_Bluetooth_Send(tx_buf)
    except:
        print(__log_title+'bluetooth send err')
    print(__log_title+'config ok')



def mesh_led_control(r, g, b, *, ID=1):  # mesh led真彩灯控制函数
    if df.mesh_control_flag == 1:  # 没有加密
        protocol = [0x04, 0x75, r, g, b, ID]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(df.sendDate(protocol, df.ONEBOT))
    elif df.mesh_control_flag == 2:  # 加密
        protocol = [0x06, 0x75, r, g, b, ID, df.mesh_sn_xor, df.mesh_random]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(df.sendDate(protocol, df.ONEBOT))
    elif df.mesh_control_flag == 0:
        print(__log_title+'错误，请打开电源 重新执行程序')


def mesh_mode_set(mode):  # mesh平衡机器人模式设置函数 自由电机模式 和 平衡模式
    df.mesh_mode_flag = 5
    if df.mesh_control_flag == 1:  # 电机模式
        if mode == constantModule.MESH_MODE_MOTOR:
            protocol = [0x01, 0x81, mode]
            loop = asyncio.get_event_loop()
            loop.run_until_complete(df.sendDate(protocol, df.ONEBOT))

        elif mode == constantModule.MESH_MODE_ACTIVE or mode == constantModule.MESH_MODE_PASSIVE:  # 平衡模式
            protocol = [0x01, 0x81, 0x03]
            loop = asyncio.get_event_loop()
            loop.run_until_complete(df.sendDate(protocol, df.ONEBOT))  # 直连设备发送模式配置信息
            protocol = [0x05, 0x7B, 0x00, 0x00, 0x01, 0x81, 0x02]
            with open(df.filename, "r+") as f:
                f_csv = csv.reader(f)
                for row in f_csv:
                    if row[1] == df.mesh_configure[0:2]:  # 从表格中查找配置设备对应的网络地址
                        tmp = row[2]
                        tmp = int(tmp)
                        protocol[3] = tmp >> 8
                        protocol[2] = tmp % 256
            loop = asyncio.get_event_loop()
            loop.run_until_complete(df.sendDate(protocol, df.ONEBOT))  # 配置设备 发送模式配置信息
            time.sleep(1)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(df.sendDate(protocol, df.ONEBOT))

    elif df.mesh_control_flag == 2:
        if mode == constantModule.MESH_MODE_MOTOR:
            protocol = [0x01, 0x81, mode, df.mesh_sn_xor, df.mesh_random]
            loop = asyncio.get_event_loop()
            loop.run_until_complete(df.sendDate(protocol, df.ONEBOT))
        elif mode == constantModule.MESH_MODE_ACTIVE or mode == constantModule.MESH_MODE_PASSIVE:
            protocol = [0x01, 0x81, 0x03, df.mesh_sn_xor, df.mesh_random]
            loop = asyncio.get_event_loop()
            loop.run_until_complete(df.sendDate(protocol, df.ONEBOT))
            protocol = [0x05, 0x7B, 0x00, 0x00, 0x01, 0x81, 0x02, df.mesh_sn_xor, df.mesh_random]
            with open(df.filename, "r+") as f:
                f_csv = csv.reader(f)
                for row in f_csv:
                    if row[1] == df.mesh_configure[0:2]:
                        tmp = row[2]
                        tmp = int(tmp)
                        protocol[3] = tmp >> 8
                        protocol[2] = tmp % 256
            loop = asyncio.get_event_loop()
            loop.run_until_complete(df.sendDate(protocol, df.ONEBOT))
            time.sleep(1)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(df.sendDate(protocol, df.ONEBOT))

