import bleach

allowed_tags = ['span', 'b']  # allowed HTML tags

def sanitize_html_input(input_str):
    return bleach.clean(input_str, tags=allowed_tags)

def sanitize_string(input_str):
    return input

def is_sanitized_string(input_str):
    return input_str.count(';') == 0 and input_str.count('-') == 0

def is_sanitized_stock_symbol(stock_symbol_str):  # stock symbols can include '-'
    return stock_symbol_str.count(';') == 0

def are_sanitized_strings(list_of_input_strings):
    for str in list_of_input_strings:
        if not is_sanitized_string(str):
            return False
    return True