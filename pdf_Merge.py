import PyPDF2
from PyPDF2 import PdfFileMerger
import os
from datetime import datetime,date
import time

from urllib2 import Request, urlopen
from pyPdf import PdfFileWriter, PdfFileReader
from StringIO import StringIO
from multiprocessing import Pool

import gevent.monkey
gevent.monkey.patch_all()

class PdfOperation(object):
	"""docstring for PdfOperation"""
	def __init__(self):
		super(PdfOperation, self).__init__()
		self.pdfData =[]
		self.pdf_files = []

	def read_file(self, file_name):
		f = open(file_name,'r')
		self.file_data = f.read()
		return self.file_data

	def get_pdf(self):
		urls = self.file_data.split(',')
		for url in urls:
			writer = PdfFileWriter()
		self.pdf_files.append(urlopen(Request(url)).read())

	def get_pdf_file(self, url):		
		data = urlopen(Request(url)).read()
		return data

	def conver_to_file(self, pdf_file):
		file_object = StringIO(pdf_file)
		pdfFile = PdfFileReader(file_object)
		self.pdfData.append(pdfFile)
		

	def merge_pdf(self):
		
		writer = PdfFileWriter()
		outputStream = open("merged_pdf.pdf","wb")
		for pdf in self.pdfData:
			for pageNum in xrange(pdf.getNumPages()):
			        currentPage = pdf.getPage(pageNum)
			        writer.addPage(currentPage)
			writer.write(outputStream)

			
		outputStream.close()
		

if __name__ == '__main__':
	p = PdfOperation()
	now = datetime.now()
	fetch_time = time.time()
	print "starting PDF Fetching at "+str(now.strftime('%c'))
	urls = p.read_file("urls.text")
	p.get_pdf()
	urls = urls.split(',')
	jobs = [gevent.spawn(p.get_pdf_file, _url) for _url in urls]
	threads = gevent.joinall(jobs)
	[p.conver_to_file(thread.value) for thread in threads]
	now2 = datetime.now()
	print "PDF Fetch completed at "+(str(now2.strftime('%c')))
	print "total time taken to Fetch {}".format(time.time() - fetch_time)
	print "PDF Merge started at "+(str(now2.strftime('%c')))
	merge_time = time.time()
	p.merge_pdf()
	t3 = datetime.now() 
	print "completed PDF Merging at "+str(t3.strftime('%c'))
	print "time taken to merge {}".format(time.time() - merge_time)
	total_fetch_time = (time.time() - fetch_time)
	total_merge_time = (time.time() - merge_time)
	print "total time taken to execute {}".format(total_fetch_time + total_merge_time)
	print "Open File merged_pdf.pdf"
	