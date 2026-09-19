# Projekt Roadmap: Todo Sync App

## Projektziele
- Entwicklung einer TODO-App für Android und Linux (Manjaro)
- Synchronisation über Heimnetzwerk mit Raspberry Pi Backend (192.168.2.2)
- Last Write Wins Konfliktlösung
- Anzeige von Logs zur Konfliktlösung in beiden GUIs

## Phase 1: Projektstruktur und Basisarchitektur
### Akzeptanzkriterien:
- Projektstruktur definiert
- Grundlegende Architektur implementiert
- README.md und ROADMAP.md erstellt
- Svelte 5 Frontend mit Tauri 2.0 Scaffold
- FastAPI Backend mit SQLite Datenbank
- REST API Endpunkte implementiert
- WebSocket Synchronisationsmechanismus funktioniert

### Tasks:
- [x] Projektstruktur definieren
- [x] README.md erstellt
- [x] ROADMAP.md erstellt
- [ ] Tauri 2.0 Frontend Setup
- [ ] FastAPI Backend Setup
- [ ] REST API Endpunkte implementieren
- [ ] WebSocket Synchronisation implementieren

## Phase 2: Backend Implementierung (Raspberry Pi)
### Akzeptanzkriterien:
- Vollständiges FastAPI Backend implementiert
- SQLite Datenbank mit WAL Mode
- REST CRUD Endpunkte funktionieren
- WebSocket Synchronisation implementiert
- Last Write Wins Strategie umgesetzt

### Tasks:
- [ ] FastAPI Backend vollständig implementieren
- [ ] Datenbankanbindung mit SQLite (WAL)
- [ ] REST Endpunkte für TODOs implementieren
- [ ] WebSocket Endpunkt für Synchronisation
- [ ] LWW Konfliktlösung implementieren
- [ ] Conflict Logs implementieren

## Phase 3: Android App Entwicklung
### Akzeptanzkriterien:
- Tauri Android App gebaut und getestet
- UI für TODOs implementiert
- Backend Integration
- Synchronisation mit Raspberry Pi Backend funktioniert
- Konflikt-Logs in GUI angezeigt

### Tasks:
- [ ] Android Build konfigurieren
- [ ] UI Komponenten für TODOs erstellen
- [ ] Backend API Integration
- [ ] Synchronisationsmechanismus implementieren
- [ ] Conflict Logs anzeigen
- [ ] Testing auf Android-Gerät

## Phase 4: Linux App Entwicklung
### Akzeptanzkriterien:
- Tauri Linux App gebaut und getestet
- UI für TODOs implementiert
- Backend Integration
- Synchronisation mit Raspberry Pi Backend funktioniert
- Konflikt-Logs in GUI angezeigt

### Tasks:
- [ ] Linux Build konfigurieren
- [ ] UI Komponenten für TODOs erstellen
- [ ] Backend API Integration
- [ ] Synchronisationsmechanismus implementieren
- [ ] Conflict Logs anzeigen
- [ ] Testing auf Linux-Maschine

## Phase 5: Synchronisation & Konfliktlösung
### Akzeptanzkriterien:
- Vollständige Synchronisation zwischen Android und Linux App
- Last Write Wins Strategie korrekt implementiert
- Konflikte werden erkannt und geloggt
- GUI Logs sind in beiden Apps verfügbar
- Performance optimiert

### Tasks:
- [ ] Synchronisationsmechanismus testen
- [ ] LWW Strategie überprüfen
- [ ] Konfliktlogging implementieren
- [ ] GUI Display für Konflikte
- [ ] Performance Testing
- [ ] Benutzerfreundlichkeit optimieren

## Phase 6: Testing, Dokumentation, Optimierung
### Akzeptanzkriterien:
- Alle Tests bestanden
- Vollständige Dokumentation
- Anwenderhandbuch erstellt
- Optimierungen implementiert
- Deployment-Prozess dokumentiert

### Tasks:
- [ ] Unit Testing
- [ ] Integration Testing
- [ ] End-to-end Testing
- [ ] Benutzerhandbuch erstellen
- [ ] Performance Optimierung
- [ ] Deployment Dokumentation
- [ ] Projektabschluss