import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from pathlib import Path
import sys

# Ajoutez cette vérification au début
try:
    from ai_engine import AIEngine
    from file_processor import FileProcessor  
    from training_manager import TrainingManager
except ImportError as e:
    print(f"Erreur d'import: {e}")
    print("Assurez-vous que tous les fichiers sont dans le même dossier")
    sys.exit(1)

class AIDesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IA Universelle - Analyseur de Code")
        self.root.geometry("1200x800")
        
        # Initialisation des composants
        self.ai_engine = AIEngine()
        self.file_processor = FileProcessor()
        self.training_manager = TrainingManager(self.ai_engine)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuration du grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Titre
        title_label = ttk.Label(main_frame, text="IA Universelle - Analyseur de Code", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Section d'entraînement
        training_frame = ttk.LabelFrame(main_frame, text="Entraînement", padding="10")
        training_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        training_frame.columnconfigure(1, weight=1)
        
        ttk.Button(training_frame, text="Sélectionner Dossier", 
                  command=self.select_training_folder).grid(row=0, column=0, padx=(0, 10))
        
        self.folder_path_var = tk.StringVar()
        ttk.Entry(training_frame, textvariable=self.folder_path_var, 
                 state="readonly").grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(training_frame, text="Commencer Entraînement", 
                  command=self.start_training).grid(row=0, column=2)
        
        # Barre de progression
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(training_frame, variable=self.progress_var, 
                                          maximum=100)
        self.progress_bar.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Section d'analyse
        analysis_frame = ttk.LabelFrame(main_frame, text="Analyse de Code", padding="10")
        analysis_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        analysis_frame.columnconfigure(0, weight=1)
        analysis_frame.rowconfigure(1, weight=1)
        
        # Zone de saisie
        input_frame = ttk.Frame(analysis_frame)
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        ttk.Label(input_frame, text="Code à analyser:").grid(row=0, column=0, sticky=tk.W)
        
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=0, column=1, padx=(10, 0))
        
        ttk.Button(button_frame, text="Charger Fichier", 
                  command=self.load_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Analyser", 
                  command=self.analyze_code).pack(side=tk.LEFT)
        
        # Zone de texte pour le code
        self.code_text = scrolledtext.ScrolledText(analysis_frame, height=15, width=80)
        self.code_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Zone de résultats
        results_frame = ttk.LabelFrame(analysis_frame, text="Résultats d'Analyse", padding="10")
        results_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        results_frame.columnconfigure(0, weight=1)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=8, width=80)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Prêt")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def select_training_folder(self):
        folder_path = filedialog.askdirectory(title="Sélectionner le dossier d'entraînement")
        if folder_path:
            self.folder_path_var.set(folder_path)
    
    def start_training(self):
        folder_path = self.folder_path_var.get()
        if not folder_path:
            messagebox.showwarning("Attention", "Veuillez sélectionner un dossier d'entraînement")
            return
        
        # Lancer l'entraînement dans un thread séparé
        threading.Thread(target=self._train_ai, args=(folder_path,), daemon=True).start()
    
    def _train_ai(self, folder_path):
        try:
            self.status_var.set("Entraînement en cours...")
            self.progress_var.set(0)
            
            # Traitement des fichiers
            files_data = self.file_processor.process_directory(folder_path, self._update_progress)
            
            # Entraînement de l'IA
            self.training_manager.train(files_data, self._update_progress)
            
            self.status_var.set("Entraînement terminé avec succès")
            self.progress_var.set(100)
            messagebox.showinfo("Succès", "L'entraînement de l'IA est terminé!")
            
        except Exception as e:
            self.status_var.set("Erreur lors de l'entraînement")
            messagebox.showerror("Erreur", f"Erreur lors de l'entraînement: {str(e)}")
    
    def _update_progress(self, value):
        self.progress_var.set(value)
        self.root.update_idletasks()
    
    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Sélectionner un fichier de code",
            filetypes=[
                ("Tous les fichiers", "*.*"),
                ("Python", "*.py"),
                ("JavaScript", "*.js"),
                ("Java", "*.java"),
                ("C++", "*.cpp"),
                ("C", "*.c"),
                ("HTML", "*.html"),
                ("CSS", "*.css")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.code_text.delete(1.0, tk.END)
                    self.code_text.insert(1.0, content)
                    self.status_var.set(f"Fichier chargé: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de charger le fichier: {str(e)}")
    
    def analyze_code(self):
        code = self.code_text.get(1.0, tk.END).strip()
        if not code:
            messagebox.showwarning("Attention", "Veuillez entrer du code à analyser")
            return
        
        threading.Thread(target=self._analyze_code, args=(code,), daemon=True).start()
    
    def _analyze_code(self, code):
        try:
            self.status_var.set("Analyse en cours...")
            self.results_text.delete(1.0, tk.END)
            
            # Analyse du code
            analysis_result = self.ai_engine.analyze_code(code)
            
            # Affichage des résultats
            self.results_text.insert(tk.END, analysis_result)
            self.status_var.set("Analyse terminée")
            
        except Exception as e:
            self.status_var.set("Erreur lors de l'analyse")
            self.results_text.insert(tk.END, f"Erreur: {str(e)}")

def main():
    root = tk.Tk()
    app = AIDesktopApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
