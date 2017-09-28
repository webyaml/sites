# path: lib/processors
# filename: wifi.py
# description: WSGI application wifi processors
''' 
	Copyright 2017 Mark Madere

	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at

	http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.
'''

''' external imports
'''
#import os
#import time
import subprocess

''' internal imports
'''
import classes.processor

''' classes
'''
class Scan(classes.processor.Processor):

	def run(self):
		
		conf = self.conf
		
		self.data = None
		
		if not conf.get('stdout'):
			
			print('stdout not in conf')
			return False

		# functions 
		def address(val):
			
			parameters = {}
			parameters['Address'] =val.split('Address:')[1].strip()
			
			return parameters

		def essid(val):
			
			parameters = {}
			parameters['ESSID'] = val.strip('"').strip()
			
			return parameters
		
		def mode(val):
			
			parameters = {}
			parameters['Mode'] = val.split('Channel:')[0].strip()
			parameters['Channel'] = val.split('Channel:')[1].strip()
			
			return parameters
		
		def signal(val):
			
			parameters = {}
			parameters['Signal'] = val.split('Quality:')[0].strip()
			parameters['Quality'] = val.split('Quality:')[1].strip()
			
			return parameters
		
		def encryption(val):
			
			parameters = {}
			parameters['Encryption'] = val.strip('"').strip()
			
			return parameters

		# scan for cells
		#cmd = "/usr/bin/iwinfo wlan0 scan" #vocore
		cmd = "/usr/bin/iwinfo apcli0 scan" #7688

		#sample output
		'''
		Cell 01 - Address: 1C:7E:E5:32:86:E8
			  ESSID: "1536 Poland"
			  Mode: Master  Channel: 1
			  Signal: -84 dBm  Quality: 26/70
			  Encryption: WPA2 PSK (CCMP)

		Cell 02 - Address: 1C:AF:F7:D2:F9:37
			  ESSID: "1536 Poland"
			  Mode: Master  Channel: 1
			  Signal: -86 dBm  Quality: 24/70
			  Encryption: WPA2 PSK (CCMP)
		'''


		try:	
			result = subprocess.check_output(cmd, shell=True)
			
			# debug
			print('stdout')
			print(result)
			
			parsers = {
				'ESSID': essid,
				'Mode': mode,
				'Signal': signal,
				'Encryption': encryption,
			}
			
			
			# parse output into a python object
			cells = []
			c = -1
			
			for line in result.split('\n'):
				
				#debug
				#print(line)
				
				line = line.strip()
				
				if not line:
					continue
				
				if line.startswith('Cell'):
					
					# new cell found
					c += 1
					cells.append(address(line))
					
				elif c > -1:
					# add parameters to cell
						
					parser,val = line.split(':',1)
					
					result = parsers[parser](val.strip())
					
					#debug
					#print(result)
					
					cells[c].update(result)
			
			# handle the stdout
			if conf.get('stdout'):
				
				conf['stdout']['value'] = cells
				conf['stdout']['format'] = 'raw'
				
				# load data
				if not self.load_data(conf['stdout']):
					
					print('failed to save')
						
					return False
			
			return True
			
		except subprocess.CalledProcessError as e:

			self.top.cache['stdout'] = e
			
			# debug
			print('stderr')
			print(e)
		
			# handle the stdout
			if conf.get('stderr'):
				
				conf['stderr']['value'] = e
				
				# load data
				if not self.load_data(conf['stderr']):
					
					print('failed to save - data failed to load')
						
					return False

			return False
			
		return False
