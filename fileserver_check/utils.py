
import unicodedata
import re

def read_file_line_by_line(file):
    lines = []
    for line in file:
        lines.append(line.decode('utf-8').strip())  # Satır sonundaki newline karakterini kaldır ve UTF-8 olarak decode et
    return lines

def process_email(email):
    # "@" karakterinden önceki kısmı al
    username = email.split('@')[0]
    # "." karakterini temizle ve ikişerli olarak bir array oluştur
    username_parts = re.split(r'[._]', username)
    # bütün değişkenleri lowercase yap
    username_parts_lower = [part.lower() for part in username_parts]
    return username_parts_lower

def process_file_server_name(file_server_name):
    # "Genel\CR\" kısmından sonra gelen kısmı al
    file_name = file_server_name.split('\\')[-1]
    # "_" veya " " karakterlerini seçerek bu kısmı iki parçaya ayır
    parts = re.split(r'[_\s]', file_name)
    
    # lowercase yap, türkçe harfleri ingilizceye çevir
    normalized_parts = [unicodedata.normalize('NFKD', part.replace('ı', 'i').replace('ğ', 'g').replace('ü', 'u').replace('ş', 's').replace('ö', 'o').replace('ç', 'c').replace('İ', 'i').replace('Ğ', 'g').replace('Ü', 'u').replace('Ş', 's').replace('Ö', 'o').replace('Ç', 'c')).encode('ascii', 'ignore').decode('utf-8').lower() for part in parts]
    
    print(normalized_parts)
    
    return normalized_parts
