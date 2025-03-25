import cv2 as cv
import numpy as np

levo_zgorajx = 0
levo_zgorajy = 0
desno_spodajx = 0
desno_spodajy = 0
selection_complete = False

def mouse_callback(event, x, y, flags, slika):

    #nastavim globalne spremenljvike, ki jih potem uporabljam v main
    #čakam dokler uporabnik ne pritisne levega gumba in si zapomnim kordinate na sliki
    #čakam dokler uporabnik ne spusti gumba in si zapomnim kordinate na sliki
    #narišem kvadrat

    global levo_zgorajx,levo_zgorajy,desno_spodajx,desno_spodajy, selection_complete

    if event == cv.EVENT_LBUTTONDOWN:

        levo_zgorajx = x
        levo_zgorajy = y

    elif event == cv.EVENT_LBUTTONUP:

        desno_spodajx = x
        desno_spodajy = y

        cv.rectangle(slika, (levo_zgorajx, levo_zgorajy), (desno_spodajx, desno_spodajy), (0, 255, 0), 2)


        selection_complete = True
        pass
        
def zmanjsaj_sliko(slika, sirina, visina):
    '''Zmanjšaj sliko na velikost sirina x visina.'''
    return cv.resize(slika, (sirina, visina))
    pass

def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze) -> list:
    
    pass

def prestej_piklse_z_barvo_koze(slika, barva_koze) -> int:
    
    pass


def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj) :
    '''Ta funkcija se kliče zgolj 1x na prvi sliki iz kamere.
    Vrne barvo kože v območju ki ga definira oklepajoča škatla (levo_zgoraj, desno_spodaj).
      Način izračuna je prepuščen vaši domišljiji.'''


    #v pixel_values dam vrednosti BGR iz podanega območja slike
    #BGR [0][1][2], ter delim z stevilom pikslov len(pixel_values)
    #shranim vse tri vrednosti v avg_color_int in ga vrnem
    pixel_values = []
    pixel_valuesB = 0
    pixel_valuesG = 0
    pixel_valuesR = 0

    for y in range(levo_zgoraj[1], desno_spodaj[1]):
        for x in range(levo_zgoraj[0], desno_spodaj[0]):
            pixel_values.append(slika[y, x])



    pixel_valuesB = np.sum([pixel[0] for pixel in pixel_values])
    pixel_valuesG = np.sum([pixel[1] for pixel in pixel_values])
    pixel_valuesR = np.sum([pixel[2] for pixel in pixel_values])

    pixel_valuesB = int(pixel_valuesB / len(pixel_values))
    pixel_valuesG = int(pixel_valuesG / len(pixel_values))
    pixel_valuesR = int(pixel_valuesR / len(pixel_values))

    print("moj bgr:", pixel_valuesB,pixel_valuesG,pixel_valuesR)


    avg_color_int = (pixel_valuesB, pixel_valuesG, pixel_valuesR)

    return avg_color_int
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

	
        cv.namedWindow('Select Skin Area')
        cv.setMouseCallback('Select Skin Area', mouse_callback, slikaTemp)

	while True:

            cv.imshow('Select Skin Area', slikaTemp)


            if selection_complete:



                avg_skin_tone_int = doloci_barvo_koze(slikaTemp, (levo_zgorajx, levo_zgorajy), (desno_spodajx, desno_spodajy))
                av_1B = avg_skin_tone_int[0] - 30
                av_1G = avg_skin_tone_int[1] - 30
                av_1R = avg_skin_tone_int[2] - 30
                av_2B = avg_skin_tone_int[0] + 30
                av_2G = avg_skin_tone_int[1] + 30
                av_2R = avg_skin_tone_int[2] + 30
                print(levo_zgorajx, levo_zgorajy, desno_spodajx, desno_spodajy)
                print('Average color of selected area (BGR):', avg_skin_tone_int)
                print(av_1B,av_1G,av_1R)
                print(av_2B,av_2G,av_2R)


                selection_complete = False


            key = cv.waitKey(1) & 0xFF
            if key == ord('q'):
                break
    pass
