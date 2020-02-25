"""
Projet Slideways, partie 3
Auteur : Matteo Rossi
N° Matricule : 499342
Date : 23/02/2020

Slideways qui est un mélange entre le jeu OXO et le jeu puissance 4

Création d'une interface graphique pour le jeu grâce à PyQt5

Possibilité de jouer contre une IA ou contre un autre Joueur
"""
import os
import random
import sys
from copy import deepcopy

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

from dialog import *
from gui import Ui_slideways


class Game(QMainWindow, Ui_slideways):

    def __init__(self, parent=None):
        super().__init__(parent)
        #dictionaire pour les coordonées du plateau en fonction du str
        self.posplateau = {'A4': (0, 0), 'A3': (0, 1), 'A2': (0, 2), 'A1': (0, 3),
        'B4': (1, 0), 'B3': (1, 1), 'B2': (1, 2), 'B1': (1, 3),
        'C4': (2, 0), 'C3': (2, 1), 'C2': (2, 2), 'C1': (2, 3),
        'D4': (3, 0), 'D3': (3, 1), 'D2': (3, 2), 'D1': (3, 3)}
        #dictionnaire pour connaitre la ligne à décaler en fonction du str
        self.dico_decalage = {'1-' : 3, '1+' : 3, '2-' : 2, '2+' : 2,
        '3-' : 1, '3+' : 1, '4-' : 0, '4+' : 0}

        self.human_playing = True #permet de savoir si un humain joue
        self.IA_playing = False #permet de savoir si une IA joue

        self.setupUi(self) #lance la fenêtre importé depuis le fichier gui.py

        self.timer = QTimer()

        self.setWindowFlags(Qt.WindowCloseButtonHint)


        self.allButtons = self.frame.findChildren(QPushButton) #liste de tout les bouttons de la fenêtre
        self.defaultPalette = QApplication.palette()

        #connect tous les bouttons à un fonctions qu'ils vont éxécuter lors du clique
        #menu
        self.actionNew_Game.triggered.connect(self.new_game)
        self.action_Exit.triggered.connect(self.close)
        self.action_Player.triggered.connect(self.choix_human)
        self.action_IA.triggered.connect(self.choix_IA)
        self.action_IAvsIA.triggered.connect(self.choix_IAvsIA)

        #bouttons du tableau
        self.A1.clicked.connect(self.button_clickedA1)
        self.A2.clicked.connect(self.button_clickedA2)
        self.A3.clicked.connect(self.button_clickedA3)
        self.A4.clicked.connect(self.button_clickedA4)
        self.B1.clicked.connect(self.button_clickedB1)
        self.B2.clicked.connect(self.button_clickedB2)
        self.B3.clicked.connect(self.button_clickedB3)
        self.B4.clicked.connect(self.button_clickedB4)
        self.C1.clicked.connect(self.button_clickedC1)
        self.C2.clicked.connect(self.button_clickedC2)
        self.C3.clicked.connect(self.button_clickedC3)
        self.C4.clicked.connect(self.button_clickedC4)
        self.D1.clicked.connect(self.button_clickedD1)
        self.D2.clicked.connect(self.button_clickedD2)
        self.D3.clicked.connect(self.button_clickedD3)
        self.D4.clicked.connect(self.button_clickedD4)

        #bouttons pour le décalage
        self.plusligne1.clicked.connect(self.decalageplus1)
        self.plusligne2.clicked.connect(self.decalageplus2)
        self.plusligne3.clicked.connect(self.decalageplus3)
        self.plusligne4.clicked.connect(self.decalageplus4)
        self.moinsligne1.clicked.connect(self.decalagemoins1)
        self.moinsligne2.clicked.connect(self.decalagemoins2)
        self.moinsligne3.clicked.connect(self.decalagemoins3)
        self.moinsligne4.clicked.connect(self.decalagemoins4)

        self.slider.valueChanged[int].connect(self.slider_timer)
        #la valeur du slider, qui détermine le temps que prend une IA a joué

        self.setFocus() 
        self.new_game() 


    def new_game(self):
        """
        Fonctions qui remet tout à zéro pour relancer un partie
        """
        self.frame.setEnabled(True)#permet de toucher au bouttons
        self.plateau = self.nouveau_plateau()
        self.joueur = 1
        self.gagnant = set()
        self.dernier_coup = None
        self.decalage = [0, 0, 0, 0]
        self.coup = None
        self.timer_IA = 100
        #variables à modifier ou le décalage
        self.xligne1 = 400
        self.xligne2 = 400
        self.xligne3 = 400
        self.xligne4 = 400
        #remet tous les bouttons à leur place
        self.A4.move(self.xligne1, 50)
        self.B4.move(self.xligne1+100, 50)
        self.C4.move(self.xligne1+200, 50)
        self.D4.move(self.xligne1+300, 50)
        self.A3.move(self.xligne2, 150)
        self.B3.move(self.xligne2+100, 150)
        self.C3.move(self.xligne2+200, 150)
        self.D3.move(self.xligne2+300, 150)
        self.A2.move(self.xligne3, 250)
        self.B2.move(self.xligne3+100, 250)
        self.C2.move(self.xligne3+200, 250)
        self.D2.move(self.xligne3+300, 250)
        self.A1.move(self.xligne4, 350)
        self.B1.move(self.xligne4+100, 350)
        self.C1.move(self.xligne4+200, 350)
        self.D1.move(self.xligne4+300, 350)

        #remet la couleur des bouttons en gris
        for button in self.allButtons:
            button.setStyleSheet('QPushButton {background-color: #D7D7D7;}')

    def choix_human(self):
        """
        Fonction si deux humain joue l'un contre l'autre
        """
        self.human_playing = True
        self.IA_playing = False
        self.text_button.setText("Current Game : Human vs Human")
        self.new_game()

    def choix_IA(self):
        """
        Fonction si un humain joue contre une IA
        """
        self.human_playing = True
        self.IA_playing = True
        self.text_button.setText("Current Game : Human vs IA")
        self.new_game()

    def choix_IAvsIA(self):
        """
        Fonction si deux IA joue l'une contre l'autre
        """
        self.text_button.setText("Current Game : IA vs IA")
        self.human_playing = False
        self.new_game()
        self.frame.setEnabled(False)
        self.timer.singleShot(int(self.timer_IA), self.AI)
        #lance un coup de l'IA avec un certain delais

    def slider_timer(self, value):
        """
        renvoie la valeur du slider
        """
        self.timer_IA = (value*15)+100
        self.label_ms.setText(str(self.timer_IA)+"ms")



    def nouveau_plateau(self):
        """
        Crée le plateau de jeu
        :return: liste de liste de dimension 4x4 contenant des 0
        """
        plateau = []
        for i in range(4):
            plateau.append([0]*4)
        return plateau


    def gagne(self ,plateau, decalage):
        """
        Vérifie si le joueur gagne la partie ou non
        :param plateau: liste de liste, 0 pour vide, 1 ou 2 pour joueur
        :param decalage: liste d'entiers, représentent le décalage des lignes du plateau
        :return ensemble 0 si pas de gagnant, sinon le numéro du joueur gagnant, ou des gagnants si match nul
        """
        factice = []
        #créer une matrice 4x10 avec le plateau en décalé
        for i in range(4):
            l= []
            for c in range(3 + decalage[i]):
                l.append(0)
            for j in range(4):
                l.append(plateau[i][j])
            for c in range(3 - decalage[i]):
                l.append(0)
            factice.append(l)

        res = []

        #lignes avec le plateau normal
        for i in range(4):
            res.append(set(plateau[i]))
        #colonnes avec la plateau factice
        for i in range(10):
            res.append(set( [factice[j][i] for j in range(4)] ))

        #diagonales avec le tableau factice
        for i in range(6):
            res.append(set( [factice[j][i+j] for j in range(4)] ))
            res.append(set( [factice[3-j][i+j] for j in range(4)] ))

        #vérifie si il y a un gagnant
        gagnants = set()
        for c in res:
            if c != {0} and len(c) == 1:
                gagnant = list(c)[0]
                gagnants.add(gagnant)

        return gagnants


    def end_game(self, gagnant):
        """Lance une fenêtre de victoire"""
        self.frame.setEnabled(False)
        if len(gagnant) == 2:
            #si il ya une égalité
            Dialog(self, gagnant).show()
        else:
            gagnant = list(gagnant)[0]
            Dialog(self, gagnant).show()

    
    def button_clickedA1(self):
        """
        Lorsqu'un boutton est cliqué, change sa couleur en fonction du joueur
        """
        coup = self.dernier_coup
        self.dernier_coup = self.coup_joueur("A1")

        if self.dernier_coup != coup:
            #rentre dans la conditions si le coup est jouable 
            if self.joueur == 1:
                self.A1.setStyleSheet('QPushButton {background-color: #FFEB00; color: #FFEB00;}')
            elif self.joueur == 2:
                self.A1.setStyleSheet('QPushButton {background-color: #FC0000; color: #FC0000;}')

            gagnant = self.gagne(self.plateau, self.decalage)
            self.joueur = (self.joueur % 2) + 1
            if len(gagnant) != 0:
                self.end_game(gagnant)
            
            self.statusBar().showMessage("Joueur " + str(self.joueur))

            if self.IA_playing:
                #lance l'IA si c'est une partie avec IA
                self.frame.setEnabled(False)
                self.timer.singleShot(int(self.timer_IA), self.AI)
                

    
    def button_clickedA2(self):
        coup = self.dernier_coup
        self.dernier_coup = self.coup_joueur("A2")
        if self.dernier_coup != coup:
            if self.joueur == 1:
                self.A2.setStyleSheet('QPushButton {background-color: #FFEB00; color: #FFEB00;}')
            elif self.joueur == 2:
                self.A2.setStyleSheet('QPushButton {background-color: #FC0000; color: #FC0000;}')
            gagnant = self.gagne(self.plateau, self.decalage)
            self.joueur = (self.joueur % 2) + 1
            if len(gagnant) != 0:
                self.end_game(gagnant)

            self.statusBar().showMessage("Joueur " + str(self.joueur))

            if self.IA_playing:
                self.frame.setEnabled(False)
                self.timer.singleShot(int(self.timer_IA), self.AI)


    def button_clickedA3(self):
        coup = self.dernier_coup
        self.dernier_coup = self.coup_joueur("A3")
        if self.dernier_coup != coup:
            if self.joueur == 1:
                self.A3.setStyleSheet('QPushButton {background-color: #FFEB00; color: #FFEB00;}')
            elif self.joueur == 2:
                self.A3.setStyleSheet('QPushButton {background-color: #FC0000; color: #FC0000;}')
            gagnant = self.gagne(self.plateau, self.decalage)
            self.joueur = (self.joueur % 2) + 1
            if len(gagnant) != 0:
                self.end_game(gagnant)

            self.statusBar().showMessage("Joueur " + str(self.joueur))

            if self.IA_playing:
                self.frame.setEnabled(False)
                self.timer.singleShot(int(self.timer_IA), self.AI)

    def button_clickedA4(self):
        coup = self.dernier_coup
        self.dernier_coup = self.coup_joueur("A4")
        if self.dernier_coup != coup:
            if self.joueur == 1:
                self.A4.setStyleSheet('QPushButton {background-color: #FFEB00; color: #FFEB00;}')
            elif self.joueur == 2:
                self.A4.setStyleSheet('QPushButton {background-color: #FC0000; color: #FC0000;}')
            gagnant = self.gagne(self.plateau, self.decalage)
            self.joueur = (self.joueur % 2) + 1
            if len(gagnant) != 0:
                self.end_game(gagnant)

            self.statusBar().showMessage("Joueur " + str(self.joueur))

            if self.IA_playing:
                self.frame.setEnabled(False)
                self.timer.singleShot(int(self.timer_IA), self.AI)


    def button_clickedB1(self):
        coup = self.dernier_coup
        self.dernier_coup = self.coup_joueur("B1")
        if self.dernier_coup != coup:
            if self.joueur == 1:
                self.B1.setStyleSheet('QPushButton {background-color: #FFEB00; color: #FFEB00;}')
            elif self.joueur == 2:
                self.B1.setStyleSheet('QPushButton {background-color: #FC0000; color: #FC0000;}')
            gagnant = self.gagne(self.plateau, self.decalage)
            self.joueur = (self.joueur % 2) + 1
            if len(gagnant) != 0:
                self.end_game(gagnant)

            self.statusBar().showMessage("Joueur " + str(self.joueur))

            if self.IA_playing:
                self.frame.setEnabled(False)
                self.timer.singleShot(int(self.timer_IA), self.AI)


    def button_clickedB2(self):
        coup = self.dernier_coup
        self.dernier_coup = self.coup_joueur("B2")
        if self.dernier_coup != coup:
            if self.joueur == 1:
                self.B2.setStyleSheet('QPushButton {background-color: #FFEB00; color: #FFEB00;}')
            elif self.joueur == 2:
                self.B2.setStyleSheet('QPushButton {background-color: #FC0000; color: #FC0000;}')
            gagnant = self.gagne(self.plateau, self.decalage)
            self.joueur = (self.joueur % 2) + 1
            if len(gagnant) != 0:
                self.end_game(gagnant)

            self.statusBar().showMessage("Joueur " + str(self.joueur))

            if self.IA_playing:
                self.frame.setEnabled(False)
                self.timer.singleShot(int(self.timer_IA), self.AI)


    def button_clickedB3(self):
        coup = self.dernier_coup
        self.dernier_coup = self.coup_joueur("B3")
        if self.dernier_coup != coup:
            if self.joueur == 1:
                self.B3.setStyleSheet('QPushButton {background-color: #FFEB00; color: #FFEB00;}')
            elif self.joueur == 2:
                self.B3.setStyleSheet('QPushButton {background-color: #FC0000; color: #FC0000;}')
            gagnant = self.gagne(self.plateau, self.decalage)
            self.joueur = (self.joueur % 2) + 1
            if len(gagnant) != 0:
                self.end_game(gagnant)

            self.statusBar().showMessage("Joueur " + str(self.joueur))

            if self.IA_playing:
                self.frame.setEnabled(False)
                self.timer.singleShot(int(self.timer_IA), self.AI)

    def button_clickedB4(self):
        coup = self.dernier_coup
        self.dernier_coup = self.coup_joueur("B4")
        if self.dernier_coup != coup:
            if self.joueur == 1:
                self.B4.setStyleSheet('QPushButton {background-color: #FFEB00; color: #FFEB00;}')
            elif self.joueur == 2:
                self.B4.setStyleSheet('QPushButton {background-color: #FC0000; color: #FC0000;}')
            gagnant = self.gagne(self.plateau, self.decalage)
            self.joueur = (self.joueur % 2) + 1
            if len(gagnant) != 0:
                self.end_game(gagnant)

            self.statusBar().showMessage("Joueur " + str(self.joueur))

            if self.IA_playing:
                self.frame.setEnabled(False)
                self.timer.singleShot(int(self.timer_IA), self.AI)

    def button_clickedC1(self):
        coup = self.dernier_coup
        self.dernier_coup = self.coup_joueur("C1")
        if self.dernier_coup != coup:
            if self.joueur == 1:
                self.C1.setStyleSheet('QPushButton {background-color: #FFEB00; color: #FFEB00;}')
            elif self.joueur == 2:
                self.C1.setStyleSheet('QPushButton {background-color: #FC0000; color: #FC0000;}')
            gagnant = self.gagne(self.plateau, self.decalage)
            self.joueur = (self.joueur % 2) + 1
            if len(gagnant) != 0:
                self.end_game(gagnant)

            self.statusBar().showMessage("Joueur " + str(self.joueur))

            if self.IA_playing:
                self.frame.setEnabled(False)
                self.timer.singleShot(int(self.timer_IA), self.AI)
                

    
    def button_clickedC2(self):
        coup = self.dernier_coup
        self.dernier_coup = self.coup_joueur("C2")
        if self.dernier_coup != coup:
            if self.joueur == 1:
                self.C2.setStyleSheet('QPushButton {background-color: #FFEB00; color: #FFEB00;}')
            elif self.joueur == 2:
                self.C2.setStyleSheet('QPushButton {background-color: #FC0000; color: #FC0000;}')
            gagnant = self.gagne(self.plateau, self.decalage)
            self.joueur = (self.joueur % 2) + 1
            if len(gagnant) != 0:
                self.end_game(gagnant)

            self.statusBar().showMessage("Joueur " + str(self.joueur))

            if self.IA_playing:
                self.frame.setEnabled(False)
                self.timer.singleShot(int(self.timer_IA), self.AI)


    def button_clickedC3(self):
        coup = self.dernier_coup
        self.dernier_coup = self.coup_joueur("C3")
        if self.dernier_coup != coup:
            if self.joueur == 1:
                self.C3.setStyleSheet('QPushButton {background-color: #FFEB00; color: #FFEB00;}')
            elif self.joueur == 2:
                self.C3.setStyleSheet('QPushButton {background-color: #FC0000; color: #FC0000;}')
            gagnant = self.gagne(self.plateau, self.decalage)
            self.joueur = (self.joueur % 2) + 1
            if len(gagnant) != 0:
                self.end_game(gagnant)

            self.statusBar().showMessage("Joueur " + str(self.joueur))

            if self.IA_playing:
                self.frame.setEnabled(False)
                self.timer.singleShot(int(self.timer_IA), self.AI)

    def button_clickedC4(self):
        coup = self.dernier_coup
        self.dernier_coup = self.coup_joueur("C4")
        if self.dernier_coup != coup:
            if self.joueur == 1:
                self.C4.setStyleSheet('QPushButton {background-color: #FFEB00; color: #FFEB00;}')
            elif self.joueur == 2:
                self.C4.setStyleSheet('QPushButton {background-color: #FC0000; color: #FC0000;}')
            gagnant = self.gagne(self.plateau, self.decalage)
            self.joueur = (self.joueur % 2) + 1
            if len(gagnant) != 0:
                self.end_game(gagnant)

            self.statusBar().showMessage("Joueur " + str(self.joueur))

            if self.IA_playing:
                self.frame.setEnabled(False)
                self.timer.singleShot(int(self.timer_IA), self.AI)

    def button_clickedD1(self):
        coup = self.dernier_coup
        self.dernier_coup = self.coup_joueur("D1")
        if self.dernier_coup != coup:
            if self.joueur == 1:
                self.D1.setStyleSheet('QPushButton {background-color: #FFEB00; color: #FFEB00;}')
            elif self.joueur == 2:
                self.D1.setStyleSheet('QPushButton {background-color: #FC0000; color: #FC0000;}')
            gagnant = self.gagne(self.plateau, self.decalage)
            self.joueur = (self.joueur % 2) + 1
            if len(gagnant) != 0:
                self.end_game(gagnant)

            self.statusBar().showMessage("Joueur " + str(self.joueur))

            if self.IA_playing:
                self.frame.setEnabled(False)
                self.timer.singleShot(int(self.timer_IA), self.AI)
                    
    def button_clickedD2(self):
        coup = self.dernier_coup
        self.dernier_coup = self.coup_joueur("D2")
        if self.dernier_coup != coup:
            if self.joueur == 1:
                self.D2.setStyleSheet('QPushButton {background-color: #FFEB00; color: #FFEB00;}')
            elif self.joueur == 2:
                self.D2.setStyleSheet('QPushButton {background-color: #FC0000; color: #FC0000;}')
            gagnant = self.gagne(self.plateau, self.decalage)
            self.joueur = (self.joueur % 2) + 1
            if len(gagnant) != 0:
                self.end_game(gagnant)

            self.statusBar().showMessage("Joueur " + str(self.joueur))

            if self.IA_playing:
                self.frame.setEnabled(False)
                self.timer.singleShot(int(self.timer_IA), self.AI)


    def button_clickedD3(self):
        coup = self.dernier_coup
        self.dernier_coup = self.coup_joueur("D3")
        if self.dernier_coup != coup:
            if self.joueur == 1:
                self.D3.setStyleSheet('QPushButton {background-color: #FFEB00; color: #FFEB00;}')
            elif self.joueur == 2:
                self.D3.setStyleSheet('QPushButton {background-color: #FC0000; color: #FC0000;}')
            gagnant = self.gagne(self.plateau, self.decalage)
            self.joueur = (self.joueur % 2) + 1
            if len(gagnant) != 0:
                self.end_game(gagnant)

            self.statusBar().showMessage("Joueur " + str(self.joueur))

            if self.IA_playing:
                self.frame.setEnabled(False)
                self.timer.singleShot(int(self.timer_IA), self.AI)


    def button_clickedD4(self):
        coup = self.dernier_coup
        self.dernier_coup = self.coup_joueur("D4")
        if self.dernier_coup != coup:
            if self.joueur == 1:
                self.D4.setStyleSheet('QPushButton {background-color: #FFEB00; color: #FFEB00;}')
            elif self.joueur == 2:
                self.D4.setStyleSheet('QPushButton {background-color: #FC0000; color: #FC0000;}')
            gagnant = self.gagne(self.plateau, self.decalage)
            self.joueur = (self.joueur % 2) + 1
            if len(gagnant) != 0:
                self.end_game(gagnant)

            self.statusBar().showMessage("Joueur " + str(self.joueur))

            if self.IA_playing:
                self.frame.setEnabled(False)
                self.timer.singleShot(int(self.timer_IA), self.AI)

    def ligne1plus(self):
        """décale la ligne voulue"""
        self.xligne1 += 100
        self.A4.setGeometry(QRect(self.xligne1, 50, 100, 100))
        self.B4.setGeometry(QRect(self.xligne1+100, 50, 100, 100))
        self.C4.setGeometry(QRect(self.xligne1+200, 50, 100, 100))
        self.D4.setGeometry(QRect(self.xligne1+300, 50, 100, 100))

    def decalageplus1(self):
        """lorsque le boutton pour le décalage est cliqué"""
        coup = self.dernier_coup
        dernier_decalage = self.decalage[0]#retient le dernier décalage
        self.dernier_coup = self.coup_joueur("4+")
        if self.dernier_coup != coup or self.dernier_coup == "4-" and dernier_decalage != 3:
            self.ligne1plus()
            gagnant = self.gagne(self.plateau, self.decalage)
            self.joueur = (self.joueur % 2) + 1
            if len(gagnant) != 0:
                self.end_game(gagnant)

            self.statusBar().showMessage("Joueur " + str(self.joueur))

            if self.IA_playing:
                #si l'IA joue
                self.frame.setEnabled(False)
                self.timer.singleShot(int(self.timer_IA), self.AI)

    def ligne1moins(self):
        self.xligne1 -= 100
        self.A4.move(self.xligne1, 50)
        self.B4.move(self.xligne1+100, 50)
        self.C4.move(self.xligne1+200, 50)
        self.D4.move(self.xligne1+300, 50)

    def decalagemoins1(self):
        coup = self.dernier_coup
        dernier_decalage = self.decalage[0]
        self.dernier_coup = self.coup_joueur("4-")
        if self.dernier_coup != coup or self.dernier_coup == "4+" and dernier_decalage != -3:
            self.ligne1moins()
            gagnant = self.gagne(self.plateau, self.decalage)
            self.joueur = (self.joueur % 2) + 1
            if len(gagnant) != 0:
                self.end_game(gagnant)

            self.statusBar().showMessage("Joueur " + str(self.joueur))

            if self.IA_playing:
                self.frame.setEnabled(False)
                self.timer.singleShot(int(self.timer_IA), self.AI)

    def ligne2plus(self):
        self.xligne2 = self.xligne2 + 100
        self.A3.setGeometry(QRect(self.xligne2, 150, 100, 100))
        self.B3.setGeometry(QRect(self.xligne2+100, 150, 100, 100))
        self.C3.setGeometry(QRect(self.xligne2+200, 150, 100, 100))
        self.D3.setGeometry(QRect(self.xligne2+300, 150, 100, 100))

    def decalageplus2(self):
        coup = self.dernier_coup
        dernier_decalage = self.decalage[1]
        self.dernier_coup = self.coup_joueur("3+")
        if self.dernier_coup != coup or self.dernier_coup == "3-" and dernier_decalage != 3:
            self.ligne2plus()
            gagnant = self.gagne(self.plateau, self.decalage)
            self.joueur = (self.joueur % 2) + 1
            if len(gagnant) != 0:
                self.end_game(gagnant)

            self.statusBar().showMessage("Joueur " + str(self.joueur))

            if self.IA_playing:
                self.frame.setEnabled(False)
                self.timer.singleShot(int(self.timer_IA), self.AI)

    def ligne2moins(self):
        self.xligne2 = self.xligne2 - 100
        self.A3.setGeometry(QRect(self.xligne2, 150, 100, 100))
        self.B3.setGeometry(QRect(self.xligne2+100, 150, 100, 100))
        self.C3.setGeometry(QRect(self.xligne2+200, 150, 100, 100))
        self.D3.setGeometry(QRect(self.xligne2+300, 150, 100, 100))


    def decalagemoins2(self):
        coup = self.dernier_coup
        dernier_decalage = self.decalage[1]
        self.dernier_coup = self.coup_joueur("3-")
        if self.dernier_coup != coup or self.dernier_coup == "3+" and dernier_decalage != -3:
            self.ligne2moins()
            gagnant = self.gagne(self.plateau, self.decalage)
            self.joueur = (self.joueur % 2) + 1
            if len(gagnant) != 0:
                self.end_game(gagnant)

            self.statusBar().showMessage("Joueur " + str(self.joueur))

            if self.IA_playing:
                self.frame.setEnabled(False)
                self.timer.singleShot(int(self.timer_IA), self.AI)

    def ligne3plus(self):
        self.xligne3 = self.xligne3 + 100
        self.A2.setGeometry(QRect(self.xligne3, 250, 100, 100))
        self.B2.setGeometry(QRect(self.xligne3+100, 250, 100, 100))
        self.C2.setGeometry(QRect(self.xligne3+200, 250, 100, 100))
        self.D2.setGeometry(QRect(self.xligne3+300, 250, 100, 100))


    def decalageplus3(self):
        coup = self.dernier_coup
        dernier_decalage = self.decalage[2]
        self.dernier_coup = self.coup_joueur("2+")
        if self.dernier_coup != coup or self.dernier_coup == "2-" and dernier_decalage != 3:
            self.ligne3plus()
            gagnant = self.gagne(self.plateau, self.decalage)
            self.joueur = (self.joueur % 2) + 1
            if len(gagnant) != 0:
                self.end_game(gagnant)

            self.statusBar().showMessage("Joueur " + str(self.joueur))
            if self.IA_playing:
                self.frame.setEnabled(False)
                self.timer.singleShot(int(self.timer_IA), self.AI)


    def ligne3moins(self):
        self.xligne3 = self.xligne3 - 100
        self.A2.setGeometry(QRect(self.xligne3, 250, 100, 100))
        self.B2.setGeometry(QRect(self.xligne3+100, 250, 100, 100))
        self.C2.setGeometry(QRect(self.xligne3+200, 250, 100, 100))
        self.D2.setGeometry(QRect(self.xligne3+300, 250, 100, 100))


    def decalagemoins3(self):
        coup = self.dernier_coup
        dernier_decalage = self.decalage[2]
        self.dernier_coup = self.coup_joueur("2-")
        if self.dernier_coup != coup or self.dernier_coup == "2+" and dernier_decalage != -3:
            self.ligne3moins()
            gagnant = self.gagne(self.plateau, self.decalage)
            self.joueur = (self.joueur % 2) + 1
            if len(gagnant) != 0:
                self.end_game(gagnant)

            self.statusBar().showMessage("Joueur " + str(self.joueur))
            if self.IA_playing:
                self.frame.setEnabled(False)
                self.timer.singleShot(int(self.timer_IA), self.AI)

    def ligne4plus(self):
        self.xligne4 = self.xligne4 + 100
        self.A1.setGeometry(QRect(self.xligne4, 350, 100, 100))
        self.B1.setGeometry(QRect(self.xligne4+100, 350, 100, 100))
        self.C1.setGeometry(QRect(self.xligne4+200, 350, 100, 100))
        self.D1.setGeometry(QRect(self.xligne4+300, 350, 100, 100))

    def decalageplus4(self):
        coup = self.dernier_coup
        dernier_decalage = self.decalage[3]
        self.dernier_coup = self.coup_joueur("1+")
        if self.dernier_coup != coup or self.dernier_coup == "1-" and dernier_decalage != 3:
            self.ligne4plus()
            gagnant = self.gagne(self.plateau, self.decalage)
            self.joueur = (self.joueur % 2) + 1
            if len(gagnant) != 0:
                self.end_game(gagnant)

            self.statusBar().showMessage("Joueur " + str(self.joueur))
            if self.IA_playing:
                self.frame.setEnabled(False)
                self.timer.singleShot(int(self.timer_IA), self.AI)

    def ligne4moins(self):
        self.xligne4 = self.xligne4 - 100
        self.A1.setGeometry(QRect(self.xligne4, 350, 100, 100))
        self.B1.setGeometry(QRect(self.xligne4+100, 350, 100, 100))
        self.C1.setGeometry(QRect(self.xligne4+200, 350, 100, 100))
        self.D1.setGeometry(QRect(self.xligne4+300, 350, 100, 100))

    def decalagemoins4(self):
        coup = self.dernier_coup
        dernier_decalage = self.decalage[3]
        self.dernier_coup = self.coup_joueur("1-")
        if self.dernier_coup != coup or self.dernier_coup == "1+" and dernier_decalage != -3:
            self.ligne4moins()
            gagnant = self.gagne(self.plateau, self.decalage)
            self.joueur = (self.joueur % 2) + 1
            if len(gagnant) != 0:
                self.end_game(gagnant)

            self.statusBar().showMessage("Joueur " + str(self.joueur))
            if self.IA_playing:
                self.frame.setEnabled(False)
                self.timer.singleShot(int(self.timer_IA), self.AI)

        

    def coups_possibles(self, plateau, dernier_coup, joueur, decalage):
        """
        fonction qui renvoie une liste des coups possible sur
        le plateau en fonction du joueur et du dernier coup
        :param plateau: liste de liste, 0 pour vide, 1 ou 2 pour joueur
        :param dernier_coup: string de deux caractères, dernier coup joué
        :param joueur: entier, 1 ou 2
        :param decalage: liste d'entiers, représentent le décalage des lignes du plateau
        :return liste_coups_possibles
        """
        liste_coups_possibles = []
        cle_decalage = self.dico_decalage.keys()
        cle_plateau = self.posplateau.keys()

        for c in cle_plateau:

            if c != dernier_coup and plateau[self.posplateau[c][1]][self.posplateau[c][0]] != joueur:
                liste_coups_possibles.append(c)

        for c in cle_decalage:

            if c != dernier_coup:

                if '+' in c and decalage[self.dico_decalage[c]] != 3:
                    liste_coups_possibles.append(c)

                elif '-' in c and decalage[self.dico_decalage[c]] != -3:
                    liste_coups_possibles.append(c)

        return liste_coups_possibles

    def evaluation_score(self, plateau, decalage):
        """
        Renvoie le score du plateau à un moment donné
        :param plateau: liste de liste, 0 pour vide, 1 ou 2 pour joueur
        :param decalage: list d'entiers, représentent le décalage des lignes du plateau
        :return: score du plateau
        """
        gagnant = self.gagne(plateau, decalage)

        if len(gagnant) != 0:
            if gagnant == {2}:
                # si l'IA gagne
                score = 1
            elif gagnant == {1}:
                #si le joueur gagne
                score = -1
            elif gagnant == {1, 2} or gagnant == {2, 1}:
                #si il y a une égalité
                score = 0
        else:
            #tant que le jeux n'est pas terminé
            score = 0
        return score
        
    def minimax(self, plateau, decalage, dernier_coup, profondeur, maxi):
        """
        Fonction de l'IA qui va choisir un coup qui va le plus maximiser son score
        et minimiser le score de l'adversaire (fonction récursive)
        :param plateau: liste de liste, 0 pour vide, 1 ou 2 pour joueur
        :param decalage: list d'entiers, représentent le décalage des lignes du plateau
        :param dernier_coup: dernier coup joué sous forme de chaine de caractère
        :parma profondeur: entier qui va déterminer combien
        de coup à l'avance elle va prévoir
        :param maxi: True si joueur maximisant, False si joueur minimisant
        :return choix pseudo aléatoire entre les meilleurs coup possible et son score

        """
        gagnant = self.gagne(plateau, decalage)
        if profondeur == 0 or len(gagnant) != 0:
            score = self.evaluation_score(plateau, decalage)
            return (None, score)

        elif maxi:
            meilleurscore = -1000
            meilleurcoup = []

            for coup in self.coups_possibles(plateau, dernier_coup, 2, decalage):
                nouveauplateau = deepcopy(plateau)
                nouveaudecalage = deepcopy(decalage)
                self.coup_AI(nouveauplateau, nouveaudecalage, 2, coup)
                score = self.minimax(nouveauplateau, nouveaudecalage, dernier_coup, profondeur - 1, False)[1]

                if meilleurscore < score:
                    meilleurscore = score
                    meilleurcoup = [(coup,score)]

                elif meilleurscore == score:
                    meilleurcoup.append((coup,score))
                    
        else:
            meilleurscore = 1000
            meilleurcoup = []

            for coup in self.coups_possibles(plateau, dernier_coup, 1, decalage):
                nouveauplateau = deepcopy(plateau)
                nouveaudecalage = deepcopy(decalage)
                self.coup_AI(nouveauplateau, nouveaudecalage , 1,coup)
                score = self.minimax(nouveauplateau, nouveaudecalage, dernier_coup, profondeur - 1, True)[1]

                if meilleurscore > score:
                    meilleurscore = score
                    meilleurcoup = [(coup,score)]

                elif meilleurscore == score:
                        meilleurcoup.append((coup,score))
        
        return (random.choice(meilleurcoup))

    def coup_AI(self, plateau, decalage, joueur, coup):
        """
        Permet de jouer un coup sur le plateau sans les conditions
        :param plateau: liste de liste, 0 pour vide, 1 ou 2 pour joueur
        :param decalage: list d'entiers, représentent le décalage des lignes du plateau
        :param joueur: entier, 1 ou 2
        :param coup: le coup à placer sous forme d'un str
        :return None
        """
        if coup in self.dico_decalage:

            if '+' in coup:
                decalage[self.dico_decalage[coup]] += 1

            elif '-' in coup:
                decalage[self.dico_decalage[coup]] -= 1

        elif coup in self.posplateau:
            plateau[self.posplateau[coup][1]][self.posplateau[coup][0]] = joueur

    def coup_decalage(self, coup):
        """décalage pour l'IA"""
        if coup == "4-":
            self.ligne1moins()
        elif coup == "4+":
            self.ligne1plus()
        elif coup == "3-":
            self.ligne2moins()
        elif coup == "3+":
            self.ligne2plus()
        elif coup == "2-":
            self.ligne3moins()
        elif coup == "2+":
            self.ligne3plus()
        elif coup == "1-":
            self.ligne4moins()
        elif coup == "1+":
            self.ligne4plus()


    def AI(self):
        """
        Permet de jouer un coup sur le plateau sans les conditions
        :param plateau: liste de liste, 0 pour vide, 1 ou 2 pour joueur
        :param decalage: list d'entiers, représentent le décalage des lignes du plateau
        :param joueur: entier, 1 ou 2
        :param coup: le coup à placer sous forme d'un str
        :return None
        """
        coup = str(self.minimax(self.plateau, self.decalage, self.dernier_coup, 2, True)[0])
        self.coup_AI(self.plateau, self.decalage, self.joueur, coup)
        self.dernier_coup = coup

        self.coup_decalage(coup)

        for button in self.allButtons:
            if coup == button.objectName():
                if self.joueur == 2:
                    button.setStyleSheet('QPushButton {background-color: #FC0000; color: #FC0000;}')
                else:
                    button.setStyleSheet('QPushButton {background-color: #FFEB00; color: #FFEB00;}')

        if '+' in self.dernier_coup:
            self.dernier_coup = self.dernier_coup[0]+'-'
        elif '-' in self.dernier_coup:
            self.dernier_coup = self.dernier_coup[0]+'+'
        
        gagnant = self.gagne(self.plateau, self.decalage)
        self.joueur = (self.joueur % 2) + 1

        self.statusBar().showMessage("Joueur " + str(self.joueur))

        self.frame.setEnabled(True)

        if len(gagnant) != 0:
            self.end_game(gagnant)

        if not self.human_playing and len(gagnant) == 0:
            self.timer.singleShot(int(self.timer_IA), self.AI) 


    def coup_joueur(self, choix):
        """
        Demande un coup au joueur jusqu'à ce qu'il soit valide et le joue en modifiant le plateau
        :param plateau: liste de liste, 0 pour vide, 1 ou 2 pour joueur
        :param decalage: liste d'entiers, représentent le décalage des lignes du plateau
        :param joueur: entier, 1 ou 2
        :param dernier_coup: string de deux caractères, dernier coup joué
        :return: coup joué lors du tour
        """

        if choix == self.dernier_coup:
            # vérifie si ce coups ne vient pas d'être joué par l'adversaire
            choix = self.dernier_coup
            self.statusBar().showMessage("ce coup vient d'être joué")

        elif choix in self.dico_decalage:

            if '+' in choix and self.decalage[self.dico_decalage[choix]] < 3:
                #empeche de décaler plus de 3 fois d'un coté
                self.decalage[self.dico_decalage[choix]] += 1
                choix = choix[0] + '-'
                #pour empecher le joueur suivant décaler dans l'autre sens juste après

            elif '-' in choix and self.decalage[self.dico_decalage[choix]] > -3:
                #empeche de décaler plus de 3 fois d'un coté
                self.decalage[self.dico_decalage[choix]] -= 1
                choix = choix[0] + '+' 
                #pour empecher le joueur suivant décaler dans l'autre sens juste après
            else:
                choix = self.dernier_coup
                self.statusBar().showMessage("impossible de décaler plus")

        elif self.plateau[self.posplateau[choix][1]][self.posplateau[choix][0]] == self.joueur:
            # si la case appartient déjà au joueur ayant joué
            choix = self.dernier_coup
            self.statusBar().showMessage("Cette case est déjà de votre couleur")

        else:
            self.plateau[self.posplateau[choix][1]][self.posplateau[choix][0]] = self.joueur

        return choix

app = QApplication(sys.argv)
game = Game()
game.show()
app.exec_()