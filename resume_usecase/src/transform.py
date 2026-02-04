import pandas as pd
import re
import pandas as pd
from io import BytesIO
from pypdf import PdfReader 

def pdf_bytes_to_text(body):
        try:
            
            reader = PdfReader(BytesIO(body))
            parts = []
            for page in reader.pages:
                parts.append(page.extract_text() or '')
            return '\n'.join(parts).strip()
        except Exception:
            pass

        raise RuntimeError(
            'PDF text extraction failed. Install one:\n'
            '  pip install pypdf\n'
            '  pip install pdfplumber'
        )
def clean_string(s):
    if not s:
        return ''
    s = s.replace('\xa0', ' ').replace('\r', '\n')
    s = re.sub(r'(?<=\w)\n(?=\w)', '', s)
    s = re.sub(r'[ \t]+', ' ', s)
    s = re.sub(r'\n{3,}', '\n\n', s)
    return s.strip()

def split_sections(text):
    section_names = [
    'summary', 'profile',
    'education',
    'experience',
    'skills',
    'projects',
    'certifications',
    ]
    sections = {}
    current_section = 'header'
    sections[current_section] = []

    lines = text.split('\n')
    for line in lines:
        clean = line.strip().lower()
        if clean in section_names:
            current_section = clean 
            sections[current_section] = []
        else:
            sections[current_section].append(line)
    for sec in sections:
        sections[sec] = '\n'.join(sections[sec]).strip()
    return sections
def transform_data(pdf_files):

    resumes = []  

    for p in pdf_files:
        body = p.get('body')
        raw_text = clean_string(pdf_bytes_to_text(body))
        sections_dict = split_sections(raw_text)

        resumes.append({
            'header': sections_dict.get('header', '').split('\n')[0],
            'summary': sections_dict.get('summary', ''),
            'education': sections_dict.get('education', ''),
            'skills': sections_dict.get('skills', ''),
            'experience': sections_dict.get('experience', ''),
            'projects': sections_dict.get('projects', ''),
            'certifications': sections_dict.get('certifications', '')
        })

    df = pd.DataFrame(resumes)
    print('transformation done')

    return df
