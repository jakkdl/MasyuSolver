
import configparser
import os

# Wrapper class for managing the configuration values stored
# in the configuration file
class ConfigMgr():

    # Class variables
    __configFileName = None
    __configFileDirectory = None
    __fullPath = None
    __configParser = None

    @classmethod
    # Method for loading the settings file
    def loadSettings(cls, directory, fileName):
        # Create the configParser object
        cls.__configParser = configparser.ConfigParser()

        # Read in the settings store in the config file
        cls.__fullPath = os.path.join(directory, fileName)
        cls.__configParser.read(cls.__fullPath)

        # Save the filename and directory, in case we need to update the file later
        cls.__configFileDirectory = directory
        cls.__configFileName = fileName

    @classmethod
    # Method for updating a configuration setting.  Also updates
    # the settings file.
    def setSettingValue(cls, section, name, value):
        # If the section doesn't exist yet, then create it
        if not(cls.__configParser.has_section(section)):
            cls.__configParser.add_section(section)

        # Add the value to the indicated section
        cls.__configParser.set(section, name, value)

        # Update the configuration file
        # But we need to create the directory hierarchy, if it doesn't exist!
        if not(os.path.exists(cls.__configFileDirectory)):
            os.makedirs(cls.__configFileDirectory)

        # Now write out the configuration settings
        with open(cls.__fullPath, 'w') as f:
            cls.__configParser.write(f)

    @classmethod
    # Method for retrieving the value of a configuration setting.
    # Returns 'None' if the setting isn't defined
    def getSettingValue(cls, section, name):
        try:
            # Attempt to retrieve the setting from the indicated section
            value = cls.__configParser.get(section, name)
        except Exception as e:
            # Value is not defined!
            value = None
        finally:
            return(value)

if (__name__ == "__main__"):
    print("Testing")
    basePath = os.path.expandvars('$APPDATA')
    appBasePath = os.path.join(basePath, 'ConfigFileTest')
    print("appBasePath =", appBasePath)
    settingsFileName = 'configTestFile.ini'

    print("loadSettings('configTestFile.ini')", ConfigMgr.loadSettings(appBasePath, settingsFileName))

    print("getSettingValue('foo', 'bar')", ConfigMgr.getSettingValue('foo', 'bar'))

    print("setSettingValue('foo', 'bar', 'baz')", ConfigMgr.setSettingValue('foo', 'bar', 'baz'))

    print("getSettingValue('foo', 'bar')", ConfigMgr.getSettingValue('foo', 'bar'))

