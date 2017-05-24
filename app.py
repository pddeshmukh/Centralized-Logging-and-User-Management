import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio
import os
import os.path
import subprocess
import sys
import crypt
import re
import mysql.connector as mariadb


builder = Gtk.Builder()
builder.add_from_file("guiappcode.glade")

class handlers:
	
	def note(self, *args):
	
		notebook = self.builder.get_object('notebook1')
		nwindow = self.builder.get_object("window1")
		notebook.remove_page(-1)

		newtablabel = Gtk.Label('page1') 
		newpagelabel = Gtk.Label('l1') 

		newtablabel2 = Gtk.Label('page2') 
		newpagelabel2 = Gtk.Label('l2') 
		
		newtablabel3 = Gtk.Label('page3') 
		newpagelabel3 = Gtk.Label('l3') 
  
		notebook.insert_page(self.newpagelabel, self.newtablabel, 0)
		notebook.insert_page(self.newpagelabel2, self.newtablabel2, 1)
		notebook.insert_page(self.newpagelabel3, self.newtablabel3, 2)

		nwindow.show_all() 
		notebook.set_current_page(0) 
		
		
		
	def on_login_clicked(self, *args):
		
		username=builder.get_object("usernam")
		passwd=builder.get_object("passwor")
		
		w1=builder.get_object("loginwindow")
		w2=builder.get_object("ipaddwindow")
		w2.set_size_request(500,400)	
			
		p1=str(passwd.get_text())
		un=str(username.get_text())
		
		linkb=builder.get_object("link")
		linkb.set_label("Register")
		
		if(un!='' and p1!=''):
			
				mariadb_connection = mariadb.connect(user='root', password='pratik', database='rit')
				cursor = mariadb_connection.cursor()
		    
				try:
					cursor.execute("select * from Register where Username=%s and Password=%s" , (un,p1))
					var=cursor.fetchall()
					if(var):
						username.set_text('')
						passwd.set_text('')
						w1.hide()
						w2.show_all()
						l=builder.get_object("l1")
		
						c="./ip.sh"
						os.system(c)
		
						s=''
						for a in open('/home/pratik/APP/ip.txt' , 'r').readlines():
							a=a.strip()
							s += a +"\n"
						l.set_text(s)	
						
					else:
						messagedialog=Gtk.MessageDialog(parent=w1, type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format="Enter correct username or password")
						messagedialog.show()
						response = messagedialog.run()
						if response == Gtk.ResponseType.OK:
							messagedialog.destroy()
						username.set_text('')
						passwd.set_text('')
					
				except mariadb.Error as error:
					print ("Error: {}".format(error))
				
				mariadb_connection.commit()
				
				mariadb_connection.close()
			
		else:
			
				messagedialog=Gtk.MessageDialog(parent=w2, type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format="Enter all Fields")
				messagedialog.show()
				response = messagedialog.run()
				if response == Gtk.ResponseType.OK:
					messagedialog.destroy()
	
	def on_reset_clicked(self, *args):
		
		window=builder.get_object("loginwindow")
		username=builder.get_object("usernam")
		password=builder.get_object("passwor")
		username.set_text('')
		password.set_text('')
		
	def on_link_clicked(self, *args):
		
		window=builder.get_object("loginwindow")
		window2=builder.get_object("authwindow")
		p=builder.get_object("authpass")
		window2.set_size_request(300,200)
		window.hide()
		p.set_text('')
		window2.show_all()
	
	
	
	
	def on_authcheck_clicked(self, *args):
		
		w1=builder.get_object("registerwindow")
		w2=builder.get_object("authwindow")
		p=builder.get_object("authpass")
		p1=str(p.get_text())
		#print(p1)
		mariadb_connection = mariadb.connect(user='root', password='pratik', database='rit')
		cursor = mariadb_connection.cursor()
		    
		try:
			cursor.execute("select * from Register where Password='"+p1+"'")
			
			var=cursor.fetchall()
			#print(var)
					
			if(var):
				
				w2.hide()
				w1.show_all()
				w1.set_size_request(500,400)
				
			else:
				messagedialog=Gtk.MessageDialog(parent=w2, type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format="Authentication failuer")
				messagedialog.show()
				response = messagedialog.run()
				if response == Gtk.ResponseType.OK:
					messagedialog.destroy()
					
				
		except mariadb.Error as error:
			print ("Error: {}".format(error))
			
		mariadb_connection.commit()
		mariadb_connection.close()

	def on_cancel5_clicked(self, *args):
		
		
		w1=builder.get_object("loginwindow")
		w1.set_size_request(500,400)
		w2=builder.get_object("authwindow")
		
		w1.show_all()
		w2.hide()




	def on_register_clicked(self, *args):
		
		name=builder.get_object("name")
		username=builder.get_object("userna")
		passwd=builder.get_object("passw")
		passwd1=builder.get_object("cpassw")
		
		w1=builder.get_object("loginwindow")
		w2=builder.get_object("registerwindow")
		
		linkb=builder.get_object("link")
		linkb.set_label("Register")
		
		p1=str(passwd.get_text())
		p2=str(passwd1.get_text())
		n=str(name.get_text())
		un=str(username.get_text())
		
		if(n!='' and un!='' and p1!='' and p2!=''):
			
			if(p1==p2):
					
					mariadb_connection = mariadb.connect(user='root', password='pratik', database='rit')
					cursor = mariadb_connection.cursor()
					
					try:
						cursor.execute("truncate Register")
						
						
					except mariadb.Error as error:
						print ("Error: {}".format(error))
					mariadb_connection.commit()	
						
					try:
						cursor.execute("INSERT INTO Register values (%s,%s,%s)" , (n,un,p1))
				
					except mariadb.Error as error:
						print ("Error: {}".format(error))
				
					mariadb_connection.commit()
			
					messagedialog=Gtk.MessageDialog(parent=w2, type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format="Registration Succesfully")
					messagedialog.show()
					response = messagedialog.run()
					if response == Gtk.ResponseType.OK:
						messagedialog.destroy()
						w2.destroy()
						w1.show_all()
				
					mariadb_connection.close()
			
			else:
			
					messagedialog=Gtk.MessageDialog(parent=w2, type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format="Password doesn't match")
					messagedialog.show()
					response = messagedialog.run()
					if response == Gtk.ResponseType.OK:
						messagedialog.destroy()
						
		else:
			
			messagedialog=Gtk.MessageDialog(parent=w2, type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format="Enter all fields")
			messagedialog.show()
			response = messagedialog.run()
			if response == Gtk.ResponseType.OK:
				messagedialog.destroy()
	
	def on_cancel4_clicked(self, *args):
		
		w1=builder.get_object("loginwindow")
		w2=builder.get_object("registerwindow")	
		linkb=builder.get_object("link")
		linkb.set_label("Register")
		w2.hide()
		w1.show_all()




	def on_back5_clicked(self, *args):
		
		w1=builder.get_object("ipaddwindow")
		w2=builder.get_object("loginwindow")
		w1.hide()
		w2.show_all()
	
	def on_refreship_clicked(self, *args):
		
		l=builder.get_object("l1")
		
		c="./ip.sh"
		os.system(c)
		
		s=''
		for a in open('/home/pratik/APP/ip.txt' , 'r').readlines():
			a=a.strip()
			#print(a)
			#print(type(a))
			s += a +"\n"
		l.set_text(s)	
			
	
	def on_userm_clicked(self, *args):
		
		ip1=builder.get_object("ipp")
		ip=ip1.get_text()
		window=builder.get_object("ipaddwindow")
		
		if(ip!=''):
							
			for a in open('/home/pratik/APP/ip.txt' , 'r').readlines():
				
				a=a.strip()
				
				if(ip == a):
					
					users=builder.get_object("userlist")
					users2=builder.get_object("userlist2")
					users.remove_all()
					users2.remove_all()

					if(os.path.isfile("/root/users.txt")=="False"):
			
						c1="ssh -X root@"+ip+" touch /root/users.txt"
						os.system(c1)
		
						c2="ssh -X root@"+ip+" chmod 400 /root/users.txt"
						os.system(c2)
		
					c3="ssh -X root@"+ip+" 'egrep -w '/bin/bash' /etc/passwd | cut -d':' -f1 &> users.txt'"
					os.system(c3)
		
		
					c5="scp -r root@"+ip+":/root/users.txt /home/pratik/APP/users.txt "
					os.system(c5)

		
					lines = tuple(open("/home/pratik/APP/users.txt", 'r'))
					for (a,i) in zip(lines,range(0,len(lines))):
						users.insert_text(i,a)		
						users2.insert_text(i,a)			

					
					window=builder.get_object("ipaddwindow")
					window2=builder.get_object("window1")
					window2.set_size_request(500,400)
					window.hide()
					window2.show_all()
						

						
				'''else:
					messagedialog=Gtk.MessageDialog(parent=window, type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format="Enter ip address from following list")
					messagedialog.show()
					response = messagedialog.run()
					if response == Gtk.ResponseType.OK:
						messagedialog.destroy()'''
			
		else:
			
			messagedialog=Gtk.MessageDialog(parent=window, type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format="Enter ip address")
			messagedialog.show()
			response = messagedialog.run()
			if response == Gtk.ResponseType.OK:
				messagedialog.destroy()
		
	def on_backup_clicked(self, *args):
		
		window=builder.get_object("ipaddwindow")
		window2=builder.get_object("backupok")
		window2.set_size_request(500,400)
		window.hide()
		window2.show_all()
	
	
	
	
	def on_adduser_clicked(self, *args):
		
		window=builder.get_object("window1")
		
		IP=builder.get_object("ipp")
		ip=str(IP.get_text())
		
		unobj=builder.get_object("username.")
		fnobj=builder.get_object("fullname.")
		passobj=builder.get_object("password.")
		cpassobj=builder.get_object("cpassword.")
		lsobj=builder.get_object("loginshell")
		hdobj=builder.get_object("homedirectory")
		hd2obj=builder.get_object("homedirectory.")
		
		username=str(unobj.get_text())
		fullname=str(fnobj.get_text())
		password=str(passobj.get_text())
		password2=str(cpassobj.get_text())
		loginshell=str(lsobj.get_active_text())
		homedirectory=str(hdobj.get_active())
		namedirectory=str(hd2obj.get_text())	
		
		if(username!='' and fullname!='' and password!='' and password2!='' and loginshell!=''):
			
			
			if(password==password2):
			
				if(homedirectory=="True"):
					
					if(namedirectory!=''):
						
						cpass=crypt.crypt(password,"22")
						c="./useradd1.sh "+ip+" "+fullname+" "+cpass+" "+loginshell+" "+namedirectory+" "+username+""
						os.system(c)
						
						s=''
						for a in open('/home/pratik/APP/error.txt' , 'r').readlines():
							a=a.strip()
							s += a +"\n"
						if(s == ''):
							messagedialog=Gtk.MessageDialog(parent=window, type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format="User added succesfully")
							messagedialog.show()
							response = messagedialog.run()
							if response == Gtk.ResponseType.OK:
								messagedialog.destroy()
						else:
							messagedialog=Gtk.MessageDialog(parent=window, type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format=s)
							messagedialog.show()
							response = messagedialog.run()
							if response == Gtk.ResponseType.OK:
								messagedialog.destroy()
							
						
						
					else:
						messagedialog=Gtk.MessageDialog(parent=window, type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format="Enter Home Directory name")
						messagedialog.show()
						response = messagedialog.run()
						if response == Gtk.ResponseType.OK:
							messagedialog.destroy()
					
					
				else:
					cpass=crypt.crypt(password,"22")
					c="./useradd2.sh "+ip+" "+fullname+" "+cpass+" "+loginshell+" "+username+""
					os.system(c)
			
					s=''
					for a in open('/home/pratik/APP/useradd2error.txt' , 'r').readlines():
						a=a.strip()
						s += a +"\n"	
					
					if(s == ''):	
						messagedialog=Gtk.MessageDialog(parent=window, type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format="User added succesfully")
						messagedialog.show()
						response = messagedialog.run()
						if response == Gtk.ResponseType.OK:
							messagedialog.destroy()
					else:
						messagedialog=Gtk.MessageDialog(parent=window, type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format=s)
						messagedialog.show()
						response = messagedialog.run()
						if response == Gtk.ResponseType.OK:
							messagedialog.destroy()
			
			else:
				messagedialog=Gtk.MessageDialog(parent=window, type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format="Password doesn't match")
				messagedialog.show()
				response = messagedialog.run()
				if response == Gtk.ResponseType.OK:
					messagedialog.destroy()
		
		else:
			
			messagedialog=Gtk.MessageDialog(parent=window, type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format="Enter all fields")
			messagedialog.show()
			response = messagedialog.run()
			if response == Gtk.ResponseType.OK:
				messagedialog.destroy()		
		
		
		unobj.set_text('')
		fnobj.set_text('')
		passobj.set_text('')
		cpassobj.set_text('')
		hd2obj.set_text('')
		lsobj.set_active(-1)
		hdobj.set_active(False)

		users=builder.get_object("userlist")
		users2=builder.get_object("userlist2")
		users.remove_all()
		users2.remove_all()

		if(os.path.isfile("/root/users.txt")=="False"):
			
			c1="ssh -X root@"+ip+" touch /root/users.txt"
			os.system(c1)
		
			c2="ssh -X root@"+ip+" chmod 400 /root/users.txt"
			os.system(c2)
		
		c3="ssh -X root@"+ip+" 'egrep -w '/bin/bash' /etc/passwd | cut -d':' -f1 &> users.txt'"
		os.system(c3)
		
		
		c5="scp -r root@"+ip+":/root/users.txt /home/pratik/APP/users.txt "
		os.system(c5)

		
		lines = tuple(open("/home/pratik/APP/users.txt", 'r'))
		for (a,i) in zip(lines,range(0,len(lines))):
			users.insert_text(i,a)		
			users2.insert_text(i,a)		

	def on_homedirectory_pressed(self, *args):
		
		w1=builder.get_object("window1")
		hd=builder.get_object("homedirectory")
		hd2=builder.get_object("homedirectory.")
		r=str(hd.get_active())
		
		if(r == 'False'):
		
			hd2.set_sensitive(True)
		
		elif(r == 'True'):
			
			hd2.set_sensitive(False)
						
	def on_cancel_clicked(self, *args):
		
		w1=builder.get_object("ipaddwindow")
		w2=builder.get_object("window1")
		w2.set_size_request(500,400)
		w2.hide()
		w1.show_all()
	
	
	
	
	def on_delete2_clicked(self, *args):
		
		ipadd=builder.get_object("ipp")
		ip=str(ipadd.get_text())
		
		window2=builder.get_object("window1")
		window2.set_size_request(500,400)
	
		dcheck=builder.get_object("deletecheck")
		check=str(dcheck.get_active())
		
		users=builder.get_object("userlist")
		users2=builder.get_object("userlist2")

		username=str(users.get_active_text())
		
			
		if(check=="True"):
			
			c2="ssh -X root@"+ip+" userdel -r -f "+username+""
			os.system(c2)	
			
			messagedialog=Gtk.MessageDialog(parent=window2, type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format="User deleted succesfully")
			messagedialog.show()
			response = messagedialog.run()
			if response == Gtk.ResponseType.OK:
				messagedialog.destroy()
		
		else:
			
			c2="ssh -X root@"+ip+" userdel -f "+username+""
			os.system(c2)
			
		
			messagedialog=Gtk.MessageDialog(parent=window2, type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format="User deleted succesfully")
			messagedialog.show()
			response = messagedialog.run()
			if response == Gtk.ResponseType.OK:
				messagedialog.destroy()
		
		dcheck.set_active(False)
		users.set_active(-1)
		
		users.remove_all()
		users2.remove_all()

		if(os.path.isfile("/root/users.txt")=="False"):
			
			c1="ssh -X root@"+ip+" touch /root/users.txt"
			os.system(c1)
		
			c2="ssh -X root@"+ip+" chmod 400 /root/users.txt"
			os.system(c2)
		
		c3="ssh -X root@"+ip+" 'egrep -w '/bin/bash' /etc/passwd | cut -d':' -f1 &> users.txt'"
		os.system(c3)
		#c4="ssh -X root@"+ipadd1+" 'egrep -w '/bin/csh' /etc/passwd | cut -d':' -f1 &> users.txt'"
		#os.system(c4)
		#c6="ssh -X root@"+ipadd1+" 'egrep -w '/bin/sh' /etc/passwd | cut -d':' -f1 &> users.txt'"
		#os.system(c6)
		#c7="ssh -X root@"+ipadd1+" 'egrep -w '/bin/tcsh' /etc/passwd | cut -d':' -f1 &> users.txt'"
		#os.system(c7)
		#c8="ssh -X root@"+ipadd1+" 'egrep -w '/sbin/nologin' /etc/passwd | cut -d':' -f1 &> users.txt'"
		#os.system(c8)
		c5="scp -r root@"+ip+":/root/users.txt /home/pratik/APP/users.txt "
		os.system(c5)

		
		lines = tuple(open("/home/pratik/APP/users.txt", 'r'))
		for (a,i) in zip(lines,range(0,len(lines))):
			users.insert_text(i,a)		
			users2.insert_text(i,a)	
	
	def on_cancel2_clicked(self, *args):
		
		w1=builder.get_object("ipaddwindow")
		w2=builder.get_object("window1")
		w1.set_size_request(500,400)
		w2.hide()
		w1.show_all()
	
	
	
	
	def on_modify_clicked(self, *args):
		
		ipadd=builder.get_object("ipp")
		ip=str(ipadd.get_text())
			
		userlistobj=builder.get_object("userlist2")
		#nobj=builder.get_object("usernm")
		fnobj=builder.get_object("fullnm")
		passobj=builder.get_object("pass")
		cpassobj=builder.get_object("cpass")
		lsobj=builder.get_object("loginshel")
		hdobj=builder.get_object("homed")
		
		username=str(userlistobj.get_active_text())
		fullname=str(fnobj.get_text())
		password=str(passobj.get_text())
		password2=str(cpassobj.get_text())
		loginshell=str(lsobj.get_active_text())
		namedirectory=str(hdobj.get_text())
		
		#print(username)
		users=builder.get_object("userlist")
		users2=builder.get_object("userlist2")
		
		#print(loginshell)
		if(password==password2):
			
			#c="ssh -X root@"+ip+" eval echo ~"+username+" &> homedir"
			#os.system(c)
			
			'''aa=subprocess.Popen([c],stdout=subprocess.PIPE)
			a=aa.stdout.read()'''
			
			'''a=subprocess.check_output('ssh -X root@"+ip+" eval echo ~"+username+"',shell=False)
			print(a)'''
			
			#c1="ssh -X root@"+ip+" chmod 755 "+a+""
			#os.system(c1)
			
			cpass=crypt.crypt(password,"22")
			command1="./usermod.sh "+ip+" "+fullname+" "+loginshell+" "+namedirectory+" "+username+""
			os.system(command1)
			
			c2="ssh -X root@"+ip+" 'echo "+cpass+" | passwd --stdin "+username+"'"
			os.system(c2)
			
			#c3="ssh -X root@"+ip+" chmod 700 "+namedirectory+""
			#os.system(c3)
			
			s=''
			for a in open('/home/pratik/APP/usermoderror.txt' , 'r').readlines():
				a=a.strip()
				s += a +"\n"
			
			if(s == ''):
					
				messagedialog=Gtk.MessageDialog(parent=window, type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format="User modified succesfully")
				messagedialog.show()
				response = messagedialog.run()
				if response == Gtk.ResponseType.OK:
					messagedialog.destroy()
			else:
				messagedialog=Gtk.MessageDialog(parent=window, type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format=s)
				messagedialog.show()
				response = messagedialog.run()
				if response == Gtk.ResponseType.OK:
					messagedialog.destroy()
			
		else:
			messagedialog=Gtk.MessageDialog(parent=window, type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format="Password doesn't match")
			messagedialog.show()
			response = messagedialog.run()
			if response == Gtk.ResponseType.OK:
				messagedialog.destroy()
		
		userlistobj.set_active(-1)
		fnobj.set_text('')
		passobj.set_text('')
		cpassobj.set_text('')
		hdobj.set_text('')
		lsobj.set_active(-1)
		
		
		users.remove_all()
		users2.remove_all()

		if(os.path.isfile("/root/users.txt")=="False"):
			
			c1="ssh -X root@"+ip+" touch /root/users.txt"
			os.system(c1)
		
			c2="ssh -X root@"+ip+" chmod 400 /root/users.txt"
			os.system(c2)
		
		c3="ssh -X root@"+ip+" 'egrep -w '/bin/bash' /etc/passwd | cut -d':' -f1 &> users.txt'"
		os.system(c3)
		
		
		c5="scp -r root@"+ip+":/root/users.txt /home/pratik/APP/users.txt "
		os.system(c5)

		
		lines = tuple(open("/home/pratik/APP/users.txt", 'r'))
		for (a,i) in zip(lines,range(0,len(lines))):
			users.insert_text(i,a)		
			users2.insert_text(i,a)	
	
	def on_cancel3_clicked(self, *args):
		
		w1=builder.get_object("ipaddwindow")
		w2=builder.get_object("window1")
		w1.set_size_request(500,400)
		w2.hide()
		w1.show_all()
	
	
	
	def on_tbackup_clicked(self, *args):
		
		ipadd=builder.get_object("ipp")
		ip=str(ipadd.get_text())
		
		dpath=builder.get_object("selectpath")
		d=str(dpath.get_filename())
		
		backupok=builder.get_object("backupok")
		backupok.set_size_request(500,400)
		
		
		if(d=="None"):
			
			messagedialog=Gtk.MessageDialog(parent=backupok, type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format="please Select Path")
			messagedialog.show()
			response = messagedialog.run()
			if response == Gtk.ResponseType.OK:
				messagedialog.destroy()
		
		else:
				
			c2="./backup.sh "+ip+" "+d+""
			os.system(c2)
			
			messagedialog=Gtk.MessageDialog(parent=backupok, type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK,message_format="Backup Received Successfully")
			messagedialog.show()
			response = messagedialog.run()
			if response == Gtk.ResponseType.OK:
				messagedialog.destroy()
			#c="scp "+d+"/log root@107.170.7.21"
			#os.system(c)
			
		dpath.set_filename('')
		
	def on_back3_clicked(self, *args):
		
		w2=builder.get_object("backupok")
		w1=builder.get_object("ipaddwindow")
		w1.set_size_request(500,400)
		w2.hide()
		w1.show_all()
		
		
builder.connect_signals(handlers)
		
window = builder.get_object("loginwindow")
linkb=builder.get_object("link")
linkb.set_label("Register here")
window.set_size_request(500,400)

window.show_all()
Gtk.main()	


