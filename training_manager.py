from typing import List, Dict, Any, Callable
import json
import time
from ai_engine import AIEngine

class TrainingManager:
    def __init__(self, ai_engine: AIEngine):
        self.ai_engine = ai_engine
        self.training_history = []
    
    def train(self, files_data: List[Dict[str, Any]], progress_callback: Callable[[float], None] = None):
        """Entraîne l'IA avec les données des fichiers"""
        if not files_data:
            raise ValueError("Aucune donnée de fichier fournie pour l'entraînement")
        
        total_files = len(files_data)
        start_time = time.time()
        
        # Phase 1: Apprentissage des patterns (50-80%)
        for i, file_data in enumerate(files_data):
            if file_data['is_code'] and file_data['content']:
                self.ai_engine.learn_from_code(file_data['content'], file_data['path'])
            
            if progress_callback:
                progress = 50 + (i / total_files) * 30  # 50% à 80%
                progress_callback(progress)
        
        # Phase 2: Optimisation de la base de connaissances (80-90%)
        if progress_callback:
            progress_callback(80)
        
        self.optimize_knowledge_base()
        
        # Phase 3: Sauvegarde (90-100%)
        if progress_callback:
            progress_callback(90)
        
        self.ai_engine.save_knowledge_base()
        
        # Enregistrement de l'historique d'entraînement
        training_session = {
            'timestamp': time.time(),
            'duration': time.time() - start_time,
            'files_processed': total_files,
            'code_files': sum(1 for f in files_data if f['is_code']),
            'languages_learned': list(self.ai_engine.knowledge_base.keys()),
            'total_lines': sum(f['line_count'] for f in files_data if f['is_code'])
        }
        
        self.training_history.append(training_session)
        self.save_training_history()
        
        if progress_callback:
            progress_callback(100)
    
    def optimize_knowledge_base(self):
        """Optimise la base de connaissances après l'entraînement"""
        for language in self.ai_engine.knowledge_base:
            kb = self.ai_engine.knowledge_base[language]
            
            # Limiter le nombre d'éléments stockés pour éviter la surcharge mémoire
            if len(kb['functions']) > 1000:
                # Garder les plus fréquents (simulation)
                kb['functions'] = set(list(kb['functions'])[:1000])
            
            if len(kb['classes']) > 500:
                kb['classes'] = set(list(kb['classes'])[:500])
            
            if len(kb['imports']) > 200:
                kb['imports'] = set(list(kb['imports'])[:200])
            
            # Mettre à jour les patterns courants
            self.ai_engine.update_common_patterns(language)
    
    def get_training_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques d'entraînement"""
        if not self.training_history:
            return {'message': 'Aucun entraînement effectué'}
        
        latest_session = self.training_history[-1]
        total_sessions = len(self.training_history)
        total_files = sum(session['files_processed'] for session in self.training_history)
        total_duration = sum(session['duration'] for session in self.training_history)
        
        return {
            'total_sessions': total_sessions,
            'total_files_processed': total_files,
            'total_training_time': total_duration,
            'latest_session': latest_session,
            'languages_in_kb': len(self.ai_engine.knowledge_base),
            'knowledge_base_size': sum(
                len(kb.get('functions', [])) + len(kb.get('classes', [])) + len(kb.get('imports', []))
                for kb in self.ai_engine.knowledge_base.values()
            )
        }
    
    def save_training_history(self):
        """Sauvegarde l'historique d'entraînement"""
        try:
            with open('training_history.json', 'w') as f:
                json.dump(self.training_history, f, indent=2)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de l'historique: {e}")
    
    def load_training_history(self):
        """Charge l'historique d'entraînement"""
        try:
            with open('training_history.json', 'r') as f:
                self.training_history = json.load(f)
        except FileNotFoundError:
            self.training_history = []
        except Exception as e:
            print(f"Erreur lors du chargement de l'historique: {e}")
            self.training_history = []
