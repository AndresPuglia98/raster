class Obj(object):
	def __init__(self):
		self.name = ""
		self.pos = [0,0,0]

		# Datos desordenados
		self.verts = []
		self.norms = []
		self.tx_coords = []
		self.indices = []

		# Datos ordenados
		self.faces = []
		# self.vertices = []
		# self.normals = []
		# self.text_coords = []

	# funcion auxiliar
	def parse_data(self, data_values, result, skip, data_type):
		for data in data_values:
			if data == skip:
				continue
			if data_type == 'float':
				result.append(float(data))
			elif data_type == 'int':
				result.append(int(data)-1)

	def load_faces(self):
		for i, ind in enumerate(self.indices):
			if i % 3 == 0: # ordena vertices
				start = ind * 3
				end = start + 3
				self.faces.extend(self.verts[start:end])
				# self.vertices.extend(self.verts[start:end])
			elif i % 3 == 1: # ordena normales
				start = ind * 3
				end = start + 3
				self.faces.extend(self.norms[start:end])
				# self.normals.extend(self.norms[start:end])
			elif i % 3 == 2: # ordena coordenadas de textura
				start = ind * 2
				end = start + 2
				self.faces.extend(self.tx_coords[start:end])
				# self.text_coords.extend(self.tx_coords[start:end])

	def parse(self,filename):
		try:
			obj_file = open(filename, 'r')

			for line in obj_file:
				values = line.split()

				#if blank line, skip
				if not len(values):
					continue

				elif values[0] == 'o':
					self.name = values[1]

				elif values[0] == 'v':
					self.parse_data(values, self.verts, 'v', 'float')

				elif values[0] == 'vn':
					self.parse_data(values, self.norms, 'vn', 'float')

				elif values[0] == 'vt':
					self.parse_data(values, self.tx_coords, 'vt', 'float')

				elif values[0] == 'f':
					for value in values[1:]:
						val = value.split('/')
						self.parse_data(val, self.indices, 'f', 'int')

			obj_file.close()

		except IOError:
			print(".obj file not found.")

		self.load_faces()
