#!/usr/bin/env python
# registerComponent.py -- interface for registering components in the ITk Production Database from the command line
# Created: 2018/08/07, Updated: 2019/03/28
# Written by Matthew Basso
import sys
from pprint import PrettyPrinter

from requests.exceptions import RequestException

from itk_pdb.databaseUtilities import Colours
from itk_pdb.databaseUtilities import ERROR
from itk_pdb.databaseUtilities import INFO
from itk_pdb.databaseUtilities import PROMPT
from itk_pdb.databaseUtilities import STATUS
from itk_pdb.databaseUtilities import WARNING
pp = PrettyPrinter(indent = 1, width = 200)

# Define an exception for raising during &CANCEL calls
class Cancel(Exception):
    pass

# Define an exception for raising during &BACK calls
class GoBack(Exception):
    pass

# Define our registration interface
class RegistrationInferface(object):

    # institutions will contain the list of institutions returned by the DB, always_print will always print available code options
    # json will contain the json for the current component to be registered and stage will contain the code of the component's stage
    def __init__(self, ITkPDSession):
        self.ITkPDSession = ITkPDSession
        self.institutions = []
        self.always_print = False
        self.json = {}
        self.stage = None

    # Update our list of institutions if it's empty
    def __startUp(self):
        if self.institutions == []:
            print('')
            INFO('Running ITk Production Database component registration interface.')
            self.ITkPDSession.authenticate()
            INFO('Updating list of institutions.')
            self.institutions = self.ITkPDSession.doSomething(action = 'listInstitutions', method = 'GET', data = {})

    # Quit our registration interface
    def __quit(self):
        STATUS('Finished successfully.', True)
        sys.exit(0)

    # Print a list of names and codes in list (assuming it has those keys) with nice printing
    def __printNamesAndCodes(self, list):
        print('    {0}{1}{2:<60} {3:<20}{4}'.format(Colours.BOLD, Colours.WHITE, 'Name:', 'Code:', Colours.ENDC))
        for item in list:
            print('    {0:<60} {1:<20}'.format(item['name'], item['code']))

    # Define a function to provide a prompt to the user and have them select from options
    # Used to get codes from the user, so options includes all possible codes for the current parameter
    def __askForSomething(self, prompt, options):

        # Generate our list of codes
        codes = [item['code'] for item in options]
        PROMPT(prompt)

        # If always_print, print the available options for the code
        if self.always_print:
            INFO('Printing options:\n')
            self.__printNamesAndCodes(options)
            print('')
            PROMPT('Please enter a code from above:')

        while True:

            # Get our user input
            response = input().upper().strip()

            # If nothing, do nothing
            if response == '':
                continue

            # Escape code &PRINT -- print the available options
            elif response == '&PRINT':
                INFO('Printing options:\n')
                self.__printNamesAndCodes(options)
                print('')
                PROMPT('Please enter a code from above:')

            # Escape code &JSON -- print JSON to show what has already been selected
            elif response == '&JSON':
                INFO('Printing JSON:\n')
                pp.pprint(self.json)
                print('')
                PROMPT('Please enter a code:')

            # Escape code &CANCEL -- raise our Cancel exception
            elif response == '&CANCEL':
                WARNING('Registration cancelled.')
                raise Cancel

            # If the user enters a valid code, return that code and its index
            elif response in codes:
                i = codes.index(response)
                INFO('Using code: {0} ({1})'.format(response, options[i]['name']))
                return i, response

            # Else the input is invalid
            else:
                if not self.always_print:
                    INFO('Options:\n')
                    self.__printNamesAndCodes(options)
                    print('')
                PROMPT('Invalid input, please try again:')
                continue

    # Define a function for getting the serial number from the user
    def __askForSerialNumber(self, first_part_of_sn):

        INFO('Serial number is required to be manually entered the component type.')
        PROMPT('Enter the last 7 digits of the component\'s serial number:')

        while True:

            # Get our user input
            response = input().strip()

            # If nothing, do nothing
            if response == '':
                continue

            # Escape code &JSON -- print JSON to show what has already been selected
            elif response == '&JSON':
                INFO('Printing JSON:\n')
                pp.pprint(self.json)
                print('')
                PROMPT('Please enter a serial number:')

            # Escape code &CANCEL -- raise our Cancel exception
            elif response == '&CANCEL':
                WARNING('Registration cancelled.')
                raise Cancel

            # If the user enters a valid serial number, return that number (string)
            elif len(response) == 7 and response.isdigit():
                serial_number = first_part_of_sn + response
                INFO('Using serial number: ' + serial_number)
                return serial_number

            # Else the input is invalid
            else:
                PROMPT('Invalid input, please enter a 7 digit serial number:')
                continue

    # Print the code, name, data type, required, and description for a component's property
    def __printProperty(self, property):
        keys = property.keys()
        print('')
        if 'code' in keys:
            print('    {0}{1}Code{2}:        '.format(Colours.WHITE, Colours.BOLD, Colours.ENDC) + '%s' % property['code'])
        if 'name' in keys:
            print('    {0}{1}Name{2}:        '.format(Colours.WHITE, Colours.BOLD, Colours.ENDC) + '%s' % property['name'])
        if 'dataType' in keys:
            print('    {0}{1}Data Type{2}:   '.format(Colours.WHITE, Colours.BOLD, Colours.ENDC) + '%s' % property['dataType'])
        if 'required' in keys:
            print('    {0}{1}Required{2}:    '.format(Colours.WHITE, Colours.BOLD, Colours.ENDC) + '%s' % property['required'])
        if 'default' in keys:
            print('    {0}{1}Default{2}:     '.format(Colours.WHITE, Colours.BOLD, Colours.ENDC) + '%s' % property['default'])
        if 'unique' in keys:
            print('    {0}{1}Unique{2}:      '.format(Colours.WHITE, Colours.BOLD, Colours.ENDC) + '%s' % property['unique'])
        if 'snPosition' in keys:
            print('    {0}{1}SN Position{2}: '.format(Colours.WHITE, Colours.BOLD, Colours.ENDC) + '%s' % property['snPosition'])
        if 'description' in keys:
            print('    {0}{1}Description{2}: '.format(Colours.WHITE, Colours.BOLD, Colours.ENDC) + '%s' % property['description'])
        if property['dataType'] == 'codeTable':
            print('    {0}{1}Code Table{2}:'.format(Colours.WHITE, Colours.BOLD, Colours.ENDC))
            row_format = '        {:<15}{:<15}'
            header = ['Code', 'Value']
            print(Colours.WHITE + Colours.BOLD + row_format.format(*header) + Colours.ENDC)
            code_table = {item['code']: item['value'] for item in property['codeTable']}
            for code in code_table.keys():
                row = [code, code_table[code]]
                print(row_format.format(*row))
        print('')

    # Convert reponse to specific type
    def __convertToType(self, response, type):

        # If the wrong input is provided, the code will throw a ValueError
        if type == 'string':
            return str(response)
        elif type == 'float':
            return float(response)
        elif type == 'integer':
            return int(response)

        # For boolean, we'll require specific inputs or else throw a ValueError
        elif type == 'boolean':
            if response.lower() in ['1', 'true', 't']:
                return True
            elif response.lower() in ['0', 'False', 'f']:
                return False
            else:
                raise ValueError

        # For a code table, we'll require keys or values to be enter or else throw a ValueError
        elif type[0] == 'codeTable':
            code_table = {item['code']: item['value'] for item in type[1]}
            if response in code_table.keys():
                return response
            else:
                raise ValueError

        return None

    # Give the user a prompt to enter a value for a property indexed by i
    def __getProperty(self, prompt, property, i):

        # Print the relevant info for that property
        self.__printProperty(property)
        PROMPT(prompt)

        while True:

            # Get our input
            response = input().strip()

            # If nothng, do nothing
            if response == '':
                continue

            # Escape code &JSON -- print JSON to show what has already been selected
            elif response.upper() == '&JSON':
                INFO('Printing JSON:\n')
                pp.pprint(self.json)
                print('')
                PROMPT('Please enter a value for the property:')

            # Escape code &SKIP -- skip the current property if it's not required
            elif response.upper() == '&SKIP':

                # Check if it's required
                if property['required']:
                    WARNING('Property is required and cannot be skipped.')
                    INFO('Please enter a value:')
                    continue
                else:
                    INFO('Skipping property: {0} ({1}).'.format(property['code'], property['name']))

                    # Increment i to move onto the next property, and return None for the current property's value
                    return i + 1, None

            # Escape code &BACK -- go back to edit the previous property by raising Back exception
            elif response.upper() == '&BACK':
                INFO('Going back.')
                raise GoBack

            # Escape code &CANCEL -- raise our Cancel exception
            elif response.upper() == '&CANCEL':
                WARNING('Registration cancelled.')
                raise Cancel

            # Else, we assume the user enter a property value
            else:
                try:

                    # Try to convert the input string to its correct data type
                    if property['dataType'] == 'codeTable':
                        property['dataType'] = ['codeTable', property['codeTable']]
                    response_converted = self.__convertToType(response, property['dataType'])
                    INFO('Using property: {0} ({1}) = {2}'.format(property['code'], property['name'], response))

                    # Return i + 1 to move onto the next property and return our converted property value
                    return i + 1, response_converted

                # Catch our ValueErrors for invalid input
                except ValueError:
                    PROMPT('Invalid input, please try again:')
                    continue

    # Define a function to ask the user a prompt and get a yes or no response
    def __getYesOrNo(self, prompt):
        PROMPT(prompt)
        while True:

            # Get our input
            response = input().strip().lower()

            # Skip empty inputs
            if response == '':
                continue

            # If yes, return True
            elif response in ['y', 'yes', '1']:
                return True

            # If no, return False
            elif response in ['n', 'no', '0']:
                return False

            # Else the input is invalid and ask again
            else:
                del response
                PROMPT('Invalid input. Please enter \'y/Y\', or \'n/N\':')
                continue

    # Define a function for opening and running the registration interface.
    def register_component_with_json(self,reg_data):

        # Fetch our list of institutions
        self.__startUp()

        # Get a value for always_print
        #self.always_print = self.__getYesOrNo('To always print the available input options for codes, please type \'y/Y\' or type \'n/N\' to suppress this output:')
        #INFO('Use escape codes &PRINT to print the available options, &JSON to print the current JSON for your component, or &CANCEL to cancel the registration at any time.')

        # The first while loops iterates over registration sessions for multiple components
        while True:

            # The second while loop iterates over a single registration session (I use break statements when &CANCEL codes are entered)
            while True:

                # Reset JSON and stage
                self.json = {}
                self.stage = None

                # Show the user what is to be registered
                INFO('Your component will be registered using JSON:\n')
                self.json = reg_data
                pp.pprint(self.json)
                print('')
                INFO('With stage:\n')
                print('    {0}{1}Stage{2} = {3}\n'.format(Colours.WHITE, Colours.BOLD, Colours.ENDC, self.stage))

                # Ask the user if they want to upload the above
                #if self.__getYesOrNo('Please type \'y/Y\' to confirm the registration or \'n/N\' to cancel:'):

                # If yes, register the component and grab its component code
                component_code = self.registerComponent(**self.json)['component']['code']

                # If the component has stages, use that component code to set the stage for that component
                if self.stage != None:
                    self.setStage(component = component_code, stage = self.stage)
                INFO('Registered successfully.')
                break


            # Ask the user if they want to register another component
            INFO('Session finished.')
            if self.__getYesOrNo('Please type \'y/Y\' to register another component or type \'n/N\' to quit:'):
                continue

            # Else quit
            else:
                self.__quit()

    # Register a component in the DB and return the JSON for that component
    def registerComponent(self, **kwargs):
        component = self.ITkPDSession.doSomething(action = 'registerComponent', method = 'POST', data = kwargs)
        return component

    # Set the stage for registered component
    def setStage(self, **kwargs):
        self.ITkPDSession.doSomething(action = 'setComponentStage', method = 'POST', data = kwargs)

if __name__ == '__main__':

    try:

        from itk_pdb.dbAccess import ITkPDSession

        # Instantiate our ITkPDSession
        session = ITkPDSession()

        # Open registration interface and run it
        interface = RegistrationInferface(session)
        interface.openInterface()

    # In the case of a keyboard interrupt, quit with error
    except KeyboardInterrupt:
        print('')
        ERROR('Exectution terminated.')
        STATUS('Finished with error.', False)
        sys.exit(1)

    except RequestException as e:
        ERROR('Request exception raised: %s' % e)
        STATUS('Finished with error.', False)
        sys.exit(1)
    except EOFError:
        print('')
        ERROR('End of input reached, interaction aborted.')
        STATUS('Finished with error.', False)
        sys.exit(1)
