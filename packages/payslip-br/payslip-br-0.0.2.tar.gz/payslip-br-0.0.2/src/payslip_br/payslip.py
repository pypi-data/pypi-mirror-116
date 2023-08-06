#  -*- coding:utf-8 -*- 

from datetime import date,timedelta
import re

class InvalidBarcodeException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Barcode is invalid. \n" \
               "Please check whether the input is correct \n" \
               "Input: {0}".format(self.value)


class InvalidTypeableLineException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Typeable line is invalid. \n" \
               "Please check whether the input is correct \n" \
               "Input: {0}".format(self.value)


def dac_string(length,elements):
    """ Generates the string of numbers required to calculate the DAC (self-check digit)
    based on an array of pre-determined allowed objects.

    :param length: Length of the barcode string minus the DAC digit.
    :type length: int
    :param elements: List of allowed objects for each modulo calculation.
                     Modulo 10: [2,1]
                     Modulo 11: [2,3,4,5,6,7,8,9]
    :type elements: list
        
    :return: String of numbers for the DAC calculation.
    :rtype: str
    """

    complete = length
    cursor = 0
    verification_string = ''
    
    while complete > 0:
        if cursor > len(elements) - 1:
            cursor = 0
        
        verification_string += str(elements[cursor])
        complete -= 1
        cursor += 1

    return verification_string


def dac(barcode, modulo):
    """ Calculates the DAC, or self-check digit, for the payslip barcode according to FEBRABAN
    specifications.

    :param barcode: A string containing the barcode
    :type barcode: str
    :param modulo: The modulo operation to be performed (either 10 or 11).
    :type modulo: int
        
    :return: The DAC self-check digit.
    :rtype: int
    """
    
    result = 0
    
    if modulo == 10:
        verification_string = dac_string(len(barcode), range(2,0,-1))
        reduce_string = ""
        
        for position in range(len(barcode)):
            product = int(barcode[position]) * int(verification_string[position])
            reduce_string += str(product)

        for i in range(len(reduce_string)):
            result += int(reduce_string[i])

        remainder = result % modulo
        
        if remainder == 0:
            return 0
        else:
            return 10 - remainder
    
    else: # Modulo 11
        verification_string = dac_string(len(barcode), range(2,10)) [::-1]

        for position in range(len(barcode)):
            product = int(barcode[position]) * int(verification_string[position])
            result += product

        remainder = result % modulo

        if remainder < 2:
            return 0
        elif remainder == 10:
            return 1
        else:
            return 11 - remainder


def to_barcode(typeable_line):
    """ Converts the typeable line or numeric representation of a payslip's barcode into
    the working barcode itself.

    :param typeable_line: A valid typeable line, comprised of either a 47-digit or 48-digit long string.
    :type typeable_line: str
        
    :return: Returns a valid barcode from the provided typeable line.
    :rtype: str

    :raises InvalidTypeableLineException: Invalid typeable line. Check input data.
    """

    if len(typeable_line) == 47:
        return typeable_line[0:4] \
            + typeable_line[32] \
            + typeable_line[33:47] \
            + typeable_line[4:9] \
            + typeable_line[10:20] \
            + typeable_line[21:31]
    elif len(typeable_line) == 48:
        return typeable_line[0:11] \
            + typeable_line[12:23] \
            + typeable_line[24:35] \
            + typeable_line[36:47]
    elif len(typeable_line) == 44:
        return typeable_line
    else:
        raise InvalidTypeableLineException(typeable_line)


def to_typeable_line(barcode):
    """ Converts the payslip's barcode into the typeable line, a numeric representation
    of such barcode that can be inserted manually by an operator.

    :param barcode: A valid payslip barcode
    :type barcode: str
    
    :rtype: str
    :return: A valid typeable line according to the type of barcode (47-digit line for regular documents,
        or 48-digit line for utility bills or tax-related obligations).
    """

    if barcode[0] == "8":
        return barcode[0:11] \
            + str(dac(barcode[0:11], 11)) \
            + barcode[11:22] \
            + str(dac(barcode[11:22], 11)) \
            + barcode[22:33] \
            + str(dac(barcode[22:33], 11)) \
            + barcode[33:] \
            + str(dac(barcode[33:], 11))
    else:
        vd = barcode[4]
        field5 = barcode[5:19]
        field1 = barcode[0:4] + barcode[19:24]
        field2 = barcode[24:35]
        field3 = barcode[35:]
        return field1 + dac(field1, 10) \
            + field2 + dac(field2, 10) \
            + field3 + dac(field3, 10) \
            + vd + field5


def is_valid(typeable_string):
    """ Validates a barcode or a typeable line.

    :param typeable_string: A string representing a barcode or a typeable line to be checked
    :type typeable_string: str

    :return: true, if the input string is valid. false, otherwise.
    :rtype: bool 
    """

    if len(typeable_string) not in [44,47,48]:
        return False
    
    barcode = to_barcode(typeable_string)
    verifier = 4
    modulo = 11

    if barcode[0] == "8":
        verifier = 3
    
    if barcode[verifier-1] in ["6","7"]:
        modulo = 10

    return dac(barcode[0:verifier] + barcode[verifier+1:], modulo) == int(barcode[verifier])


def due_date(no_of_days):
    """Returns the date when the payment will be due.

    :param no_of_days: aa
    :type no_of_days: int

    :rtype: date
    :return: due date
    """
    return date(1997, 10, 7) + timedelta(days=no_of_days)


def decode(typeable_string):
    """ Decodes a string associated with a payslip barcode or its typeable line.

    :param typeable_string: 
    :type typeable_string: str

    :return: A dictionary of data fields contained in the payslip's barcode.
    :rtype: dict

    :raises InvalidBarcodeException: Invalid barcode
    """

    if is_valid(typeable_string):
        payslip = {}
        barcode = to_barcode(typeable_string)
        isUtility = False
        payslip["barcode"] = barcode
        
        if barcode[0] == "8":
            payslip["type"] = "tax-utility"
            isUtility = True
        else:
            payslip["type"] = "regular"

        if not isUtility:
            payslip["bank"] = barcode[0:3]
            payslip["amount"] = float(barcode[9:17] + "." + barcode[17:19])
            payslip["due_date"] = due_date(int(barcode[5:9])).isoformat()
        else:
            payslip["expense_type"] = barcode[1]
            payslip["amount"] = float(barcode[4:13] + "." + barcode[13:15])
            payslip["entity"] = barcode[15:19]

        payslip["reserved"] = barcode[19:]
        
        return payslip
    else:
        raise InvalidBarcodeException(typeable_string)
