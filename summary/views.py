
import unicodedata
from django.shortcuts import render
from requests import request
from .utils import  robin

import re




# Create your views here.
# Create your views here.



def tool(request):
    
    
    if request.method == 'POST':
        show_statistics = False
        text = request.POST.get("description").lower()
        keywords = request.POST.get("keywords")

        summary_length = request.POST.get("summary_length")  

        context = robin(keywords,text, summary_length)
        
    
        context['oldDescription'] = text

        '''statistic starts'''

        count = count_paragraphs_helper(text)
        lines = count_lines_helper(text)
        updated_lines = count_lines(text)
        char_count = character_count(text)
        char_count_one = count_char_one(text)
        word_count = count_words(text)
        pages = count_pages(text)
        
        show_statistics = True


        context.update({
            'count': count,
            'lines': lines,
            'pages': pages,
            'text': text,
            'updated_lines': updated_lines,
            'char_count': char_count,
            'char_count_one': char_count_one,
            'word_count': word_count,
            'show_statistics' : show_statistics,
            
        })


        '''statistic ends''' 

        top_keywords = summarize_text(text)

        context.update({
             
             
             'top_keywords': top_keywords,
        })
        return render(request,'textsum.html',context)
       
    return render(request, 'textsum.html')



def count_paragraphs_helper(text):
    paragraphs = re.split(r'\n\s*\n', text.strip())
    return len(paragraphs)

def count_lines_helper(text):
    sentences = re.split(r'\.\s+', text)
    
    line_count = len(sentences)
    return line_count

def count_pages(text):
    
    lines_per_page = 50
    lines = count_lines_helper(text)
    pages = lines // lines_per_page
    if lines % lines_per_page != 0:
        pages += 1
    return pages

def character_count(text):
    c = 0
    for i in range(len(text)):
        if text[i] != " ":
            c += 1
    return c

def count_char_one(text):
    return len(text)

def count_words(text):
    words = text.split()
    return len(words)

def count_lines(text):
    lines = re.split(r'\.\s+', text)
    formatted_lines = '<br>'.join(lines)
    return formatted_lines



import string
from django.shortcuts import render
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def summarize_text(text):
    
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    punctuation = set(string.punctuation)
    filtered_words = [word.lower() for word in words if word.lower() not in stop_words and word not in punctuation]

    keyword_counts = Counter(filtered_words)
    
    # Get the top 10 keywords
    top_keywords = keyword_counts.most_common(10)
    
    # Filter keywords with count >= 5
    filtered_top_keywords = [(keyword, count) for keyword, count in top_keywords if count >= 5]
    
    return filtered_top_keywords

# Example text











'''

from rake_nltk import Rake


def get_top_keywords_with_rake(text, num_keywords=10):
    r = Rake()  # Initialize the RAKE extractor
    r.extract_keywords_from_text(text)  # Extract keywords from the text
    keyword_scores = r.get_word_degrees()  # Get keyword scores (single words)
    
    # Convert decimal scores to integers
    for word, score in keyword_scores.items():
        keyword_scores[word] = int(round(score))  # Convert and round the score to an integer
    
    # Filter out numeric keywords
    non_numeric_keywords = {word: score for word, score in keyword_scores.items() if not word.isnumeric()}
    
    # Sort the non-numeric keywords by score in descending order
    sorted_keywords = sorted(non_numeric_keywords.items(), key=lambda x: x[1], reverse=True)
    
    # Select the top N keywords
    top_keywords = sorted_keywords[:num_keywords]
    
    return top_keywords

'''






'''

import io
import PyPDF2

from PyPDF2 import PdfReader
# Create your views here.


def count_paragraphs_helper(text):
    paragraphs = re.split(r'\n\s*\n', text.strip())
    return len(paragraphs)

 

def upload_pdf(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        uploaded_file = request.FILES['pdf_file']

        
        file_contents = uploaded_file.read()

        
        if uploaded_file.name.lower().endswith('.pdf'):
            
            pdf_stream = io.BytesIO(file_contents)
            pdf_reader = PyPDF2.PdfReader(pdf_stream)
            text = ""
            
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text()

         
            num_paragraphs = count_paragraphs_helper(text)
            lines = count_lines_helper(text)
            char_count = character_count(text)
            total_pages = len(pdf_reader.pages)
            char_count_spaces = len(text)
            word_count = count_words(text)

            return render(request, 'index2.html', {
                'file_contents': text, 
                'total_pages': total_pages, 
                'num_paragraphs': num_paragraphs,
                'lines': lines,
                'char_count': char_count,
                'char_count_spaces': char_count_spaces,
                'word_count': word_count,
                
                
                
                
                })
    
    return render(request, 'index2.html')

'''


import io
import PyPDF2


from PyPDF2 import PdfReader

from django.shortcuts import render
from .utils import robin
from datetime import datetime


def format_pdf_date(pdf_date_string):
    year = int(pdf_date_string[2:6])
    month = int(pdf_date_string[6:8])
    day = int(pdf_date_string[8:10])
    hour = int(pdf_date_string[10:12])
    minute = int(pdf_date_string[12:14])
    second = int(pdf_date_string[14:16])
    return f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"

def remove_non_ascii(text):
    normalized_text = unicodedata.normalize('NFKD', text)
    clean_text = ''.join(char for char in normalized_text if ord(char) < 128 and char in string.printable and char not in ('.', ''))
    return clean_text


def remove_urls(text):
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    cleaned_text = re.sub(url_pattern, '', text)
    return cleaned_text





def pdf_date_to_readable(pdf_date):
    try:
        # Extract the year, month, day, hour, minute, and second components
        year = int(pdf_date[2:6])
        month = int(pdf_date[6:8])
        day = int(pdf_date[8:10])
        hour = int(pdf_date[10:12])
        minute = int(pdf_date[12:14])
        second = int(pdf_date[14:16])
        
        # Create a datetime object
        dt = datetime(year, month, day, hour, minute, second)
        
        # Return the human-readable format
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return "Unknown"


def upload_pdf(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        uploaded_file = request.FILES['pdf_file']
        file_contents = uploaded_file.read()

        if uploaded_file.name.lower().endswith('.pdf'):
            pdf_stream = io.BytesIO(file_contents)
            pdf_reader = PyPDF2.PdfReader(pdf_stream)
            text = ""

            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text()

            cleaned_text = remove_non_ascii(text)
            cleaned_text_without_urls = remove_urls(cleaned_text)
            normalized_text = re.sub(r'\s+', ' ', cleaned_text_without_urls)

            keywords = request.POST.get("keywords")
            summary_length = request.POST.get("summary_length")
            summary = robin(keywords, normalized_text, summary_length)
            
            creation_date = pdf_reader.metadata.get('/CreationDate', '') 
            readable_creation_date = pdf_date_to_readable(creation_date)

            mod_date = pdf_reader.metadata.get('/ModDate', '')
            readable_mod_date = pdf_date_to_readable(mod_date)
            
            metadata = pdf_reader.metadata
            title = metadata.get('/Title', 'UnKnown')
            
            author = metadata.get('/Author', 'Unknown')
            
            creator = metadata.get('/Creator', 'Unknown')
           # creation_date = metadata.get('/CreationDate', '')
            producer = metadata.get('/Producer', 'Unknown')
           # mod_date = metadata.get('/ModDate', '')
            
          

            num_paragraphs = count_paragraphs_helper(text)
            lines = count_lines_helper(text)
            char_count = character_count(text)
            char_count_spaces = len(text)
            word_count = count_words(text)

            top_keywords = summarize_text(cleaned_text_without_urls)

            context = {
                'file_contents': text,
                'total_pages': len(pdf_reader.pages),
                'num_paragraphs': num_paragraphs,
                'lines': lines,
                'char_count': char_count,
                'char_count_spaces': char_count_spaces,
                'word_count': word_count,
                'context': summary,
                'top_keywords': top_keywords,
                #'metadata': metadata,
                'title': title,
                'author': author,
                'creator': creator,
                'creation_date': readable_creation_date,
                'producer': producer,
                'mod_date': readable_mod_date,
               
                'uploaded_pdf': True
            }

            return render(request, 'pdf2.html', context)

    return render(request, 'pdf2.html')


"""
def upload_pdf(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        uploaded_file = request.FILES['pdf_file']

        file_contents = uploaded_file.read()

        if uploaded_file.name.lower().endswith('.pdf'):
            pdf_stream = io.BytesIO(file_contents)
            pdf_reader = PyPDF2.PdfReader(pdf_stream)
            text = ""

            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text()

            # Assuming you have the 'robin' function for text summarization
            keywords = request.POST.get("keywords")
            summary_length = request.POST.get("summary_length") # Convert to int
            summary = robin(keywords, text, summary_length)

            # Retrieve metadata from the PDF
            metadata = pdf_reader.metadata

            # Assuming you have the functions for text statistics
            num_paragraphs = count_paragraphs_helper(text)
            lines = count_lines_helper(text)
            char_count = character_count(text)
            char_count_spaces = len(text)
            word_count = count_words(text)

            # Applying the summarization logic to the uploaded PDF text
            top_keywords = summarize_text(text)

            # Set the uploaded_pdf variable in the context
            context = {
                'file_contents': text,
                'total_pages': len(pdf_reader.pages),
                'num_paragraphs': num_paragraphs,
                'lines': lines,
                'char_count': char_count,
                'char_count_spaces': char_count_spaces,
                'word_count': word_count,
                'context': summary,
                'top_keywords': top_keywords,
                'metadata': metadata,
                'uploaded_pdf': True  
            }

            return render(request, 'index2.html', context)

    return render(request, 'index2.html')

"""

'''
import io
import re
import pdfplumber

def upload_pdf(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        uploaded_file = request.FILES['pdf_file']
        file_contents = uploaded_file.read()

        if uploaded_file.name.lower().endswith('.pdf'):
            pdf_stream = io.BytesIO(file_contents)
            
            # Use pdfplumber for text extraction
            with pdfplumber.open(pdf_stream) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()

            cleaned_text = remove_non_ascii(text)
            cleaned_text_without_urls = remove_urls(cleaned_text)
            normalized_text = re.sub(r'\s+', ' ', cleaned_text_without_urls)

            keywords = request.POST.get("keywords")
            summary_length = request.POST.get("summary_length")
            summary = robin(keywords, normalized_text, summary_length)
            
            creation_date = pdf.metadata.get('/CreationDate', '') 
            readable_creation_date = pdf_date_to_readable(creation_date)

            mod_date = pdf.metadata.get('/ModDate', '')
            readable_mod_date = pdf_date_to_readable(mod_date)
            
            metadata = pdf.metadata
            title = metadata.get('/Title', 'UnKnown')
            
            author = metadata.get('/Author', 'Unknown')
            
            creator = metadata.get('/Creator', 'Unknown')
            producer = metadata.get('/Producer', 'Unknown')
            
            num_paragraphs = count_paragraphs_helper(text)
            lines = count_lines_helper(text)
            char_count = character_count(text)
            char_count_spaces = len(text)
            word_count = count_words(text)

            top_keywords = summarize_text(cleaned_text_without_urls)

            context = {
                'file_contents': text,
                'total_pages': len(pdf.pages),
                'num_paragraphs': num_paragraphs,
                'lines': lines,
                'char_count': char_count,
                'char_count_spaces': char_count_spaces,
                'word_count': word_count,
                'context': summary,
                'top_keywords': top_keywords,
                'title': title,
                'author': author,
                'creator': creator,
                'creation_date': readable_creation_date,
                'producer': producer,
                'mod_date': readable_mod_date,
                'uploaded_pdf': True
            }

            return render(request, 'pdf2.html', context)

    return render(request, 'pdf2.html')

'''
'''
import io
import re
import fitz
from django.shortcuts import render  # Import the appropriate Django rendering function

def upload_pdf(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        uploaded_file = request.FILES['pdf_file']
        file_contents = uploaded_file.read()

        if uploaded_file.name.lower().endswith('.pdf'):
            pdf_stream = io.BytesIO(file_contents)
            
            # Use PyMuPDF for text extraction
            pdf_document = fitz.open(stream=pdf_stream)
            text = ""
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text += page.get_text().lower()

            cleaned_text = remove_non_ascii(text)
            cleaned_text_without_urls = remove_urls(cleaned_text)
            normalized_text = re.sub(r'\s+', ' ', cleaned_text_without_urls)

            keywords = request.POST.get("keywords")
            summary_length = request.POST.get("summary_length")
            summary = robin(keywords, normalized_text, summary_length)
            
            creation_date = pdf_document.metadata['creationDate']
            readable_creation_date = pdf_date_to_readable(creation_date)

            mod_date = pdf_document.metadata['modDate']
            readable_mod_date = pdf_date_to_readable(mod_date)
            
            metadata = pdf_document.metadata
            title = metadata['title']
            
            author = metadata['author']
            
            creator = metadata['creator']
            producer = metadata['producer']
            
            num_paragraphs = count_paragraphs_helper(text)
            lines = count_lines_helper(text)
            char_count = character_count(text)
            char_count_spaces = len(text)
            word_count = count_words(text)

            top_keywords = summarize_text(cleaned_text_without_urls)

            context = {
                'file_contents': text,
                'total_pages': pdf_document.page_count,
                'num_paragraphs': num_paragraphs,
                'lines': lines,
                'char_count': char_count,
                'char_count_spaces': char_count_spaces,
                'word_count': word_count,
                'context': summary,
                'top_keywords': top_keywords,
                'title': title,
                'author': author,
                'creator': creator,
                'creation_date': readable_creation_date,
                'producer': producer,
                'mod_date': readable_mod_date,
                'uploaded_pdf': True
            }

            pdf_document.close()  # Close the PDF document

            return render(request, 'pdf2.html', context)

    return render(request, 'pdf2.html')
'''
def homepage(request):
    return render(request, 'homepage.html')

