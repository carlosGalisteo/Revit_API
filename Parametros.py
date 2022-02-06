# -*- coding: utf-8 -*-
#Nuestra primera linea de código nos evita errores de código ASCII

#BIBLIOTECAS
import clr
import System
from System.Collections.Generic import List

clr.AddReference('RevitAPI') 
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference('RevitAPIUI') 
import Autodesk
from Autodesk.Revit.UI.Selection import Selection, ObjectType

clr.AddReference('RevitNodes') 
import Revit
clr.ImportExtensions(Revit.Elements) 
clr.ImportExtensions(Revit.GeometryConversion) 

clr.AddReference('RevitServices') 
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
uidoc = uiapp.ActiveUIDocument


#Parametros
#---------------------------------------------------------------------------------------------------------
def parametro_global_creacion(txt):
	"""
 	Uso: 
 	Dado un nombre (string) crea un parámetro global, 
  	si el nombre no esta en uso. 
   	Salida un string, mensaje exito/fallo.
    """
	if GlobalParametersManager.IsUniqueName(doc, txt):
		if int(doc.Application.VersionNumber) >= 2022:
			GlobalParameter.Create(doc, txt, SpecTypeId.Length)
			return "Completado"
		else:
			GlobalParameter.Create(doc, txt, ParameterType.Length)
			return "Completado"
	else:
		return "Nombre en uso."

def parametro_valor(p):
    """
    Uso: 
    Dado un parametro me da el valor sin importarle 
    el tipo de almacenaje. 
    Cuidado: Campos vacios rellenos con mensaje.
    """
    if p != None: #Descarto todos los Nulls
        if p.StorageType == StorageType.String:
            v = p.AsString()
            return _parametro_valor_vacio(v)
        elif p.StorageType == StorageType.ElementId:
            v = doc.GetElement(p.AsElementId())
            return _parametro_valor_vacio(v)
        elif p.StorageType == StorageType.Double:
            v = p.AsDouble()
            return _parametro_valor_vacio(v)        
        else:
            v = p.AsInteger()
            return _parametro_valor_vacio(v)
    else:
        pass

def parametro_valor_vacio(v):
	"""
 	Uso: 
  	Dado un valor, si está vacio me da un mensaje 
   	de salida: "Campo vacio" 
    """
	if v == None:
		return "Campo vacio"
	else:
		return v

def parametro_tipo(p):
	"""
 	Uso: 
  	Conocer el tipo de un parametro.
	"""
	if int(doc.Application.VersionNumber) >= 2022: 
		#Lo que se viene: autodesk.spec: spec.string
		return p.Definition.GetDataType() #.TypeId
	else:
		#Tipo de parametro: Texto, Longitud, Volumen, Yes/No, Invalid, etc. OBSOLETO EN REVIT 2023
		return p.Definition.ParameterType

def parametro_tipo_unidad(p):
	"""
 	Uso: 
  	Conocer el tipo de unidad de un parametro.
	"""
	if int(doc.Application.VersionNumber) >= 2022:
		#Lo que se viene: autodesk.spec: spec.string
		return p.Definition.GetSpecTypeId() #.TypeId
	else:
		#Tipo de parametro: UT_Area, UT_Volumen, etc. OBSOLETO EN REVIT 2022
		return p.Definition.UnitType

def parametro_obtener_valor(parametro, elemento):
    """
    Uso:
    Obtener el valor del parametro de un elemento.
    Cuidado: Hay que pasar el nombre del parametro
    como cadena de texto
    """
    par = elemento.LookupParameter(parametro)
    valor = parametro_valor(par)
    return valor


