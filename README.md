## icaledit.py - ein Python Programm zur Erstellung und Bearbeitung von .ics Kalender Dateien.

Dieses Programm ermöglicht die Erstellung und Bearbeitung von Kalender-Dateien, insbesondere mit der Möglichkeit, Properties die von Standard-Kalender Client Programmen (z.B. Thunderbird/Lightning, KDE Kalender, die meisten mobilen Kalender Apps...) nicht oder schlecht unterstützt werden, einzufügen bzw. zu ändern.  
Eine dieser Properties die ich öfter brauche, ist URL - also ein Link, oder auch geografische Koordinaten (GEO).  
Das einzige mir bekannte Programm, das dies (URL) kann, ist die Webanwendung [Infcloud](https://inf-it.com/open-source/clients/infcloud/).  
Etwas unbefriedigend ist hier jedoch, dass dies nur für selbst gehostete Kalender funktioniert, nicht jedoch z.B. für Google Kalender.  
Das hier vorgestellte Programm hat folgende Grundfunktionen:
-   Vorhandene Kalenderdatei öffnen und bearbeiten (z.B. Events mit URL und/oder GEO ergänzen)
-   Neue Kalenderdatei erstellen
-   Datei speichern

Eine vorhandene Kalenderdatei kann mehrere Events beinhalten, diese werden einzeln zur Bearbeitung angeboten.  
Eine neue Datei wird zunächst mit EINEM Event zur Bearbeitung angelegt, weitere Events können hinzugefügt werden.  
Default-Werte (PRODID, ORGANIZER, Timezone...) werden aus einer yaml Datei (icaledit.yaml) im Programmverzeichnis gelesen.  
In einer vorhandenen Datei gespeicherte Properties, die hier nicht zur Bearbeitung angeboten werden, bleiben beim Speichern erhalten.  
Die nach der Bearbeitung gespeicherte Datei kann dann einfach in einen bestehenden Online-Kalender importiert werden.  

Das Programm benötigt zur Laufzeit die Librarys icalendar, yaml und PyQt6, es kann von meiner [GitHub Seite](https://github.com/wernerjoss/icaledit) bezogen werden.

## English Version:
This program allows creating and editing of calendar files, in particular with the ability to insert or change properties that are not supported or poorly supported by standard calendar client programmes (e.g. Thunderbird/Lightning, KDE Calendar, most mobile calendar apps...).  
One of these properties that I often need is URL – a link – or geographical coordinates (GEO).  
The only program I know of that can do this (URL) is the web application [Infcloud](https://inf-it.com/open-source/clients/infcloud/).  
However, it is somewhat unsatisfactory that this only works for self-hosted calendars and not, for example, for Google Calendars.  
The program presented here has the following basic functions:

-   Open and edit existing calendar files (e.g. add events with URL and/or GEO)
-   Create new calendar files
-   Save files

An existing calendar file can contain multiple events, which are offered for editing individually.  
A new file is initially created with ONE event for editing, additional events can be added later.  
Default values (PRODID, ORGANIZER, time zone, etc.) are read from a yaml file (icaledit.yaml) in the programme directory.  
Properties stored in an existing file that are not offered for editing here are retained when the file is saved.  
The file saved after editing can then be easily imported into an existing online calendar.  

This program needs the Python Librarys icalendar, yaml and PyQt6 installed, it can be downloaded from my [GitHub Site](https://github.com/wernerjoss/icaledit).
