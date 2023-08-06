#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import Any, Callable, Dict, Optional

from kast.interface.qt5.service.UiEvent import UiEvent
from kast.media.casting.CastState import CastState
from kast.utils.Loggable import Loggable


class UiEventObserver(Loggable):

    Callback = Callable[[UiEvent, CastState], None]

    def __init__(self) -> None:
        self._listeners: Dict[Any, UiEventObserver.Callback] = {}
        self._uiEvent = UiEvent()
        self._castState = CastState()

    @property
    def uiEvent(self) -> UiEvent:
        return self._uiEvent

    @property
    def castState(self):
        return self._castState

    def register(self, listener: Any, callback: Callback) -> None:
        self._listeners[listener] = callback

    def unregister(self, listener: Any) -> None:
        if listener in self._listeners.keys():
            self._listeners.pop(listener)

    def notify(
        self,
        uiEvent: Optional[UiEvent] = None,
        castState: Optional[CastState] = None
    ) -> None:
        if uiEvent is None and castState is None:
            return

        uiEvent = uiEvent if uiEvent is not None else self.uiEvent
        castState = castState if castState is not None else self.castState

        if(
            self.uiEvent.state != uiEvent.state or
            self.castState.connection != castState.connection or
            self.castState.mediaState.playerState != castState.mediaState.playerState
        ):
            self.log.info(
                f"UiState={uiEvent.state.name}, "
                f"DeviceState={castState.connection.value.lower().capitalize()}, "
                f"MediaState={castState.mediaState.playerState.value.lower().capitalize()}"
            )

        self._uiEvent = uiEvent
        self._castState = castState

        for callback in self._listeners.values():
            callback(self.uiEvent, self.castState)
