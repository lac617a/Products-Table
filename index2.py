from tkinter import ttk
from tkinter import *

import sqlite3

class Products:

	db_name = 'database.db'

	def __init__(self,ventana):
		self.vtn = ventana
		self.vtn.title('Products Application')

		# creating a FRame Container
		frame = LabelFrame(self.vtn, text='Register a new product')
		frame.grid(row=0,column=0,columnspan=3,pady=20)

		# Name Input
		Label(frame,text='Name: ').grid(row=1,column=0)
		self.name = Entry(frame)
		self.name.focus()
		self.name.grid(row=1,column=1)

		# Price Input
		Label(frame,text='Price: ').grid(row=2,column=0)
		self.price = Entry(frame)
		self.price.grid(row=2,column=1)

		# Button add Produts
		ttk.Button(frame,text='Save Product', command=self.add_products).grid(row=3,columnspan=2,sticky=W+E)

		# Output Messages
		self.message = Label(text='', fg='red')
		self.message.grid(row=3, column=0, columnspan=2,sticky=W+E)

		# Table
		self.tree = ttk.Treeview(height=10, columns=2)
		self.tree.grid(row=4,column=0,columnspan=2)
		self.tree.heading('#0',text='Name', anchor=CENTER)
		self.tree.heading('#1',text='Price',anchor=CENTER)

		# Buttons
		ttk.Button(text='DELETE',command=self.delete_products).grid(row=5, column=0, columnspan=1,sticky=W+E)
		ttk.Button(text='EDIT',command=self.edit_products).grid(row=5, column=1, columnspan=1,sticky=W+E)

		# Filling the Filas
		self.get_products()

	def run_query(self,query,parameters=()):
		with sqlite3.connect(self.db_name) as conn:
			cursor = conn.cursor()
			result = cursor.execute(query,parameters)
			conn.commit()
		return result

	def get_products(self):
		#cleaning table
		records = self.tree.get_children()
		for element in records:
			self.tree.delete(element)

		#quering data
		query = 'SELECT * FROM products ORDER BY name DESC'
		db_rows = self.run_query(query)
		# filling data
		for row in db_rows:
			self.tree.insert('',0,text=row[1], values=row[2])
	def validation(self):
		return len(self.name.get()) != 0 and len(self.price.get()) != 0

	def add_products(self):
		if self.validation():
			query = 'INSERT INTO products VALUES(NULL,?,?)'
			parameters = (self.name.get(), self.price.get())
			self.run_query(query,parameters)
			self.message['text'] = 'Product {} added Successfully'.format(self.name.get())
			self.name.delete(0,END)
			self.price.delete(0,END)
		else:
			self.message['text'] = 'Name and Price are Required'.format(self.name.get())
		self.get_products()
	
	def delete_products(self):
		self.message['text'] = ''
		try:
			self.tree.item(self.tree.selection())['text'][0]
		except IndexError as e:
			self.message['text'] = 'Please Select a Record'
			return
		self.message['text'] = ''
		name = self.tree.item(self.tree.selection())['text']
		query = 'DELETE FROM products WHERE name = ?'
		self.run_query(query,(name,))
		self.message['text'] = 'Record {} deleted Seccessfully'.format(name)
		self.get_products()
	
	def edit_products(self):
		self.message['text'] = ''
		try:
			self.tree.item(self.tree.selection())['text'][0]
		except IndexError as e:
			self.message['text'] = 'Please Select a Record'
			return
		name = self.tree.item(self.tree.selection())['text']
		old_price = self.tree.item(self.tree.selection())['values'][0]
		self.edit_vtn = Toplevel()
		self.edit_vtn.title = 'Edit Product'

		# Old Name

		Label(self.edit_vtn, text='Old Name: ').grid(row=0,column=1)
		Entry(self.edit_vtn, textvariable=StringVar(self.edit_vtn,value=name),state='readonly').grid(row=0,column=2)

		#Nuevo nombre
		Label(self.edit_vtn, text='New Name: ').grid(row=1,column=1)
		new_name = Entry(self.edit_vtn)
		new_name.grid(row=1,column=2)

		#old Price
		Label(self.edit_vtn, text='Old Price: ').grid(row=2,column=1)
		Entry(self.edit_vtn, textvariable=StringVar(self.edit_vtn,value=old_price),state='readonly').grid(row=2,column=2)
		
		#Nuevo Price
		Label(self.edit_vtn, text='New Name: ').grid(row=1,column=1)
		new_price = Entry(self.edit_vtn)
		new_price.grid(row=3,column=2)

		Button(self.edit_vtn,text='Update',command=lambda:self.edit_records(new_name.get(),new_price.get(),name,old_price)).grid(row=4,column=2,sticky=W)

	def edit_records(self,new_name,new_price,name,old_price):
		query = 'UPDATE products SET name = ?, price = ? WHERE name = ? and price = ?'
		parameters = (new_name,new_price,name,old_price)
		self.run_query(query,parameters)
		self.edit_vtn.destroy()
		self.message['text'] = 'Record {} update Successfully'.format(name)
		self.get_products()

def main():
	ventana = Tk()
	app = Products(ventana)
	ventana.mainloop()

if __name__ == '__main__':
	main()