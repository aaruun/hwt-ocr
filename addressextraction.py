import re

def extract_us_addresses(text):
    # List of US state abbreviations and full names
    states = r'\b(?:AL|Alabama|AK|Alaska|AZ|Arizona|AR|Arkansas|CA|California|CO|Colorado|CT|Connecticut|DE|Delaware|FL|Florida|GA|Georgia|HI|Hawaii|ID|Idaho|IL|Illinois|IN|Indiana|IA|Iowa|KS|Kansas|KY|Kentucky|LA|Louisiana|ME|Maine|MD|Maryland|MA|Massachusetts|MI|Michigan|MN|Minnesota|MS|Mississippi|MO|Missouri|MT|Montana|NE|Nebraska|NV|Nevada|NH|New\sHampshire|NJ|New\sJersey|NM|New\sMexico|NY|New\sYork|NC|North\sCarolina|ND|North\sDakota|OH|Ohio|OK|Oklahoma|OR|Oregon|PA|Pennsylvania|RI|Rhode\sIsland|SC|South\sCarolina|SD|South\sDakota|TN|Tennessee|TX|Texas|UT|Utah|VT|Vermont|VA|Virginia|WA|Washington|WV|West\sVirginia|WI|Wisconsin|WY|Wyoming)\b'

    # Enhanced regex pattern to handle non-standard formats, noise, and missing punctuation
    address_pattern = re.compile(fr'''
        (?P<street_address>
            \d{{1,6}}                              # Street number (up to 6 digits)
            \s+                                   # Space after street number
            [A-Za-z0-9.\-]+(?:\s+[A-Za-z0-9.\-]+)* # Street name (including possible abbreviations like St, Rd, etc.)
            (?:\s*(?:Apt|Suite|Ste|#|Unit|Fl|Floor|Rm)\s*\d+)?   # Optional apartment, suite, unit, or floor number
        ),?\s*                                    # Optional comma or extra space
        (?P<city>[A-Za-z\s]+?)                    # City name (allowing multiple words and spaces)
        ,?\s*                                     # Optional comma
        (?P<state>{states})                       # State abbreviation or full name (from hardcoded list)
        \s*                                       # Optional space
        (?P<zip_code>\d{{5}}(?:-\d{{4}})?)         # ZIP code (5 digits, optionally followed by ZIP+4)
    ''', re.VERBOSE | re.IGNORECASE)

    # Find all matches
    matches = address_pattern.finditer(text)

    # List to store the extracted addresses
    addresses = []

    for match in matches:
        # Extract the named groups and form the address dictionary
        address_dict = {
            "street_address": match.group("street_address").strip(),
            "city": match.group("city").strip(),
            "state": match.group("state").strip(),
            "zip_code": match.group("zip_code").strip()
        }
        addresses.append(address_dict)

    return addresses


# Example usage with noisy, non-standard formats:
support_notes = """
    Customer 1 lives at 1234 Elm St Apt 56 Springfield Illinois 62704. 
    Another person mentioned address: 5678 Oak Ave Ste 12,Chicago IL60616-1234! 
    Shipping problem from 9876 Pine Dr Los Angeles, California 90210 was noted. 
    A note says "4321 Maple St., Suite 5B,SomeCity Kansas 12345" could be wrong.
    Another report has 4567 Birch Ln, Denver CO 80014-5567.
"""
extracted_addresses = extract_us_addresses(support_notes)

for address in extracted_addresses:
    print(address)



import re

# Define regex pattern for complex US addresses
address_regex = re.compile(r'''
    # Street Number
    (?P<street_number>\d{1,5})\s+
    
    # Street Name and Type (allowing directions, street suffixes)
    (?P<street_name>(?:[A-Za-z0-9]+\s?)+)
    (?:\b(?:St|Street|Ave|Avenue|Rd|Road|Blvd|Boulevard|Dr|Drive|Ln|Lane|Ct|Court|Pl|Place|Way|Pkwy|Parkway|Cir|Circle)\b)?\s*
    
    # Optional Unit Designators (e.g., Apt, Ste, Unit, etc.)
    (?:\b(?:Apt|Apartment|Suite|Ste|Unit|#)\s*\d+)?\s*

    # Optional City Name (supporting alphabetic characters and spaces)
    ,?\s*(?P<city>(?:[A-Za-z]+\s?)+)\s*

    # Mandatory State Abbreviation or Full State Name (strict list)
    (?P<state>
        AL|Alabama|AK|Alaska|AZ|Arizona|AR|Arkansas|CA|California|CO|Colorado|CT|Connecticut|DE|Delaware|FL|Florida|
        GA|Georgia|HI|Hawaii|ID|Idaho|IL|Illinois|IN|Indiana|IA|Iowa|KS|Kansas|KY|Kentucky|LA|Louisiana|ME|Maine|MD|Maryland|
        MA|Massachusetts|MI|Michigan|MN|Minnesota|MS|Mississippi|MO|Missouri|MT|Montana|NE|Nebraska|NV|Nevada|NH|New\ Hampshire|
        NJ|New\ Jersey|NM|New\ Mexico|NY|New\ York|NC|North\ Carolina|ND|North\ Dakota|OH|Ohio|OK|Oklahoma|OR|Oregon|
        PA|Pennsylvania|RI|Rhode\ Island|SC|South\ Carolina|SD|South\ Dakota|TN|Tennessee|TX|Texas|UT|Utah|
        VT|Vermont|VA|Virginia|WA|Washington|WV|West\ Virginia|WI|Wisconsin|WY|Wyoming
    )\b\s*

    # ZIP Code (strict format for 5-digit or ZIP+4)
    (?P<zip_code>\d{5}(?:-\d{4})?)
''', re.VERBOSE | re.IGNORECASE)

# Example usage with noisy customer service notes
customer_service_notes = """
    The address is 1234 Elm St Apt 56, Springfield, IL 62704. 
    Another address to ship to: 5678 Oak Avenue Suite 12 Chicago IL 60616-1234!
    Can you also verify if 8765 Pine Dr, Los Angeles, CA 90210 is correct?
"""

# Find all matches in the text
matches = address_regex.finditer(customer_service_notes)

# Extract and print each matched address
for match in matches:
    print(match.groupdict())


Here's an enhanced highly robust Python regular expression designed to extract complex US addresses from noisy and unstructured text, while being strict about valid US states. This regex will handle common complexities like apartment numbers, suite numbers, and varying formats for ZIP codes.

Key Features:
Recognizes valid street numbers, street names, road types (e.g., St, Ave, Blvd).
Identifies addresses with secondary unit designators (e.g., Apt, Ste, Unit).
Handles city names (allowing alphabetic characters and spaces).
Validates US state abbreviations or full state names strictly.
Extracts valid ZIP codes, supporting 5-digit and 9-digit (ZIP+4) formats.
Accounts for noisy punctuation or extra text around the address.
List of US State Abbreviations and Full Names
We include both two-letter state abbreviations and full state names in the regex, making it strict about valid states.

Enhanced Regex for US Addresses

Explanation of Regex Components:
Street Number: (?P<street_number>\d{1,5}) captures street numbers from 1 to 5 digits.
Street Name and Type: (?P<street_name>(?:[A-Za-z0-9]+\s?)+) captures the street name, supporting both alphabetic characters and numbers, followed by common street suffixes (e.g., St, Ave, Blvd).
Unit Designators: Optional secondary unit identifiers like Apt, Ste, or Unit followed by a number (e.g., Apt 56, Ste 12).
City: (?P<city>(?:[A-Za-z]+\s?)+) captures the city name, allowing alphabetic characters and spaces.
State: (?P<state>...) is a strict match for valid US state abbreviations or full names, accounting for case-insensitive matching and strict state validation.
ZIP Code: (?P<zip_code>\d{5}(?:-\d{4})?) matches valid ZIP codes, supporting both 5-digit and ZIP+4 formats.

Key Enhancements:
Strict Validation of US States: The regex only allows valid US state abbreviations or full state names, reducing false positives.
Complex Address Formats: Supports addresses with street suffixes, unit designators, and secondary information (like apartments and suites).
Flexible ZIP Code Matching: Handles both standard 5-digit ZIP codes and the extended 9-digit ZIP+4 format.
Noise Tolerance: The regex is robust to noisy text, extra punctuation, or spacing issues commonly found in unstructured text like customer service notes.
This enhanced regex is highly robust for extracting US addresses from noisy and unstructured text, while being strict about validating US states and ensuring the correctness of the ZIP code format.


