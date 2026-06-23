## Datenbereinigung

### Zweck der Daten

Der Zweck des Datensatzes besteht darin, Muster aus verschiedenen Merkmalen zu finden. Damit soll vorhergesagt werden, ob ein Passagier das Unglück auf der Titanic überlebt hat oder nicht.

### Relevanz der Attribute

Einige Spalten haben keinen logischen Zusammenhang mit den Überlebenschancen. Sie würden die Grafiken verzerren oder die Modelle verwirren. Deshalb wurden sie gelöscht:

- **PassengerId, Ticket, Name:** Diese Angaben sind für die Vorhersage unwichtig und wurden aus dem Datensatz entfernt.
- **Cabin:** Diese Spalte ist extrem unvollständig (viele fehlende Werte) und wurde wegen der schlechten Datenqualität komplett gelöscht.

### Datenqualität und Bereinigungsschritte

Um mit den Daten arbeiten zu können, wurden folgende Schritte durchgeführt:

- **Zahlenformate reparieren:** Die Spalten für ID, Überleben, Klasse, Alter, Geschwister, Eltern/Kinder und Ticketpreis wurden sauber in Zahlen umgewandelt. Fehlerhafte Text-Einträge wurden dabei automatisch als "leer" (`NaN`) markiert.
- **Namen der Häfen ausschreiben:** Die abgekürzten Einstiegshäfen wurden durch die echten Namen ersetzt (_Cherbourg_, _Queenstown_, _Southampton_), damit sie lesbar sind.
- **Text in Zahlen umwandeln (One-Hot-Encoding):** Da Computer nicht direkt mit Text wie "male" oder "female" rechnen können, wurden das Geschlecht und die Häfen in Ja/Nein-Spalten (0 und 1) aufgeteilt. Dabei wurde jeweils eine Spalte weggelassen, um doppelte Informationen zu vermeiden.
- **Umgang mit leeren Feldern:** Nach allen Umwandlungen wurden alle Zeilen gelöscht, in denen noch wichtige Informationen (wie das Alter oder der Ticketpreis) gefehlt haben. Das sorgt für einen vollständig ausgefüllten Datensatz am Ende.
