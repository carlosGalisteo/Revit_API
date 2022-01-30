def todos_elementos_por_familia(familia):
	"""
 	Uso: 
  	Colecta todas las instancias de una familia,
	agrupando por tipo.
	Entrada: una familia
	Salida: Lista de instancias
   	"""
	tiposIds = familia.GetFamilySymbolIds()
	
	salida = []
	for id in tiposIds:
		filtro = FamilyInstanceFilter(doc, id)
		elementos = FilteredElementCollector(doc).WherePasses(filtro).ToElements()
		salida.append(elementos)
	return salida

def todos_elementos_por_nivel(n):
	"""
 	Uso: 
  	Colecta todas las instancias que se encuentran
	en el nivel dado.
  	"""
	colector = FilteredElementCollector(doc)
	filtro = ElementLevelFilter(n.Id)
	elementos = colector.WherePasses(filtro).WhereElementIsNotElementType().ToElements()
	return elementos	

def todas_instancias():
    """
    Uso: 
    Colecta todas las instancias del documento.
    Entrada: Sin argumentos.
    Salida: Lista de tipos.
    """
    return FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements()

def todos_tipos_por_familia(familia):
	"""
 	Uso: 
 	Colecta todos los tipos conocida la familia.
  	Entrada: Una familia.
   	Salida: Lista de tipos.
    """
	tiposIds = familia.GetFamilySymbolIds()
	return [doc.GetElement(i) for i in tiposIds]

def todos_tipos():
    """
    Uso: 
    Colecta todos los tipos del documento.
    Entrada: Sin argumentos.
    Salida: Lista de tipos.
    """
    return FilteredElementCollector(doc).WhereElementIsElementType().ToElements()

def todas_vistas_por_tipo():
	"""
 	Uso: 
 	Colecta todas las vistas organizadas por tipos.
  	Entrada: Sin argumentos.
   	Salida: Lista con dos sublitas: Tipos de vista; 
    y Todas las vistas en ese orden por tipo.
    """
	tipos = System.Enum.GetValues(ViewType)
	colector = FilteredElementCollector(doc).OfClass(View).ToElements()
	
	vistas = []
	for t in tipos:
		salida = []
		for v in colector:
			if v.ViewType == t:
				salida.append(v)
			else:
				pass
		vistas.append(salida)
	return [tipos, vistas]


def todos_tipos_por_categoria(bics,doc):
	"""
 	Uso:
  	Colecta todos los tipos de la categoria o 
	categorias seleccionadas, ya sean del modelo
 	o de vinculos
  	Entrada: Lista de categorias (BuiltInCategories)
   	Salida: Tipos de las categorias seleccionadas
    """
	builtInCat = List[BuiltInCategory]() #Creamos una lista fuertemente tipada de categorias
	[builtInCat.Add(x) for x in bics]
	filtro = ElementMulticategoryFilter(builtInCat)
	vinculos = FilteredElementCollector(doc).OfClass(RevitLinkInstance)
	documentos = [x.GetLinkDocument() for x in vinculos if x.GetLinkDocument() and vinculos]
	tipos = FilteredElementCollector(doc).WherePasses(filtro).WhereElementIsElementType()
	if documentos:
		vinTipos = [FilteredElementCollector(x).WherePasses(filtro).WhereElementIsElementType() for x in documentos]
		a = [tipos] + vinTipos
		todos = []
		[[todos.append(x) for x in y]for y in a]
	else:
		todos = tipos
	return todos
