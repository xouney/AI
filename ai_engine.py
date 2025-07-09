import re
import json
from collections import defaultdict
from typing import Dict, List, Any
import pickle
import os

class AIEngine:
    def __init__(self):
        self.knowledge_base = defaultdict(dict)
        self.language_patterns = {
            'python': [r'def\s+\w+', r'import\s+\w+', r'class\s+\w+', r'if\s+__name__\s*==\s*["\']__main__["\']'],
            'javascript': [r'function\s+\w+', r'const\s+\w+', r'let\s+\w+', r'var\s+\w+', r'=>'],
            'java': [r'public\s+class', r'private\s+\w+', r'public\s+static\s+void\s+main'],
            'cpp': [r'#include\s*<\w+>', r'int\s+main\s*\(', r'std::', r'cout\s*<<'],
            'c': [r'#include\s*<\w+\.h>', r'int\s+main\s*\(', r'printf\s*\('],
            'html': [r'<html>', r'<head>', r'<body>', r'<div>', r'<!DOCTYPE'],
            'css': [r'\w+\s*{', r':\s*\w+;', r'@media', r'#\w+'],
            'sql': [r'SELECT\s+', r'FROM\s+', r'WHERE\s+', r'INSERT\s+INTO', r'CREATE\s+TABLE'],
            'php': [r'<\?php', r'\$\w+', r'function\s+\w+', r'class\s+\w+'],
            'ruby': [r'def\s+\w+', r'class\s+\w+', r'require\s+', r'puts\s+'],
            'go': [r'package\s+\w+', r'func\s+\w+', r'import\s+', r'var\s+\w+'],
            'rust': [r'fn\s+\w+', r'let\s+\w+', r'use\s+\w+', r'struct\s+\w+'],
            'swift': [r'func\s+\w+', r'var\s+\w+', r'let\s+\w+', r'class\s+\w+'],
            'kotlin': [r'fun\s+\w+', r'val\s+\w+', r'var\s+\w+', r'class\s+\w+'],
            'typescript': [r'interface\s+\w+', r'type\s+\w+', r'function\s+\w+', r':\s*\w+'],
        }
        
        self.code_patterns = {
            'functions': r'(?:def|function|func|fn)\s+(\w+)',
            'classes': r'(?:class|struct)\s+(\w+)',
            'variables': r'(?:var|let|const|val)\s+(\w+)',
            'imports': r'(?:import|include|require|use)\s+([^\s;]+)',
            'comments': r'(?://.*|/\*.*?\*/|#.*|<!--.*?-->)',
        }
        
        self.load_knowledge_base()
    
    def detect_language(self, code: str) -> str:
        """Détecte le langage de programmation du code"""
        scores = defaultdict(int)
        
        for language, patterns in self.language_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, code, re.IGNORECASE | re.MULTILINE)
                scores[language] += len(matches)
        
        if not scores:
            return 'unknown'
        
        return max(scores, key=scores.get)
    
    def extract_code_features(self, code: str) -> Dict[str, Any]:
        """Extrait les caractéristiques du code"""
        features = {
            'language': self.detect_language(code),
            'functions': [],
            'classes': [],
            'variables': [],
            'imports': [],
            'comments': [],
            'lines_count': len(code.split('\n')),
            'complexity_score': 0
        }
        
        # Extraction des éléments
        for feature_type, pattern in self.code_patterns.items():
            matches = re.findall(pattern, code, re.IGNORECASE | re.MULTILINE)
            features[feature_type] = matches
        
        # Calcul de la complexité
        features['complexity_score'] = self.calculate_complexity(code)
        
        return features
    
    def calculate_complexity(self, code: str) -> int:
        """Calcule un score de complexité basique"""
        complexity = 0
        
        # Structures de contrôle
        control_structures = ['if', 'else', 'elif', 'for', 'while', 'switch', 'case', 'try', 'catch']
        for structure in control_structures:
            complexity += len(re.findall(rf'\b{structure}\b', code, re.IGNORECASE))
        
        # Fonctions et méthodes
        complexity += len(re.findall(r'(?:def|function|func|fn)\s+\w+', code, re.IGNORECASE))
        
        # Classes
        complexity += len(re.findall(r'(?:class|struct)\s+\w+', code, re.IGNORECASE)) * 2
        
        return complexity
    
    def analyze_code(self, code: str) -> str:
        """Analyse le code et retourne un rapport détaillé"""
        features = self.extract_code_features(code)
        
        analysis = []
        analysis.append("=== ANALYSE DU CODE ===\n")
        
        # Langage détecté
        analysis.append(f"Langage détecté: {features['language'].upper()}")
        analysis.append(f"Nombre de lignes: {features['lines_count']}")
        analysis.append(f"Score de complexité: {features['complexity_score']}\n")
        
        # Fonctions
        if features['functions']:
            analysis.append(f"Fonctions trouvées ({len(features['functions'])}):")
            for func in features['functions'][:10]:  # Limite à 10
                analysis.append(f"  - {func}")
            if len(features['functions']) > 10:
                analysis.append(f"  ... et {len(features['functions']) - 10} autres")
            analysis.append("")
        
        # Classes
        if features['classes']:
            analysis.append(f"Classes trouvées ({len(features['classes'])}):")
            for cls in features['classes'][:10]:
                analysis.append(f"  - {cls}")
            if len(features['classes']) > 10:
                analysis.append(f"  ... et {len(features['classes']) - 10} autres")
            analysis.append("")
        
        # Imports
        if features['imports']:
            analysis.append(f"Imports/Includes ({len(features['imports'])}):")
            for imp in features['imports'][:10]:
                analysis.append(f"  - {imp}")
            if len(features['imports']) > 10:
                analysis.append(f"  ... et {len(features['imports']) - 10} autres")
            analysis.append("")
        
        # Recommandations basées sur la base de connaissances
        recommendations = self.get_recommendations(features)
        if recommendations:
            analysis.append("=== RECOMMANDATIONS ===")
            for rec in recommendations:
                analysis.append(f"• {rec}")
            analysis.append("")
        
        # Analyse de qualité
        quality_analysis = self.analyze_code_quality(code, features)
        analysis.append("=== ANALYSE DE QUALITÉ ===")
        analysis.extend(quality_analysis)
        
        return "\n".join(analysis)
    
    def analyze_code_quality(self, code: str, features: Dict[str, Any]) -> List[str]:
        """Analyse la qualité du code"""
        quality_issues = []
        
        # Vérification de la longueur des lignes
        long_lines = [i+1 for i, line in enumerate(code.split('\n')) if len(line) > 100]
        if long_lines:
            quality_issues.append(f"Lignes trop longues (>100 caractères): {len(long_lines)} lignes")
        
        # Vérification des commentaires
        comment_ratio = len(features['comments']) / max(features['lines_count'], 1)
        if comment_ratio < 0.1:
            quality_issues.append("Peu de commentaires détectés (< 10% des lignes)")
        
        # Vérification de la complexité
        if features['complexity_score'] > 20:
            quality_issues.append("Complexité élevée détectée - considérer la refactorisation")
        
        # Vérification des noms de variables courtes
        short_vars = [var for var in features['variables'] if len(var) < 3 and var not in ['i', 'j', 'k', 'x', 'y', 'z']]
        if short_vars:
            quality_issues.append(f"Variables avec noms courts: {', '.join(short_vars[:5])}")
        
        if not quality_issues:
            quality_issues.append("✓ Aucun problème de qualité majeur détecté")
        
        return quality_issues
    
    def get_recommendations(self, features: Dict[str, Any]) -> List[str]:
        """Génère des recommandations basées sur la base de connaissances"""
        recommendations = []
        language = features['language']
        
        if language in self.knowledge_base:
            lang_knowledge = self.knowledge_base[language]
            
            # Recommandations basées sur les patterns appris
            if 'common_patterns' in lang_knowledge:
                recommendations.append(f"Patterns courants en {language}: {', '.join(lang_knowledge['common_patterns'][:3])}")
            
            if 'best_practices' in lang_knowledge:
                recommendations.extend(lang_knowledge['best_practices'][:2])
        
        return recommendations
    
    def learn_from_code(self, code: str, file_path: str = ""):
        """Apprend à partir du code analysé"""
        features = self.extract_code_features(code)
        language = features['language']
        
        if language not in self.knowledge_base:
            self.knowledge_base[language] = {
                'patterns': defaultdict(int),
                'functions': set(),
                'classes': set(),
                'imports': set(),
                'file_count': 0,
                'total_lines': 0,
                'common_patterns': [],
                'best_practices': []
            }
        
        kb = self.knowledge_base[language]
        
        # Mise à jour des statistiques
        kb['file_count'] += 1
        kb['total_lines'] += features['lines_count']
        
        # Apprentissage des patterns
        for func in features['functions']:
            kb['functions'].add(func)
        
        for cls in features['classes']:
            kb['classes'].add(cls)
        
        for imp in features['imports']:
            kb['imports'].add(imp)
        
        # Mise à jour des patterns courants
        self.update_common_patterns(language)
    
    def update_common_patterns(self, language: str):
        """Met à jour les patterns courants pour un langage"""
        if language in self.knowledge_base:
            kb = self.knowledge_base[language]
            
            # Les fonctions les plus communes
            common_functions = list(kb['functions'])[:10]
            kb['common_patterns'] = common_functions
            
            # Bonnes pratiques basiques
            kb['best_practices'] = [
                f"Utilisez des noms de fonctions descriptifs comme: {', '.join(common_functions[:3])}",
                f"Organisez votre code avec des classes appropriées",
                f"Documentez vos fonctions importantes"
            ]
    
    def save_knowledge_base(self):
        """Sauvegarde la base de connaissances"""
        try:
            # Conversion des sets en listes pour la sérialisation
            serializable_kb = {}
            for lang, data in self.knowledge_base.items():
                serializable_kb[lang] = {}
                for key, value in data.items():
                    if isinstance(value, set):
                        serializable_kb[lang][key] = list(value)
                    elif isinstance(value, defaultdict):
                        serializable_kb[lang][key] = dict(value)
                    else:
                        serializable_kb[lang][key] = value
            
            with open('knowledge_base.pkl', 'wb') as f:
                pickle.dump(serializable_kb, f)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
    
    def load_knowledge_base(self):
        """Charge la base de connaissances"""
        try:
            if os.path.exists('knowledge_base.pkl'):
                with open('knowledge_base.pkl', 'rb') as f:
                    loaded_kb = pickle.load(f)
                
                # Reconversion des listes en sets
                for lang, data in loaded_kb.items():
                    self.knowledge_base[lang] = {}
                    for key, value in data.items():
                        if key in ['functions', 'classes', 'imports']:
                            self.knowledge_base[lang][key] = set(value)
                        elif key == 'patterns':
                            self.knowledge_base[lang][key] = defaultdict(int, value)
                        else:
                            self.knowledge_base[lang][key] = value
        except Exception as e:
            print(f"Erreur lors du chargement: {e}")
