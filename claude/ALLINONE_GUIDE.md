# AllInOne Multiple Choice Karten erstellen

## Übersicht

Der "AllInOne (kprim, mc, sc)" Notentyp unterstützt drei verschiedene Fragetypen:
- **mc** (Multiple Choice) - Mehrere Antworten können richtig sein
- **sc** (Single Choice) - Nur eine Antwort ist richtig  
- **kprim** - Jede Aussage muss als richtig/falsch bewertet werden

## Felder

Der Notentyp hat folgende Felder:

| Feld | Beschreibung |
|------|--------------|
| `Question` | Die Hauptfrage |
| `Title` | Optionaler Titel |
| `QType (0=kprim,1=mc,2=sc)` | **0** = kprim, **1** = mc, **2** = sc |
| `Q_1` bis `Q_5` | Bis zu 5 Antwortmöglichkeiten |
| `Answers` | Lösungsstring (z.B. "1 0 0 1 0" für richtig/falsch) |
| `Sources` | Optionale Quellenangaben |
| `Extra 1` | Zusätzliche Notizen |

## Verwendung mit Claude

### Multiple Choice (mc) - Mehrere richtige Antworten

```
Erstelle eine Multiple-Choice Karte im Deck "Medizin" mit dem Notentyp "AllInOne (kprim, mc, sc)":

Frage: Welche der folgenden sind Symptome einer Grippe?
Typ: 1 (mc)
Antworten:
- Fieber (richtig)
- Kopfschmerzen (richtig)
- Hautausschlag (falsch)
- Husten (richtig)
- Knochenbruch (falsch)
```

Claude erstellt dann automatisch die Karte mit:
- `QType (0=kprim,1=mc,2=sc)`: 1
- `Q_1`: Fieber
- `Q_2`: Kopfschmerzen
- `Q_3`: Hautausschlag
- `Q_4`: Husten
- `Q_5`: Knochenbruch
- `Answers`: 1 1 0 1 0

### Single Choice (sc) - Nur eine richtige Antwort

```
Erstelle eine Single-Choice Karte im Deck "Geschichte" mit dem Notentyp "AllInOne (kprim, mc, sc)":

Frage: Wann fiel die Berliner Mauer?
Typ: 2 (sc)
Antworten:
- 1987 (falsch)
- 1989 (richtig)
- 1991 (falsch)
- 1993 (falsch)
```

### K-Prim (kprim) - Jede Aussage bewerten

```
Erstelle eine K-Prim Karte im Deck "Biologie" mit dem Notentyp "AllInOne (kprim, mc, sc)":

Frage: Bewerten Sie folgende Aussagen über Photosynthese:
Typ: 0 (kprim)
Aussagen:
- Findet in Chloroplasten statt (richtig)
- Produziert Sauerstoff (richtig)
- Benötigt kein Licht (falsch)
- Kommt nur in Bäumen vor (falsch)
```

## Batch-Erstellung aus PDF

Der Hauptanwendungsfall - PDF hochladen und Karten erstellen lassen:

```
[PDF hochladen]

Analysiere dieses PDF über Biochemie und erstelle 15 Multiple-Choice Karten 
für mein Deck "Biochemie" mit dem Notentyp "AllInOne (kprim, mc, sc)".

Verwende hauptsächlich Typ 1 (mc) für Fragen mit mehreren richtigen Antworten.
Erstelle je Karte 4-5 Antwortmöglichkeiten mit einer guten Mischung aus 
richtigen und falschen Antworten.
```

## Wichtige Hinweise

### Answers-Feld Format

Das `Answers`-Feld enthält die Lösungen als Zahlen getrennt durch Leerzeichen:
- **1** = richtige Antwort
- **0** = falsche Antwort

Beispiele:
- `1 0 0 0` = Nur die erste Antwort ist richtig
- `1 1 0 1` = Erste, zweite und vierte Antwort sind richtig
- `0 0 1 0 0` = Nur die dritte Antwort ist richtig

### Maximale Anzahl Antworten

Der Notentyp unterstützt nur 5 Antworten (`Q_1` bis `Q_5`). Falls Sie mehr benötigen, 
können Sie das "multiple choice with 12 options" Addon verwenden.

### QType Werte

**Wichtig:** Das Feld `QType (0=kprim,1=mc,2=sc)` muss exakt diese Werte haben:
- `0` für K-Prim
- `1` für Multiple Choice
- `2` für Single Choice

## Beispiel: Vollständige Karte

```json
{
  "type": "AllInOne (kprim, mc, sc)",
  "deck": "Medizin",
  "fields": {
    "Question": "Welche Aussagen über das menschliche Herz sind korrekt?",
    "Title": "Anatomie: Das Herz",
    "QType (0=kprim,1=mc,2=sc)": "1",
    "Q_1": "Hat vier Kammern",
    "Q_2": "Pumpt Blut durch den Körper",
    "Q_3": "Produziert rote Blutkörperchen",
    "Q_4": "Ist ein Muskelorgan",
    "Q_5": "Liegt auf der linken Körperseite",
    "Answers": "1 1 0 1 0",
    "Sources": "Anatomie-Lehrbuch, Kapitel 7",
    "Extra 1": "Das Herz schlägt durchschnittlich 70 Mal pro Minute"
  }
}
```

## Zusammenfassung

1. **PDF hochladen** in Claude
2. **Sagen:** "Erstelle X Karten mit dem AllInOne Notentyp"
3. **Claude macht automatisch:**
   - PDF analysieren
   - Fragen formulieren
   - Antworten erstellen
   - Korrekte Lösungsstrings generieren
   - Alle Karten in Anki speichern

**Kein Code nötig!** 🎉
