## Auswertung

### Lineare Regression

Flavanoide scheinen ein guter Indikator für den Proteinwert (R²=0.59, Pearson=0.77), die Menge aller Phenole (R²=0.67, Pearson=0.82) sowie in geringerem Maße auch den Proanthocyaniden (R²=0.44, Pearson=0.66) zu sein.

Ansonsten lassen sich sonst einzelne etwas schwächere Korrelationen feststellen (z.B. Alkohol und Prolinwert mit R²=0.41, Pearson=0.64), die meisten Attribute haben aber wohl recht wenig miteinander zu tun, was in den Scatter Plots auch ersichtlich wird.

### K-Means Clustering

Zweidimensionale PCA-Projektion scheint bereits auszureichen, um einen großen Teil der Gesamtvarianz abzudecken. PC 1 erklärt etwa 35.72% der Varianz, PC 2 etwa 18.66%, was insgesamt etwa 54.38% der Gesamtvarianz ausmacht. Die Projektion ist also durchaus schon in zwei Dimensionen aussagekräftig.

Bei Betrachtung des Davies Bouldin Indizes und des Silhouette Coefficients scheint k=3 ein Optimum zu sein, da es den niedrigsten (also besten) addierten Rang der beiden Werte besitzt (wobei niedriger = besser bei Davies Bouldin, höher = besser bei durchschnittlichem Silhouettenkoeffizient).

Trotzdem sind bei k=3 ein Davies Bouldin Index von 1.422 und ein durchschnittlicher Silhouette Coefficient von 0.278 zu schlecht um auf eine sehr eindeutige Separation hinzuweisen, was sich auch durch recht weit gestreute und sich gegenseitig überschneidende Cluster im Scatter Plot bestätigt. Grob lassen sich die Weine jedoch definitiv nach ihrer chemischen Beschaffenheit  in Cluster unterteilen.
