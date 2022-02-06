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

#Listados
#------------------------------------------------------------------------------------------
def listado_builtInCategory():
	"""
 	Uso: 
  	Obtener el listado completo de todas las builtInCategory.
   	Entrada: Sin argumentos.
    Salida: Lista BuiltInCategory.
    """
	return System.Enum.GetValues(BuiltInCategory)

def listado_builtInParameter():
	"""
 	Uso: 
 	Obtener el listado completo de todas las builtInParameter.
  	Entrada: Sin argumentos.
   	Salida: Lista BuiltInParameter.
    """
	return System.Enum.GetValues(BuiltInParameter)

def listado_categorias():
	"""
 	Uso:
 	Obtener el listado completo de todas las categorias en dos formatos.
  	Entrada: Sin argumentos.
   	Salida: Lista con sublitas: categorias formato Revit y Dynamo.
    """
	catRevit = doc.Settings.Categories
	catDynamo = [Elements.Category.ById(c.Id.IntegerValue) for c in catRevit] #Requiere: clr.AddReference("RevitNodes")
	return [catRevit, catDynamo]

def listado_documentos_nombres():
	"""
 	Uso: 
  	Obtener el listado completo de todos los documentos.
   	Entrada: Sin argumentos.
    Salida: Lista con sublitas: documentos (doc y vinculos) y nombres.
    """
	docs = app.Documents
	nombres = [d.Title for d in docs]
	return [docs, nombres]
 
def listado_tipos_de_vista():
	"""
 	Uso: 
  	Obtener el listado completo de tipos de vista.
   	Entrada: Sin argumentos.
    Salida: Lista tipos de vista.
    """
	return System.Enum.GetValues(ViewType)
 
def listado_vinculos_documentos_nombres_rutas():
	"""
 	Uso: 
  	Obtener el listado completo de vinculos, sus documentos, 
   	sus nombres y sus rutas.
    Entrada: Sin argumentos.
    Salida: Lista con sublistas:instancias, documentos, 
    nombres y rutas.
    """
	vinculos = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()
	documentos = [x.GetLinkDocument() for x in vinculos]
	nombres = [x.Name for x in vinculos]	
	rutas = [d.PathName for d in documentos]
	return {"Link Doc": documentos, "Link Nombres": nombres, "Link Instancias": vinculos, "Link Ruta": rutas}

def listado_vistas_por_tipo():
	"""
 	Uso:
 	Sin introducir argumentos. Genera una lista con dos listas anidadas. 
  	La primera son los tipos de vista. 
   	La segunda son todas las vistas por tipo.
    """
	colector = FilteredElementCollector(doc).OfClass(View).ToElements()
	tipos = set(map(lambda v: v.ViewType, colector))
	vistas = [[v for v in colector if v.ViewType == t and v.IsTemplate == False]for t in tipos]
	return [tipos, vistas]

def listado_plantillas_vista_por_tipo():
	"""
 	Uso: 
 	Obtener el listado de plantillas de vista ordenado por tipos.
  	Entrada: Sin argumentos.
   	Salida: Dos sublistas: la primera seran los tipos; 
    la segunda las plantillas.
    Cuidado: Las plantillas 3D saldran como Null.
    """
	colector = FilteredElementCollector(doc).OfClass(View).ToElements()
	plantillas = [v for v in colector if v.IsTemplate == True]
	tipos = set(map(lambda v: v.ViewType, plantillas))
	listado = [[p for p in plantillas if p.ViewType == t]for t in tipos]
	return [tipos, listado]

def listado_plantillas_vista():
	"""
 	Uso: 
  	Lista todas las plantillas de vista.
   	Entrada: Sin argumentos.
    Salida: Lista.
    """
	colector = FilteredElementCollector(doc).OfClass(View).ToElements()
	plantillas = [v for v in colector if v.IsTemplate == True]	
	return plantillas
