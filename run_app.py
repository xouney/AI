#!/usr/bin/env python3
"""
Script de lancement pour l'application IA Desktop
"""

import sys
import os
from pathlib import Path

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    missing_deps = []
    
    try:
        import tkinter
    except ImportError:
        missing_deps.append("tkinter (généralement inclus avec Python)")
    
    try:
        import chardet
    except ImportError:
        missing_deps.append("chardet")
    
    if missing_deps:
        print("❌ Dépendances manquantes:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\nPour installer les dépendances manquantes:")
        print("pip install chardet")
        return False
    
    return True

def check_files():
    """Vérifie que tous les fichiers nécessaires sont présents"""
    required_files = [
        'main.py',
        'ai_engine.py', 
        'file_processor.py',
        'training_manager.py'
    ]
    
    missing_files = []
    current_dir = Path(__file__).parent
    
    for file in required_files:
        if not (current_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Fichiers manquants:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    
    return True

def main():
    """Fonction principale de lancement"""
    print("🚀 Lancement de l'application IA Desktop...")
    print("=" * 50)
    
    # Vérifications préliminaires
    if not check_dependencies():
        input("\nAppuyez sur Entrée pour quitter...")
        return
    
    if not check_files():
        input("\nAppuyez sur Entrée pour quitter...")
        return
    
    print("✅ Toutes les vérifications sont passées")
    print("📱 Lancement de l'interface graphique...")
    
    try:
        # Import et lancement de l'application
        from main import main as app_main
        app_main()
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        print(f"Type d'erreur: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        input("\nAppuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main()
