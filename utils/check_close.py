

def check_close(name, value, target, tolerance):
    '''
    compare 2 floating point values

    inputs
        name: string, test name
        value: scalar, computed value
        target: scalar, reference value
        tolerance: scalar, tolerance

    returns
        bool
    '''

    error = abs(value - target)

    print(name)
    print('value =', value)
    print('target =', target)
    print('error =', error)

    return error < tolerance

