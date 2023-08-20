import time
import tkinter.ttk
from tkinter import messagebox
from tkinter import *
import pyautogui as ss
from requests import get
import pytesseract as pay
import cv2
import os
from googletrans import Translator
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
#çeviri i.in sözlük:
languages = {"İngilizce":"en","Türkçe":"tr","Fransızca":"fr","İspanyolca":"es"}
tokinizer = {"İngilizce":"English","Türkçe":"Turkish","Fransızca":"French","İspanyolca":"Spanish"}
#pencere kısmı
pencere = Tk()
pencere_etiket = pencere.title("Brightened Brains' Product")
pencere_geometrisi = pencere.geometry("700x700+420+150")
pencere_ana_label = Label(pencere,text="Reader&Translator&Summirizer From Image&Text",font="times 14 italic bold")
pencere_ana_label.pack()
#internet kontrolü
check = get("https://www.google.com")
status = check.status_code
if status == 200:
    messagebox.showinfo("Başarılı","İnternet Bağlantısı Başarılı 5 saniye içerisinde Giriş Yapılıyor!!")
    time.sleep(5)
elif status == 404:
    messagebox.showwarning("Kontrol","Bağlantıyı kontrol ediniz")
else:
    messagebox.showerror("hata","Bağlantı problemi\nİnternete Bağlı mısnız?")


#input büyük kısım
text_area = Text(pencere,width=65,font="times 12 italic")
text_area.insert(tkinter.END,"PROGRAMI KULLANMAK İÇİN:\nDİL SEÇENEKLERİNİ SEÇİN (SADECE YAZI OKUMAK İÇİN HER İKİ "
                             "DİL SEÇENEĞİ DE AYNI OLMALI) VE ÇEVİR BUTONUNA BASTIKTAN SONRA GELEN EKRANDAN "
                             "ÇEVİRİLECEK VEYA ÖZETLENECEK KISMI SEÇİN, ŞU ANKİ BÖLÜME ÇEVRİLMİŞ&ÖZETLENMİŞ HALİ GELECEKTİR...")
text_area.pack()
text_area.place(x=25,y=250,height=400)

#spinbox
sp_label = Label(pencere,text="Kaç cümlede özetlenecek?",fg="blue",font="times 12")
sp_label.pack()
sp_label.place(x=25,y=150)
spin_box = Spinbox(pencere,from_=1,to=100,wrap=True)
spin_box.pack()
spin_box.place(x=260,y=150)

#dropdownd dil seçenekleri
#hangi dilden
combo_label = Label(pencere,text="Algılanacak dil :",font="times 12 bold",fg="red")
combo_label.pack()
combo_label.place(x=20,y=60)
Combo = tkinter.ttk.Combobox(pencere,width=20)
Combo['values'] = ('Türkçe','İngilizce','İspanyolca','Fransızca')
Combo.current(0)
Combo.pack()
Combo.place(x=20,y=100)
#hangi dile
combo_label2 = Label(pencere,text="Çevirilecek dil :",font="times 12 bold",fg="purple")
combo_label2.pack()
combo_label2.place(x=500,y=60)
Combo2 = tkinter.ttk.Combobox(pencere,width=20)
Combo2['values'] = ('Türkçe','İngilizce','İspanyolca','Fransızca')
Combo2.current(0)
Combo2.pack()
Combo2.place(x=500,y=100)
#özetleme dropmenu
combo_label3 = Label(pencere,text="Özetleme dili:",font="times 12 bold",fg="forest green")
combo_label3.pack()
combo_label3.place(x=280,y=60)
Combo3 = tkinter.ttk.Combobox(pencere,width=20)
Combo3['values'] = ('Türkçe','İngilizce','İspanyolca','Fransızca')
Combo3.current(0)
Combo3.pack()
Combo3.place(x=260,y=100)
#çevirme fonksiyonu
def get_rectangle_points():
    # fonksiyon için combobox değerlerini almak
    combo_1_al = Combo.get()
    combo_2_al = Combo2.get()
    #get pc_name
    pc_name = os.getlogin()
    translator = Translator()
    #get screenshot and save it
    screen = ss.screenshot(f"C:/Users/{pc_name}/Desktop/ss.png")
    #select roi from the image
    img = cv2.imread(f"C:/Users/{pc_name}/Desktop/ss.png")
    roi = cv2.selectROI("wins",img)
    x,y,w,h = roi[0],roi[1],roi[2],roi[3]
    frame = img[y:y+h,x:x+w]
    cv2.destroyWindow("wins")
    #tesseract ocr section and translating the text using by googletranslator
    try:
        tesseract_text = pay.image_to_string(frame)
        result = translator.translate(tesseract_text,src=f"{languages[f'{combo_1_al}']}",dest=f"{languages[f'{combo_2_al}']}").text
        text_area.delete('1.0',END)
        text_area.insert(tkinter.END,result)
    except:
        messagebox.showerror("Erorr","Hata meydana geldi")
#kes_ve çevir butonu
ceviri_butonu = Button(pencere,text="Çeviri Yap & Yazıyı oku",command=get_rectangle_points,bg="cyan",padx=25,pady=10)
ceviri_butonu.pack()
ceviri_butonu.place(x=20,y=195)
#özetleme fonksiyonu
def summiraze():
    #combobox değeri
    text = text_area.get("1.0",END)
    sentence = int(spin_box.get())
    language = Combo3.get()
    parser = PlaintextParser.from_string(text,Tokenizer(tokinizer[f'{language}']))
    summirizer = LexRankSummarizer()
    summary = summirizer(parser.document,sentence)
    text_area.delete("1.0",END)
    for i in summary:
        text_area.insert(tkinter.END,i)


#kes ve özetle butonu
summi_butonu = Button(pencere,text="Yazıyı Özetle",command=summiraze,bg="forest green",padx=40,pady=10)
summi_butonu.pack()
summi_butonu.place(x=500,y=195)


#çeviri için çıkış sorusu
def cikis():
    sorgu = messagebox.askyesno("Çıkış","Çıkış Yapmak İstiyor Musunuz?")
    if sorgu is True:
        pencere.destroy()
        exit()
    else:
        pass
pencere.protocol('WM_DELETE_WINDOW',cikis)
pencere.mainloop()