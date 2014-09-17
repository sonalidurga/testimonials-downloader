import urllib, urllib2, cookielib
from BeautifulSoup import BeautifulSoup

def download_testimonials(username,passwd):
	cookie_file = 'moodle.cookiesbypython'

	# set up a cookie jar to store cookies
	cj = cookielib.MozillaCookieJar(cookie_file)
	 
	# set up opener to handle cookies, redirects etc
	opener = urllib2.build_opener(
	     urllib2.HTTPRedirectHandler(),
	     urllib2.HTTPHandler(debuglevel=0),
	     urllib2.HTTPSHandler(debuglevel=0),            
	     urllib2.HTTPCookieProcessor(cj)
	)
	# pretend we're a web browser and not a python script
	opener.addheaders = [('User-agent',
	    ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_7) '
	     'AppleWebKit/535.1 (KHTML, like Gecko) '
	     'Chrome/13.0.782.13 Safari/535.1'))
	]

	url = 'http://bits-melange.com/index.php/main/login'
	response = opener.open(url)
	cj.save()

	for x in cj:
		if x.name == 'csrf_cookie_name':
			csrf_token_is = x.value 			#without csrf token we can't log in.



	values = {	'csrf_test_name' : csrf_token_is,
				'user_name' : username,
				'password' : passwd }
	data = urllib.urlencode(values)	#encoding the parameters for POST form.
	req = urllib2.Request(url,data)	#forming a request object. Proper structure.
	response = opener.open(url,data)
	html = response.read()

	if(response.geturl()=='http://bits-melange.com/index.php/user/dashboard'):		#a sign of successful login.
		
		print "Logged in succesfully. Downloading..."
		url_testimonials = 'http://bits-melange.com/index.php/user/your_testimonials'
		response_testimonials = opener.open(url_testimonials)
		html_testimonials = response_testimonials.read()
		#f1 = open('testimonials.html','w')		#making a clone of the testimonial page too! Bonus. 
		#f1.write(html_testimonials)
		#f1.close()

		parsed_html = BeautifulSoup(html_testimonials)

		private_testimonials = parsed_html.find('div',attrs={'id':'private'})
		public_testimonials = parsed_html.find('div',attrs={'id':'public'})
		written_testimonials = parsed_html.find('div',attrs={'id':'written_by_you'})

		file1 = open('public_testimonials.txt','w')
		file2 = open('private_testimonials.txt','w')
		file3 = open('testimonials_by_you.txt','w')

		for i in range(0,len(public_testimonials('p'))/2):
			file1.write(public_testimonials('p')[2*i+1].text.encode('utf-8'))		#encoding done because some characters weren't getting converted by default. 
			file1.write("\n-----------------------------------\n")
			file1.write(public_testimonials('p')[2*i].text.encode('utf-8'))
			file1.write("\n\n\n\n")
		file1.close()

		for i in range(0,len(private_testimonials('p'))/2):
			file2.write(private_testimonials('p')[2*i+1].text.encode('utf-8'))
			file2.write("\n-----------------------------------\n")
			file2.write(private_testimonials('p')[2*i].text.encode('utf-8'))
			file2.write("\n\n\n\n")
		file2.close()

		for i in range(0,len(written_testimonials('p'))/2):
			file3.write(written_testimonials('p')[2*i+1].text.encode('utf-8'))
			file3.write("\n-----------------------------------\n")
			file3.write(written_testimonials('p')[2*i].text.encode('utf-8'))
			file3.write("\n\n\n\n")
		file3.close()

		print "Done. Check the files in the folder. :)"
	else:
		print "Incorrect Login. Program exiting."


print "Hello! I download and format your Testimonials better. The csv generated by Melange website kinda sucks."
print "\n\nEnter your Bits-Melange Login Details : "
username = raw_input("Username : ")
password = raw_input("Password : ")
download_testimonials(username,password)
