import urllib
import urllib2
import time

success = 0
pending = 0
denied = 0
url = 'https://egov.uscis.gov/casestatus/mycasestatus.do'
for tmp in range (120000, 128999, 5):
	#caseNumber = "YSC1890090188"
	caseNumber = "YSC1890" + `tmp`
	#print caseNumber
	values = {'appReceiptNum' : caseNumber}

	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	the_page = response.read()
	a= the_page.find("<p>On")
	b = the_page.find("Number YSC189");

	mysubString=the_page[a+3:b+20]
	if mysubString.find("I-765") > 0:
		#print mysubString
		status= mysubString.find("we");
		#print status, status+3, status+10, mysubString[22:22+7]
	#	print caseNumber, 
		if mysubString[status+3:status+10] == "ordered":
			print caseNumber,  "New Card Is Being Produced" 
			success += 1
			continue
		if mysubString[status+3:status+11] == "received":
			print  caseNumber, "Case Was Received"
			pending += 1
			continue
		if mysubString[status+3:status+9] == "mailed":
			print  caseNumber, "Card Was Mailed"
			success += 1 
			continue			
		if mysubString[status+3:status+9] == "denied":
			print  caseNumber, "Denied Notice Mailed"
			denied += 1 
			continue
		del the_page, a, b
	#	time.sleep(0.05)
		#print the_page
print "Approved" , success, "Pending" , pending, "Denied", denied, "Total I-756", pending+success+denied
print "Handled", round((float(success+denied)/(float(success+pending+denied)))*100,2) , "%"
