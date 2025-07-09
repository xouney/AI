import os
import mimetypes
from pathlib import Path
from typing import List, Dict, Callable, Any
import chardet

class FileProcessor:
    def __init__(self):
        self.supported_extensions = {
            # Langages de programmation
            '.py', '.js', '.java', '.cpp', '.c', '.h', '.hpp',
            '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt',
            '.ts', '.jsx', '.tsx', '.vue', '.scala', '.r',
            '.m', '.mm', '.pl', '.sh', '.bat', '.ps1',
            
            # Web
            '.html', '.htm', '.css', '.scss', '.sass', '.less',
            '.xml', '.json', '.yaml', '.yml',
            
            # Base de données
            '.sql', '.sqlite', '.db',
            
            # Configuration
            '.ini', '.cfg', '.conf', '.config', '.toml',
            '.properties', '.env',
            
            # Documentation
            '.md', '.txt', '.rst', '.tex',
            
            # Autres
            '.dockerfile', '.makefile', '.cmake'
        }
        
        self.binary_extensions = {
            '.exe', '.dll', '.so', '.dylib', '.bin', '.obj',
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico',
            '.mp3', '.mp4', '.avi', '.mov', '.wav', '.pdf',
            '.zip', '.rar', '.tar', '.gz', '.7z'
        }
    
    def process_directory(self, directory_path: str, progress_callback: Callable[[float], None] = None) -> List[Dict[str, Any]]:
        """Traite récursivement tous les fichiers d'un répertoire"""
        files_data = []
        all_files = list(Path(directory_path).rglob('*'))
        total_files = len([f for f in all_files if f.is_file()])
        
        processed_files = 0
        
        for file_path in all_files:
            if file_path.is_file():
                try:
                    file_data = self.process_file(str(file_path))
                    if file_data:
                        files_data.append(file_data)
                    
                    processed_files += 1
                    if progress_callback and total_files > 0:
                        progress = (processed_files / total_files) * 50  # 50% pour le traitement des fichiers
                        progress_callback(progress)
                        
                except Exception as e:
                    print(f"Erreur lors du traitement de {file_path}: {e}")
                    continue
        
        return files_data
    
    def process_file(self, file_path: str) -> Dict[str, Any]:
        """Traite un fichier individuel"""
        path_obj = Path(file_path)
        extension = path_obj.suffix.lower()
        
        # Ignorer les fichiers binaires non supportés
        if extension in self.binary_extensions:
            return None
        
        # Traiter seulement les extensions supportées ou les fichiers sans extension
        if extension not in self.supported_extensions and extension != '':
            # Vérifier si c'est un fichier texte par son contenu
            if not self.is_text_file(file_path):
                return None
        
        try:
            content = self.read_file_content(file_path)
            if content is None:
                return None
            
            file_data = {
                'path': file_path,
                'name': path_obj.name,
                'extension': extension,
                'size': path_obj.stat().st_size,
                'content': content,
                'encoding': self.detect_encoding(file_path),
                'line_count': len(content.split('\n')),
                'is_code': self.is_code_file(extension, content),
                'language': self.detect_file_language(extension, path_obj.name, content)
            }
            
            return file_data
            
        except Exception as e:
            print(f"Erreur lors de la lecture de {file_path}: {e}")
            return None
    
    def read_file_content(self, file_path: str) -> str:
        """Lit le contenu d'un fichier avec détection d'encodage"""
        try:
            # Tentative avec UTF-8 d'abord
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                # Détection automatique de l'encodage
                with open(file_path, 'rb') as f:
                    raw_data = f.read()
                    encoding = chardet.detect(raw_data)['encoding']
                    if encoding:
                        return raw_data.decode(encoding)
            except:
                pass
            
            # Dernière tentative avec latin-1
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except:
                return None
    
    def detect_encoding(self, file_path: str) -> str:
        """Détecte l'encodage d'un fichier"""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)  # Lire les premiers 10KB
                result = chardet.detect(raw_data)
                return result['encoding'] or 'utf-8'
        except:
            return 'utf-8'
    
    def is_text_file(self, file_path: str) -> bool:
        """Vérifie si un fichier est un fichier texte"""
        try:
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type and mime_type.startswith('text/'):
                return True
            
            # Vérification par échantillonnage
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                if b'\0' in chunk:  # Fichier binaire probable
                    return False
                
                # Vérifier le ratio de caractères imprimables
                printable_chars = sum(1 for byte in chunk if 32 <= byte <= 126 or byte in [9, 10, 13])
                return printable_chars / len(chunk) > 0.7 if chunk else False
                
        except:
            return False
    
    def is_code_file(self, extension: str, content: str) -> bool:
        """Détermine si un fichier contient du code"""
        code_extensions = {
            '.py', '.js', '.java', '.cpp', '.c', '.h', '.hpp',
            '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt',
            '.ts', '.jsx', '.tsx', '.scala', '.r', '.m', '.mm',
            '.pl', '.sh', '.bat', '.ps1', '.html', '.css', '.sql'
        }
        
        if extension in code_extensions:
            return True
        
        # Vérification par patterns de code
        code_patterns = [
            r'function\s+\w+', r'def\s+\w+', r'class\s+\w+',
            r'import\s+\w+', r'#include', r'<\?php',
            r'public\s+class', r'private\s+\w+', r'var\s+\w+',
            r'const\s+\w+', r'let\s+\w+'
        ]
        
        import re
        for pattern in code_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        return False
    
    def detect_file_language(self, extension: str, filename: str, content: str) -> str:
        """Détecte le langage de programmation d'un fichier"""
        # Mapping des extensions
        extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.cxx': 'cpp',
            '.cc': 'cpp',
            '.c': 'c',
            '.h': 'c',
            '.hpp': 'cpp',
            '.cs': 'csharp',
            '.php': 'php',
            '.rb': 'ruby',
            '.go': 'go',
            '.rs': 'rust',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.r': 'r',
            '.m': 'objective-c',
            '.mm': 'objective-c',
            '.pl': 'perl',
            '.sh': 'bash',
            '.bat': 'batch',
            '.ps1': 'powershell',
            '.html': 'html',
            '.htm': 'html',
            '.css': 'css',
            '.scss': 'scss',
            '.sass': 'sass',
            '.less': 'less',
            '.sql': 'sql',
            '.xml': 'xml',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.md': 'markdown',
            '.txt': 'text'
        }
        
        if extension in extension_map:
            return extension_map[extension]
        
        # Détection par nom de fichier
        filename_lower = filename.lower()
        if filename_lower in ['dockerfile', 'makefile', 'cmake']:
            return filename_lower
        
        # Détection par contenu (patterns basiques)
        if not content:
            return 'unknown'
        
        content_lower = content.lower()
        
        if '#!/usr/bin/env python' in content or 'import ' in content and 'def ' in content:
            return 'python'
        elif 'function(' in content or 'var ' in content or 'const ' in content:
            return 'javascript'
        elif 'public class' in content and 'static void main' in content:
            return 'java'
        elif '#include' in content and 'int main' in content:
            return 'c' if '.h"' in content else 'cpp'
        elif '<?php' in content:
            return 'php'
        elif 'SELECT' in content.upper() and 'FROM' in content.upper():
            return 'sql'
        
        return 'unknown'
    
    def get_file_stats(self, files_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Génère des statistiques sur les fichiers traités"""
        if not files_data:
            return {}
        
        stats = {
            'total_files': len(files_data),
            'total_size': sum(f['size'] for f in files_data),
            'total_lines': sum(f['line_count'] for f in files_data),
            'languages': {},
            'extensions': {},
            'code_files': sum(1 for f in files_data if f['is_code']),
            'largest_file': max(files_data, key=lambda x: x['size']),
            'most_lines': max(files_data, key=lambda x: x['line_count'])
        }
        
        # Statistiques par langage
        for file_data in files_data:
            lang = file_data['language']
            if lang not in stats['languages']:
                stats['languages'][lang] = {'count': 0, 'lines': 0, 'size': 0}
            
            stats['languages'][lang]['count'] += 1
            stats['languages'][lang]['lines'] += file_data['line_count']
            stats['languages'][lang]['size'] += file_data['size']
        
        # Statistiques par extension
        for file_data in files_data:
            ext = file_data['extension'] or 'no_extension'
            if ext not in stats['extensions']:
                stats['extensions'][ext] = 0
            stats['extensions'][ext] += 1
        
        return stats
