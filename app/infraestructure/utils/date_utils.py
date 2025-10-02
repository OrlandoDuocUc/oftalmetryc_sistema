from datetime import datetime, timezone, timedelta
import pytz

# Zona horaria de Chile (UTC-3 en invierno, UTC-4 en verano)
CHILE_TIMEZONE = pytz.timezone('America/Santiago')

def get_chile_datetime():
    """
    Obtiene la fecha y hora actual en la zona horaria de Chile
    """
    utc_now = datetime.now(timezone.utc)
    chile_time = utc_now.astimezone(CHILE_TIMEZONE)
    return chile_time

def get_chile_date():
    """
    Obtiene solo la fecha actual en la zona horaria de Chile
    """
    return get_chile_datetime().date()

def get_chile_datetime_naive():
    """
    Obtiene la fecha y hora actual en Chile sin información de zona horaria
    (para compatibilidad con SQLAlchemy)
    """
    return get_chile_datetime().replace(tzinfo=None)

def get_day_start_end_chile(target_date=None):
    """
    Obtiene el inicio y fin del día en la zona horaria de Chile
    
    Args:
        target_date: Fecha específica (opcional). Si no se proporciona, usa la fecha actual
    
    Returns:
        tuple: (inicio_dia, fin_dia) en datetime objects
    """
    if target_date is None:
        target_date = get_chile_date()
    
    # Crear datetime para inicio del día (00:00:00)
    start_of_day = datetime.combine(target_date, datetime.min.time())
    start_of_day = CHILE_TIMEZONE.localize(start_of_day)
    
    # Crear datetime para fin del día (23:59:59.999999)
    end_of_day = datetime.combine(target_date, datetime.max.time())
    end_of_day = CHILE_TIMEZONE.localize(end_of_day)
    
    return start_of_day, end_of_day

def convert_utc_to_chile(utc_datetime):
    """
    Convierte un datetime UTC a la zona horaria de Chile
    
    Args:
        utc_datetime: datetime en UTC
    
    Returns:
        datetime en zona horaria de Chile
    """
    if utc_datetime.tzinfo is None:
        # Si no tiene zona horaria, asumir que es UTC
        utc_datetime = utc_datetime.replace(tzinfo=timezone.utc)
    
    return utc_datetime.astimezone(CHILE_TIMEZONE)

def format_datetime_chile(datetime_obj, format_str='%d/%m/%Y %H:%M'):
    """
    Formatea un datetime en la zona horaria de Chile
    
    Args:
        datetime_obj: datetime object
        format_str: formato de salida
    
    Returns:
        str: datetime formateado
    """
    if datetime_obj is None:
        return 'Sin fecha'
    
    # Convertir a zona horaria de Chile si es necesario
    if datetime_obj.tzinfo is None:
        # Asumir que es UTC si no tiene zona horaria
        datetime_obj = datetime_obj.replace(tzinfo=timezone.utc)
    
    chile_time = convert_utc_to_chile(datetime_obj)
    return chile_time.strftime(format_str) 