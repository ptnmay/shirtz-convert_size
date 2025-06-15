# Conversion dictionary
convert = {
    "20": 7.9, "21": 8.3, "22": 8.7, "23": 9.1, "24": 9.4, "25": 9.8, "26": 10.2,
    "27": 10.6, "28": 11.0, "29": 11.4, "30": 11.8, "31": 12.2, "32": 12.6, "33": 13.0,
    "34": 13.4, "35": 13.8, "36": 14.2, "37": 14.6, "38": 15.0, "39": 15.4, "40": 15.7,
    "41": 16.1, "42": 16.5, "43": 16.9, "44": 17.3, "45": 17.7, "46": 18.1, "47": 18.5,
    "48": 18.9, "49": 19.3, "50": 19.7, "51": 20.1, "52": 20.5, "53": 20.9, "54": 21.3,
    "55": 21.7, "56": 22.0, "57": 22.4, "58": 22.8, "59": 23.2, "60": 23.6, "61": 24.0,
    "62": 24.4, "63": 24.8, "64": 25.2, "65": 25.6, "66": 26.0, "67": 26.4, "68": 26.8,
    "69": 27.2, "70": 27.6, "71": 28.0, "72": 28.3, "73": 28.7, "74": 29.1, "75": 29.5,
    "76": 29.9, "77": 30.3, "78": 30.7, "79": 31.1, "80": 31.5, "81": 31.9, "82": 32.3,
    "83": 32.7, "84": 33.1, "85": 33.5, "86": 33.9, "87": 34.3, "88": 34.6, "89": 35.0,
    "90": 35.4, "91": 35.8, "92": 36.2, "93": 36.6, "94": 37.0, "95": 37.4, "96": 37.8,
    "97": 38.2, "98": 38.6, "99": 39.0, "100": 39.4, "101": 39.8, "102": 40.2, "103": 40.6,
    "104": 40.9, "105": 41.3, "106": 41.7, "107": 42.1, "108": 42.5, "109": 42.9, "110": 43.3,
    "111": 43.7, "112": 44.1, "113": 44.5, "114": 44.9, "115": 45.3, "116": 45.7, "117": 46.1,
    "118": 46.5, "119": 46.9, "120": 47.2, "121": 47.6, "122": 48.0, "123": 48.4, "124": 48.8,
    "125": 49.2, "126": 49.6, "127": 50.0, "128": 50.4, "129": 50.8, "130": 51.2, "131": 51.6,
    "132": 52.0, "133": 52.4, "134": 52.8, "135": 53.1, "136": 53.5, "137": 53.9, "138": 54.3,
    "139": 54.7, "140": 55.1, "141": 55.5, "142": 55.9, "143": 56.3, "144": 56.7, "145": 57.1,
    "146": 57.5, "147": 57.9, "148": 58.3, "149": 58.7, "150": 59.1, "151": 59.4, "152": 59.8
}
# Conversion dictionary (unchanged)...

def round_float(number):
    """Round to nearest 0.5"""
    return round(number * 2) / 2

def convert_value(value):
    """
    Converts a single value, a range (e.g. 100-120), or a dash ("-").
    Returns float, tuple, or "-" as needed.
    """
    value = value.strip()
    if value == "-":
        return "-"
    if '-' in value and not value.startswith('-') and not value.endswith('-'):
        parts = value.split('-')
        if len(parts) != 2:
            raise ValueError(f"Invalid range format: {value}")
        low_key = ''.join(filter(str.isdigit, parts[0]))
        high_key = ''.join(filter(str.isdigit, parts[1]))
        if low_key not in convert or high_key not in convert:
            raise KeyError(f"One of {low_key} or {high_key} not in conversion dictionary.")
        low_val = round_float(convert[low_key])
        high_val = round_float(convert[high_key])
        return (low_val, high_val)
    else:
        key = ''.join(filter(str.isdigit, value))
        if key not in convert:
            raise KeyError(f"{key} not in conversion dictionary.")
        return round_float(convert[key])

def format_value(val):
    """Formats float, tuple, or '-' for output"""
    if val == "-":
        return "-"
    if isinstance(val, tuple):
        return f"{val[0]}-{val[1]}"
    return f"{val}"

def process_input(input_string):
    components = input_string.strip().split()

    if len(components) != 3:
        raise ValueError("Input must contain exactly 3 values (including '-' if missing).")

    chest_raw, shoulder_raw, length_raw = components

    chest = convert_value(chest_raw)
    shoulder = convert_value(shoulder_raw)
    length = convert_value(length_raw)

    return f"อก {format_value(chest)} ไหล่ {format_value(shoulder)} ยาว {format_value(length)}"

# Main loop
while True:
    try:
        s = input("Enter Chinese size (or 'exit' to quit): ")
        if s.lower() == 'exit':
            break
        result = process_input(s)
        print("\n" + result + "\n")
    except ValueError as e:
        print(f"Error: {e}")
    except KeyError as e:
        print(f"Error: Key {e} not found in conversion dictionary.")
    except Exception as e:
        print(f"Unexpected error: {e}")
