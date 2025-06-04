#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Patient models module for SQLAlchemy models.

This module contains the SQLAlchemy models for patient data.
"""

# Import modules #
#----------------#

from sqlalchemy import Column, DateTime, Float, Integer, String

# Import project modules #
#------------------------#

from app.db import BaseModel
from app.constants.table_names import (
    CIERRE_ULCERA,
    CONSTANTES,
    CONTENCION,
    CUIDADO_ULCERA,
    DEPOSICIONES,
    DIURESIS,
    ELECTROCARDIOGRAMA,
    FOTOS_HOSPWIN,
    FRECUENCIA_CARDIACA,
    FRECUENCIA_RESPIRATORIA,
    GLUCOSA,
    GRUPOUSU_HOSPWIN,
    MEDICACION,
    MENSTRUACION,
    MONITORES_ACTIVOS,
    MONITOR,
    PACIENTES_HOSPWIN,
    PESO,
    PRESION_ARTERIAL,
    SATURACION_OXIGENO,
    TALLA,
    TARJETA,
    TEMPERATURA,
    TIPO_SONDA,
    TRATAMIENTO_ULCERA,
    ULCERAS,
    USUARIO_HOSPWIN
)
from app.constants.table_mappings import TABLE_FIELD_MAPPING
from app.utils.hl7_formatter import format_vital_signs_message
from app.utils.time_formatters import dt_to_string

# Define classes and methods #
#----------------------------#

# Saturacion Oxigeno model
class SaturacionOxigeno(BaseModel):
    """
    SQLAlchemy data model for the 'saturacion_oxigeno' table.
    """
    __tablename__ = SATURACION_OXIGENO
    
    id_secuencia_so = Column(Integer, primary_key=True)
    id_paciente_so = Column(String(50), nullable=False)
    valor_so = Column(Float, nullable=False)
    fecha_medicion_so = Column(DateTime, nullable=False)
    observaciones_so = Column(String(250))
    usuario_graba_so = Column(String(150), nullable=False)
    fecha_registro_so = Column(DateTime)
    usuario_modifica_so = Column(String(150))
    fecha_modifica_so = Column(DateTime)

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        date_field = table_mapping['date_field']
        std_table_name = table_mapping['standard_table_name']
        
        # Get patient ID and registration date
        patient_id = getattr(self, id_field)
        registration_date = getattr(self, date_field) if date_field else None
        
        # Combine observations and user information
        observations = []
        if self.observaciones_so:
            observations.append(self.observaciones_so)
        observations.append(f"Recorded by: {self.usuario_graba_so}")
        if self.usuario_modifica_so and self.fecha_modifica_so:
            observations.append(f"Last modified by: {self.usuario_modifica_so} on {dt_to_string(self.fecha_modifica_so)}")
        
        return format_vital_signs_message(
            patient_id=patient_id,
            measurement_type=std_table_name,
            measurement_id=str(self.id_secuencia_so),
            value=self.valor_so,
            register_datetime=registration_date,
            units="%",
            reference_range="95-100",
            observation_datetime=self.fecha_medicion_so,
            observation=" | ".join(observations) if observations else None,
            period_end=dt_to_string(self.fecha_modifica_so) if self.fecha_modifica_so else None
        )

# Register the model
SaturacionOxigeno.register_model(SATURACION_OXIGENO)

# Temperatura model
class Temperatura(BaseModel):
    """
    SQLAlchemy data model for the 'temperatura' table.
    """
    __tablename__ = TEMPERATURA
    
    id_secuencia_temp = Column(Integer, primary_key=True)
    id_paciente_temp = Column(String(50), nullable=False)
    valor_temp = Column(Float, nullable=False)
    escala_temp = Column(String(250), nullable=False)
    fecha_medicion_temp = Column(DateTime, nullable=False)
    observaciones_temp = Column(String(250))
    usuario_graba_temp = Column(String(150), nullable=False)
    fecha_registro_temp = Column(DateTime, nullable=False)
    usuario_modifica_temp = Column(String(150))
    fecha_modifica_temp = Column(DateTime)

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        date_field = table_mapping['date_field']
        std_table_name = table_mapping['standard_table_name']
        
        # Get patient ID and registration date
        patient_id = getattr(self, id_field)
        registration_date = getattr(self, date_field) if date_field else None
        
        # Combine observations and user information
        observations = []
        if self.observaciones_temp:
            observations.append(self.observaciones_temp)
        observations.append(f"Recorded by: {self.usuario_graba_temp}")
        if self.usuario_modifica_temp and self.fecha_modifica_temp:
            observations.append(f"Last modified by: {self.usuario_modifica_temp} on {dt_to_string(self.fecha_modifica_temp)}")
        
        return format_vital_signs_message(
            patient_id=patient_id,
            measurement_type=std_table_name,
            measurement_id=str(self.id_secuencia_temp),
            value=self.valor_temp,
            register_datetime=registration_date,
            units=self.escala_temp,
            reference_range="36-40" if self.escala_temp == "ºC" else "96.8-104",
            observation_datetime=self.fecha_medicion_temp,
            observation=" | ".join(observations) if observations else None,
            period_end=dt_to_string(self.fecha_modifica_temp) if self.fecha_modifica_temp else None
        )

# Register the model
Temperatura.register_model(TEMPERATURA)

# Presion Arterial model
class PresionArterial(BaseModel):
    """
    SQLAlchemy data model for the 'presion_arterial' table.
    """
    __tablename__ = PRESION_ARTERIAL
    
    id_secuencia_pa = Column(Integer, primary_key=True)
    id_paciente_pa = Column(String(50), nullable=False)
    sistolica_pa = Column(Integer, nullable=False)
    diastolica_pa = Column(Integer, nullable=False)
    fecha_medicion_pa = Column(DateTime, nullable=False)
    observaciones_pa = Column(String(250))
    usuario_graba_pa = Column(String(150), nullable=False)
    fecha_registro_pa = Column(DateTime, nullable=False)
    usuario_modifica_pa = Column(String(150))
    fecha_modifica_pa = Column(DateTime)

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        date_field = table_mapping['date_field']
        std_table_name = table_mapping['standard_table_name']
        
        # Get patient ID and registration date
        patient_id = getattr(self, id_field)
        registration_date = getattr(self, date_field) if date_field else None
        
        # Combine observations and user information
        observations = []
        if self.observaciones_pa:
            observations.append(self.observaciones_pa)
        observations.append(f"Recorded by: {self.usuario_graba_pa}")
        if self.usuario_modifica_pa and self.fecha_modifica_pa:
            observations.append(f"Last modified by: {self.usuario_modifica_pa} on {dt_to_string(self.fecha_modifica_pa)}")
        
        return format_vital_signs_message(
            patient_id=patient_id,
            measurement_type=std_table_name,
            measurement_id=str(self.id_secuencia_pa),
            value=f"{self.sistolica_pa}/{self.diastolica_pa}",
            register_datetime=registration_date,
            units="mmHg",
            reference_range="90-120/60-80",
            observation_datetime=self.fecha_medicion_pa,
            observation=" | ".join(observations) if observations else None,
            period_end=dt_to_string(self.fecha_modifica_pa) if self.fecha_modifica_pa else None
        )

# Register the model
PresionArterial.register_model(PRESION_ARTERIAL)

# Frecuencia Cardiaca model
class FrecuenciaCardiaca(BaseModel):
    """
    SQLAlchemy data model for the 'frecuencia_cardiaca' table.
    """
    __tablename__ = FRECUENCIA_CARDIACA
    
    id_secuencia_fc = Column(Integer, primary_key=True)
    id_paciente_fc = Column(String(50), nullable=False)
    valor_fc = Column(Float, nullable=False)
    fecha_medicion_fc = Column(DateTime, nullable=False)
    observaciones_fc = Column(String(250))
    usuario_graba_fc = Column(String(150), nullable=False)
    fecha_registro_fc = Column(DateTime)
    usuario_modifica_fc = Column(String(150))
    fecha_modifica_fc = Column(DateTime)

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        date_field = table_mapping['date_field']
        std_table_name = table_mapping['standard_table_name']

        # Get patient ID and registration date
        patient_id = getattr(self, id_field)
        registration_date = getattr(self, date_field) if date_field else None
        
        # Combine observations and user information
        observations = []
        if self.observaciones_fc:
            observations.append(self.observaciones_fc)
        observations.append(f"Recorded by: {self.usuario_graba_fc}")
        if self.usuario_modifica_fc and self.fecha_modifica_fc:
            observations.append(f"Last modified by: {self.usuario_modifica_fc} on {dt_to_string(self.fecha_modifica_fc)}")
        
        return format_vital_signs_message(
            patient_id=patient_id,
            measurement_type=std_table_name,
            measurement_id=str(self.id_secuencia_fc),
            value=self.valor_fc,
            register_datetime=registration_date,
            units="bpm",
            reference_range="60-100",
            observation_datetime=self.fecha_medicion_fc,
            observation=" | ".join(observations) if observations else None,
            period_end=dt_to_string(self.fecha_modifica_fc) if self.fecha_modifica_fc else None
        )

# Register the model
FrecuenciaCardiaca.register_model(FRECUENCIA_CARDIACA)

# Frecuencia Respiratoria model
class FrecuenciaRespiratoria(BaseModel):
    """
    SQLAlchemy data model for the 'frecuencia_respiratoria' table.
    """
    __tablename__ = FRECUENCIA_RESPIRATORIA
    
    id_secuencia_fr = Column(Integer, primary_key=True)
    id_paciente_fr = Column(String(50), nullable=False)
    valor_fr = Column(Float, nullable=False)
    fecha_medicion_fr = Column(DateTime, nullable=False)
    observaciones_fr = Column(String(250))
    usuario_graba_fr = Column(String(150), nullable=False)
    fecha_registro_fr = Column(DateTime, nullable=False)
    usuario_modifica_fr = Column(String(150))
    fecha_modifica_fr = Column(DateTime)

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        date_field = table_mapping['date_field']
        std_table_name = table_mapping['standard_table_name']

        # Get patient ID and registration date
        patient_id = getattr(self, id_field)
        registration_date = getattr(self, date_field) if date_field else None
        
        # Combine observations and user information
        observations = []
        if self.observaciones_fr:
            observations.append(self.observaciones_fr)
        observations.append(f"Recorded by: {self.usuario_graba_fr}")
        if self.usuario_modifica_fr and self.fecha_modifica_fr:
            observations.append(f"Last modified by: {self.usuario_modifica_fr} on {dt_to_string(self.fecha_modifica_fr)}")
        
        return format_vital_signs_message(
            patient_id=patient_id,
            measurement_type=std_table_name,
            measurement_id=str(self.id_secuencia_fr),
            value=self.valor_fr,
            register_datetime=registration_date,
            units="breaths/min",
            reference_range="12-20",
            observation_datetime=self.fecha_medicion_fr,
            observation=" | ".join(observations) if observations else None,
            period_end=dt_to_string(self.fecha_modifica_fr) if self.fecha_modifica_fr else None
        )

# Register the model
FrecuenciaRespiratoria.register_model(FRECUENCIA_RESPIRATORIA)

# Glucosa model
class Glucosa(BaseModel):
    """
    SQLAlchemy data model for the 'glucosa' table.
    """
    __tablename__ = GLUCOSA
    
    id_secuencia = Column(Integer, primary_key=True)
    id_paciente = Column(String(50), nullable=False)
    valor = Column(Float, nullable=False)
    escala = Column(String(250), nullable=False)
    fecha_medicion = Column(DateTime, nullable=False)
    observaciones = Column(String(250))
    usuario_graba = Column(String(150), nullable=False)
    fecha_registro = Column(DateTime, nullable=False)
    usuario_modifica = Column(String(150))
    fecha_modifica = Column(DateTime)
    hemoglob_glucosilada = Column(Float)

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        date_field = table_mapping['date_field']
        std_table_name = table_mapping['standard_table_name']
        
        # Get patient ID and registration date
        patient_id = getattr(self, id_field)
        registration_date = getattr(self, date_field) if date_field else None
        
        # Combine observations and user information
        observations = []
        if self.observaciones:
            observations.append(self.observaciones)
        observations.append(f"Recorded by: {self.usuario_graba}")
        if self.usuario_modifica and self.fecha_modifica:
            observations.append(f"Last modified by: {self.usuario_modifica} on {dt_to_string(self.fecha_modifica)}")
        
        glucose_msg = format_vital_signs_message(
            patient_id=patient_id,
            measurement_type=std_table_name,
            measurement_id=str(self.id_secuencia),
            value=self.valor,
            register_datetime=registration_date,
            units=self.escala,
            reference_range="70-100" if self.escala == "mg/dL" else "3.9-5.6",
            observation_datetime=self.fecha_medicion,
            observation=" | ".join(observations) if observations else None,
            period_end=dt_to_string(self.fecha_modifica) if self.fecha_modifica else None
        )
        
        if self.hemoglob_glucosilada is not None:
            hba1c_msg = format_vital_signs_message(
                patient_id=patient_id,
                measurement_type=std_table_name,
                measurement_id=f"{self.id_secuencia}_hba1c",
                value=self.hemoglob_glucosilada,
                register_datetime=registration_date,
                units="%",
                reference_range="4.0-5.6",
                observation_datetime=self.fecha_medicion,
                observation=" | ".join(observations) if observations else None,
                period_end=dt_to_string(self.fecha_modifica) if self.fecha_modifica else None
            )
            return f"{glucose_msg}\r{hba1c_msg}"
        
        return glucose_msg

# Register the model
Glucosa.register_model(GLUCOSA)

# Peso model
class Peso(BaseModel):
    """
    SQLAlchemy data model for the 'peso' table.
    """
    __tablename__ = PESO
    
    id_secuencia = Column(Integer, primary_key=True)
    id_paciente = Column(String(50), nullable=False)
    valor = Column(Float, nullable=False)
    imc = Column(Float, nullable=False)
    escala = Column(String(250), nullable=False)
    fecha_medicion = Column(DateTime, nullable=False)
    observaciones = Column(String(250))
    usuario_graba = Column(String(150), nullable=False)
    fecha_registro = Column(DateTime, nullable=False)
    usuario_modifica = Column(String(150))
    fecha_modifica = Column(DateTime)

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        date_field = table_mapping['date_field']
        std_table_name = table_mapping['standard_table_name']
        
        # Get patient ID and registration date
        patient_id = getattr(self, id_field)
        registration_date = getattr(self, date_field) if date_field else None
        
        # Combine observations and user information
        observations = []
        if self.observaciones:
            observations.append(self.observaciones)
        observations.append(f"Recorded by: {self.usuario_graba}")
        if self.usuario_modifica and self.fecha_modifica:
            observations.append(f"Last modified by: {self.usuario_modifica} on {dt_to_string(self.fecha_modifica)}")
        
        # Create two OBX segments for weight and BMI
        weight_msg = format_vital_signs_message(
            patient_id=patient_id,
            measurement_type=std_table_name,
            measurement_id=str(self.id_secuencia),
            value=self.valor,
            register_datetime=registration_date,
            units=self.escala,
            reference_range=None,
            observation_datetime=self.fecha_medicion,
            observation=" | ".join(observations) if observations else None,
            period_end=dt_to_string(self.fecha_modifica) if self.fecha_modifica else None
        )
        
        bmi_msg = format_vital_signs_message(
            patient_id=patient_id,
            measurement_type=std_table_name,
            measurement_id=f"{self.id_secuencia}_bmi",
            value=self.imc,
            register_datetime=registration_date,
            units="kg/m²",
            reference_range="18.5-24.9",
            observation_datetime=self.fecha_medicion,
            observation=" | ".join(observations) if observations else None,
            period_end=dt_to_string(self.fecha_modifica) if self.fecha_modifica else None
        )
        return f"{weight_msg}\r{bmi_msg}"

# Register the model
Peso.register_model(PESO)

# Talla model
class Talla(BaseModel):
    """
    SQLAlchemy data model for the 'talla' table.
    """
    __tablename__ = TALLA
    
    id_secuencia = Column(Integer, primary_key=True)
    id_paciente = Column(String(50), nullable=False)
    valor = Column(Float, nullable=False)
    fecha_medicion = Column(DateTime, nullable=False)
    observaciones = Column(String(250))
    usuario_graba = Column(String(150), nullable=False)
    fecha_registro = Column(DateTime, nullable=False)
    usuario_modifica = Column(String(150))
    fecha_modifica = Column(DateTime)

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        date_field = table_mapping['date_field']
        std_table_name = table_mapping['standard_table_name']
        
        # Get patient ID and registration date
        patient_id = getattr(self, id_field)
        registration_date = getattr(self, date_field) if date_field else None
        
        # Combine observations and user information
        observations = []
        if self.observaciones:
            observations.append(self.observaciones)
        observations.append(f"Recorded by: {self.usuario_graba}")
        if self.usuario_modifica and self.fecha_modifica:
            observations.append(f"Last modified by: {self.usuario_modifica} on {dt_to_string(self.fecha_modifica)}")
        
        return format_vital_signs_message(
            patient_id=patient_id,
            measurement_type=std_table_name,
            measurement_id=str(self.id_secuencia),
            value=self.valor,
            register_datetime=registration_date,
            units="cm",
            reference_range=None,
            observation_datetime=self.fecha_medicion,
            observation=" | ".join(observations) if observations else None,
            period_end=dt_to_string(self.fecha_modifica) if self.fecha_modifica else None
        )

# Register the model
Talla.register_model(TALLA)

# Medicacion model
class Medicacion(BaseModel):
    """
    SQLAlchemy data model for the 'medicacion' table.
    """
    __tablename__ = MEDICACION
    
    id_secuencia = Column(Integer, primary_key=True)
    id_paciente = Column(String(50), nullable=False)
    medicacion = Column(String(50), nullable=False)
    fecha_dispensacion = Column(DateTime, nullable=False)
    hora_dispensacion = Column(String(4), nullable=False)
    observaciones = Column(String(250))
    usuario_graba = Column(String(150), nullable=False)
    fecha_registro = Column(DateTime, nullable=False)
    usuario_modifica = Column(String(150))
    fecha_modifica = Column(DateTime)

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        date_field = table_mapping['date_field']
        std_table_name = table_mapping['standard_table_name']
        
        # Get patient ID and registration date
        patient_id = getattr(self, id_field)
        registration_date = getattr(self, date_field) if date_field else None
        
        # Combine observations and user information
        observations = []
        if self.observaciones:
            observations.append(self.observaciones)
        observations.append(f"Recorded by: {self.usuario_graba}")
        if self.usuario_modifica and self.fecha_modifica:
            observations.append(f"Last modified by: {self.usuario_modifica} on {dt_to_string(self.fecha_modifica)}")
        
        # Combine date and time for medication administration
        admin_datetime = f"{dt_to_string(self.fecha_dispensacion, dt_fmt_str='%Y%m%d')}{self.hora_dispensacion}"
        return format_vital_signs_message(
            patient_id=patient_id,
            measurement_type=std_table_name,
            measurement_id=str(self.id_secuencia),
            value=self.medicacion,
            register_datetime=registration_date,
            units=None,
            reference_range=None,
            observation_datetime=admin_datetime,
            observation=" | ".join(observations) if observations else None,
            period_end=dt_to_string(self.fecha_modifica) if self.fecha_modifica else None
        )

# Register the model
Medicacion.register_model(MEDICACION)

# Deposiciones model
class Deposiciones(BaseModel):
    """
    SQLAlchemy data model for the 'deposiciones' table.
    """
    __tablename__ = DEPOSICIONES
    
    id_secuencia = Column(Integer, primary_key=True)
    id_paciente = Column(String(50), nullable=False)
    valor = Column(String(50), nullable=False)
    fecha_medicion = Column(DateTime, nullable=False)
    usuario_graba = Column(String(150), nullable=False)
    fecha_registro = Column(DateTime, nullable=False)
    usuario_modifica = Column(String(150))
    fecha_modifica = Column(DateTime)
    observaciones = Column(String(250))

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        date_field = table_mapping['date_field']
        std_table_name = table_mapping['standard_table_name']
        
        # Get patient ID and registration date
        patient_id = getattr(self, id_field)
        registration_date = getattr(self, date_field) if date_field else None
        
        # Combine observations and user information
        observations = []
        if self.observaciones:
            observations.append(self.observaciones)
        observations.append(f"Recorded by: {self.usuario_graba}")
        if self.usuario_modifica and self.fecha_modifica:
            observations.append(f"Last modified by: {self.usuario_modifica} on {dt_to_string(self.fecha_modifica)}")
        
        return format_vital_signs_message(
            patient_id=patient_id,
            measurement_type=std_table_name,
            measurement_id=str(self.id_secuencia),
            value=self.valor,
            register_datetime=registration_date,
            units=None,
            reference_range=None,
            observation_datetime=self.fecha_medicion,
            observation=" | ".join(observations) if observations else None,
            period_end=dt_to_string(self.fecha_modifica) if self.fecha_modifica else None
        )

# Register the model
Deposiciones.register_model(DEPOSICIONES)

# Diuresis model
class Diuresis(BaseModel):
    """
    SQLAlchemy data model for the 'diuresis' table.
    """
    __tablename__ = DIURESIS
    
    id_secuencia = Column(Integer, primary_key=True)
    id_paciente = Column(String(50), nullable=False)
    valor = Column(String(50), nullable=False)
    vaciado_bolsa = Column(String(50), nullable=False)
    cambio_bolsa = Column(String(50), nullable=False)
    total_diario = Column(Integer, nullable=False)
    observaciones = Column(String(250))
    fecha_medicion = Column(DateTime, nullable=False)
    usuario_graba = Column(String(150), nullable=False)
    fecha_registro = Column(DateTime, nullable=False)
    usuario_modifica = Column(String(150))
    fecha_modifica = Column(DateTime)

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        date_field = table_mapping['date_field']
        std_table_name = table_mapping['standard_table_name']
        
        # Get patient ID and registration date
        patient_id = getattr(self, id_field)
        registration_date = getattr(self, date_field) if date_field else None
        
        return format_vital_signs_message(
            patient_id=patient_id,
            measurement_type=std_table_name,
            measurement_id=str(self.id_secuencia),
            value=self.valor,
            register_datetime=registration_date,
            units="mL",
            reference_range=None,
            observation=self.observaciones
        )

# Register the model
Diuresis.register_model(DIURESIS)

# Electrocardiograma model
class Electrocardiograma(BaseModel):
    """
    SQLAlchemy data model for the 'electrocardiograma' table.
    """
    __tablename__ = ELECTROCARDIOGRAMA
    
    id_secuencia = Column(Integer, primary_key=True)
    id_paciente = Column(String(50))
    unidad = Column(String(150), nullable=False)
    fecha_medicion = Column(DateTime, nullable=False)
    fecha_registro = Column(DateTime, nullable=False)
    idmonitor = Column(String(150), nullable=False)
    fecha_modifica = Column(DateTime)
    usuario_modifica = Column(String(150))
    nombrearchivo = Column(String(150), nullable=False)

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        date_field = table_mapping['date_field']
        std_table_name = table_mapping['standard_table_name']
        
        # Get patient ID and registration date
        patient_id = getattr(self, id_field)
        registration_date = getattr(self, date_field) if date_field else None
        
        # Combine observations and user information
        observations = []
        observations.append(f"Unit: {self.unidad}")
        observations.append(f"Monitor ID: {self.idmonitor}")
        if self.usuario_modifica and self.fecha_modifica:
            observations.append(f"Last modified by: {self.usuario_modifica} on {dt_to_string(self.fecha_modifica)}")
        
        return format_vital_signs_message(
            patient_id=patient_id,
            measurement_type=std_table_name,
            measurement_id=str(self.id_secuencia),
            value=self.nombrearchivo,  # Using filename as value since ECG is typically stored as a file
            register_datetime=registration_date,
            units=None,
            reference_range=None,
            observation_datetime=self.fecha_medicion,
            observation=" | ".join(observations) if observations else None,
            period_end=dt_to_string(self.fecha_modifica) if self.fecha_modifica else None
        )

# Register the model
Electrocardiograma.register_model(ELECTROCARDIOGRAMA)

# Fotos Hospwin model
class FotosHospwin(BaseModel):
    """
    SQLAlchemy data model for the 'fotos_hospwin' table.
    """
    __tablename__ = FOTOS_HOSPWIN
    
    id_paciente = Column(String(50), primary_key=True)
    f_actual = Column(DateTime)
    tipo = Column(String(3))
    foto = Column(String)  # This should be a binary field in PostgreSQL
    observaciones = Column(String(250))

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        date_field = table_mapping['date_field']
        std_table_name = table_mapping['standard_table_name']
        
        # Get patient ID and registration date
        patient_id = getattr(self, id_field)
        registration_date = getattr(self, date_field) if date_field else None
        
        # Combine observations and user information
        observations = []
        if self.observaciones:
            observations.append(self.observaciones)
        if self.f_actual:
            observations.append(f"Photo taken on: {dt_to_string(self.f_actual)}")
        
        return format_vital_signs_message(
            patient_id=patient_id,
            measurement_type=std_table_name,
            measurement_id=patient_id,  # Using patient ID as measurement ID since it's the primary key
            value=self.tipo,  # Using photo type as value
            register_datetime=registration_date,
            units=None,
            reference_range=None,
            observation_datetime=self.f_actual,
            observation=" | ".join(observations) if observations else None
        )

# Register the model
FotosHospwin.register_model(FOTOS_HOSPWIN)

# Monitores Activos model
class MonitoresActivos(BaseModel):
    """
    SQLAlchemy data model for the 'monitores_activos' table.
    """
    __tablename__ = MONITORES_ACTIVOS
    
    id_monitor = Column(String(50), primary_key=True)
    id_paciente = Column(String(50), nullable=False)
    usuario = Column(String(250))
    fecha_conexion = Column(DateTime)
    estado = Column(String(1))

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        date_field = table_mapping['date_field']
        std_table_name = table_mapping['standard_table_name']
        
        # Get patient ID and registration date
        patient_id = getattr(self, id_field)
        registration_date = getattr(self, date_field) if date_field else None
        
        # Combine observations and user information
        observations = []
        if self.usuario:
            observations.append(f"User: {self.usuario}")
        if self.fecha_conexion:
            observations.append(f"Connection date: {dt_to_string(self.fecha_conexion)}")
        
        return format_vital_signs_message(
            patient_id=patient_id,
            measurement_type=std_table_name,
            measurement_id=self.id_monitor,
            value=self.estado,
            register_datetime=registration_date,
            units=None,
            reference_range=None,
            observation_datetime=self.fecha_conexion,
            observation=" | ".join(observations) if observations else None
        )

# Register the model
MonitoresActivos.register_model(MONITORES_ACTIVOS)

# Pacientes Hospwin model
class PacientesHospwin(BaseModel):
    """
    SQLAlchemy data model for the 'pacientes_hospwin' table.
    """
    __tablename__ = PACIENTES_HOSPWIN
    
    id_paciente = Column(String(50), primary_key=True)
    numehist = Column(String(10))
    niu = Column(String(10))
    nombre = Column(String(50))
    apellido1 = Column(String(50))
    apellido2 = Column(String(50))
    fonetica = Column(String(50))
    situacion = Column(String(2))
    situhpar = Column(String(2))
    situcext = Column(String(2))
    numecama = Column(String(5))
    unihpar = Column(String(4))
    unicext = Column(String(4))
    equipo = Column(String(4))
    equipohpar = Column(String(4))
    equipocext = Column(String(4))
    cuentacontable = Column(String(12))
    cuentaentidad = Column(String(12))
    cuentabancaria = Column(String(20))
    formapago = Column(String(2))
    sexo = Column(String(1))
    estacivil = Column(String(50))

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        std_table_name = table_mapping['standard_table_name']
        # Get patient ID
        patient_id = getattr(self, id_field)
        
        # Combine patient information into observations
        observations = []
        if self.numehist:
            observations.append(f"History number: {self.numehist}")
        if self.niu:
            observations.append(f"NIU: {self.niu}")
        if self.situacion:
            observations.append(f"Situation: {self.situacion}")
        if self.numecama:
            observations.append(f"Bed number: {self.numecama}")
        if self.unihpar:
            observations.append(f"Unit: {self.unihpar}")
        if self.equipo:
            observations.append(f"Team: {self.equipo}")
        
        return format_vital_signs_message(
            patient_id=patient_id,
            measurement_type=std_table_name,
            measurement_id=patient_id,
            value=f"{self.nombre} {self.apellido1} {self.apellido2}",
            register_datetime=None,
            units=None,
            reference_range=None,
            observation=" | ".join(observations) if observations else None
        )

# Register the model
PacientesHospwin.register_model(PACIENTES_HOSPWIN)

# Usuario Hospwin model
class UsuarioHospwin(BaseModel):
    """
    SQLAlchemy data model for the 'usuario_hospwin' table.
    """
    __tablename__ = USUARIO_HOSPWIN
    
    id_usuario = Column(String(150), primary_key=True)
    apellido1 = Column(String(50))
    apellido2 = Column(String(50))
    nombre = Column(String(50))
    clave = Column(String(20))
    activo = Column(String(1))
    codigo = Column(String(10))
    operador = Column(String(10))
    idpersonal = Column(String(5))
    consupervision = Column(String(1))
    claveage = Column(String(33))
    fecha_ultimo_cambio_clave = Column(DateTime)

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        date_field = table_mapping['date_field']
        std_table_name = table_mapping['standard_table_name']
        
        # Get user ID and last password change date
        user_id = getattr(self, id_field)
        last_pwd_change = getattr(self, date_field) if date_field else None
        
        # Combine user information into observations
        observations = []
        if self.codigo:
            observations.append(f"Code: {self.codigo}")
        if self.operador:
            observations.append(f"Operator: {self.operador}")
        if self.idpersonal:
            observations.append(f"Staff ID: {self.idpersonal}")
        if self.activo:
            observations.append(f"Active: {self.activo}")
        if self.consupervision:
            observations.append(f"Supervision required: {self.consupervision}")
        
        return format_vital_signs_message(
            patient_id=user_id,  # Using user ID as patient ID for HL7 message
            measurement_type=std_table_name,
            measurement_id=user_id,
            value=f"{self.nombre} {self.apellido1} {self.apellido2}",
            register_datetime=last_pwd_change,
            units=None,
            reference_range=None,
            observation=" | ".join(observations) if observations else None,
            period_end=dt_to_string(last_pwd_change) if last_pwd_change else None
        )

# Register the model
UsuarioHospwin.register_model(USUARIO_HOSPWIN)

# Cierre Ulcera model
class CierreUlcera(BaseModel):
    """
    SQLAlchemy data model for the 'cierre_ulcera' table.
    """
    __tablename__ = CIERRE_ULCERA
    
    id_secuencia = Column(Integer, primary_key=True)
    id_paciente = Column(String(50), nullable=False)
    fecha = Column(DateTime, nullable=False)
    observaciones = Column(String(250))
    usuario_graba = Column(String(150), nullable=False)
    fecha_registro = Column(DateTime, nullable=False)
    usuario_modifica = Column(String(150))
    fecha_modifica = Column(DateTime)

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        date_field = table_mapping['date_field']
        std_table_name = table_mapping['standard_table_name']
        
        # Get patient ID and registration date
        patient_id = getattr(self, id_field)
        registration_date = getattr(self, date_field) if date_field else None
        
        # Combine observations and user information
        observations = []
        if self.observaciones:
            observations.append(self.observaciones)
        observations.append(f"Recorded by: {self.usuario_graba}")
        if self.usuario_modifica and self.fecha_modifica:
            observations.append(f"Last modified by: {self.usuario_modifica} on {dt_to_string(self.fecha_modifica)}")
        
        return format_vital_signs_message(
            patient_id=patient_id,
            measurement_type=std_table_name,
            measurement_id=str(self.id_secuencia),
            value="CLOSED",
            register_datetime=registration_date,
            units=None,
            reference_range=None,
            observation_datetime=self.fecha,
            observation=" | ".join(observations) if observations else None,
            period_end=dt_to_string(self.fecha_modifica) if self.fecha_modifica else None
        )

# Register the model
CierreUlcera.register_model(CIERRE_ULCERA)

# Constantes model
class Constantes(BaseModel):
    """
    SQLAlchemy data model for the 'constantes' table.
    """
    __tablename__ = CONSTANTES
    
    id_constantes = Column(Integer, primary_key=True)
    id_secuencia_temp = Column(Integer, nullable=False)
    id_secuencia_pa = Column(Integer, nullable=False)
    id_secuencia_fc = Column(Integer, nullable=False)
    id_secuencia_fr = Column(Integer, nullable=False)
    id_secuencia_so = Column(Integer, nullable=False)
    id_paciente = Column(String(50), nullable=False)
    fecha_medicion = Column(DateTime)

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        date_field = table_mapping['date_field']
        std_table_name = table_mapping['standard_table_name']
        
        # Get patient ID and measurement date
        patient_id = getattr(self, id_field)
        measurement_date = getattr(self, date_field) if date_field else None
        
        # Create observations with sequence IDs for each vital sign
        observations = [
            f"Temperature sequence: {self.id_secuencia_temp}",
            f"Blood pressure sequence: {self.id_secuencia_pa}",
            f"Heart rate sequence: {self.id_secuencia_fc}",
            f"Respiratory rate sequence: {self.id_secuencia_fr}",
            f"Oxygen saturation sequence: {self.id_secuencia_so}"
        ]
        
        return format_vital_signs_message(
            patient_id=patient_id,
            measurement_type=std_table_name,
            measurement_id=str(self.id_constantes),
            value="COMPLETE",  # Indicates a complete set of vital signs
            register_datetime=measurement_date,
            units=None,
            reference_range=None,
            observation_datetime=measurement_date,
            observation=" | ".join(observations) if observations else None
        )

# Register the model
Constantes.register_model(CONSTANTES)

# Contencion model
class Contencion(BaseModel):
    """
    SQLAlchemy data model for the 'contencion' table.
    """
    __tablename__ = CONTENCION
    
    id_secuencia = Column(Integer, primary_key=True)
    id_paciente = Column(String(50), nullable=False)
    tipo_apoyo = Column(String(50), nullable=False)
    anyo = Column(Integer, nullable=False)
    mes = Column(String(2), nullable=False)
    motivo = Column(String(250))
    tipo_contencion = Column(String(250), nullable=False)
    numero_puntos = Column(String(250), nullable=False)
    fecha_inicio = Column(DateTime, nullable=False)
    hora_inicio = Column(Integer, nullable=False)
    usuario_registro_inicio = Column(String(150), nullable=False)
    fecha_fin = Column(DateTime)
    hora_fin = Column(Integer, nullable=False)
    usuario_registro_fin = Column(String(250))
    duracion = Column(String(10))
    frecuencia_revision = Column(String(50))
    descripcion = Column(String(250))
    observaciones = Column(String(250))
    usuario_graba = Column(String(150), nullable=False)
    fecha_registro = Column(DateTime, nullable=False)
    usuario_modifica = Column(String(150))
    fecha_modifica = Column(DateTime)

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        date_field = table_mapping['date_field']
        std_table_name = table_mapping['standard_table_name']
        
        # Get patient ID and registration date
        patient_id = getattr(self, id_field)
        registration_date = getattr(self, date_field) if date_field else None
        
        # Format start and end times
        start_time = f"{dt_to_string(self.fecha_inicio, dt_fmt_str='%Y%m%d')}{self.hora_inicio:04d}"
        end_time = f"{dt_to_string(self.fecha_fin, dt_fmt_str='%Y%m%d')}{self.hora_fin:04d}" if self.fecha_fin else 'Ongoing'
        
        # Combine observations and user information
        observations = []
        if self.motivo:
            observations.append(f"Reason: {self.motivo}")
        if self.descripcion:
            observations.append(f"Description: {self.descripcion}")
        if self.observaciones:
            observations.append(f"Notes: {self.observaciones}")
        observations.append(f"Recorded by: {self.usuario_graba}")
        if self.usuario_modifica and self.fecha_modifica:
            observations.append(f"Last modified by: {self.usuario_modifica} on {dt_to_string(self.fecha_modifica)}")
        
        return format_vital_signs_message(
            patient_id=patient_id,
            measurement_type=std_table_name,
            measurement_id=str(self.id_secuencia),
            value=self.tipo_contencion,
            register_datetime=registration_date,
            units=None,
            reference_range=None,
            observation_datetime=self.fecha_inicio,
            observation=" | ".join(observations) if observations else None,
            period_start=start_time,
            period_end=end_time
        )

# Register the model
Contencion.register_model(CONTENCION)

# Cuidado Ulcera model
class CuidadoUlcera(BaseModel):
    """
    SQLAlchemy data model for the 'cuidado_ulcera' table.
    """
    __tablename__ = CUIDADO_ULCERA
    
    id_secuencia = Column(Integer, primary_key=True)
    id_paciente = Column(String(50), nullable=False)
    anyo = Column(String(4), nullable=False)
    mes = Column(String(2), nullable=False)
    dia = Column(String(2), nullable=False)
    usuario_graba = Column(String(150), nullable=False)
    fecha_registro = Column(DateTime, nullable=False)
    usuario_modifica = Column(String(150))
    fecha_modifica = Column(DateTime)

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        date_field = table_mapping['date_field']
        std_table_name = table_mapping['standard_table_name']
        
        # Get patient ID and registration date
        patient_id = getattr(self, id_field)
        registration_date = getattr(self, date_field) if date_field else None
        
        # Format care date
        care_date = f"{self.anyo}{self.mes}{self.dia}"
        
        # Combine user information and modification details into observations
        observations = []
        observations.append(f"Recorded by: {self.usuario_graba}")
        if self.usuario_modifica and self.fecha_modifica:
            observations.append(f"Last modified by: {self.usuario_modifica} on {dt_to_string(self.fecha_modifica)}")
        
        return format_vital_signs_message(
            patient_id=patient_id,
            measurement_type=std_table_name,
            measurement_id=str(self.id_secuencia),
            value="PERFORMED",
            register_datetime=registration_date,
            units=None,
            reference_range=None,
            observation_datetime=care_date,
            observation=" | ".join(observations) if observations else None,
            period_end=dt_to_string(self.fecha_modifica) if self.fecha_modifica else None
        )

# Register the model
CuidadoUlcera.register_model(CUIDADO_ULCERA)

# Menstruacion model
class Menstruacion(BaseModel):
    """
    SQLAlchemy data model for the 'menstruacion' table.
    """
    __tablename__ = MENSTRUACION
    
    id_secuencia = Column(Integer, primary_key=True)
    id_paciente = Column(String(10), nullable=False)
    anyo = Column(String(4), nullable=False)
    mes = Column(String(2), nullable=False)
    fecha_inicio = Column(String(11), nullable=False)
    observaciones = Column(String(250))
    usuario_graba = Column(String(150), nullable=False)
    fecha_registro = Column(DateTime, nullable=False)
    usuario_modifica = Column(String(150))
    fecha_modifica = Column(DateTime)
    fecha_fin = Column(String(11))

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        date_field = table_mapping['date_field']
        std_table_name = table_mapping['standard_table_name']
        
        # Get patient ID and registration date
        patient_id = getattr(self, id_field)
        registration_date = getattr(self, date_field) if date_field else None
        
        # Format period dates
        period_start = f"{self.anyo}{self.mes}{self.fecha_inicio}"
        period_end = f"{self.anyo}{self.mes}{self.fecha_fin}" if self.fecha_fin else None
        
        return format_vital_signs_message(
            patient_id=patient_id,
            measurement_type=std_table_name,
            measurement_id=str(self.id_secuencia),
            value="ACTIVE",
            register_datetime=registration_date,
            units=None,
            reference_range=None,
            period_start=period_start,
            period_end=period_end,
            observation=self.observaciones
        )

# Register the model
Menstruacion.register_model(MENSTRUACION)

# Monitor model
class Monitor(BaseModel):
    """
    SQLAlchemy data model for the 'monitor' table.
    """
    __tablename__ = MONITOR
    
    id_secuencia = Column(Integer, primary_key=True)
    id_monitor = Column(String(50), nullable=False)
    descripcion = Column(String(250))
    fecha_registro = Column(DateTime, nullable=False)
    usuario_graba = Column(String(50), nullable=False)
    fecha_modifica = Column(DateTime)
    usuario_modifica = Column(String(50))
    estado = Column(String(1), nullable=False)
    unidad = Column(String(150))

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        date_field = table_mapping['date_field']
        std_table_name = table_mapping['standard_table_name']
        
        # Get monitor ID and registration date
        monitor_id = getattr(self, id_field)
        registration_date = getattr(self, date_field) if date_field else None
        
        # Combine description and user information into observations
        observations = []
        if self.descripcion:
            observations.append(f"Description: {self.descripcion}")
        if self.unidad:
            observations.append(f"Unit: {self.unidad}")
        observations.append(f"Recorded by: {self.usuario_graba}")
        if self.usuario_modifica and self.fecha_modifica:
            observations.append(f"Last modified by: {self.usuario_modifica} on {dt_to_string(self.fecha_modifica)}")
        
        return format_vital_signs_message(
            patient_id=monitor_id,  # Using monitor ID as patient ID
            measurement_type=std_table_name,
            measurement_id=str(self.id_secuencia),
            value=self.estado,
            register_datetime=registration_date,
            units=None,
            reference_range=None,
            observation_datetime=self.fecha_registro,
            observation=" | ".join(observations) if observations else None,
            period_end=dt_to_string(self.fecha_modifica) if self.fecha_modifica else None
        )

# Register the model
Monitor.register_model(MONITOR)

# Tarjeta model
class Tarjeta(BaseModel):
    """
    SQLAlchemy data model for the 'tarjeta' table.
    """
    __tablename__ = TARJETA
    
    idtarjeta = Column(String(50), primary_key=True)
    idusuario = Column(String(50), nullable=False)

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        date_field = table_mapping['date_field']
        std_table_name = table_mapping['standard_table_name']
        
        # Get card ID and registration date
        card_id = getattr(self, id_field)
        registration_date = getattr(self, date_field) if date_field else None
        
        # Create observation with user assignment
        observation = f"Assigned to user: {self.idusuario}"
        
        return format_vital_signs_message(
            patient_id=card_id,  # Using card ID as patient ID
            measurement_type=std_table_name,
            measurement_id=card_id,
            value=self.idusuario,  # The user ID this card is assigned to
            register_datetime=registration_date,
            units=None,
            reference_range=None,
            observation=observation
        )

# Register the model
Tarjeta.register_model(TARJETA)

# Tipo Sonda model
class TipoSonda(BaseModel):
    """
    SQLAlchemy data model for the 'tipo_sonda' table.
    """
    __tablename__ = TIPO_SONDA
    
    id_secuencia = Column(Integer, primary_key=True)
    id_paciente = Column(String(50), nullable=False)
    tipo_sonda = Column(String(50), nullable=False)
    fecha_colocacion = Column(DateTime, nullable=False)
    usuario_graba = Column(String(150), nullable=False)
    fecha_registro = Column(DateTime, nullable=False)
    usuario_modifica = Column(String(150))
    fecha_modifica = Column(DateTime)

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        date_field = table_mapping['date_field']
        std_table_name = table_mapping['standard_table_name']
        
        # Get patient ID and registration date
        patient_id = getattr(self, id_field)
        registration_date = getattr(self, date_field) if date_field else None
        
        # Combine user information into observations
        observations = [f"Recorded by: {self.usuario_graba}"]
        if self.usuario_modifica and self.fecha_modifica:
            observations.append(f"Last modified by: {self.usuario_modifica} on {dt_to_string(self.fecha_modifica)}")
        
        return format_vital_signs_message(
            patient_id=patient_id,
            measurement_type=std_table_name,
            measurement_id=str(self.id_secuencia),
            value=self.tipo_sonda,
            register_datetime=registration_date,
            units=None,
            reference_range=None,
            observation_datetime=self.fecha_colocacion,
            observation=" | ".join(observations) if observations else None,
            period_end=dt_to_string(self.fecha_modifica) if self.fecha_modifica else None
        )

# Register the model
TipoSonda.register_model(TIPO_SONDA)

# Tratamiento Ulcera model
class TratamientoUlcera(BaseModel):
    """
    SQLAlchemy data model for the 'tratamiento_ulcera' table.
    """
    __tablename__ = TRATAMIENTO_ULCERA
    
    id_secuencia = Column(Integer, primary_key=True)
    id_paciente = Column(String(50), nullable=False)
    fecha = Column(DateTime, nullable=False)
    estado = Column(String(100), nullable=False)
    fecha_deteccion = Column(DateTime, nullable=False)
    descripccion = Column(String(250), nullable=False)
    usuario_graba = Column(String(150), nullable=False)
    fecha_registro = Column(DateTime, nullable=False)
    usuario_modifica = Column(String(150))
    fecha_modifica = Column(DateTime)

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        date_field = table_mapping['date_field']
        std_table_name = table_mapping['standard_table_name']
        
        # Get patient ID and registration date
        patient_id = getattr(self, id_field)
        registration_date = getattr(self, date_field) if date_field else None
        
        # Combine description and user information into observations
        observations = [f"Description: {self.descripccion}"]
        observations.append(f"Detection date: {dt_to_string(self.fecha_deteccion)}")
        observations.append(f"Recorded by: {self.usuario_graba}")
        if self.usuario_modifica and self.fecha_modifica:
            observations.append(f"Last modified by: {self.usuario_modifica} on {dt_to_string(self.fecha_modifica)}")
        
        return format_vital_signs_message(
            patient_id=patient_id,
            measurement_type=std_table_name,
            measurement_id=str(self.id_secuencia),
            value=self.estado,
            register_datetime=registration_date,
            units=None,
            reference_range=None,
            observation_datetime=self.fecha,
            observation=" | ".join(observations) if observations else None,
            period_end=dt_to_string(self.fecha_modifica) if self.fecha_modifica else None
        )

# Register the model
TratamientoUlcera.register_model(TRATAMIENTO_ULCERA)

# Ulceras model
class Ulceras(BaseModel):
    """
    SQLAlchemy data model for the 'ulceras' table.
    """
    __tablename__ = ULCERAS
    
    id_secuencia = Column(Integer, primary_key=True)
    id_paciente = Column(String(50), nullable=False)
    localizacion = Column(String(100), nullable=False)
    tipo = Column(String(50), nullable=False)
    fecha_deteccion = Column(DateTime, nullable=False)
    procedencia = Column(String(100), nullable=False)
    usuario_graba = Column(String(50), nullable=False)
    fecha_registro = Column(DateTime, nullable=False)
    usuario_modifica = Column(String(50))
    fecha_modifica = Column(DateTime)

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        date_field = table_mapping['date_field']
        std_table_name = table_mapping['standard_table_name']
        
        # Get patient ID and registration date
        patient_id = getattr(self, id_field)
        registration_date = getattr(self, date_field) if date_field else None
        
        # Combine location, origin, and user information into observations
        observations = [
            f"Location: {self.localizacion}",
            f"Origin: {self.procedencia}",
            f"Recorded by: {self.usuario_graba}"
        ]
        if self.usuario_modifica and self.fecha_modifica:
            observations.append(f"Last modified by: {self.usuario_modifica} on {dt_to_string(self.fecha_modifica)}")
        
        return format_vital_signs_message(
            patient_id=patient_id,
            measurement_type=std_table_name,
            measurement_id=str(self.id_secuencia),
            value=self.tipo,
            register_datetime=registration_date,
            units=None,
            reference_range=None,
            observation_datetime=self.fecha_deteccion,
            observation=" | ".join(observations) if observations else None,
            period_end=dt_to_string(self.fecha_modifica) if self.fecha_modifica else None
        )

# Register the model
Ulceras.register_model(ULCERAS)

# Grupousu Hospwin model
class GrupousuHospwin(BaseModel):
    """
    SQLAlchemy data model for the 'grupousu_hospwin' table.
    """
    __tablename__ = GRUPOUSU_HOSPWIN
    
    id_usuario = Column(String(50), primary_key=True)
    id_grupo = Column(String(4), nullable=False)

    def to_hl7_v2(self) -> str:
        # Get field names from mapping
        table_mapping = TABLE_FIELD_MAPPING[self.__tablename__]
        id_field = table_mapping['id_field']
        date_field = table_mapping['date_field']
        std_table_name = table_mapping['standard_table_name']
        
        # Get user ID and registration date
        user_id = getattr(self, id_field)
        registration_date = getattr(self, date_field) if date_field else None
        
        return format_vital_signs_message(
            patient_id=user_id,  # Using user ID as patient ID
            measurement_type=std_table_name,
            measurement_id=user_id,
            value=self.id_grupo,  # The group ID this user belongs to
            register_datetime=registration_date,
            units=None,
            reference_range=None
        )

# Register the model
GrupousuHospwin.register_model(GRUPOUSU_HOSPWIN)

# Parameters and constants #
#--------------------------#

# Table mappings #
#----------------#

# Map of table names to their corresponding model classes
TABLE_MODEL_MAP = {
    SATURACION_OXIGENO: SaturacionOxigeno,
    TEMPERATURA: Temperatura,
    PRESION_ARTERIAL: PresionArterial,
    FRECUENCIA_CARDIACA: FrecuenciaCardiaca,
    FRECUENCIA_RESPIRATORIA: FrecuenciaRespiratoria,
    GLUCOSA: Glucosa,
    PESO: Peso,
    TALLA: Talla,
    MEDICACION: Medicacion,
    DEPOSICIONES: Deposiciones,
    DIURESIS: Diuresis,
    ELECTROCARDIOGRAMA: Electrocardiograma,
    FOTOS_HOSPWIN: FotosHospwin,
    MONITORES_ACTIVOS: MonitoresActivos,
    PACIENTES_HOSPWIN: PacientesHospwin,
    USUARIO_HOSPWIN: UsuarioHospwin,
    CIERRE_ULCERA: CierreUlcera,
    CONSTANTES: Constantes,
    CONTENCION: Contencion,
    CUIDADO_ULCERA: CuidadoUlcera,
    MENSTRUACION: Menstruacion,
    MONITOR: Monitor,
    TARJETA: Tarjeta,
    TIPO_SONDA: TipoSonda,
    TRATAMIENTO_ULCERA: TratamientoUlcera,
    ULCERAS: Ulceras,
    GRUPOUSU_HOSPWIN: GrupousuHospwin
}