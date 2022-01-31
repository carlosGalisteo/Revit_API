# -*- coding: utf-8 -*-
#Nuestra primera linea de código nos evita errores de código ASCII

#BIBLIOTECAS
import clr

clr.AddReference('RevitAPI') 
import Autodesk
from Autodesk.Revit.DB import UnitUtils, Document

clr.AddReference('RevitNodes') 
import Revit
clr.ImportExtensions(Revit.Elements) 
clr.ImportExtensions(Revit.GeometryConversion) 

clr.AddReference('RevitServices') 
from RevitServices.Persistence import DocumentManager


doc = DocumentManager.Instance.CurrentDBDocument



def unidades_pies_a_metros(x):
	"""
 	Uso: 
  	Esta función convierte de pies a metros.
	"""
	if int(doc.Application.VersionNumber) >= 2022:
		return UnitUtils.Convert(x, UnitTypeId.Feet, UnitTypeId.Meters)
	else:
		return UnitUtils.Convert(x, DisplayUnitType.DUT_DECIMAL_FEET, DisplayUnitType.DUT_METERS)


def unidades_metros_a_pies(x):
	"""
 	Uso: 
  	Esta función convierte de metros a pies.
	"""
	if int(doc.Application.VersionNumber) >= 2022:
		return UnitUtils.Convert(x, UnitTypeId.Meters, UnitTypeId.Feet)
	else:
		return UnitUtils.Convert(x, DisplayUnitType.DUT_METERS, DisplayUnitType.DUT_DECIMAL_FEET)  
    
    
def unidades_internas_a_metros(x):
	"""
 	Uso: 
  	Esta función convierte de unidades 
   	internas a metros.
   	"""
	if int(doc.Application.VersionNumber) >= 2022:
		return UnitUtils.ConvertFromInternalUnits(x,UnitTypeId.Meters)
	else:
		return UnitUtils.ConvertFromInternalUnits(x, DisplayUnitType.DUT_METERS)

def unidades_internas_a_modelo(x):
	"""
 	Uso: 
  	Esta función convierte de unidades internas 
   	a unidades de modelo. 
	Cuidado: Unidades de longitud.
 	"""
	if int(doc.Application.VersionNumber) >= 2022:
		unidadModelo = Document.GetUnits(doc).GetFormatOptions(SpecTypeId.Length).GetUnitTypeId()
		return UnitUtils.ConvertFromInternalUnits(x,unidadModelo)
	else:
		unidadModelo = Document.GetUnits(doc).GetFormatOptions(UnitType.UT_Length).DisplayUnits
		return UnitUtils.ConvertFromInternalUnits(x, unidadModelo)

def unidades_modelo_a_internas(x):
	"""
 	Uso: 
  	Esta función convierte de unidades de modelo
   	a unidades internas. 
   	Cuidado: Unidades de longitud.
    """
	if int(doc.Application.VersionNumber) >= 2022:
		unidadModelo = Document.GetUnits(doc).GetFormatOptions(SpecTypeId.Length).GetUnitTypeId()
		return UnitUtils.ConvertToInternalUnits(x,unidadModelo)
	else:
		unidadModelo = Document.GetUnits(doc).GetFormatOptions(UnitType.UT_Length).DisplayUnits
		return UnitUtils.ConvertToInternalUnits(x, unidadModelo)


def unidades_internas_a_modelo_truncadas(x):
	"""
 	Uso: 
  	Esta función convierte de unidades de modelo
   	a unidades internas, haciendo un redondeo.
   	Cuidado: Unidades de longitud.	
	"""
	if int(doc.Application.VersionNumber) >= 2022:
		unidadModelo = Document.GetUnits(doc).GetFormatOptions(SpecTypeId.Length).GetUnitTypeId()
		#Filtramos valores de texto para evitar casos en los que no aplique
		if type(x).__name__!="str":
			valor = UnitUtils.ConvertFromInternalUnits(x,unidadModelo)
			if len(str(valor)) > 4: return round(valor,3)
			elif len(str(valor)) < 4: return round((valor + 0.0004), 3)
			else: return valor
		else:
			return x
	else:
		unidadModelo = Document.GetUnits(doc).GetFormatOptions(UnitType.UT_Length).DisplayUnits
		#Filtramos valores de texto para evitar casos en los que no aplique
		if type(x).__name__!="str":
			valor = UnitUtils.ConvertFromInternalUnits(x,unidadModelo)
			if len(str(valor)) > 4: return round(valor,3)
			elif len(str(valor)) < 4: return round((valor + 0.0004), 3)
			else: return valor
		else:
			return x