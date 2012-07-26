from ConfigParser import SafeConfigParser

"""
    class Config
    Configuration class used to handle reading from the config file (config.ini).
    
    Usage:
    - To initialize and load the configuration into memory:
        config = config.Config()
    
    - To retrieve an item from the config, you can do this:
        1. Retrieve an option's value:
            config['section_name']['option_name']
        2. Retrieve an entire section:
            config['section_name']
    
        If you call config['section_name'] and no section exists, or you call an option that doesn't exist, return data is {'' : ''} (empty)
        
    - To dump all the configuration information:
        config.dump()
"""
class Config:
    """
        Initialize the config class and parse the config file.
    """
    def __init__(self, path=os.path.normpath(os.getcwd()), filename="config.ini"):
        # Default config file: <current directory of script>/config.ini
        self.file = "%s/%s" % (path, filename)
        
        # Initialize the ini parser class
        self.parser = SafeConfigParser()
        
        # Read and parse the ini file
        self.parser.read(self.file)
        
        # We initially have an empty config to deal with
        self.config = {}
        
        # So we don't initialize this every...damn...time.
        val = ""
        
        # Loop through each section in the ini file
        for section in self.parser.sections():
            # Create an empty dictionary entry for each entry (otherwise: exceptions)
            self.config.update({section : dict()})
            
            # Loop through each option in the section
            for option in self.parser.options(section):
                # Get the value of the option (just done for clarity)
                val = self.parser.get(section, option)
                
                # Store the new 'option' : 'option val' dictionary entry into the section dictionary
                self.config[section].update({ option : val })
    
    """
        Retrieve an item from the configuration.
    """
    def __getitem__(self, section, option=None):
        # First we MUST have a section name given, and only continue if it's valid
        if self.config.has_key(section):
            # If an option key was given and it exists, return the value
            if option != None and self.config[section].has_key(option):
                return self.config[section][option]
            else if option == None:
                # No option was given, user wants just the section data
                return self.config[section]
            else:
                # No option was found, even tho it was requested, return empty string
                return ""
        else:
            return {'' : ''}
    
    """
        Simply returns a dump of the config file.  Primarily for debugging purposes.
    """
    def dump(self):
        print self.config
    
    def file(self):
        return self.file
