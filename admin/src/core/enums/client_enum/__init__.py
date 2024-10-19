from enum import Enum

class Discapacidad(Enum):
    MENTAL = 1
    MOTORA = 2
    SENSORIAL = 3
    VISCERAL = 4

class AsignacionFamiliar(Enum):
    ASIG_UNIVERSAL_HIJO = "Asignación Universal por hijo"
    ASIG_UNIVERSAL_HIJO_DISC = "Asignación Universal por hijo con Discapacidad"
    ASIG_AYUDA_ESCOLAR_ANUAL = "Asignación por ayuda escolar anual"

class Pension(Enum):
    PROVINCIAL = 1
    NACIONAL = 2

class Condicion(Enum):
    ECNE = 1
    LESION_POST_TRAUMATICA = 2
    MIELOMENINGOCELE = 3
    ESCLEROSIS_MULTIPLE = 4
    ESCOLIOSIS_LEVE = 5
    SECUELAS_DE_ACV = 6
    DISCAPACIDAD_INTELECTUAL = 7
    TRASTORNO_DEL_ESPECTRO_AUTISTA = 8
    TRASTORNO_DEL_APRENDIZAJE_1 = 9
    TRASTORNO_DEL_APRENDIZAJE_2 = 10
    TDAH = 11  # Trastorno por Déficit de Atención/Hiperactividad
    TRASTORNO_DE_LA_COMUNICACION = 12
    TRASTORNO_DE_ANSIEDAD = 13
    SINDROME_DE_DOWN = 14
    RETRASO_MADURATIVO = 15
    PSICOSIS = 16
    TRASTORNO_DE_CONDUCTA = 17
    TRASTORNOS_DEL_ANIMO = 18

class PropuestasInstitucionales(Enum):
    Hipoterapia = 1
    Monta_Terapéutica = 2
    Deporte_Ecuestre_Adaptado = 3
    Actividades_Recreativas = 4
    Equitación = 5