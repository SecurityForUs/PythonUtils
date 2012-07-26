<html>
<head id="head"><script type="text/javascript">var NREUMQ=NREUMQ||[];NREUMQ.push(["mark","firstbyte",new Date().getTime()]);</script>
  <title>#4333668 - Pastie</title>
	<link rel="icon" type="image/gif" href="/images/pastie.gif">
	<link rel="SHORTCUT ICON" type="image/gif" href="/images/pastie.gif">
</head>
<body>
	
<pre>
from ConfigParser import SafeConfigParser<br/><br/>&quot;&quot;&quot;<br/>    class Config<br/>    Configuration class used to handle reading from the config file (config.ini).<br/>    <br/>    Usage:<br/>    - To initialize and load the configuration into memory:<br/>        config = config.Config()<br/>    <br/>    - To retrieve an item from the config, you can do this:<br/>        1. Retrieve an option's value:<br/>            config['section_name']['option_name']<br/>        2. Retrieve an entire section:<br/>            config['section_name']<br/>    <br/>        If you call config['section_name'] and no section exists, or you call an option that doesn't exist, return data is {'' : ''} (empty)<br/>        <br/>    - To dump all the configuration information:<br/>        config.dump()<br/>&quot;&quot;&quot;<br/>class Config:<br/>    &quot;&quot;&quot;<br/>        Initialize the config class and parse the config file.<br/>    &quot;&quot;&quot;<br/>    def __init__(self):<br/>        # Default config file: &lt;current directory of script&gt;/config.ini<br/>        self.file = &quot;%s/config.ini&quot; % os.path.normpath(os.getcwd())<br/>        <br/>        # Initialize the ini parser class<br/>        self.parser = SafeConfigParser()<br/>        <br/>        # Read and parse the ini file<br/>        self.parser.read(self.file)<br/>        <br/>        # We initially have an empty config to deal with<br/>        self.config = {}<br/>        <br/>        # So we don't initialize this every...damn...time.<br/>        val = &quot;&quot;<br/>        <br/>        # Loop through each section in the ini file<br/>        for section in self.parser.sections():<br/>            # Create an empty dictionary entry for each entry (otherwise: exceptions)<br/>            self.config.update({section : dict()})<br/>            <br/>            # Loop through each option in the section<br/>            for option in self.parser.options(section):<br/>                # Get the value of the option (just done for clarity)<br/>                val = self.parser.get(section, option)<br/>                <br/>                # Store the new 'option' : 'option val' dictionary entry into the section dictionary<br/>                self.config[section].update({ option : val })<br/>    <br/>    &quot;&quot;&quot;<br/>        Retrieve an item from the configuration.<br/>    &quot;&quot;&quot;<br/>    def __getitem__(self, section, option=None):<br/>        # First we MUST have a section name given, and only continue if it's valid<br/>        if self.config.has_key(section):<br/>            # If an option key was given and it exists, return the value<br/>            if option != None and self.config[section].has_key(option):<br/>                return self.config[section][option]<br/>            else if option == None:<br/>                # No option was given, user wants just the section data<br/>                return self.config[section]<br/>            else:<br/>                # No option was found, even tho it was requested, return empty string<br/>                return &quot;&quot;<br/>        else:<br/>            return {'' : ''}<br/>    <br/>    &quot;&quot;&quot;<br/>        Simply returns a dump of the config file.  Primarily for debugging purposes.<br/>    &quot;&quot;&quot;<br/>    def dump(self):<br/>        print self.config
</pre>

<script type="text/javascript">if (!NREUMQ.f) { NREUMQ.f=function() {
NREUMQ.push(["load",new Date().getTime()]);
var e=document.createElement("script");
e.type="text/javascript";e.async=true;e.src="https://d1ros97qkrwjf5.cloudfront.net/39/eum/rum.js";
document.body.appendChild(e);
if(NREUMQ.a)NREUMQ.a();
};
NREUMQ.a=window.onload;window.onload=NREUMQ.f;
};
NREUMQ.push(["nrfj","beacon-1.newrelic.com","4f1b2792f0",10734,"Jw4PQUVeXVxXRR8TUBcVBEYYRVRIRg==",0,10,new Date().getTime(),"","","","",""])</script></body>
</html>
