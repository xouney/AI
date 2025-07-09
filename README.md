# IA Desktop - Analyseur de Code Universel

Une application de bureau Python avec intelligence artificielle capable d'analyser et d'apprendre de tous types de fichiers et langages de programmation.

## 🚀 Installation et Lancement

### Méthode 1: Lancement rapide
\`\`\`bash
# 1. Installer les dépendances
python install_dependencies.py

# 2. Lancer l'application
python run_app.py
\`\`\`

### Méthode 2: Installation manuelle
\`\`\`bash
# 1. Installer les dépendances
pip install chardet

# 2. Lancer l'application directement
python main.py
\`\`\`

## 📋 Prérequis

- Python 3.8 ou supérieur
- tkinter (généralement inclus avec Python)
- chardet (pour la détection d'encodage)

## 🎯 Fonctionnalités

### Intelligence Artificielle
- ✅ Détection automatique de 20+ langages de programmation
- ✅ Apprentissage adaptatif à partir des dossiers fournis
- ✅ Analyse de qualité du code avec recommandations
- ✅ Base de connaissances persistante

### Support de Fichiers
- ✅ Python, JavaScript, Java, C++, C, HTML, CSS, SQL
- ✅ PHP, Ruby, Go, Rust, Swift, Kotlin, TypeScript
- ✅ Et bien d'autres langages...
- ✅ Détection intelligente d'encodage
- ✅ Traitement récursif de dossiers

### Interface Utilisateur
- ✅ Interface graphique intuitive
- ✅ Barre de progression pour l'entraînement
- ✅ Analyse de code en temps réel
- ✅ Rapports détaillés

## 📖 Utilisation

1. **Entraîner l'IA**:
   - Cliquez sur "Sélectionner Dossier"
   - Choisissez un dossier contenant vos projets de code
   - Cliquez sur "Commencer Entraînement"

2. **Analyser du code**:
   - Collez votre code dans la zone de texte
   - Ou cliquez sur "Charger Fichier"
   - Cliquez sur "Analyser"

3. **Consulter les résultats**:
   - L'IA détecte automatiquement le langage
   - Analyse les fonctions, classes, imports
   - Fournit des recommandations d'amélioration

## 🗂️ Structure des Fichiers

\`\`\`
ai-desktop-app/
├── main.py                 # Application principale
├── ai_engine.py           # Moteur d'intelligence artificielle
├── file_processor.py      # Traitement des fichiers
├── training_manager.py    # Gestionnaire d'entraînement
├── run_app.py            # Script de lancement
├── install_dependencies.py # Installation des dépendances
└── README.md             # Ce fichier
\`\`\`

## 🔧 Dépannage

### Erreur "No module named 'tkinter'"
- **Linux**: `sudo apt-get install python3-tk`
- **macOS**: tkinter est inclus avec Python
- **Windows**: tkinter est inclus avec Python

### Erreur "No module named 'chardet'"
\`\`\`bash
pip install chardet
\`\`\`

### L'application ne se lance pas
1. Vérifiez que Python 3.8+ est installé: `python --version`
2. Vérifiez que tous les fichiers sont présents
3. Lancez avec: `python run_app.py`

## 📊 Langages Supportés

| Langage | Extension | Support |
|---------|-----------|---------|
| Python | .py | ✅ Complet |
| JavaScript | .js, .jsx | ✅ Complet |
| TypeScript | .ts, .tsx | ✅ Complet |
| Java | .java | ✅ Complet |
| C++ | .cpp, .hpp | ✅ Complet |
| C | .c, .h | ✅ Complet |
| C# | .cs | ✅ Complet |
| PHP | .php | ✅ Complet |
| Ruby | .rb | ✅ Complet |
| Go | .go | ✅ Complet |
| Rust | .rs | ✅ Complet |
| Swift | .swift | ✅ Complet |
| Kotlin | .kt | ✅ Complet |
| HTML | .html, .htm | ✅ Complet |
| CSS | .css, .scss | ✅ Complet |
| SQL | .sql | ✅ Complet |
| Et plus... | | ✅ |

## 🤝 Contribution

Cette application est conçue pour être extensible. Vous pouvez facilement ajouter le support de nouveaux langages en modifiant les fichiers de configuration.

## 📄 Licence

MIT License - Libre d'utilisation et de modification.
\`\`\`

Créons aussi un script de test pour vérifier que tout fonctionne :

```python file="test_installation.py"
#!/usr/bin/env python3
"""
Script de test pour vérifier l'installation
"""

def test_imports():
    """Test des imports"""
    print("🧪 Test des imports...")
    
    try:
        import tkinter as tk
        print("✅ tkinter: OK")
    except ImportError as e:
        print(f"❌ tkinter: {e}")
        return False
    
    try:
        import chardet
        print("✅ chardet: OK")
    except ImportError as e:
        print(f"❌ chardet: {e}")
        return False
    
    try:
        from ai_engine import AIEngine
        print("✅ ai_engine: OK")
    except ImportError as e:
        print(f"❌ ai_engine: {e}")
        return False
    
    try:
        from file_processor import FileProcessor
        print("✅ file_processor: OK")
    except ImportError as e:
        print(f"❌ file_processor: {e}")
        return False
    
    try:
        from training_manager import TrainingManager
        print("✅ training_manager: OK")
    except ImportError as e:
        print(f"❌ training_manager: {e}")
        return False
    
    return True

def test_ai_engine():
    """Test du moteur IA"""
    print("\n🧠 Test du moteur IA...")
    
    try:
        from ai_engine import AIEngine
        ai = AIEngine()
        
        # Test de détection de langage
        python_code = "def hello():\n    print('Hello World')"
        language = ai.detect_language(python_code)
        print(f"✅ Détection de langage: {language}")
        
        # Test d'analyse
        analysis = ai.analyze_code(python_code)
        print("✅ Analyse de code: OK")
        
        return True
    except Exception as e:
        print(f"❌ Erreur dans le moteur IA: {e}")
        return False

def test_file_processor():
    """Test du processeur de fichiers"""
    print("\n📁 Test du processeur de fichiers...")
    
    try:
        from file_processor import FileProcessor
        processor = FileProcessor()
        
        # Test de détection de langage
        language = processor.detect_file_language('.py', 'test.py', 'def test(): pass')
        print(f"✅ Détection de langage de fichier: {language}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur dans le processeur de fichiers: {e}")
        return False

def main():
    print("🔍 Test de l'installation de l'application IA Desktop")
    print("=" * 55)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Imports
    if test_imports():
        tests_passed += 1
    
    # Test 2: Moteur IA
    if test_ai_engine():
        tests_passed += 1
    
    # Test 3: Processeur de fichiers
    if test_file_processor():
        tests_passed += 1
    
    print(f"\n📊 Résultats: {tests_passed}/{total_tests} tests réussis")
    
    if tests_passed == total_tests:
        print("🎉 Tous les tests sont passés! L'application est prête à être utilisée.")
        print("\n🚀 Lancez l'application avec: python run_app.py")
    else:
        print("⚠️  Certains tests ont échoué. Vérifiez l'installation.")
    
    input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
