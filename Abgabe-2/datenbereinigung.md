## Datenbereinigung

Viele der Felder enthalten einen überflüssigen Punkt am Ende, dieser wird zuallererst einmal entfernt. Damit sind alle Felder schon mal gültige numerische Werte.

Es fällt auf, dass ein Farbintensitätswert eine viel höhere Präzision hat als alle anderen Werte. Als nächstes werden also alle Werte einheitlich auf zwei Nachkommastellen gerundet.

Zuletzt ist in einer Reihe noch ein Farbwert von 906, was sich von den anderen Farbwerten welche zwischen 0 und 2 liegen drastisch unterscheidet und daher höchstwahrscheinlich ein Fehler ist. Da sich nicht sicher feststellen lässt ob eigentlich 0.906 oder 1.906 gemeint war, wird die gesamte Reihe aus dem Datensatz entfernt (bzw. sogar alle anderen ähnlich drastischen Outlier die mehr als 100 mal grösser als der Mittelwert ihrer jwlg. Spalte sind theoretisch auch, es gibt aber sonst keine).
