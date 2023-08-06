#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import threading
from pathlib import Path
from typing import Any, Callable, List, Optional

from PyQt5.QtWidgets import QComboBox, QFileDialog, QStyle, QWidget

from kast.interface.qt5.UiServices import UiServices
from kast.interface.qt5.service.UiEvent import Progress, UiEvent, UiState
from kast.interface.qt5.dialogs import dialogError, dialogQuestionOkCancel, dialogWarning
from kast.interface.qt5.view.VideoSettingsView import Ui_VideoSettingsView
from kast.interface.qt5.viewModel.ViewModelBase import ViewBase, ViewModelBase
from kast.media.casting.CastException import CastException
from kast.media.casting.CastState import CastState
from kast.media.processing.MetaData import MetaData
from kast.media.processing.SubtitleUtils import SubtitleException
from kast.media.processing.SubtitlesSource import SubtitlesFromFile, SubtitlesFromStream
from kast.media.processing.SubtitlesSourceList import SubtitlesSourceList
from kast.media.processing.Transcoder import Codecs, Streams, TranscodeParams, Transcoder
from kast.media.processing.common import containerExtension
from kast.utils.Loggable import Loggable


class View(ViewBase, QWidget, Ui_VideoSettingsView):
    pass


class VideoSettingsViewModel(ViewModelBase, Loggable):

    def __init__(self, parent: QWidget, uiServices: UiServices) -> None:
        self._view = View(parent=parent)
        super().__init__(uiServices=uiServices, view=self._view)
        self.uiServices.uiEventObserver.register(self, self._onUiEvent)

        self._view.buttonDeviceRefresh.setIcon(self._view.style().standardIcon(QStyle.SP_BrowserReload))
        self._view.buttonVideoOpen.setIcon(self._view.style().standardIcon(QStyle.SP_DirOpenIcon))
        self._view.buttonSubtitlesAdd.setIcon(self._view.style().standardIcon(QStyle.SP_DirOpenIcon))

        self._view.buttonDeviceRefresh.clicked.connect(self._signalDevicesRefresh)
        self._view.buttonVideoOpen.clicked.connect(self._signalVideoOpen)
        self._view.buttonSubtitlesAdd.clicked.connect(self._signalSubtitlesAdd)
        self._view.buttonStream.clicked.connect(self._signalStream)

        self._metaData = MetaData()
        self._subtitlesSourceList = SubtitlesSourceList()
        self._lastTranscodeParams: Optional[TranscodeParams] = None

        self._fillSubtitlesComboBox()

    def _onUiEvent(self, uiEvent: UiEvent, castState: CastState) -> None:
        viewEnabled = uiEvent.state in [UiState.Idle]
        self._view.setEnabled(viewEnabled)

        self._view.setVisible(uiEvent.state != UiState.Streaming)

    def _signalDevicesRefresh(self) -> None:
        self.uiServices.uiEventObserver.notify(
            uiEvent=UiEvent(state=UiState.DeviceSearch, progress=Progress(complete=False)))

        def interfaceCallback(deviceNames: List[str]) -> None:
            self._view.comboBoxDevice.clear()
            self._view.comboBoxDevice.addItems(deviceNames)

            if not deviceNames:
                message = "No devices could be found!"
                "\n(Make sure this PC and your cast device are in the same network.)"
                dialogWarning(message=message)

            self.uiServices.uiEventObserver.notify(uiEvent=UiEvent(state=UiState.Idle))

        def backgroundTask() -> None:
            devicesList = self.services.castController.searchDevices()
            self.uiServices.interfaceScheduler.schedule(lambda: interfaceCallback(deviceNames=devicesList))

        self.uiServices.backgroundRunner.execute(lambda: backgroundTask())

    def _signalVideoOpen(self) -> None:
        filePath = QFileDialog.getOpenFileName(
            self._view,
            "Open Video",
            str(self.services.settings.browseMediaDir),
            "Videos (*.mp4 *.mkv *.webm *.avi)"
        )[0]
        if not filePath:
            return

        filePath = Path(filePath)
        self.services.settings.browseMediaDir = filePath.parent
        self._view.lineEditVideo.setText(str(filePath))

        self.uiServices.uiEventObserver.notify(
            uiEvent=UiEvent(state=UiState.VideoProbe, progress=Progress(complete=False)))

        def interfaceCallback(metaData: MetaData) -> None:
            self._metaData = metaData

            self._subtitlesSourceList.clear()
            for streamId in range(len(metaData.subtitleStreamLangs)):
                self._subtitlesSourceList.append(SubtitlesFromStream(
                    mediaProcessingService=self.services.mediaProcessingService,
                    mediaFile=filePath,
                    streamId=streamId
                ))

            self._fillAudioComboBox(items=metaData.audioStreamLangs)
            self._fillSubtitlesComboBox(items=metaData.subtitleStreamLangs)
            self.uiServices.uiEventObserver.notify(uiEvent=UiEvent(state=UiState.Idle))

        def backgroundTask() -> None:
            metaData = self.services.mediaProcessingService.extractMetaData(inputFile=filePath)
            self.uiServices.interfaceScheduler.schedule(lambda: interfaceCallback(metaData=metaData))

        self.uiServices.backgroundRunner.execute(lambda: backgroundTask())

    def _signalSubtitlesAdd(self) -> None:
        filePath = QFileDialog.getOpenFileName(
            self._view,
            "Open Subtitles",
            str(self.services.settings.browseMediaDir),
            "Subtitles (*.srt *.sub *.ass *.ssa *.txt *.vtt)"
        )[0]
        if not filePath:
            return

        filePath = Path(filePath)
        self.services.settings.browseMediaDir = filePath.parent
        self._subtitlesSourceList.append(SubtitlesFromFile(
            mediaProcessingService=self.services.mediaProcessingService,
            subtitlesFile=filePath
        ))
        self._view.comboBoxSubtitles.addItem(filePath.name)
        self._view.comboBoxSubtitles.setCurrentIndex(self._view.comboBoxSubtitles.count() - 1)

    def _signalStream(self) -> None:
        errors = []

        deviceName = self._view.comboBoxDevice.currentText()
        (not deviceName) and errors.append("No cast device selected!")

        videoFilePath = str(self._view.lineEditVideo.text())
        (not videoFilePath) and errors.append("No video file selected!")

        if errors:
            errors = ["Could not start streaming! Preconditions that failed:"] + errors
            dialogWarning(message='\n - '.join(errors))
            return

        self.uiServices.uiEventObserver.notify(
            uiEvent=UiEvent(state=UiState.Preprocessing, progress=Progress(complete=False)))

        selectedSubtitlesId = (self._view.comboBoxSubtitles.currentIndex() - 1)
        selectedSubtitlesSource = self._subtitlesSourceList[selectedSubtitlesId] \
            if selectedSubtitlesId >= 0 else None

        videoFilePath = Path(videoFilePath)
        audioStreamId = self._view.comboBoxAudio.currentIndex()  # TODO: Should we care if it fails (-1)?
        videoTitle = self._metaData.title

        def interfaceCallbackError(message: str) -> None:
            dialogError(message=message)
            self.uiServices.uiEventObserver.notify(uiEvent=UiEvent(state=UiState.Idle))

        def interfaceCallbackTranscoding(percent: int, complete: bool, cancelEvent: threading.Event) -> None:
            self.uiServices.uiEventObserver.notify(uiEvent=UiEvent(state=UiState.AvProcessing, progress=Progress(
                complete=complete, percentage=percent, cancelEvent=cancelEvent
            )))

        def interfaceCallbackCanceled() -> None:
            self.uiServices.uiEventObserver.notify(uiEvent=UiEvent(state=UiState.Idle))

        def interfaceCallbackConnecting() -> None:
            self.uiServices.uiEventObserver.notify(uiEvent=UiEvent(state=UiState.Connecting, progress=Progress(complete=False)))

        def interfaceCallbackStreaming() -> None:
            self.uiServices.uiEventObserver.notify(uiEvent=UiEvent(state=UiState.Streaming))

        def backgroundTaskCallbackRunner(callback: Callable[[Any], None], *args, **kwargs) -> None:
            try:
                callback(*args, **kwargs)
            except (SubtitleException, CastException) as ex:
                message = str(ex)  # Workaround for a 'free variable referenced before assignment' problem.
                self.log.exception(ex)
                self.uiServices.interfaceScheduler.schedule(lambda: interfaceCallbackError(message=message))

        def backgroundTaskStreaming(videoFile: Path) -> None:
            mediaContent = self.services.mediaServer.mediaContent
            mediaContent.movieFile = videoFile
            mediaContent.subtitlesFile = selectedSubtitlesSource.toVtt() if selectedSubtitlesSource else None

            self.uiServices.interfaceScheduler.schedule(interfaceCallbackConnecting)

            self.services.castController.connect(name=deviceName)
            self.services.castController.stream(
                movieUrl=self.services.mediaServer.movieUrl,
                subtitlesUrl=self.services.mediaServer.subtitleUrl,
                thumbnailUrl=self.services.mediaServer.thumbnailUrl,
                title=videoTitle
            )

            self.uiServices.interfaceScheduler.schedule(interfaceCallbackStreaming)

        def interfaceCallbackPlayConfirmation(videoFile: Path) -> None:
            message = "Media processing finished!\n\nProceed with streaming?\n"

            if not dialogQuestionOkCancel(title="Streaming", message=message):
                interfaceCallbackCanceled()
                return

            self.uiServices.backgroundRunner.execute(lambda: backgroundTaskCallbackRunner(backgroundTaskStreaming, videoFile))

        def backgroundTaskTranscodingRun(transcoder: Transcoder) -> None:
            if not transcoder.run():
                self.uiServices.interfaceScheduler.schedule(interfaceCallbackCanceled)
                return

            self._lastTranscodeParams = transcoder.params

            self.uiServices.interfaceScheduler.schedule(lambda: interfaceCallbackPlayConfirmation(transcoder.outputFile))

        def interfaceCallbackTranscodingConfirmation(transcoder: Transcoder) -> None:
            message = "Selected media is not supported in it's current form. " \
                "Either because of a codec mismatch or not supported media container type. " \
                "Your file can be transcoded or remuxed to address those issues respectively.\n" \
                "\n" \
                "Remuxing is a quick process. While duration of transcoding varies. " \
                "It is usually fast for audio codecs and can take some time for video codecs. " \
                "Actual times will depend on your machine processing power.\n" \
                "\n" \
                "Provided Container -> Supported Container:\n" \
                f"- {containerExtension(transcoder.inputFile)} -> {containerExtension(transcoder.outputFile)}\n" \
                "\n" \
                "Provided Codecs -> Supported Codecs:\n" \
                f"- Video: '{transcoder.inputCodecNames.video}' -> '{transcoder.outputCodecNames.video}'\n" \
                f"- Audio: '{transcoder.inputCodecNames.audio}' -> '{transcoder.outputCodecNames.audio}'\n" \
                "\n" \
                "Proceed with media processing?\n" \
                "(Your original file will not be modified.)\n"

            if not dialogQuestionOkCancel(title="Media Processing", message=message):
                interfaceCallbackCanceled()
                return

            self.uiServices.backgroundRunner.execute(lambda: backgroundTaskCallbackRunner(backgroundTaskTranscodingRun, transcoder))

        def backgroundTaskTranscodingInit() -> None:
            cancelEvent = threading.Event()

            def progressCallback(percent: int, complete: bool) -> None:
                self.log.info(f"Transcoding progress: {percent}% ({'Complete' if complete else 'Running'})")
                self.uiServices.interfaceScheduler.schedule(
                    lambda: interfaceCallbackTranscoding(percent=percent, complete=complete, cancelEvent=cancelEvent))

            castController = self.services.castController

            inputContainer = containerExtension(videoFilePath)
            outputContainer = inputContainer if inputContainer in castController.supportedContainerFormats \
                else castController.preferredContainerFormat

            outputCodecNames = Codecs(
                video=castController.preferredVideoCodec,
                audio=castController.preferredAudioCodec
            )

            transcoder = self.services.mediaProcessingService.createTranscoder(
                inputFile=videoFilePath,
                inputStreamIds=Streams(video=0, audio=audioStreamId),
                outputCodecNames=outputCodecNames,
                containerFormat=outputContainer,
                progressCallback=progressCallback,
                cancelEvent=cancelEvent
            )
            self.log.info(f"Input file: container='{inputContainer}', codecs={transcoder.inputCodecNames}")
            self.log.info(f"Output file: container='{outputContainer}', codecs={transcoder.outputCodecNames}")
            if transcoder.requireProcessing and self._lastTranscodeParams != transcoder.params:
                self.uiServices.interfaceScheduler.schedule(lambda: interfaceCallbackTranscodingConfirmation(transcoder))
                return

            backgroundTaskStreaming(transcoder.outputFile)

        self.uiServices.backgroundRunner.execute(lambda: backgroundTaskCallbackRunner(backgroundTaskTranscodingInit))

    def _fillDeviceComboBox(self, items: List[str]) -> None:
        self._fillComboBox(self._view.comboBoxDevice, items)

    def _fillAudioComboBox(self, items: List[str] = None) -> None:
        self._fillComboBox(self._view.comboBoxAudio, items)

    def _fillSubtitlesComboBox(self, items: List[str] = None) -> None:
        items = items if items else []
        self._fillComboBox(self._view.comboBoxSubtitles, ['No Subtitles'] + items)

    @staticmethod
    def _fillComboBox(comboBox: QComboBox, items: List[str] = None) -> None:
        comboBox.clear()
        items and comboBox.addItems(items)
