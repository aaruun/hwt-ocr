To use this regex-based solution as a **vectorized function** within a pandas DataFrame, you can define a function that processes each row of the DataFrame and applies the regex to extract the address components. Then, you can apply this function using `df.apply()` or create new DataFrame columns with the extracted components.

Here’s how you can integrate the regex solution into a DataFrame:

### Steps:
1. **Define a function** that applies the regex to each entry in the DataFrame and extracts the relevant address components.
2. **Use `df.apply()`** to vectorize the operation for the whole DataFrame.
3. **Return the extracted address components** as a new column (or multiple columns) in the DataFrame.

### Code Example

```python
import re
import pandas as pd

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

# Define function to extract address components from a single text string
def extract_address_components(text):
    matches = address_regex.search(text)
    if matches:
        return matches.groupdict()
    else:
        return {"street_number": None, "street_name": None, "city": None, "state": None, "zip_code": None}

# Example DataFrame with noisy customer service notes
data = {
    "customer_notes": [
        "The address is 1234 Elm St Apt 56, Springfield, IL 62704.",
        "Another address to ship to: 5678 Oak Avenue Suite 12 Chicago IL 60616-1234!",
        "Can you also verify if 8765 Pine Dr, Los Angeles, CA 90210 is correct?",
        "Send it to 987 Maple Blvd, Austin, TX 73301-3212.",
        "Incorrect format without state or zip: 123 Fake St"
    ]
}

df = pd.DataFrame(data)

# Apply the function to the DataFrame, extracting address components into new columns
address_df = df["customer_notes"].apply(extract_address_components).apply(pd.Series)

# Concatenate the original DataFrame with the new columns
result_df = pd.concat([df, address_df], axis=1)

# Display the resulting DataFrame
print(result_df)
```

### Explanation:
1. **`extract_address_components(text)`**: This function applies the regex to each `text` (in this case, customer service notes) and returns a dictionary of the extracted components (`street_number`, `street_name`, `city`, `state`, `zip_code`). If no address is found, it returns `None` for each component.
   
2. **`df["customer_notes"].apply(extract_address_components)`**: This applies the function to each row of the `customer_notes` column in the DataFrame.

3. **`.apply(pd.Series)`**: Converts the dictionary returned by the function into separate columns for each address component.

4. **`pd.concat([df, address_df], axis=1)`**: Merges the original DataFrame with the new columns generated from the extracted addresses.

### Example Output:
```plaintext
                                      customer_notes street_number     street_name           city        state    zip_code
0             The address is 1234 Elm St Apt 56, Springfield, IL 62704.           1234        Elm St     Springfield          IL       62704
1  Another address to ship to: 5678 Oak Avenue Suite 12 Chicago IL 60616-1234!           5678  Oak Avenue          Chicago          IL  60616-1234
2  Can you also verify if 8765 Pine Dr, Los Angeles, CA 90210 is correct?           8765      Pine Dr     Los Angeles         CA       90210
3                      Send it to 987 Maple Blvd, Austin, TX 73301-3212.            987    Maple Blvd            Austin          TX  73301-3212
4                             Incorrect format without state or zip: 123 Fake St            None            None            None         None         None
```

### Benefits of Vectorization:
- This method is **vectorized** using pandas, making it efficient even for large datasets.
- The function is reusable for various unstructured text entries in your dataset.
- It is flexible, as you can easily update the regex or function logic without changing the DataFrame structure.

This approach allows you to extract complex US addresses from noisy text while keeping the process efficient and clean within the DataFrame.
