import spacy
import pandas as pd
import pdfminer
import re
import os
import pdf2text

# Create directories
if os.path.exists(os.path.join(os.getcwd(), 'output')):
    print('Output folder exists!')
    pass
else:
    print('Creating output folder...')
    os.mkdir(os.path.join(os.getcwd(), 'output'))
    output_path = os.path.join(os.getcwd(), 'output')

    if os.path.exists(os.path.join(output_path, 'csv')):
        print('csv output folder exists!')
        pass
    else:
        print('Creating csv folder...')
        os.mkdir(os.path.join(output_path, 'csv'))
    if os.path.exists(os.path.join(output_path, 'txt')):
        print('txt folder exists!')
        pass
    else:
        print('Creating txt folder...')
        os.mkdir(os.path.join(output_path, 'txt'))

# Load the english language model
nlp = spacy.load("en_core_web_sm")
result_dict = {'names': [], "phones": [], "emails": [], "skills": []}
names = []
phones = []
emails = []
skills = []


class ResumeParser:
    """

    """

    def __init__(self):
        pass

    def convert_pdf(self, f):
        """
        Convert the pdf to a txt file
        :param f: the input file as a pdf format
        :return: read output .txt file
        """
        output_filename = os.path.basename(os.path.splitext(f)[0]) + '.txt'
        output_filepath = os.path.join('output/txt/', output_filename)
        pdf2text.main(args=[f, "--outfile", output_filepath])
        print(output_filepath + " saved successfully!!!")
        return open(output_filepath, encoding='utf8').read()

    def parse_content(self, text):
        """
        Parse the .txt file and extract meaningful information
        :param text: output of the convert_pdf method
        :return: None
        """
        skillset = re.compile("python|java|sql|hadoop|tableau")
        phone_num = re.compile(
            '(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
        doc = nlp(text)
        name = [entity.text for entity in doc.ents if entity.label_ is "PERSON"][0]
        print(name)
        email = [word for word in doc if word.like_email == True][0]
        print(email)
        phone = str(re.findall(phone_num, text.lower()))
        skills_list = re.findall(skillset, text.lower())
        unique_skills_list = str(set(skills_list))

        names.append(name)
        emails.append(email)
        phones.append(phone)
        skills.append(unique_skills_list)
        print('Extraction completed successfully!!!')


if __name__ == '__main__':
    for file in os.listdir('resumes/'):
        if file.endswith('.pdf'):
            print('Reading........' + file)
            resume_parser = ResumeParser()
            txt = resume_parser.convert_pdf(os.path.join('resumes/', file))
            resume_parser.parse_content(txt)

    result_dict['names'] = names
    result_dict['emails'] = emails
    result_dict["phones"] = phones
    result_dict["skills"] = skills

    result = pd.DataFrame(result_dict).to_csv('output/csv/result_csv.csv')
