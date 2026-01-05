import json
import os
import sys

class Config:
    """Configuration loader with error handling"""
    
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config_data = None
        self.load_config()
    
    def load_config(self):
        """Load configuration from JSON file"""
        try:
            # Check if config file exists
            if not os.path.exists(self.config_file):
                raise FileNotFoundError(f"Configuration file '{self.config_file}' not found")
            
            # Read and parse JSON
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config_data = json.load(f)
            
            # Validate required fields
            self._validate_config()
            
        except FileNotFoundError as e:
            print(f"ERROR: {e}")
            print("Please create config.json file in the root directory")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON format in config file: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"ERROR: Failed to load configuration: {e}")
            sys.exit(1)
    
    def _validate_config(self):
        """Validate that all required configuration fields are present"""
        required_fields = ['database']
        for field in required_fields:
            if field not in self.config_data:
                raise ValueError(f"Missing required configuration field: {field}")
        
        # Validate database config
        db_required = ['host', 'database', 'user', 'password']
        for field in db_required:
            if field not in self.config_data['database']:
                raise ValueError(f"Missing required database field: {field}")
    
    def get_database_config(self):
        """Get database configuration"""
        return self.config_data['database']
    
    def get(self, key, default=None):
        """Get configuration value by key"""
        return self.config_data.get(key, default)
