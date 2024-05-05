'''
from client.controller import ClientApplicationController
from client.model.subpages import GameRoomModel
from client.view.subpages import GameRoomView
from shared import SwingResources, SwingStylesheet

from javax.sound.sampled import AudioInputStream, AudioSystem, Clip
from javax import swing
from java import awt

import java.io.File
import java.io.IOException
import java.util
import java.util.List

class GameRoomController:
    def __init__(self, model, view, parent):
        self.view = view
        self.model = model
        self.parent = parent
        self.musicOn = True
        self.sfxOn = True
        self.audioSoundStream = None
        self.sfxClip = None
        self.style = SwingStylesheet()
        self.badInput = "res/audio/sfx/bad-input-sfx.wav"
        self.goodInput = "res/audio/sfx/good-input-sfx.wav"
        self.countdown = "res/audio/sfx/countdown-10s-sfx.wav"
        self.roundOver = "res/audio/sfx/round-over-sfx.wav"
        self.lose = "res/audio/sfx/lose-sfx.wav"
        self.win = "res/audio/sfx/winner-sfx.wav"

        view.setMusicToggleListener(MusicListener())
        view.setSoundToggleListener(SoundListener())
        view.setInputListener(InputListener())
        view.setClearListener(lambda e: [view.getTxtWordInput().setText(""), view.setErrorMessage("")])
        view.getBtnClear().addMouseListener(SwingResources.CursorChanger(view.getBtnClear()))
        view.getBtnMusicToggle().addMouseListener(SwingResources.CursorChanger(view.getBtnMusicToggle()))
        view.getBtnSoundToggle().addMouseListener(SwingResources.CursorChanger(view.getBtnSoundToggle()))
        view.getTxtWordInput().addFocusListener(SwingResources.TextFieldFocus(view.getTxtWordInput(), "Enter word here.", view.getLblErrorMessage()))
        view.revalidate()
        view.repaint()
        timer = threading.Thread(target=self.gameTimer)
        timer.start()

    def gameTimer(self):
        try:
            inSeconds = int(self.model.getWfImpl().getGameDurationVal(self.model.getGameRoomID() / 1000))
            print("IN SECONDS: " + str(inSeconds))
            self.view.setPrgTimerMaxVal(inSeconds)
            print(inSeconds)
            while inSeconds >= 0:
                time.sleep(1)
                self.view.setLblTimerTxt(inSeconds)
                inSeconds = int(self.model.getWfImpl().getGameDurationVal(self.model.getGameRoomID() / 1000))
                self.view.setPrgTimerValue(inSeconds)
                print(inSeconds)
                if inSeconds == 10:
                    self.playSFX("countdown")
                    SwingUtilities.invokeLater(lambda: [self.view.getPrgTimer().setBackground(self.style.red), self.view.getLblTimer().setForeground(self.style.red)])
                elif inSeconds == 0:
                    self.playSFX("countdown")
                    SwingUtilities.invokeLater(lambda: [self.view.getPrgTimer().setBackground(self.style.goldenTainoi), self.view.getLblTimer().setForeground(self.style.white)])
                    
                    # TODO: Send wordlist to server using: sendUserWordList method
                    # TODO: Get the winner of the round using: getRoundWinner()
                    # TODO: Check if there is an overall winner, if there isn't return value will be undecided
                    # TODO: Get the letterSet for the next round using the method: getNextRoundLetterSet and start next round
        except Exception as e:
            print(e)

    class InputListener(ActionListener):
        def actionPerformed(self, e):
            self.view.setErrorMessage("")
            input = self.view.getTxtWordInput().getText().strip()
            if not input.contains(" ") and len(input) >= 4:
                if not self.validateInput(input):
                    self.view.setErrorMessage("Input must only contain LETTERS!")
                    self.view.getTxtWordInput().setText("")
                    self.playSFX("badInput")
                else:
                    self.view.addUserInput(self.model.getUsername(), input)
                    self.view.updateTxaHeight()
                    self.model.getWordSet().add(input)
                    self.view.getTxtWordInput().setText("")
                    self.playSFX("goodInput")
            elif len(input) < 4:
                self.view.setErrorMessage("Input must be at least 4 CHARACTERS!")
                self.view.getTxtWordInput().setText("")
                self.playSFX("badInput")
            else:
                self.view.setErrorMessage("Input must only be a WORD!")
                self.view.getTxtWordInput().setText("")
                self.playSFX("badInput")

    class MusicListener(ActionListener):
        def actionPerformed(self, e):
            SwingUtilities.invokeLater(lambda: [self.musicOn = False, self.view.setBtnMusicIcon(self.style.iconMusicOff), self.parent.getMusicClip().getMicrosecondPosition(), self.parent.getMusicClip().stop()] if self.musicOn else [self.musicOn = True, self.view.setBtnMusicIcon(self.style.iconMusicOn), self.parent.getMusicClip().getMicrosecondPosition(), self.parent.getMusicClip().start()])

    class SoundListener(ActionListener):
        def actionPerformed(self, e):
            SwingUtilities.invokeLater(lambda: [self.sfxOn = False, self.view.setBtnSoundIcon(self.style.iconSoundOff), self.audioSoundStream.reset()] if self.sfxOn else [self.sfxOn = True, self.view.setBtnSoundIcon(self.style.iconSoundOn)])

    def validateInput(self, input):
        for i in range(len(input)):
            if not input[i].isalpha() or input[i].isspace():
                return False
        return True

    def playSFX(self, type):
        if self.sfxOn:
            try:
                self.audioSoundStream = AudioSystem.getAudioInputStream(File(self.badInput))
                self.sfxClip = AudioSystem.getClip()
                self.sfxClip.open(self.audioSoundStream)
                self.sfxClip.stop()
                if type == "badInput":
                    self.sfxClip.stop()
                    self.audioSoundStream = AudioSystem.getAudioInputStream(File(self.badInput))
                    self.sfxClip = AudioSystem.getClip()
                    self.sfxClip.open(self.audioSoundStream)
                    self.sfxClip.start()
                elif type == "goodInput":
                    self.sfxClip.stop()
                    self.audioSoundStream = AudioSystem.getAudioInputStream(File(self.goodInput))
                    self.sfxClip = AudioSystem.getClip()
                    self.sfxClip.open(self.audioSoundStream)
                    self.sfxClip.start()
                elif type == "countdown":
                    self.sfxClip.stop()
                    self.audioSoundStream = AudioSystem.getAudioInputStream(File(self.countdown))
                    self.sfxClip = AudioSystem.getClip()
                    self.sfxClip.open(self.audioSoundStream)
                    self.sfxClip.start()
                elif type == "roundOver":
                    self.sfxClip.stop()
                    self.audioSoundStream = AudioSystem.getAudioInputStream(File(self.roundOver))
                    self.sfxClip = AudioSystem.getClip()
                    self.sfxClip.open(self.audioSoundStream)
                    self.sfxClip.start()
                elif type == "winner":
                    self.sfxClip.stop()
                    self.audioSoundStream = AudioSystem.getAudioInputStream(File(self.win))
                    self.sfxClip = AudioSystem.getClip()
                    self.sfxClip.open(self.audioSoundStream)
                    self.sfxClip.start()
                elif type == "lose":
                    self.sfxClip.stop()
                    self.audioSoundStream = AudioSystem.getAudioInputStream(File(self.lose))
                    self.sfxClip = AudioSystem.getClip()
                    self.sfxClip.open(self.audioSoundStream)
                    self.sfxClip.start()
            except Exception as e:
                print(e)

    def getCurrentRoundWordList(self):
        userWordMap = {}
        wordList = list(self.model.getWordSet())
        username = self.model.getUsername()
        userWordMap[username] = wordList
        return userWordMap

    def populateLetterSet(self, vowelSet, consonantSet):
        letterSet = []
        letterSet.append(Arrays.toString(vowelSet))
        letterSet.append(Arrays.toString(consonantSet))
        backgroundColor = None
        random.shuffle(letterSet)
        for letter in letterSet:
            backgroundColor = self.style.deepSkyBlue if re.match("[AEIOU]", letter) else self.style.goldenTainoi
            self.view.addLetterToLetterSet(letter, backgroundColor)

'''