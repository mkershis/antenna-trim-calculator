import streamlit as st 
from math import floor

def fractional_inches(decimal_inches: float, precision: str) -> str:
    '''
    Converts decimal inches to the closest fraction
    with either a precision of 1/32" or 1/16"
    '''
    # map the user's choice to the correct starting point in the
    # list of possible denominators

    precision_to_index = {'1/32':0,'1/16':1}
    index = precision_to_index[precision]

    int_part = floor(decimal_inches)
    frac_part = decimal_inches - int_part

    # handle cases where decimal_inches is a whole number
    if frac_part == 0:
        return f'{int_part}'
    else:
        
        denominators = [32, 16, 8, 4, 2]

        # want to get to the closest fraction for accuracy
        numerator = round(frac_part * denominators[index])

        # to catch small fractions which are < 1/16 or < 1/32
        if numerator == 0:
            return f'{int_part}'
        
        # check if the numerator can be simplified, but don't let
        # the loop overrun the list of denominators
        while (numerator % 2 == 0) & (index < len(denominators) - 1):
            numerator /= 2
            index += 1
        if int_part == 0:
            # return f'{int(numerator)}/{denominators[index]}'
            return r'\frac{{{}}}{{{}}}'.format(int(numerator), denominators[index])
        elif numerator == denominators[index]:
            return f'{int_part + 1}'
        else:
            # return f'{int_part} {int(numerator)}/{denominators[index]}'
            return r'{}\frac{{{}}}{{{}}}'.format(int_part,int(numerator), denominators[index])

def unit_convert(value: float, to_unit: str, precision: str=None) -> str:
    '''
    Takes an input length in feet and converts to
    the desired unit. Returns the value along with a 
    display unit for printing    
    '''
    if to_unit == 'feet/inches':
        feet = floor(value)
        decimal_inches = (value - feet) * 12
        if feet > 0:
            if decimal_inches == 0:
                return f'$${feet:,}\\, ft$$'
            else:
                return f'$${feet:,}\\, ft\\quad{fractional_inches(decimal_inches, precision)}\\,in$$'
        else:
            if decimal_inches == 0:
                return ''
            else:
                return f'$${fractional_inches(decimal_inches, precision)}\\, in$$'

    elif to_unit == 'centimeters':
        centimeters = value * 12 * 2.54
        return f'$${centimeters:,.1f}\\, cm$$'

intro_text = open('readme.md').read()

st.markdown(intro_text)

current_freq = st.number_input('Current resonant frequency (MHz)', format = '%0.3f', step = 0.001, min_value = 0.001, value = None, placeholder=None)
desired_freq = st.number_input('Desired resonant frequency (MHz)', format = '%0.3f', step = 0.001, min_value = 0.001, value = None, placeholder=None)

to_unit = st.radio(label = 'Select preferred display units', options = ['feet/inches','centimeters'], horizontal = True)
if to_unit == 'feet/inches':
    precision = st.radio(label = 'Select desired precision (inches)',options = ['1/32','1/16'], horizontal = True, index=1)
else:
    precision = None
calculate = st.button('Run Calculation')

if calculate & ((current_freq is not None) & (desired_freq is not None)):
    st.divider()

    diff_feet = abs((468 / current_freq) - (468 / desired_freq))
    
    full_trim = unit_convert(diff_feet, to_unit, precision)
    half_trim = unit_convert(diff_feet / 2, to_unit, precision)

    if current_freq == desired_freq:
        st.write('Your antenna is perfectly tuned. No changes required.')
    else:
    
        if current_freq < desired_freq:
            st.write('Antenna is too long. Reduce total length by:')
        elif current_freq > desired_freq:
            st.write('Antenna is too short. Increase total length by:')

        # st.metric(label = 'Full Trim', value = full_trim, border = True, label_visibility = 'collapsed')
        st.markdown(full_trim)

        if current_freq < desired_freq:
            st.write('or trim each side of the dipole by:')
        elif current_freq > desired_freq:
            st.write('or extend each side of the dipole by:')

        # st.metric(label = 'Half Trim', value = half_trim, border = True, label_visibility = 'collapsed')
        st.markdown(half_trim)

elif calculate & ((current_freq is None) | (desired_freq is None)):
    st.markdown(':red[Error: Both frequencies must be greater than zero.]')
