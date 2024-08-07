import re
from collections import defaultdict

def extract_tags(text):
    tag_pattern = re.compile(r'<(\w+)>(.*?)</\1>')
    
    result = defaultdict(str)
    
    matches = tag_pattern.findall(text)
    
    for tag, content in matches:
        result[tag] = content
    
    return dict(result)

input_text = '''<info>Informacje</info>
                <analiza>Oto jest analiza</analiza>
                a reszta jest nie ważna
                '''
output = extract_tags(input_text)
print(output)
