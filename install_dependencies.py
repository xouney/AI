#!/usr/bin/env python3
"""
Script d'installation automatique des dépendances
"""

import subprocess
import sys
import os

def install_package(package):
    """Installe un package Python"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🔧 Installation des dépendances pour l'application IA Desktop")
    print("=" * 60)
    
    # Liste des dépendances requises
    dependencies = [
        "chardet>=5.0.0"
    ]
    
    print("📦 Dépendances à installer:")
    for dep in dependencies:
        print(f"  - {dep}")
    
    print("\n🚀 Début de l'installation...")
    
    success_count = 0
    for dep in dependencies:
        print(f"\n📥 Installation de {dep}...")
        if install_package(dep):
            print(f"✅ {dep} installé avec succès")
            success_count += 1
        else:
            print(f"❌ Échec de l'installation de {dep}")
    
    print(f"\n📊 Résultat: {success_count}/{len(dependencies)} dépendances installées")
    
    if success_count == len(dependencies):
        print("🎉 Toutes les dépendances ont été installées avec succès!")
        print("\n🚀 Vous pouvez maintenant lancer l'application avec:")
        print("   python run_app.py")
    else:
        print("⚠️  Certaines dépendances n'ont pas pu être installées.")
        print("   Essayez d'installer manuellement avec: pip install chardet")
    
    input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
