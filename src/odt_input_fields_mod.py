#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zipfile

class input_field():
	def __init__(self, i_text, xml_start_index):
		# desc, text, start, len
		self.i_description, self.i_text, self.start_index, self.text_len = self.__parse_i_field(i_text, xml_start_index)
	
	def __parse_i_field(self, f_text, xml_start_index):
		desc = self.get_expr_between_str(f_text, b'text:description="', b'"')
		i_text = self.get_expr_between_str(f_text, b'>', b'<')
		
		temp_start = f_text.find(b'>') + len(b'>')
		temp_stop = f_text[temp_start:].find(b'<') + temp_start
		
		start_index = temp_start + xml_start_index
		text_len = temp_stop - temp_start
		
		return desc, i_text, start_index, text_len
	
	def __repr__(self):
		return str(self.i_description) + " : " + str(self.i_text) + "; Start: " + str(self.start_index) + "; Len: " + str(self.text_len)
	
	def check_text_equ_str(self, comp_str):
		if (comp_str == self.i_description):
			return True
		else:
			return False
	
	def check_description_equ_str(self, comp_str):
		if (comp_str == self.i_description):
			return True
		else:
			return False
	
	def change_text(self, new_text):
		self.i_text = new_text
		self.text_len = len(new_text)
	
	def get_expr_between_str(self, s_str, start_str, stop_str):
		temp_b_str=s_str
		
		temp_start = temp_b_str.find(start_str) + len(start_str)
		temp_stop = temp_b_str[temp_start:].find(stop_str) + temp_start
		#print(temp_b_str[temp_start:temp_stop])
		target_str=temp_b_str[temp_start:temp_stop]
		
		return target_str 

class odt_input_fields_mod:
	def __init__(self, template_file_path):
		with zipfile.ZipFile(template_file_path, 'r') as z:
			self.content_file = z.read("content.xml")
		
		self.template_file_path=template_file_path
		
		self.__check_for_empty_fields_and_fill_with_whitespace()
		
		self.i_fields=self.__get_i_fields()
	
	def save_changes(self, output_path):
		zin = zipfile.ZipFile (self.template_file_path, 'r')
		zout = zipfile.ZipFile (output_path, 'w')
		for item in zin.infolist():
			buffer = zin.read(item.filename)
			if (item.filename != "content.xml"):
				zout.writestr(item, buffer)
			else:
				zout.writestr("content.xml", self.content_file)
		zout.close()
		zin.close()
	
	def replace_field_text(self, descriptor_str, new_text_str):
		# check if arguments are strings or bytearrays 
		if isinstance(new_text_str, str):
			new_text=bytes(new_text_str, 'utf-8')
		else:
			new_text=new_text_str
		if isinstance(descriptor_str, str):
			descriptor=bytes(descriptor_str, 'utf-8')
		else:
			descriptor=descriptor_str
		
		temp_lst = [n.i_description for n in self.i_fields]
		
		if descriptor in temp_lst:
			temp_field= self.i_fields[temp_lst.index(descriptor)]
			self.content_file = self.__insert_b_into_a(self.content_file, new_text, temp_field.start_index, temp_field.text_len)
			temp_field.change_text(new_text)
	
	def __insert_b_into_a(self, a, b, index_start, delete_n_chars_after_start=0):
		return a[0:index_start] + b + a[index_start + delete_n_chars_after_start:]
	
	def get_input_field_list(self):
		ret_val=[]
		for n in self.i_fields:
			ret_val.append([n.i_description, n.i_text])
		return ret_val
	
	def __str__(self):
		return "<odt_input_fields object>"
	
	def __check_for_empty_fields_and_fill_with_whitespace(self):
		insert_index_lst=[]
		temp_b_str=self.content_file
		#print(self.content_file)
		last_index=0
		while (temp_b_str.find(b'<text:text-input', last_index) > (-1)):
			temp_start = temp_b_str.find(b'<text:text-input', last_index)
			temp_stop=0
			#catch input fields without text and add to list
			if(temp_b_str.find(b'>', temp_start) == temp_b_str.find(b'/>', temp_start)+1):
				temp_stop = temp_b_str.find(b'/>', temp_start) + len(b'/>')-1
				insert_index_lst.append(temp_b_str.find(b'/>', temp_start))
			else:
				temp_stop = temp_b_str.find(b'</text:text-input>', temp_start) + len(b' </text:text-input>') -1
			last_index=temp_stop
			
		#catch input fields without text and insert whitespace
		#reverse list and start from big to small to preserve the location of the other indices
		insert_index_lst.sort(reverse=True)
		
		#print(insert_index_lst)
		
		for n in insert_index_lst:
			self.content_file = self.__insert_b_into_a(self.content_file, b'> </text:text-input>', n, 2)
	
	def __get_i_fields(self):
		ret_val=[]
		temp_b_str=self.content_file
		last_index=0
		
		while (temp_b_str.find(b'<text:text-input', last_index) > (-1)):
			temp_start = temp_b_str.find(b'<text:text-input', last_index)
			temp_stop = temp_b_str.find(b'</text:text-input>', temp_start) + len(b' </text:text-input>') -1
			ret_val.append(input_field(temp_b_str[temp_start:temp_stop], temp_start))
			last_index=temp_stop
		
		return ret_val
