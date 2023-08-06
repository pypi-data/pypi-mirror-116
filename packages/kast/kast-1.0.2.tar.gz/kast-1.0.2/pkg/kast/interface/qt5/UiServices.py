#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from kast.Services import Services
from kast.interface.qt5.service.BackgroundRunner import BackgroundRunner
from kast.interface.qt5.service.BackgroundEventRouter import BackgroundEventRouter
from kast.interface.qt5.service.InterfaceScheduler import InterfaceScheduler
from kast.interface.qt5.service.UiEventObserver import UiEventObserver


class UiServices:

    def __init__(self, services: Services) -> None:
        self.services = services
        self.interfaceScheduler = InterfaceScheduler()
        self.backgroundRunner = BackgroundRunner(interfaceScheduler=self.interfaceScheduler)
        self.uiEventObserver = UiEventObserver()
        self.backgroundEventRouter = BackgroundEventRouter(
            interfaceScheduler=self.interfaceScheduler,
            uiEventObserver=self.uiEventObserver,
            castEventObserver=self.services.castEventObserver
        )
