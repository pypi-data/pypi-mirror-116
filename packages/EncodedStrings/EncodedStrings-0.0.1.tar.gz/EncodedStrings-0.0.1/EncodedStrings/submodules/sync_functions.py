import base64
import os
import sys


class SubModule:
    def __init__(self):
        self.BasicEncode = self.BasicEncodeModule()
        self.AdvanceEncode = self.AdvanceEncodeModule()

    class BasicEncodeModule:
        class encode:

            def binary(self, word):
                return " ".join("".format(ord(i), 'b') for i in word)

            def hex(self, word):
                return " ".join("{:02x}".format(ord(c)) for c in word)

            def octal(self, word):
                return " ".join(oct(ord(c)) for c in word)

        class decode:

            def binary(self, word):
                result = ""
                for item in word.split():
                    result += chr(int(item, 2))
                return result

            def hex(self, word):
                result = ""
                for item in word.split():
                    result += chr(int(item, 16))
                return result

            def octal(self, word):
                result = ""
                for item in word.split():
                    result += chr(int(item, 8))
                return result

        # TODO: This is where the init for the code happens so we can call them without init in the Programm
        # TODO: Its for pleasure of view XD
        def __init__(self):
            self.Encode = self.encode()
            self.Decode = self.decode()

    class AdvanceEncodeModule:
        class cipherEncode:
            pass

        class cipherDecode:
            pass

        # TODO: This is where the init for the code happens so we can call them without init in the Programm
        # TODO: Its for pleasure of view XD
        def __init__(self):
            self.CipherEncode = self.cipherEncode()
            self.CipherDecode = self.cipherDecode()