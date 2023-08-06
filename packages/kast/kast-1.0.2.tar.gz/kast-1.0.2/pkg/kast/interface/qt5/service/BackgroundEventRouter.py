#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import copy

from kast.interface.qt5.service.InterfaceScheduler import InterfaceScheduler
from kast.interface.qt5.service.UiEventObserver import UiEventObserver
from kast.media.casting.CastEventObserver import CastEventObserver
from kast.media.casting.CastState import CastState


class BackgroundEventRouter:

    def __init__(
        self,
        interfaceScheduler: InterfaceScheduler,
        uiEventObserver: UiEventObserver,
        castEventObserver: CastEventObserver
    ) -> None:
        self._interfaceScheduler = interfaceScheduler
        self._uiEventObserver = uiEventObserver
        self._castEventObserver = castEventObserver

        self._castEventObserver.register(listener=self, callback=self._onCastEvent)

    def _onCastEvent(self, event: CastState) -> None:

        def interfaceCallback() -> None:
            self._uiEventObserver.notify(castState=copy.deepcopy(event))

        self._interfaceScheduler.schedule(callback=interfaceCallback)
