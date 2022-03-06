import re
from io import StringIO
from itertools import combinations

import PyPDF2
import docx
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

from rework.settings import MEDIA_URL, MEDIA_ROOT
from django.db.models.signals import post_save
from .models import FileBin, Cvbin, cvcombination, Cvgroups
from django.dispatch import receiver
import hashlib

email_reg= r"\b\w*[@]\w*.[a-z]{2,4}\b"
phone_reg= r"(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[6789]\d{9}"
applicant_name=r"\b[a-zA-Z]*[^\s@.]\b\s?\b[a-zA-Z]*[^\s@.]\b"
@receiver(post_save,sender=FileBin)
def read_file(sender,instance,created,**kwargs):

    if created:
        sha256_hash = hashlib.sha256()
        filename=MEDIA_ROOT + '/' + str(instance.path)
        with open(filename, "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
            print(sha256_hash.hexdigest())
            instance.file_hash=sha256_hash.hexdigest()
        pdf = open(filename, 'rb')
        extension=instance.filename.rsplit('.')[1]
        if extension=='pdf':
            pdfReader = PyPDF2.PdfFileReader(pdf)
            pageObj = pdfReader.getPage(0)

            # printing number of pages in pdf file
            instance.page = pdfReader.numPages
            data = re.sub('\n+', ' ', convert_pdf_to_txt(filename).lower())

        else:


            doc = docx.Document(filename)
            print(filename)
            print('%' * 50)
            fullText = []
            print('%'*50)
            for para in doc.paragraphs:
                fullText.append(para.text)
            data= '\n'.join(fullText).lower()
            instance.page = 0
            print(data)




        data = re.sub('\ +', ' ', data)
        instance.email = get_contact_info(email_reg,data)
        instance.phone=get_contact_info(phone_reg,data)
        instance.name=get_contact_info(applicant_name,data)


        instance.content=data

        instance.save()





@receiver(post_save,sender=Cvbin)
def process_bucket(sender,instance,created,**Kwargs):
    hitcounter = {}
    hit = 0
    all_options = []
    print (instance.bucketname)
    allcvs=FileBin.objects.filter(project=instance.project)

    serach_string = instance.bucketname
    serach_string = serach_string.split(",")

    count = len(serach_string)
    notmatch='notfound'
    create_combinations(notmatch,instance)

    for i in range(len(serach_string) + 1):

        for j in combinations(serach_string, i):
            str1 = ','.join(str(e) for e in j)
            print(str1)

            if (len(str1) > 0):
                hitcounter[str1] = 0
                all_options.append(str1)
                create_combinations(str1, instance)

    dbcombo=cvcombination.objects.filter( bin_id=instance)



    for cvobj in allcvs:
        s=cvobj.content
        flag = 0
        for items in all_options:
            item = items.split(",")

            count = 0;
            if (len(item) > 1):
                for x in item:

                    count += int(deep_search(x, s))
                    if len(item) == count:
                        # p = "result/" + items + '/' + pdffile
                        # copyfile(pdffile, p)
                        print("combo found")
                        group=Cvgroups()
                        group.combination=get_cv_combo_instance(dbcombo,items)
                        group.cv=cvobj
                        group.save()

                        hitcounter[items] = hitcounter.get(items, 0) + 1

            i = r'\b' + items + '\\b'
            matchNum = deep_search(items, s)

            if matchNum:
                hit = hit + 1
                # p = result_folder_name + "/" + items + '/' + pdffile
                # copyfile(pdffile, p)
                group = Cvgroups()
                group.combination = get_cv_combo_instance(dbcombo, items)
                group.cv = cvobj
                group.save()
                hitcounter[items] = hitcounter.get(items, 0) + 1

                flag = 1
            # print(pdffile, count, items, hitcounter.get(items, 0))

        if not flag:
            group = Cvgroups()
            group.combination = get_cv_combo_instance(dbcombo, notmatch)
            group.cv = cvobj
            group.save()
            hitcounter[items] = hitcounter.get(items, 0) + 1
        #copyfile(pdffile, default_folder + "/" + pdffile)
    print('#' * 30)
    for key, value in sorted(hitcounter.items()):
        print(str(key) + ":" + str(value))


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()
    return text

def  get_contact_info(regex,search_string):
    matches = re.finditer(regex, search_string, re.MULTILINE)

    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1
        if(match.group()):
            return (match.group())
            break
    return 0

def create_combinations(comboname,instance):
    combination = cvcombination()
    combination.bin_id = instance
    combination.combo =comboname;
    combination.save()

def deep_search(a, b):
    i = r'\b' + a+'\\b'
    matches = re.finditer(i, b, re.MULTILINE)
    matchNum = 0
    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1
    return 1 if matchNum!=0 else 0

def get_cv_combo_instance(all_combo_instance,search_string):


    for items in all_combo_instance:
        if items.combo==search_string:
            print('$' * 20)
            print(search_string)
            return items
