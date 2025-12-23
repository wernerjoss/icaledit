#!/usr/bin/env python3

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QFileDialog, QMessageBox, QWidget, QVBoxLayout
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QDate

import icedit_ui
# calendars
from icalendar import Calendar, Event, vCalAddress, vText
from datetime import date, datetime
from pathlib import Path
import os
import pytz


class MainWindow(QMainWindow, icedit_ui.Ui_MainWindow):
	ecal = Calendar()
	actEventName = ''
	selectedEvent = Event()
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.setupUi(self)
		self.actionNeu.triggered.connect(self.NewFile)
		self.actionOpen.triggered.connect(self.OpenFile)
		self.actionSpeichern.triggered.connect(self.SaveFile)
		self.actionSpeichern_unter.triggered.connect(self.SaveAsFile)
		self.okButton.clicked.connect(self.EditOk)
		self.edit_menu = self.menubar.addMenu('&Edit Event(s)')
		self.addevent_menu = self.menubar.addMenu('&Add Event(s)')
		# edit Events menu
		event_action = QAction("Neuer Termin", self)
		event_action.triggered.connect(self.AddEvents)
		self.addevent_menu.addAction(event_action)
		
	def message(self, s):
		self.plainTextEdit.appendPlainText(s)
	
	def OpenFile(self):
		self.filename, ok = QFileDialog.getOpenFileName(self, 'Open File', '', 'ics Files (*.ics)')
		if self.filename:
			self.edit_menu.clear()	#	important !
			fileName = Path(self.filename)	#.selectedFiles()
			print(fileName)
			e = open(fileName, 'rb')
			self.ecal = Calendar.from_ical(e.read())
			self.UpdateInfoPane()
			e.close()
		    
	def UpdateInfoPane(self):
		self.plainTextEdit.clear()
		self.edit_menu.clear()	#	important !
		if (self.filename):
			self.message('Datei:\t'+self.filename)
		enum = 1
		for component in self.ecal.walk():
			if component.name == "VEVENT":
				event = Event()
				event = component
				#if not str(component.get("name")):
				if (str(event.get("summary")) == "None"):
					eventId = 'Event '+str(enum)
				else:
					eventId = str(event.get("summary"))
				
				# edit Events menu
				event_action = QAction(eventId, self)
				event_action.triggered.connect(self.EditEvent)
				self.edit_menu.addAction(event_action)

				#print ("eventId: ", eventId)
				event["summary"] = eventId	# finally, that's it :-)
				event["name"] = eventId	# finally, that's it :-)
				#self.message('eventId:\t'+eventId)
				#self.message('Event:\t'+str(event.get("name")))
				self.message('Summary:\t'+str(event.get("summary")))
				self.message('Descr.:\t'+str(event.get("description")))
				self.message('Orga:\t'+str(event.get("organizer")))
				self.message('Ort:\t'+str(event.get("location")))
				self.message('URL:\t'+str(event.get("url")))
				#self.message('GEO:\t'+str(event.get("geo")))
				if (event.get("dtstart")):
					self.message('Start:\t'+str(event.decoded("dtstart")))
				if (event.get("dtend")):
					self.message('End:\t'+str(event.decoded("dtend")))
				self.message('\t')
				enum += 1
					
	def NewFile(self):
		self.filename, ok = QFileDialog.getSaveFileName(self,  'New File', '', 'ics Files (*.ics)')
		fileName = Path(self.filename)
		if (ok):
			self.ecal = Calendar()	# new empty Calendar
			self.ecal.add("prodid", "-//hoernerfranzracing//DE")	# TODO: get prodid from yaml cfg File
			self.ecal.add("version", "2.0")

			event = Event()
			event.add("summary","New")
			event.add("dtstart",date.today())
			event.add("dtend",date.today())
			event.add("location","")
			event.add("name","New")
			#event.add("geo","49.1,3.2")
			event.add("url","")
			today = QDate.currentDate()
			self.ecal.add_component(event)
			with open(fileName, "wb") as f:
			    f.write(self.ecal.to_ical())
			print(self.ecal)
			print(fileName)
			self.UpdateInfoPane()
	
	def AddEvents(self):
		selectedEvent = self.sender()
		self.edit_menu.clear()	#	important !
		print("Sender: ", selectedEvent.text())
		if (self.ecal):
			event = Event()
			for component in self.ecal.walk():
				if component.name == "VEVENT":
					event = component
					start = event.get("dtstart")	# get a valid dtstart
					#print("Event: ", event.get("summary"))
			event = Event()	# new Event !
			event["summary"] = selectedEvent.text()
			event["name"] = event["summary"]
			event["dtstart"] = start	#	these 2 must be populated !
			event["dtend"] = start
			self.ecal.add_component(event)	# kompletten event zum Kalender hinzufügen !
			event = Event()
			self.edit_menu.clear()	#	important !
			for component in self.ecal.walk():
				if component.name == "VEVENT":
					event = component
					print("Event added: ", event.get("summary"))
					#edit Events menu
					event_action = QAction(event.get("summary"), self)
					event_action.triggered.connect(self.EditEvent)
					self.edit_menu.addAction(event_action)

	def SaveFile(self):
		fileName = Path(self.filename)
		if (self.ecal):
			with open(fileName, "wb") as f:
			    f.write(self.ecal.to_ical())
			print(self.ecal)
			print(fileName)
		self.UpdateInfoPane()
	
	def SaveAsFile(self):
		self.filename, ok = QFileDialog.getSaveFileName(self,  'Save as File', '', 'ics Files (*.ics)')
		fileName = Path(self.filename)
		#print(fileName)
		if (self.ecal):
			with open(fileName, "wb") as f:
			    f.write(self.ecal.to_ical())
			print(self.ecal)
			print(fileName)
		self.UpdateInfoPane()
	
	def EditEvent(self):
		# see https://stackoverflow.com/questions/52526040/how-to-get-the-name-of-a-qmenu-item-when-clicked
		selectedEvent = self.sender()
		print("selected Event (edit): ",selectedEvent.text())

		for component in self.ecal.walk():
			if component.name == "VEVENT":
				event = Event()
				event = component
				eventId = str(event.get("summary"))
				print("eventId: ", eventId)
				if (eventId == selectedEvent.text()):
					self.selectedEvent = event
					#print("Found: ", eventId)
					break
		print("selected eventId: ", eventId)
		#self.nameEdit.setEnabled(True)
		self.sumEdit.setEnabled(True)
		self.nameEdit.setText(eventId)
		self.sumEdit.setText(eventId)
		self.startEdit.setEnabled(True)
		
		#print(str(event.decoded("dtstart")))
		line = str(event.decoded("dtstart"))
		arr = line.split("-")
		#print(arr)
		y = int(arr[0])
		m = int(arr[1])
		d = int(arr[2])
		#print(y,m,d)
		evStart = QDate(y, m, d)
		self.startEdit.setDate(evStart)
		self.startEdit.setDisplayFormat('dd.MM.yyyy')
		#print(str(event.decoded("dtend")))
		line = str(event.decoded("dtend"))
		arr = line.split("-")
		#print(arr)
		y = int(arr[0])
		m = int(arr[1])
		d = int(arr[2])
		#print(y,m,d)
		evEnd = QDate(y, m, d)
		self.endEdit.setDate(evEnd)
		self.endEdit.setDisplayFormat('dd.MM.yyyy')
		self.endEdit.setEnabled(True)
		self.urlEdit.setEnabled(True)
		self.urlEdit.setText(event.get("url"))
		self.descEdit.setEnabled(True)
		self.descEdit.setText(event.get("description"))
		self.sumEdit.setEnabled(True)
		self.sumEdit.setText(event.get("summary"))
		self.urlEdit.setEnabled(True)
		self.urlEdit.setText(event.get("url"))
		self.locEdit.setEnabled(True)
		self.locEdit.setText(event.get("location"))
		#self.geoEdit.setEnabled(True)
		#self.geoEdit.setText(event.get("geo"))
		self.okButton.setEnabled(True)
		self.cancelButton.setEnabled(True)
		
	def EditOk(self):
		event = Event()
		for component in self.ecal.walk():
			if component.name == "VEVENT":
				event = Event()
				event = component
				eventId = str(event.get("summary"))
				if (eventId == self.sumEdit.text()):
					self.selectedEvent = event
					#print("Found: ", eventId)
					break
		print("selected eventId: ", eventId)
		self.selectedEvent["summary"] = self.sumEdit.text()
		self.selectedEvent["name"] = self.sumEdit.text()
		self.selectedEvent["description"] = self.descEdit.text()
		line = self.startEdit.text()
		print(line)
		arr = line.split(".")
		#print(arr)
		y = int(arr[2]);		m = int(arr[1]);		d = int(arr[0])
		print(y,m,d)
		evStart = QDate(y, m, d)
		self.selectedEvent["dtstart"] = evStart.toString('yyyyMMdd')
		line = self.endEdit.text()
		print(line)
		arr = line.split(".")
		#print(arr)
		y = int(arr[2]);		m = int(arr[1]);		d = int(arr[0])
		print(y,m,d)
		evEnd = QDate(y, m, d)
		self.selectedEvent["dtend"] = evEnd.toString('yyyyMMdd')
		self.selectedEvent["location"] = self.locEdit.text()
		self.selectedEvent["url"] = self.urlEdit.text()
		#if not self.geoEdit.text() == "":
		#	self.selectedEvent.add("geo", self.geoEdit.text())
		self.selectedEvent["summary"] = self.sumEdit.text()
		self.selectedEvent["last-modified"] = datetime.today()
		self.UpdateInfoPane()
				
	def quit(self):
		self.destroy()


app = QApplication(sys.argv)

w = MainWindow()
title = "icaledit.py v 0.1.0 (C) Werner Joss 2025"
w.setWindowTitle(title)

w.show()

app.setStyle("Fusion")
app.exec()		 