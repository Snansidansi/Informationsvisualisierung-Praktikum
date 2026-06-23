## Auswertung

### Modellvergleich

Die Logistische Regression scheint hier der beste Indikator zu sein und schneidet insgesamt am stärksten ab. Sie erreicht sowohl in der 10-Fold Cross-Validation als auch beim Bootstrap 0.632 die höchste Accuracy und den stabilsten F1-Score. K-Nearest Neighbor (mit $k=3$) liefert hingegen die schwächsten Ergebnisse.

### Confusion Matrix & Decision Tree

Bei Betrachtung der Confusion Matrix wird ersichtlich, dass die Modelle die Klasse 0 ("Nicht überlebt") deutlich präziser vorhersagen als Klasse 1 ("Überlebt"). Das ist auf die Unausgewogenheit der Zieldaten zurückzuführen, da historisch bedingt deutlich mehr Passagiere gestorben sind.

Im generierten Entscheidungsbaum reicht eine geringe Tiefe bereits aus, um eine aussagekräftige Separation zu erzielen. Es fällt sofort auf, dass das Geschlecht (`Sex`) das mit Abstand wichtigste Trennkriterium ist, da der Algorithmus dieses direkt als Root-Node wählt. In den darauffolgenden tieferen Knoten wird meist nach der Passagierklasse (`Pclass`) gesplittet. Die Modelle haben die historischen Rettungsprioritäten ("Frauen zuerst", Bevorzugung höherer Klassen) also sehr eindeutig aus den Daten extrahiert.
