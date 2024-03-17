import os
import csv
import pandas as pd
import shutil
import zipfile

def archive_logs(text_files, archive_directory, package_name = "vpn_logs"):
    print("Arşiv işlemi başlatılıyor...")
    # Arşiv klasörünü oluştur
    os.makedirs(archive_directory, exist_ok=True)
    print(f"Arşiv klasörü oluşturuldu: {archive_directory}")

    # Text dosyalarını al ve işle
    for text_file in text_files:
        print(f"{text_file.name} dosyası işleniyor...")
        # Dosyanın adını al
        file_name = os.path.splitext(text_file.name)[0]
        
        # Dosyayı Excel'e dönüştür
        csv_file_path = text_file.file.path
        excel_file_path = os.path.join(archive_directory, f'{file_name}.xlsx')
        convert_to_excel(csv_file_path, excel_file_path)
        
        # Dosyayı arşiv klasörüne kopyala
        shutil.copy(csv_file_path, archive_directory)
        print(f"{text_file.name} dosyası arşiv klasörüne kopyalandı.")
        
    
    # Aynı kişileri ayıkla
    all_emails = set()
    for text_file in text_files:
        csv_file_path = text_file.file.path
        emails = extract_unique_emails(csv_file_path)
        all_emails.update(emails)
    
    # Tekrar unique e-postaları al
    unique_emails = list(all_emails)
    print(f"Unique e-postalar: {unique_emails}")
    
    # Unique e-postaları bir Excel dosyasına kaydet
    unique_emails_file_path = os.path.join(archive_directory, 'unique_emails.xlsx')
    save_to_excel(unique_emails, unique_emails_file_path)
    print(f"Unique e-postalar dosyası oluşturuldu: {unique_emails_file_path}")
    
    # Arşiv klasörünü ve unique e-postaları aynı dosyaya al
    zip_file_path = os.path.join(archive_directory, f'{package_name}.zip')
    print("zip_file_path: ", zip_file_path)
    
    print("archive_directory: ", archive_directory)
    
    project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("project_directory: ", project_directory)


    
    archive_directory = archive_directory.replace("./", "")
    
    # Arşiv klasörünü zip dosyasına al
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for root, dirs, files in os.walk(os.path.join(project_directory, archive_directory), topdown=True):
            print("debug walk: ", os.path.join(project_directory, archive_directory))
            for file in files:
                # Dosya yolu oluştur
                file_path = os.path.join(root, file)
                
                print("file_path debug: ", file_path)
                
                # .DS_Store dosyasını atla
                if '.DS_Store' in file_path:
                    continue
                
                # Proje dizinini içeriyorsa işlemi yap
                if project_directory in file_path:
                    if package_name in  file_path:
                        continue
                    
                    print(file_path, "file_path debug 22")
                    
                    zipf.write(file_path, arcname=file)

        # Tüm dosyaları sil
    for root, dirs, files in os.walk(os.path.join(project_directory, archive_directory), topdown=True):
        print("removal walk: ", os.path.join(project_directory, archive_directory))
        for file in files:
            
            file_path = os.path.join(root, file)
            
            if project_directory in file_path:
                if package_name in  file_path:
                    continue
                
                print(file_path, "file_path debug 777")
                
                os.remove(file_path)
                

    print(f"Arşiv dosyası oluşturuldu: {zip_file_path}")
    
    return zip_file_path
def convert_to_excel(csv_file_path, excel_file_path):
    # Dosyayı oku
    with open(csv_file_path, 'r') as file:
        # İlk satırı sütun isimleri olarak al
        columns = file.readline().strip().split(',')
        
        # Geri kalan satırları oku ve DataFrame'e dönüştür
        df = pd.read_csv(file, names=columns)
        
        # Excel dosyasına kaydet
        df.to_excel(excel_file_path, index=False)

def extract_unique_emails(csv_file_path):
    emails = set()
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # İkinci sütundaki e-postaları al
            if len(row) > 1:
                emails.add(row[1])
    return emails

def save_to_excel(data, excel_file_path):
    # Veri dizisinde "SourceUserName" sütunu var mı kontrol et
    if 'SourceUserName' in data:
        # "SourceUserName" sütununu kaldır
        data.remove('SourceUserName')

    # Veri dizisini DataFrame'e dönüştür
    df = pd.DataFrame(data, columns=['SourceUserName'])

    # Excel'e dönüştürme işlemine devam et
    df.to_excel(excel_file_path, index=False)
