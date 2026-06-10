## Datenbereinigung

### Zweck der Daten

Der Zweck der Daten liegt wahrscheinlich darin ein Muster aus verschiedenen Attributen (oder Attributkombinationen) zu finden, mit welchen sich darauf schließen lässt, ob eine Person auf der Titanic überlebt hat.

### Attribute

Dabei sind einige Attribute irrelevant und könnten zu falschen Rückschlüssen führen und somit die Visualisierungen verzerren.

Beispielsweise könnte es eine Korrelation zwischen dem `PassangerId` und dem Überleben geben, welche so aussieht, dass Passagiere mit einer geraden `PassangerId` häufiger überlebt haben. Hier lässt sich allerdings eine Kausalität fast schon ausschließen. Eine Kausalität wäre hier nur möglich, wenn z.B. alle geraden `PassengerId` sich in einem sichereren Teil des Schiffes befinden. Dafür gibt es jedoch schon ein Attribut.

Ähnliches lässt sich für Attribute wie `Ticked` und `Fare` vermuten

### Datenqualität

Weiterhin lässt sich zur Datenqualität sagen, das viele wichtige Informationen Fehlen.

Bei dem Attribut `Alter` fehelen einige Werte. Dies ist Problematisch, da Kinder bei Rettungen udn Evakuierungen oft Vorrang haben. Hier wäre es eventuell über einen Titel der Person (z.b. Mr., Mrs, ...) darauf zu schließen, ob es sicht um ein Kind handelt oder nicht.

Auch bei dem Attribut `Fare` gibt es große Probleme, da hier über die Hälfte der Daten fehlen.
