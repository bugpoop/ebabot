import PySimpleGUI as sg
from datetime import datetime
from threading import Timer
import time
from selenium import webdriver
import os

sg.theme('DarkAmber')   # Color
# All the stuff inside your window.
layout = [[sg.Text('Gerekli EBA Bilgilerini Gir.')],
          [sg.Text('EBABOT bu bilgileri kimse ile paylaşmaz.')],
          [sg.Text('Kimlik Numaranız', size=(20, 1)), sg.InputText()],
          [sg.Text('EBA Şifreniz', size=(20, 1)), sg.InputText()],
          [sg.Text('Ders Başlangıç Saati', size=(20, 1)), sg.InputText(size=(3, 1)), sg.Text(':'), sg.InputText(size=(3,
                                                                                                                      1)), sg.Checkbox('Dersim bugün', key='checkbox')],
          [sg.Text('Tenefüs uzunluğu (dakika)', size=(20, 1)), sg.InputText(size=(3, 1), key='ara')],
          [sg.Text('Ders Sayısı', size=(20, 1)), sg.InputText(size=(3, 1), key='sayi')],
          [sg.Button('Başlat'), sg.Button('İptal')]]

# Create the Window
window = sg.Window('EBABOT 2021 v1.0', layout)

while True:
    event, values = window.read()
    tckn = values[0]
    sifre = values[1]
    saat = int(values[2])
    dakika = int(values[3])
    ara = int(values['ara'])
    sayi = int(values['sayi'])
    if event == 'Başlat':
        print("Giriş Bilgilerin:", tckn, sifre, "Ders başlangıç saati", saat,
              "teneffüs uzunluğu:", ara, "ders sayısı:", sayi)
        print("EBABOT 2021")
        print("Başlatılıyor!")
        print("EBABOT Akşamöncesi sürümünü kullanıyorsunuz.")
        path = os.getcwd()
        profile = path + r"\dyrdas9x.EBA"
        print("Profil klasörü", profile, "adresinde bulundu.")
        print("Programdan tamamen çıkmak için CTRL + Pause/Break tuşuna basın.")
        # DEFINITIOS
        if values['checkbox'] is True:
            print("Dersin bugün")
            bugun = 1
        else:
            print("Dersin yarın")
            bugun = 0
        fp = webdriver.FirefoxProfile(profile)
        driver = webdriver.Firefox(firefox_profile=fp)

        # giriş
        def giris():

            driver.get("https://eba.gov.tr/#/anasayfa")
            driver.find_element_by_xpath(
                "/html/body/app-root/app-anasayfa-page/div[2]/div/div/div[1]/div[2]/div[3]/div[3]/a[2]").click()
            driver.find_element_by_id("tckn").send_keys(tckn)
            driver.find_element_by_id("password").send_keys(sifre)
            driver.find_element_by_class_name("nl-form-send-btn").click()

        # derse katılım
        def katil():

            driver.get("https://eba.gov.tr/#/anasayfa")
            driver.find_element_by_xpath(
                "/html/body/app-root/app-anasayfa-page/div[2]/div/div/div[1]/div[2]/div[3]/div[3]/a[2]").click()
            time.sleep(2)
            driver.find_element_by_id("joinMeeting").click()
            time.sleep(2)
            driver.find_element_by_id("join").click()


        def ders():
            print("Derse giriş yapılıyor!")
            katil()
            time.sleep(ara * 60)  # DERS UZUNLUĞU
            print("Ders Bitti! Beklemeye geçiliyor.")
            time.sleep(605)  # TENEFÜS UZUNLUĞU


        def okul():
            print("Giriş yapılıyor..")
            giris()
            print("Başarıyla Giriş Yapıldı!")
            ders_sayisi = 0
            while ders_sayisi <= sayi:
                ders()
                ders_sayisi += 1
            print("Daha fazla dersin yok")

        if bugun == 1:
            gun = datetime.today()
            yarin = gun.replace(day=gun.day + 0, hour=saat, minute=dakika, second=2,
                                microsecond=0)
            fark = yarin - gun
            sure = fark.seconds + 1
            print("Dersin başlamasına", sure / 3600, "saat kaldı!")
            t = Timer(sure, okul)
            t.start()
        else:
            gun = datetime.today()
            yarin = gun.replace(day=gun.day + 1, hour=saat, minute=dakika, second=2,
                                microsecond=0)
            fark = yarin - gun
            sure = fark.seconds + 1
            print("Dersin başlamasına", sure / 3600, "saat kaldı!")
            t = Timer(sure, okul)
            t.start()

    if event == sg.WIN_CLOSED or event == 'İptal':  # if user closes window or clicks cancel
        window.close()
        break
window.close()