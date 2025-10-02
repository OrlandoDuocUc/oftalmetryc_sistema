# Utilidades para formateo de moneda
def format_currency(value, currency='USD'):
    """
    Formatea un valor numérico como moneda
    Args:
        value: Valor numérico a formatear
        currency: Tipo de moneda (USD por defecto)
    Returns:
        String formateado como moneda
    """
    if value is None:
        return '$0.00'
    
    try:
        # Convertir a float si no lo es
        if isinstance(value, str):
            value = float(value)
        
        # Formatear como moneda USD con separadores de miles
        if currency == 'USD':
            return f'${value:,.2f}'
        else:
            return f'{currency} {value:,.2f}'
    except (ValueError, TypeError):
        return '$0.00'

def format_currency_simple(value):
    """
    Versión simple del formato de moneda para templates
    """
    return format_currency(value, 'USD')

def format_currency_input(value):
    """
    Formato para campos de entrada (sin símbolo $)
    """
    if value is None:
        return '0.00'
    
    try:
        if isinstance(value, str):
            value = float(value)
        return f'{value:.2f}'
    except (ValueError, TypeError):
        return '0.00'