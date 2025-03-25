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
    '''Zmanjsamo jo zato, ker na velikih slikah je veliko več računanja, kot na manjših slikah'''
    return cv.resize(slika, (sirina, visina))
    pass

def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze) -> list:
    '''Sprehodi se skozi sliko v velikosti škatle (sirina_skatle x visina_skatle) in izračunaj število pikslov kože v vsaki škatli.
    Škatle se ne smejo prekrivati!
    Vrne seznam škatel, s številom pikslov kože.
    Primer: Če je v sliki 25 škatel, kjer je v vsaki vrstici 5 škatel, naj bo seznam oblike
      [[1,0,0,1,1],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,1]]. 
      V tem primeru je v prvi škatli 1 piksel kože, v drugi 0, v tretji 0, v četrti 1 in v peti 1.'''

    #sprehodim se skozi sliko in sicer naredim 25 skatel sirina 44, visina 68
    #vsako skatlo prestejem stevilo pikslov, ki ustreza barvi koze in če jih je ve kot 40%
    #se odločim da je skatla najverjetneje vsebuje barvo koze in dodam 1 v nasprotnem primeru pa dodam 0.

    skatle = []
    totalpiksel = (sirina_skatle * visina_skatle) * 0.5
    # Iterate over the image to process each pixel
    for y in range(0, slika.shape[0], visina_skatle):
        row = []
        for x in range(0, slika.shape[1], sirina_skatle):

            slikatemp = slika[y:y + visina_skatle, x:x + sirina_skatle]

            skatla = prestej_piklse_z_barvo_koze(slikatemp, barva_koze)


            print(skatla)

            if(skatla>=totalpiksel):
                row.append(1)
            else:
                row.append(0)
        skatle.append(row)

    return skatle
    pass

def prestej_piklse_z_barvo_koze(slika, barva_koze) -> int:
    '''Prestej število pikslov z barvo kože v škatli.'''

    #dobim izrezano sliko in glede na njene dimenzije grem skozi vse piksle in za vsak piksel,
    # ki ima vse tri vrednosti barve koze vecje od spodnje meje ali enake ter  manjse od zgornje meje
    # ali enake povečam counter za 1

    count = 0


    for y in range(slika.shape[0]):
        for x in range(slika.shape[1]):

            if np.all(barva_koze[0] <= slika[y, x]) and np.all(slika[y, x] <= barva_koze[1]):

                count += 1

    return count
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


    #sprehodim se skozi skatle in ce je trenutna skatla 1 potem pomnozim x z 44 in jz 68 tako, da dobim začetne kordinate skatle
    #za skatlo vem kakšne ima mere in jo izrišem
    #odločil sem se da zraven te skatle ki ima najverjetneje obraz se izrisem vse sorodne skatle(8)
    #če je y + i * visina skatle večji ali enak 0 ter x + j * sirian skatle večji ali enak 0 da ne prekoračim levega in zgornjega roba
    #ter da y+i * visina skatle ni večji od velikosti slike in x+j * sirina skatle večji od slike
    highlighted_image = slika.copy()


    box_width = 52
    box_height = 60


    thickness = 2


    for y in range(len(skatle)):
        for x in range(len(skatle[0])):
            if skatle[y][x] != 0:



                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if 0 <= y + i < len(skatle) and 0 <= x + j < len(skatle[0]):

                            neighbor_top_left_x = (x + j) * box_width
                            neighbor_top_left_y = (y + i) * box_height
                            cv.rectangle(highlighted_image, (neighbor_top_left_x, neighbor_top_left_y),
                                          (neighbor_top_left_x + box_width, neighbor_top_left_y + box_height),
                                          (0, 0, 255), thickness)

    return highlighted_image

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
        slikaTemp = zmanjsaj_sliko(slika, 260, 300)---------

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

        cv.destroyAllWindows()
        sirina_skatle = int(width/5)
        visina_skatle = int(height / 5)


        barva_koze = (np.array([av_1B, av_1G, av_1R]), np.array([av_2B, av_2G, av_2R]))

        print("sirina,visina skatle: " , sirina_skatle,visina_skatle)

        ''' v barva_koze si zapomnim spodnjo ter zgornjo mejo BGR in v zanki pridobivam sliko kamere in
          pridobivam skatle in jih na sliki z kvadratom obrišem če je skatla 1  '''

        while True:


            ret, slika = kamera.read()
            slika = zmanjsaj_sliko(slika,260,300)
            cv.imshow('Kamera', slika)
            skatle = obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze)
            print(skatle)
            pobarvanaSlika = pobarvaj_sliko(slika, skatle)
            cv.imshow('Highlighted Image', pobarvanaSlika)



            if cv.waitKey(1) & 0xFF == ord('q'):
                break



            #ret, slika = kamera.read()
            #slikaTemp = zmanjsaj_sliko(slika, 220, 340)
            #cv.imshow('Kamera', slikaTemp)
            #skatle = obdelaj_sliko_s_skatlami(slikaTemp, sirina_skatle, visina_skatle, barva_koze)
            #print(skatle)
            #pobarvanaSlika = pobarvaj_sliko(slikaTemp, skatle)
            #cv.imshow('Highlighted Image', pobarvanaSlika)
            #cv.waitKey(0)
            #if key == ord('q'):
            #    break

        kamera.release()
        cv.destroyAllWindows()


    pass
