# -*- coding: utf-8 -*-
from zklib import zklib
from zklib import zkconst
from datetime import datetime , timedelta
import time
import xmlrpclib
from openerp import models, fields, api
from openerp.exceptions import Warning
from odoo.exceptions import UserError
from openerp.exceptions import UserError
import config
import os


class hr_create_user_bio_machine(models.Model):
	_inherit = 'hr.employee'

	_sql_constraints= [('card_no','unique(card_no)','this Card No is already exist')]
	
	
	@api.model
	def create(self, values):
		record = super(hr_create_user_bio_machine, self).create(values)
		record.emp_machine_id = record.id	
		return record


	@api.multi
	def createBioUsers(self):
		machine_list=self.env['machine.info'].search([('id','=',2)])
		ip_list=[]
		for x in machine_list.product_ids:
			if not x.status=="no":
				ip=x.ip
				zk = zklib.ZKLib(ip, int(config.key['port']))
				result=zk.connect()
				if result == False:
					continue
				self._singleBioUser(ip)

	def _singleBioUser(self,ip):
		zk = zklib.ZKLib(ip, int(config.key['port']))
		res = zk.connect()
		if res == True:
			zk.enableDevice()
			zk.disableDevice()
			BioUsers = zk.getUser()
			for user in BioUsers[0]:
				if (BioUsers[0][user][0] == str(self.card_no)):
					raise Warning('User Already Present in Machine.')
			zk.setUser(uid=False, userid=str(self.card_no), name=str(self.name), password='', role=zkconst.LEVEL_USER)

			zk.enableDevice()
		zk.disconnect()
		zk.refreshData()

	# @api.multi
	# def createBioUsersall(self):
	# 	zk = zklib.ZKLib(config.key['ip'], int(config.key['port']))
	# 	res = zk.connect()
	# 	if res == True:
	# 		zk.enableDevice()
	# 		zk.disableDevice()
	# 		BioUsers = zk.getUser()
	# 		if BioUsers==({}, []):
	# 			record=self.env['hr.employee'].search([])
	# 			for r_list in record:
	# 				for user in BioUsers[0]:
	# 					if (BioUsers[0][user][0] == str(r_list.emp_machine_id)):
	# 						pass
	# 				zk.setUser(uid=False, userid=str(r_list.emp_machine_id), name=str(r_list.name), password='', role=zkconst.LEVEL_USER)

	# 				zk.enableDevice()				
	# 		else:
	# 			for user in BioUsers[0]:
	# 				if (BioUsers[0][user][0] == str(self.emp_machine_id)):
	# 					raise Warning('User Already Present in Machine.')
	# 			zk.setUser(uid=False, userid=str(self.emp_machine_id), name=str(self.name), password='', role=zkconst.LEVEL_USER)

	# 			zk.enableDevice()
				
	# 		zk.disconnect()
	# 		zk.refreshData()
			


	
	@api.multi
	def _updateAttendanceAll(self):
		# all_del_raw_attendence=self.env['ecube.raw.attendance'].search(['attendance_date','=',])
		# for x in all_del_raw_attendence:
		# 	x.unlink()
		machine_list=self.env['machine.info'].search([])
		if not machine_list:
			machine_list=self.env['machine.info'].create({
				'db' : 'data base',
				})
		data_base=machine_list.db
		print data_base
		login=machine_list.odooLogin
		print login
		odoopwd=machine_list.odooPasswd
		print odoopwd
		ip_list=[]
		for x in machine_list.product_ids:
			if not x.status=="no":
				ip=x.ip
				print ip
				zk = zklib.ZKLib(ip, int(config.key['port']))
				result=zk.connect()
				if result == False:
					print ip
					print "falseeeeeeeeeeeeeeeeeeeee"
					self._attendance_error(ip)
					continue
				print "startttttttttttttttttt"
				self._updateAttendance(ip,data_base,login,odoopwd)

	def _updateAttendance(self,ip,data_base,login,odoopwd):
		print "nextttttttttttttttttttttttttt"
		zk = zklib.ZKLib(ip, int(config.key['port']))
		common =  xmlrpclib.ServerProxy('%s/xmlrpc/2/common' % config.key['odooserver'])
		common.version()
		uid = common.authenticate(data_base, login, odoopwd, {})
		api = xmlrpclib.ServerProxy('%s/xmlrpc/2/object' % config.key['odooserver'])
		res = zk.connect()
		zk.enableDevice()
		zk.disableDevice()
		info = []
		attendance = zk.getAttendance()
		actualServerTime = str(datetime.now())
		requiredServerTime = actualServerTime.split('.')
		requiredServerDate = requiredServerTime[0].split(' ')
		if (attendance):
			for lattendance in attendance:
				time_att = str(lattendance[2].date()) + ' ' +str(lattendance[2].time())
				atten_time1 = datetime.strptime(str(time_att), '%Y-%m-%d %H:%M:%S')
				atten_time = atten_time1
				atten_time = datetime.strftime(atten_time,'%Y-%m-%d %H:%M:%S')
				attenDate = str(atten_time).split(' ')
				if (requiredServerDate[0] == attenDate[0]):
					data = {
					'user_id' :lattendance[0],
					'Date' : str(lattendance[2].date()),
					'Time' : str(lattendance[2].time()),
					'M_date' : attenDate[0],
					'M_time' : attenDate[1],
					'DateTime' : atten_time
						}

					info.append(data)
			# allOdooAttendance=self.env.cr.execute("SELECT attendance_date,name,employee_id FROM  ecube_raw_attendance")
			# allOdooAttendance = api.execute_kw(config.key['db'], uid, config.key['odooPasswd'],
			#  'ecube.raw.attendance','search_read',[],
			#  {'fields': ['employee_id', 'attendance_date', 'name']})
			# user_machine=zk.getUser()[1]
			print "77777777777777777777"
			for rec in info:
				print rec['M_time']
				print "qqqqqqqqqqqqqqqqqqqqqqqqqqq"
				user_id_name =rec['user_id']
				# machine_date=(rec['DateTime']+ timedelta(hours=5)).strftime("%H:%M:%S")
				# print rec['DateTime']
				machine_date= rec['DateTime']
				# machine_date=machine_date + str(timedelta(hours=5))
				print "DATE timeeeeeeeeeeeeee"
				# print machine_date
				record_date=time.strftime("%d/%m/%Y")
				record_time=(datetime.now() + timedelta(hours=5)).strftime("%H:%M:%S")
				employee_id_raw =self.env['hr.employee'].search([('card_no','=',user_id_name)])
				raw_attendence=self.env['ecube.raw.attendance'].search([('employee_id','=',employee_id_raw.id),('attendance_date','=',machine_date),('machine_id','=',user_id_name),('name','=',ip),('department','=',employee_id_raw.department_id.id)])
				print "create raw attendenceeeeeeee"

				if not raw_attendence:
				# if (rec['DateTime'] not in [odooAtten['attendance_date'] for odooAtten in allOdooAttendance]):
					self.env['ecube.raw.attendance'].create({
									'employee_id': employee_id_raw.id,
									'department': employee_id_raw.department_id.id,
									'attendance_date': machine_date,
									'name': ip,
									'machine_id': str(user_id_name),
									'date': rec['M_date'],
									'time': rec['M_time'],
									# 'time': (datetime.now() + timedelta(hours=5)).strftime("%H:%M:%S"),
									# 'machine_name': 'yasir',
							})
				# continue
				

					# user_id_name=""
					# api.execute_kw(config.key['db'], uid, config.key['odooPasswd'], 'ecube.raw.attendance',
					# 'create', [{
					# 			'employee_id': employee_id.id,
					# 			'attendance_date': rec['DateTime'],
					# 			'name': ip,
					# 			'machine_id': user_id_name,
					# 			# 'machine_name': self._get_machine_name(user_id_name,user_machine),
					# 			}])

# 
	# def _get_machine_name(self,user_id_name, user_machine):
	# 	username = None
	# 	for user in user_machine:
	# 		raw_user=user.split(":")
	# 		if raw_user[0]==user_id_name:
	# 			username=raw_user[1]
	# 	return username

	def _attendance_error(self,ip):
		print ip
		print "ppppppppppppppppppppppp"
		print "ppprrrrrrrrrrrrrrrrrrrrrrpppppppp"
		record=self.env['ecube.attendence.error'].search([('date','=',time.strftime("%d/%m/%Y"))])
		print record
		if not record:
			record=self.env['ecube.attendence.error'].create({
				'date': time.strftime("%d/%m/%Y"),
				})
		for x in record:
			x.product_ids.create({
				'machine_ip_error': ip,
				'time': (datetime.now() + timedelta(hours=5)).strftime("%H:%M:%S"),
				'partner_id': x.id,
				})

# Steps that required for this F*****G machine
# Install https://github.com/dnaextrim/python_zklib this library
# Install Selenium
# Download Gekodriver
# Export path of Geckodriver
# Install sudo apt-get install xvfb
#install sudo pip install pyvirtualdisplay

# sudo apt-get install python-pip
# sudo pip install git+https://github.com/ehtishamfaisal/zklib.git
# sudo pip install pyvirtualdisplay
# sudo pip install selenium
# sudo apt-get install xvfb