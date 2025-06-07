import os
from typing import Optional

class EditorCore:
    def __init__(self):
        self.current_file: Optional[str] = None
        self.is_modified: bool = False
        self.encoding: str = 'utf-8'

    def new_file(self):
        """ cria novo arquivo """
        self.current_file = None
        self.is_modified = False
    
    def open_file(self, filepath: str) -> str:
        """ abrir arquivo existente """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        try:
            with open(filepath, 'r', encoding=self.encoding) as file:
                content = file.read()

            self.current_file = filepath
            self.is_modified = False

            return content
        
        except UnicodeDecodeError:
            try:
                with open(filepath, 'r', encoding='latin-1') as file:
                    content = file.read()
                    
                self.current_file = filepath
                self.is_modified = False
                
                return content
                
            except Exception as e:
                raise Exception(f"Error reading file: {str(e)}")
            
        except Exception as e:
            raise Exception(f"Error opening file: {str(e)}")

    def save_file(self, content: str, filepath: Optional[str] = None) -> bool:
        """ salvar arquivo """
        target_file = filepath or self.current_file

        if not target_file:
            raise ValueError("No file path specified")
        
        try:
            directory = os.path.dirname(target_file)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            with open(target_file, 'w', encoding=self.encoding) as file:
                file.write(content)

            self.current_file = target_file
            self.is_modified = False

            return True
        
        except Exception as e:
            raise Exception(f"Error saving file: {str(e)}")
        
    def get_file_info(self) -> dict:
        """ retorna informações sobre o arquivo atual """
        if not self.current_file:
            return {
                'name': 'No title',
                'path': None,
                'size': 0,
                'modified': self.is_modified
            }
        
        try:
            stat = os.stat(self.current_file)
            return {
                'name': os.path.basename(self.current_file),
                'path': self.current_file,
                'size': stat.st_size,
                'modified': self.is_modified
            }
        except:
            return {
                'name': os.path.basename(self.current_file),
                'path': self.current_file,
                'size': 0,
                'modified': self.is_modified
            }


