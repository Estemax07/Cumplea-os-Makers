from datetime import date, timedelta


def calcular_edad(fecha_nacimiento: date, hoy: date | None = None) -> int:
    """Edad en años cumplidos a partir de la fecha de nacimiento."""
    hoy = hoy or date.today()
    edad = hoy.year - fecha_nacimiento.year
    # Todavía no llegó el cumpleaños este año
    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    return max(edad, 0)


def _cumple_en_mes_dia(fecha_nacimiento: date, mes: int, dia: int) -> bool:
    """
    Compara mes/día de nacimiento contra un mes/día dado.
    Los nacidos el 29 de febrero festejan el 28 en años no bisiestos.
    """
    fm, fd = fecha_nacimiento.month, fecha_nacimiento.day
    if fm == 2 and fd == 29 and mes == 2 and dia == 28:
        # Solo aplica si el año objetivo no es bisiesto (dia=28 ya es el ajuste)
        return True
    return fm == mes and fd == dia


def es_hoy(fecha_nacimiento: date, hoy: date | None = None) -> bool:
    hoy = hoy or date.today()
    return _cumple_en_mes_dia(fecha_nacimiento, hoy.month, hoy.day)


def es_manana(fecha_nacimiento: date, hoy: date | None = None) -> bool:
    hoy = hoy or date.today()
    manana = hoy + timedelta(days=1)
    return _cumple_en_mes_dia(fecha_nacimiento, manana.month, manana.day)


def dias_hasta_proximo_cumple(fecha_nacimiento: date, hoy: date | None = None) -> int:
    """
    Días que faltan para el próximo cumpleaños (0 si es hoy).
    Maneja el caso de 29 de febrero corriendo la fecha al 28/feb o 1/mar
    en años no bisiestos.
    """
    hoy = hoy or date.today()

    def proxima_ocurrencia(anio: int) -> date | None:
        mes, dia = fecha_nacimiento.month, fecha_nacimiento.day
        try:
            return date(anio, mes, dia)
        except ValueError:
            # 29 de febrero en año no bisiesto -> usamos 28 de febrero
            if mes == 2 and dia == 29:
                return date(anio, 2, 28)
            return None

    candidata = proxima_ocurrencia(hoy.year)
    if candidata is None or candidata < hoy:
        candidata = proxima_ocurrencia(hoy.year + 1)

    return (candidata - hoy).days
