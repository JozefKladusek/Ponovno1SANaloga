import cv2 as cv
import numpy as np

levo_zgorajx = 0
levo_zgorajy = 0
desno_spodajx = 0
desno_spodajy = 0
selection_complete = False

def mouse_callback(event, x, y, flags, slika):

        pass
        
def zmanjsaj_sliko(slika, sirina, visina):
    '''Zmanjšaj sliko na velikost sirina x visina.'''
    '''Zmanjsamo jo zato, ker na velikih slikah je veliko več računanja, kot na manjših slikah'''
    return cv.resize(slika, (sirina, visina))
    pass

def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze) -> list:
    
    pass

def prestej_piklse_z_barvo_koze(slika, barva_koze) -> int:
    
    pass


def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj) :
    
    pass

def pobarvaj_sliko(slika,skatle) :

    pass


if __name__ == '__main__':
    #Pripravi kamero

    #Zajami prvo sliko iz kamere

    #Izračunamo barvo kože na prvi sliki

    #Zajemaj slike iz kamere in jih obdeluj     
    
    #Označi območja (škatle), kjer se nahaja obraz (kako je prepuščeno vaši domišljiji)
        #Vprašanje 1: Kako iz števila pikslov iz vsake škatle določiti celotno območje obraza (Floodfill)?
        #Vprašanje 2: Kako prešteti število ljudi?

        #Kako velikost prebirne škatle vpliva na hitrost algoritma in točnost detekcije? Poigrajte se s parametroma velikost_skatle
        #in ne pozabite, da ni nujno da je škatla kvadratna.
	
	#slika = cv.imread('.utils/lenna.png')
    height = 300
    width = 260




    #if slika is None:
    #    print('Slika ni bila naložena.')
    #else:
    #    print('Slika je bila naložena.')

    ''' pridobim sliko iz kamere in označim del slike kjer je koža. Ko uporabnik označi naredim povprečni 
    BGR označenega območja na sliki ter spodnjo in zgornjo mejo'''

    kamera = cv.VideoCapture(0)

    if not kamera.isOpened():
        print('Kamera ni bila odprta.')
    else:
        ret, slika = kamera.read()
        slikaTemp = zmanjsaj_sliko(slika, 260, 300)



    pass
