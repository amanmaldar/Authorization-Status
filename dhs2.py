import urllib
import urllib2
import time





def execute(aa,bb):
	#print "in execute"
	printing = 0
	success = 0
	pending = 0
	denied = 0
	others = 0
	rejected = 0
	url = 'https://egov.uscis.gov/casestatus/mycasestatus.do'

	for tmp in range (aa, bb, 4):	#YSC1890120108
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
		#print mysubString, mysubString.find("I-765")
		status= mysubString.find("we");
		#if 1:
		if (mysubString.find("I-130") == -1 and (mysubString.find("I-765") > 0  or  mysubString[status+3:status+10] == "ordered")):
			#print mysubString
			#status= mysubString.find("we");
			#print status, status+3, status+10, mysubString[22:22+7]
		#	print caseNumber, 
			if mysubString[status+3:status+10] == "ordered":		# This is a special case. They do not have i-765 written here
				if printing == 1:
					print caseNumber,  "New Card Is Being Produced ->" , the_page[a+3:a+100]
				success += 1
				continue
			if mysubString[status+3:status+11] == "received":
				if printing == 1:
					print  caseNumber, "Case Was Received ->", the_page[a+3:a+100]
				pending += 1
				continue
			if mysubString[status+3:status+9] == "mailed":
				if printing == 1:
					print  caseNumber, "Card Was Mailed ->", the_page[a+3:a+100]
				success += 1 
				continue			
			if mysubString[status+3:status+9] == "denied":
				if printing == 1:
					print  caseNumber, "Denied Notice Mailed ->", the_page[a+3:a+100]
				denied += 1 
				continue
			if mysubString[status+3:status+11] == "rejected":
				if printing == 1:
					print  caseNumber, "Form is rejected ->", the_page[a+3:a+100]
				rejected += 1 
				continue
			if mysubString[status+3:status+11] == "approved":
				if printing == 1:
					print  caseNumber, "Case is approved ->", the_page[a+3:a+100]
				success += 1 
				continue
			else:
				if printing == 1:
					print  caseNumber, "others case ->", the_page[a+3:a+100]
				others += 1
				
			del the_page, a, b
		#	time.sleep(0.05)
			#print the_page
		
	return success, pending, denied, rejected, others	
	

		
def main():
	start_time = time.time()
	print "     Range       | Approved | Pending | Denied | Rejected | Others | Total I-765 | Handled" 
	for i in range (120,129,1):
		success, pending, denied, rejected, others= execute(i*1000,i*1000+1000)
		t1= pending+success+denied+rejected+others
		h1 = round((float(success+denied+rejected+others)/(float(pending+success+denied+rejected+others)))*100,2)
		print i*1000,"-",i*1000+999, "  |  " ,success ,"    " ,pending ,"  	" ,denied ,"  	" ,rejected ,"  	" ,others ,"        " ,t1 ,"       " ,h1 ,"%"

		#print "Approved" , success, "Pending" , pending, "Denied", denied, "Rejected" , rejected, "Others", others, "Total I-765", pending+success+denied+rejected+others, \
		#"Handled", round((float(success+denied+rejected+others)/(float(pending+success+denied+rejected+others)))*100,2) , "%"
		
		
		#print "Handled", round((float(success+denied+rejected+others)/(float(pending+success+denied+rejected+others)))*100,2) , "%"
	elapsed_time = time.time() - start_time
	time.strftime("%H:%M:%S", time.gmtime(elapsed_time))


if __name__== "__main__":
    main()
