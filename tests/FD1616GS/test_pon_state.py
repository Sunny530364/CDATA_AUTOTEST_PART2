#!/usr/bin/python
# -*- coding UTF-8 -*-

#author: ZHONGQI

from src.FD1616GS.olt_opera import *
import pytest
import allure
from src.config.initialization_config import *

@allure.feature("PON口操作")
@allure.story("PON口使能")
@allure.title("PON口使能")
@pytest.mark.run(order=1601)
def test_pon_enable(login3):

    cdata_info("=========pon口使能测试=========")
    tn=login3
    with allure.step('pon口使能'):
        shutdown_pon(tn, Epon_PonID)
        assert noshutdown_pon(tn,Gpon_PonID)

@allure.feature("PON口操作")
@allure.story("PON口使能")
@allure.title("PON口使能")
@pytest.mark.run(order=1629)
def test_pon_disable(login3):

    cdata_info("=========pon口去使能测试=========")
    tn=login3
    with allure.step('pon口去使能'):
        assert shutdown_pon(tn, Gpon_PonID)