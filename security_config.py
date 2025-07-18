import os
import sys
import logging
import hashlib
from datetime import datetime, timezone
from dotenv import load_dotenv

class SecurityError(Exception):
    """Custom exception for security-related errors"""
    pass

class BotSecurity:
    def __init__(self):
        self.setup_logging()
        load_dotenv()
        
        # Security validation
        self.token = self._validate_token()
        self.owner_id = self._validate_owner_id()
        self.environment = self._validate_environment()
        self.debug_mode = self._validate_debug_mode()
        
        # Log security status
        self._log_security_status()
    
    def setup_logging(self):
        """Configure secure logging (Windows compatible)"""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # Configure logging with UTF-8 encoding for Windows
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.StreamHandler(sys.stdout)
            ],
            force=True
        )
        
        # Set Discord logging to WARNING to reduce noise
        logging.getLogger('discord').setLevel(logging.WARNING)
        logging.getLogger('discord.http').setLevel(logging.WARNING)
    
    def _validate_token(self):
        """Validate Discord bot token"""
        # FIXED: Use the environment variable NAME, not the value!
        token = os.getenv('DISCORD_BOT_TOKEN')
        
        if not token:
            logging.critical("CRITICAL: No Discord bot token provided!")
            logging.critical("Create a .env file with DISCORD_BOT_TOKEN=your_token_here")
            raise SecurityError("Missing Discord bot token")
        
        # Basic token format validation
        if len(token) < 50:
            logging.critical("CRITICAL: Token appears to be invalid (too short)")
            raise SecurityError("Invalid token format")
        
        # Create token hash for logging (never log the actual token!)
        token_hash = hashlib.sha256(token.encode()).hexdigest()[:8]
        logging.info(f"Token validated successfully (hash: {token_hash})")
        
        return token
    
    def _validate_owner_id(self):
        """Validate bot owner ID"""
        # FIXED: Use the environment variable NAME, not the value!
        owner_id = os.getenv('BOT_OWNER_ID')
        
        if not owner_id:
            logging.warning("No bot owner ID set - admin commands will be disabled")
            return None
        
        try:
            owner_id = int(owner_id)
            logging.info(f"Bot owner ID validated: {owner_id}")
            return owner_id
        
        except ValueError:
            logging.error("Invalid BOT_OWNER_ID format (must be a number)")
            return None
    
    def _validate_environment(self):
        """Validate environment setting"""
        env = os.getenv('ENVIRONMENT', 'development').lower()
        
        valid_environments = ['development', 'production', 'testing']
        if env not in valid_environments:
            logging.warning(f"Unknown environment '{env}', using 'development'")
            env = 'development'
        
        logging.info(f"Environment: {env}")
        return env
    
    def _validate_debug_mode(self):
        """Validate debug mode setting"""
        debug = os.getenv('DEBUG_MODE', 'true').lower()
        debug_bool = debug in ['true', '1', 'yes', 'on']
        
        if self.environment == 'production' and debug_bool:
            logging.warning("WARNING: Debug mode enabled in production!")
        
        logging.info(f"Debug mode: {debug_bool}")
        return debug_bool
    
    def _log_security_status(self):
        """Log security status summary (Windows compatible)"""
        logging.info("=" * 50)
        logging.info("SECURITY STATUS SUMMARY")
        logging.info("=" * 50)
        logging.info(f"Environment: {self.environment}")
        logging.info(f"Debug Mode: {self.debug_mode}")
        logging.info(f"Owner ID Set: {'Yes' if self.owner_id else 'No'}")
        logging.info(f"Startup Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        logging.info("=" * 50)
    
    def is_owner(self, user_id):
        """Check if user is the bot owner"""
        return self.owner_id and user_id == self.owner_id
    
    def is_production(self):
        """Check if running in production"""
        return self.environment == 'production'
    
    def should_log_debug(self):
        """Check if debug logging should be enabled"""
        return self.debug_mode and self.environment != 'production'

# Initialize security config
security = BotSecurity()