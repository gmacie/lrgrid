# $Id: scanner.py 11684 2010-05-19 10:43:47Z nkraft $
#
#   A scanner class for Python
#
#   written by John C. Lusth
#   modified by Nicholas A. Kraft
#
#   Fine, old-world, made-by-hand craftsmanship!
#
#   Examples:
#    
#       from scanner import Scanner
#
#       s = Scanner(string='now is the time')      # read from string
#
#       s = Scanner(file='file_name',string='hi')  # read from string
#
#       s = Scanner(file='file_name');             # read from file_name
#
#       s = Scanner(file='-')                      # read from stdin
#
#       s.readline()        # read the rest of the current or next line
#       s.read_rawchar()    # read the next character (whitespace or not)
#       s.read_char()       # read the next non-whitespace character
#       s.read_token()      # read the next whitespace delimited token
#       s.read_string()     # read the next quote delimited token

from sys import stdin

class Scanner:

    def __init__(self,file='-',string=''):
        self.index = 0
        self.length = 0
        self.pushedBackChar = ''
        self.pushedBack = False
        self.lineNumber = 0

        if '' != string:
            self.closed = True
            self.store = string
            self.length = len(string)
            self.lineNumber = 1
        else:
            self.closed = False
            if '-' != file:
                self.input = open(file,'r')
            else:
                self.input = stdin


    def readline(self):
        """
        readline works the same as regular python readline
        """
        if self.index < self.length:
            result = self.store[self.index:]
        elif False == self.closed:
            result = self.input.readline()
            self.lineNumber += 1
        else:
            result =''
        self.index = 0
        self.length = 0
        return result


    def read_rawchar(self):
        """
        read and return the next character, even if it is whitespace
        """
        ch = self._get_next_character()
        return ch


    def read_char(self):
        """
        read and return the next non-whitespace character
        """
        self._skip_white_space()
        ch = self._get_next_character()
        return ch


    def read_token(self):
        """
        read and return the next token
        """
        self._skip_white_space()
        return self._get_token()


    def read_string(self):
        """
        read and return a string enclosed in quotes
        """
        self._skip_white_space()
        return self._get_string()
        

    def _get_token(self):
        ch = self._get_next_character()
        if '' == ch:
            return ch
        str = ''
        while '' != ch and not ch.isspace():
            str += ch
            ch = self._get_next_character()
        return str


    def _get_string(self):
        delimiter = self._get_next_character() # should be some kind of quote
        if '' == delimiter:
            return ''
        str = delimiter
        ch = self._get_next_character()
        while '' != ch and ch != delimiter:
            str += ch
            if ch == '\\':
                ch = self._get_next_character()
                if ch == '': return str
                str += ch
            ch = self._get_next_character()
        str += delimiter
        return str


    def _skip_white_space(self):
        ch = self._get_next_character()
        while '' != ch and ch.isspace():
            ch = self._get_next_character()
        self._push_back(ch)


    def _get_next_character(self):
        if self.pushedBack:
            self.pushedBack = False
            return self.pushedBackChar
        if self.index == self.length:
            if False == self.closed:
                self.store = self.input.readline()
                self.lineNumber += 1
            else:
                self.store = ''
            if self.store == '':
                return ''
            self.index = 0
            self.length = len(self.store)
        value = self.store[self.index]
        self.index += 1
        return value


    def _push_back(self,ch):
        self.pushedBack = True
        self.pushedBackChar = ch
