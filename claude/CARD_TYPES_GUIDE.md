# Anki Kartentypen - Vollständige Anleitung

Übersicht aller verfügbaren Kartentypen in Ihrer Anki-Installation und wie Sie diese mit Claude über den MCP Server nutzen.

## Verfügbare Kartentypen

1. **AllInOne (kprim, mc, sc)** - Multiple Choice mit 3 Modi
2. **Basic** - Einfache Vorder-/Rückseite
3. **Basic (and reversed card)** - Zwei Karten: A→B und B→A
4. **Basic (optional reversed card)** - Optional umgekehrte Karte
5. **Basic (type in the answer)** - Antwort muss eingetippt werden
6. **Basic with Deck Reference Tags** - Mit Deck-Referenzen
7. **Basic with Reference Image** - Mit Referenzbild
8. **Cloze** - Lückentext-Karten
9. **Cloze Reference Tag** - Lückentext mit Referenzen
10. **Image Occlusion** - Bilder mit verdeckten Bereichen

---

## 1. AllInOne (kprim, mc, sc)

**Verwendung:** Multiple-Choice Fragen mit bis zu 5 Antworten

**Felder:**
- `Question` - Die Frage
- `Title` - Optionaler Titel
- `QType (0=kprim,1=mc,2=sc)` - Typ: 0=kprim, 1=mc, 2=sc
- `Q_1` bis `Q_5` - Antwortmöglichkeiten
- `Answers` - Lösungsstring (z.B. "1 0 1 0 0")
- `Sources` - Quellenangaben
- `Extra 1` - Zusätzliche Infos

**Beispiel für Claude:**
```
Erstelle eine Multiple-Choice Karte mit dem AllInOne Typ im Deck "Medizin":
Frage: Welche sind Symptome einer Grippe?
Typ: 1 (mc)
Antworten:
- Fieber (richtig)
- Kopfschmerzen (richtig)
- Hautausschlag (falsch)
- Husten (richtig)
```

📖 Siehe: `ALLINONE_GUIDE.md` für Details

---

## 2. Basic

**Verwendung:** Klassische Karteikarte - Frage auf der Vorderseite, Antwort auf der Rückseite

**Felder:**
- `Front` - Vorderseite (Frage)
- `Back` - Rückseite (Antwort)

**Beispiel für Claude:**
```
Erstelle eine Basic-Karte im Deck "Vokabeln":
Vorderseite: What is the capital of France?
Rückseite: Paris
```

**Batch-Erstellung aus PDF:**
```
[PDF hochladen]
Erstelle 20 Basic-Karten aus diesem PDF für mein "Geschichte" Deck.
Extrahiere wichtige Fakten und erstelle Frage-Antwort Paare.
```

---

## 3. Basic (and reversed card)

**Verwendung:** Erstellt automatisch ZWEI Karten - eine in jede Richtung

**Felder:**
- `Front` - Vorderseite
- `Back` - Rückseite

**Was passiert:**
- Karte 1: Front → Back
- Karte 2: Back → Front (automatisch erstellt)

**Beispiel für Claude:**
```
Erstelle eine "Basic (and reversed card)" im Deck "Sprachen":
Front: Hund
Back: dog

Das erstellt automatisch:
Karte 1: Hund → dog
Karte 2: dog → Hund
```

**Perfekt für:**
- Vokabeln (Deutsch ↔ Englisch)
- Hauptstädte (Land ↔ Stadt)
- Definitionen in beide Richtungen

---

## 4. Basic (optional reversed card)

**Verwendung:** Wie "Basic (and reversed card)", aber mit zusätzlichem Kontrollfeld

**Felder:**
- `Front` - Vorderseite
- `Back` - Rückseite
- `Add Reverse` - Wenn ausgefüllt, wird umgekehrte Karte erstellt

**Beispiel für Claude:**
```
Erstelle eine "Basic (optional reversed card)" im Deck "Chemie":
Front: H2O
Back: Wasser
Add Reverse: y

Wenn Add Reverse leer ist, wird nur eine Karte erstellt.
```

---

## 5. Basic (type in the answer)

**Verwendung:** Zwingt Sie, die Antwort einzutippen (nicht nur zu denken)

**Felder:**
- `Front` - Frage
- `Back` - Erwartete Antwort

**Was passiert:**
- Sie müssen die Antwort eintippen
- Anki vergleicht Ihre Eingabe mit der richtigen Antwort
- Tippfehler werden angezeigt

**Beispiel für Claude:**
```
Erstelle eine "Basic (type in the answer)" Karte im Deck "Programmierung":
Front: Welches Schlüsselwort definiert eine Funktion in Python?
Back: def
```

**Perfekt für:**
- Vokabeln (exakte Schreibweise üben)
- Programmier-Syntax
- Formeln und Befehle

---

## 6. Cloze (Lückentext)

**Verwendung:** Text mit Lücken zum Ausfüllen

**Felder:**
- `Text` - Text mit {{c1::Lücke}} Markierungen
- `Back Extra` - Zusätzliche Infos auf der Rückseite

**Syntax:**
- `{{c1::Wort}}` - Erste Lücke
- `{{c2::Wort}}` - Zweite Lücke
- usw.

**Beispiel für Claude:**
```
Erstelle eine Cloze-Karte im Deck "Biologie":
Text: Die {{c1::Photosynthese}} findet in den {{c2::Chloroplasten}} statt und produziert {{c3::Sauerstoff}}.
Back Extra: Dieser Prozess benötigt Licht und CO2.

Das erstellt 3 separate Karten:
Karte 1: Die _____ findet in den Chloroplasten statt...
Karte 2: Die Photosynthese findet in den _____ statt...
Karte 3: ...und produziert _____.
```

**Perfekt für:**
- Definitionen
- Komplexe Zusammenhänge
- Prozesse mit mehreren Schritten

**Batch-Erstellung aus PDF:**
```
[PDF hochladen]
Erstelle 15 Cloze-Karten aus diesem PDF für mein "Medizin" Deck.
Markiere wichtige Begriffe und Konzepte als Lücken.
Verwende maximal 3 Lücken pro Karte.
```

---

## 7. Basic with Deck Reference Tags

**Verwendung:** Basic-Karte mit Deck-Referenzen

**Felder:**
- `Front`
- `Back`
- `Deck Reference Tags` - Verweise auf andere Decks

**Beispiel für Claude:**
```
Erstelle eine "Basic with Deck Reference Tags" im Deck "Anatomie":
Front: Wo befindet sich das Herz?
Back: Im Brustkorb, leicht links versetzt
Deck Reference Tags: Herz-Kreislauf::Anatomie
```

---

## 8. Basic with Reference Image

**Verwendung:** Basic-Karte mit Referenzbild

**Felder:**
- `Front`
- `Back`
- `Reference Image` - Bild als Referenz

**Beispiel für Claude:**
```
Erstelle eine "Basic with Reference Image" im Deck "Kunst":
Front: Wer malte die Mona Lisa?
Back: Leonardo da Vinci
Reference Image: [Bild der Mona Lisa]
```

---

## 9. Cloze Reference Tag

**Verwendung:** Cloze-Karte mit Referenz-Tags

**Felder:**
- `Text` - Text mit Lücken
- `Back Extra` - Zusätzliche Infos
- `Reference Tag` - Referenzen

**Beispiel für Claude:**
```
Erstelle eine "Cloze Reference Tag" im Deck "Geschichte":
Text: Der {{c1::Erste Weltkrieg}} begann im Jahr {{c2::1914}}.
Back Extra: Endete 1918
Reference Tag: Weltkriege::20Jahrhundert
```

---

## 10. Image Occlusion

**Verwendung:** Bereiche in Bildern verdecken und abfragen

**Hinweis:** Benötigt das Image Occlusion Enhanced Addon

**Verwendung:**
- Bild hochladen
- Bereiche markieren, die verdeckt werden sollen
- Anki erstellt automatisch Karten für jeden verdeckten Bereich

**Perfekt für:**
- Anatomie-Diagramme
- Landkarten
- Diagramme und Charts
- Architektur

---

## Empfehlungen nach Anwendungsfall

### Vokabeln lernen
- **Basic (and reversed card)** - Für beidseitiges Lernen
- **Basic (type in the answer)** - Für exakte Schreibweise

### Fakten & Definitionen
- **Basic** - Einfache Frage-Antwort
- **Cloze** - Für Definitionen mit mehreren wichtigen Begriffen

### Multiple Choice Tests vorbereiten
- **AllInOne (kprim, mc, sc)** - Verschiedene MC-Formate
- Typ 1 (mc) für mehrere richtige Antworten
- Typ 2 (sc) für nur eine richtige Antwort

### Medizin/Anatomie
- **Image Occlusion** - Für Diagramme
- **Cloze** - Für Prozesse und Zusammenhänge
- **AllInOne** - Für Prüfungsvorbereitung

### Programmierung
- **Basic (type in the answer)** - Für Syntax
- **Cloze** - Für Code-Snippets mit Lücken
- **Basic** - Für Konzepte

### Sprachen
- **Basic (and reversed card)** - Vokabeln
- **Basic (type in the answer)** - Rechtschreibung
- **Cloze** - Grammatik und Satzstrukturen

---

## Batch-Erstellung aus PDF - Universal-Befehl

```
[PDF hochladen in Claude]

Analysiere dieses PDF und erstelle 20 Karten für mein "[Deckname]" Deck.

Verwende folgende Kartentypen:
- 60% Basic - für einfache Fakten
- 30% Cloze - für Definitionen und Prozesse
- 10% AllInOne (mc) - für wichtige Konzepte als Multiple Choice

Achte auf:
- Klare, präzise Fragen
- Nicht zu viele Informationen pro Karte
- Logische Progression vom Einfachen zum Komplexen
```

---

## Tipps für effektive Karten

### Allgemein
1. **Eine Karte, ein Konzept** - Nicht zu viel auf einmal
2. **Klare Fragen** - Eindeutig formuliert
3. **Kurze Antworten** - Leichter zu merken
4. **Kontext hinzufügen** - Nutzen Sie "Back Extra" Felder

### Bei Cloze-Karten
- Maximal 3 Lücken pro Karte
- Wichtigste Begriffe zuerst
- Nicht ganze Sätze als Lücke

### Bei Multiple Choice
- 4-5 Antwortmöglichkeiten optimal
- Plausible falsche Antworten
- Nicht zu offensichtlich

### Bei Basic-Karten
- Fragen Sie "Was?", "Wer?", "Wann?", "Wo?"
- Vermeiden Sie "Warum?" (zu komplex für eine Karte)

---

## Zusammenfassung

**Für Claude Desktop sagen Sie einfach:**

"Erstelle Karten aus diesem PDF mit [Kartentyp]"

Claude:
1. ✅ Liest das PDF
2. ✅ Analysiert den Inhalt
3. ✅ Erstellt passende Karten
4. ✅ Speichert sie in Anki

**Kein Code, keine Konfiguration - nur natürliche Sprache!** 🎉
