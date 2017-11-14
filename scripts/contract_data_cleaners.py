def parse_naics(naics_string):
    import re

    #parsed_naic_list_single is only 1 instance of naic, it is a list because each digit in the naic is an element
    parsed_naic_list_single = re.findall(r'\d', str(naics_string))
    if len(parsed_naic_list_single) == 9:
        parsed_naic = parsed_naic_list_single[3] + parsed_naic_list_single[4] + parsed_naic_list_single[5] + parsed_naic_list_single[6] + \
                      parsed_naic_list_single[7] + parsed_naic_list_single[8]
    else:
        parsed_naic = 'None'
    return parsed_naic

def parse_solicitation_number(solicitation_number_string):
    return solicitation_number_string.lstrip("Solicitation Number: ")