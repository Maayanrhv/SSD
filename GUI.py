from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QLabel, QVBoxLayout
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
import RTdata as rt
import Trials
from DataHandler import DistanceErrorFile


global start  # determines whether the application (gui) is currently running or not
start = True  # set the app status to be - running


# Return whether the app is currently running
def appOngoing():
    return start


# The app's window that appears on screen
class Window(QWidget):
    # window initializer function
    def __init__(self):
        super().__init__()
        self.title = "SSD App"
        self.win = QDialog()
        self.init_window()

    def init_window(self):
        self.win.setWindowTitle(self.title)
        self.win.setWindowIcon(QtGui.QIcon('icon.png'))
        # self.setGeometry(self.left, self.top, self.width, self.height)

        self.win.setFixedWidth(700)

        # Show icon
        pic = QLabel(self.win)
        pixmap = QtGui.QPixmap('icon.png')
        smaller_pixmap = pixmap.scaled(83, 85, Qt.KeepAspectRatio, Qt.FastTransformation)
        pic.setPixmap(smaller_pixmap)
        pic.move(50, 400)
        pic.show()

        # Start Trial Button
        self.startTrialB = QPushButton(self.win)
        self.startTrialB.setText("Start Trial")
        self.startTrialB.move(50, 20)
        self.startTrialB.clicked.connect(self.start_trial_clicked)

        # End Trial Button
        self.endTrialB = QPushButton(self.win)
        self.endTrialB.setText("End Trial")
        self.endTrialB.move(50, 50)
        self.endTrialB.clicked.connect(self.end_trial_clicked)

        # Mute Button
        self.muteB = QPushButton(self.win)
        self.muteB.setText("Mute")
        self.muteB.move(50, 80)
        self.muteB.clicked.connect(self.mute_clicked)

        # UnMute Button
        self.unmuteB = QPushButton(self.win)
        self.unmuteB.setText("Combined")
        self.unmuteB.move(50, 110)
        self.unmuteB.clicked.connect(self.unmute_clicked)

        # Pitch Button
        self.pitchB = QPushButton(self.win)
        self.pitchB.setText("Roll")
        self.pitchB.move(50, 140)
        self.pitchB.clicked.connect(self.roll_clicked)
        
        # Roll Button
        self.rollB = QPushButton(self.win)
        self.rollB.setText("Yaw")
        self.rollB.move(50, 170)
        self.rollB.clicked.connect(self.yaw_clicked)

        # Exit Button
        self.exitB = QPushButton(self.win)
        self.exitB.setText("Exit")
        self.exitB.move(50, 375)
        self.exitB.clicked.connect(self.exit_clicked)

        # Error 1 - Diagonal distance fill-in label
        self.diagonal_dist_label = QLabel(self.win)
        self.diagonal_dist_label.move(50, 220)
        self.diagonal_dist_label.setText("Diagonal Distance:")

        # Error 1 - Diagonal distance fill-in double value
        self.diagonal_dist_err_input = QLineEdit(self.win)
        self.diagonal_dist_err_input.setValidator(QtGui.QDoubleValidator(0.99, 99.99, 2))
        self.diagonal_dist_err_input.move(50, 235)
        self.diagonal_dist_err_input.setMaximumWidth(40)
        # self.remain_dist_err_input.setText("Distance of Diagonal Line")

        # Error 2 - Horizontal distance fill-in label
        self.horizontal_dist_label = QLabel(self.win)
        self.horizontal_dist_label.move(50, 260)
        self.horizontal_dist_label.setText("Horizontal Distance:")

        # Error 2 - Horizontal distance fill-in double value
        self.horizontal_dist_err_input = QLineEdit(self.win)
        self.horizontal_dist_err_input.setValidator(QtGui.QDoubleValidator(0.99, 99.99, 2))
        self.horizontal_dist_err_input.move(50, 275)
        self.horizontal_dist_err_input.setMaximumWidth(40)
        # self.stray_dist_err_input.setText("Horizontal Distance From Original Line")

        # Error 3 - Vertical distance fill-in label
        self.vertical_dist_label = QLabel(self.win)
        self.vertical_dist_label.move(50, 300)
        self.vertical_dist_label.setText("Vertical Distance:")

        # Error 3 - Vertical distance fill-in double value
        self.vertical_dist_err_input = QLineEdit(self.win)
        self.vertical_dist_err_input.setValidator(QtGui.QDoubleValidator(0.99, 99.99, 2))
        self.vertical_dist_err_input.move(50, 315)
        self.vertical_dist_err_input.setMaximumWidth(40)
        # self.stray_dist_err_input.setText("Vertical Distance From Original Line")

        # Error 1 backwards - Diagonal distance fill-in label
        self.back_diagonal_dist_label = QLabel(self.win)
        self.back_diagonal_dist_label.move(160, 220)
        self.back_diagonal_dist_label.setText("Backwards Diagonal Distance:")

        # Error 1 backwards - Diagonal distance fill-in double value
        self.back_diagonal_dist_err_input = QLineEdit(self.win)
        self.back_diagonal_dist_err_input.setValidator(QtGui.QDoubleValidator(0.99, 99.99, 2))
        self.back_diagonal_dist_err_input.move(160, 235)
        self.back_diagonal_dist_err_input.setMaximumWidth(40)
        # self.remain_dist_err_input.setText("Backwards Distance of Diagonal Line")

        # Error 2 backwards - Horizontal distance fill-in label
        self.back_horizontal_dist_label = QLabel(self.win)
        self.back_horizontal_dist_label.move(160, 260)
        self.back_horizontal_dist_label.setText("Backwards Horizontal Distance:")

        # Error 2 backwards - Horizontal distance fill-in double value
        self.back_horizontal_dist_err_input = QLineEdit(self.win)
        self.back_horizontal_dist_err_input.setValidator(QtGui.QDoubleValidator(0.99, 99.99, 2))
        self.back_horizontal_dist_err_input.move(160, 275)
        self.back_horizontal_dist_err_input.setMaximumWidth(40)
        # self.stray_dist_err_input.setText("Backwards Horizontal Distance From Original Line")

        # Error 3 backwards - Vertical distance fill-in label
        self.back_vertical_dist_label = QLabel(self.win)
        self.back_vertical_dist_label.move(160, 300)
        self.back_vertical_dist_label.setText("Backwards Vertical Distance:")

        # Error 3 backwards - Vertical distance fill-in double value
        self.back_vertical_dist_err_input = QLineEdit(self.win)
        self.back_vertical_dist_err_input.setValidator(QtGui.QDoubleValidator(0.99, 99.99, 2))
        self.back_vertical_dist_err_input.move(160, 315)
        self.back_vertical_dist_err_input.setMaximumWidth(40)
        # self.stray_dist_err_input.setText("Backwards Vertical Distance From Original Line")

        # Distance error Button
        self.dist_err_B = QPushButton(self.win)
        self.dist_err_B.setText("Insert Errors")
        self.dist_err_B.move(50, 340)
        self.dist_err_B.clicked.connect(self.insert_error_clicked)

        # Trials List Status
        self.trialListStatus = QPlainTextEdit(self.win)
        self.trialListStatus.move(320, 20)
        self.trialListStatus.setFixedHeight(400)
        self.trialListStatus.setFixedWidth(300)
        self.trialListStatus.setReadOnly(True)

        self.win.show()
        self.showTrials()

    # Starting trial manually (by click)
    def start_trial_clicked(self):
        Trials.start_trial_by_click()
        self.showTrials()

    # Ending trial manually (by click)
    def end_trial_clicked(self):
        Trials.set_end_trial(True)

    # Save the distances errors values of a certain trial
    def insert_error_clicked(self):
        DistanceErrorFile.set_distance_errors(self.diagonal_dist_err_input.text(),
                                              self.horizontal_dist_err_input.text(),
                                              self.vertical_dist_err_input.text(),
                                              self.back_diagonal_dist_err_input.text(),
                                              self.back_horizontal_dist_err_input.text(),
                                              self.back_vertical_dist_err_input.text())
        self.diagonal_dist_err_input.clear()
        self.horizontal_dist_err_input.clear()
        self.vertical_dist_err_input.clear()
        self.back_diagonal_dist_err_input.clear()
        self.back_horizontal_dist_err_input.clear()
        self.back_vertical_dist_err_input.clear()

    # Exiting the app and end the program
    def exit_clicked(self):
        print("Stop")
        global start
        start = False
        print("Exit Clicked")

    # Mute all sound
    def mute_clicked(self):
        rt.set_sound_status(rt.Sound.NoSound)
        print("Mute Clicked")

    # Play all sounds
    def unmute_clicked(self):
        rt.set_sound_status(rt.Sound.Combined)
        print("UnMute Clicked")

    # Play roll sound only
    def roll_clicked(self):
        rt.set_sound_status(rt.Sound.RollOnly)
        print("Roll Clicked")

    # Play yaw sound only
    def yaw_clicked(self):
        rt.set_sound_status(rt.Sound.YawOnly)
        print("Yaw Clicked")

    # Display Trials On Screen
    def showTrials(self):
        self.trialListStatus.clear()
        Trials.update_rows()  # create list of all trials' titles and statuses
        # display each trial's string (that represents its details)
        for index in Trials.trialsIndexes:
            # get a trial's string (with: serial num., name, status)
            trial_name = Trials.trials_displayed_list[index]
            # set trial's color according to its status
            color = QtGui.QColor(Trials.trialStatusColor[Trials.trialsStatVec[index]])
            color_format = self.trialListStatus.currentCharFormat()
            color_format.setForeground(color)
            self.trialListStatus.setCurrentCharFormat(color_format)
            # split trials by enter to display a vertical list
            self.trialListStatus.insertPlainText(trial_name + "\n")
        print("Rows Updated")


App = QApplication(sys.argv)
win = Window()
# sys.exit(App.exec())
