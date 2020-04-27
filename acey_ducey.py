#!/usr/bin/env python3
# -*- coding: utf8 -*-
import sys   # sys.exit -komento
import random   # Korttipakan sekoittamiseta varten
import time   # Satunnainen nostoaika
import argparse   # Komentoriviparametrien (argument) lukemista varten


def aloita_peli(aloituskassa=100, kierrokset=10):
    """Aloittaa uuden interaktiivisen peli.
    
    Parametrit
    ----------
    aloituskassa : int of float
        Rahan määrä pelin alussa

    kierrokset : int
        Kierrosten lukumäärä

    """
    try:
        tulosta_aloitusviesti(aloituskassa, kierrokset)

        input("Paina <enter> kun olet valmis aloittamaan.")
        print()

        aloita_uusi_peli = True
        while (aloita_uusi_peli):
            kierroksia_jäljellä = kierrokset
            kassa = uusi_kassa(aloituskassa)
            
            while kierroksia_jäljellä > 0 and kassassa_rahaa(kassa) > 0:
                print()
                print("Kierros {}/{}.".format(kierrokset-kierroksia_jäljellä+1, kierrokset))

                print("Pakkaa sekoitetaan  ...")
                time.sleep(random.uniform(0.5, 1.0))
                pakka = uusi_pakka()
                
                kortti1, pakka = nosta_kortti(pakka)
                kortti2, pakka = nosta_kortti(pakka)

                print("\t{}".format(tulosta_kortti(kortti1)))
                print("\t{}".format(tulosta_kortti(kortti2)))

                erotus = korttien_erotus(kortti1, kortti2)
                if erotus <= 1:
                    print("Et voi voittaa tätä kierrosta. Hävisit automaattisesti yhden rahan.")
                    kassa = muuta_kassaa(-1, kassa)
                else:
                    kerroin = int(11/erotus * 1.5 + 0.5)

                    print("Kertoimesi tällä kierroksella on {:d}.".format(kerroin))
                    print("Voit voittaa 0 - {:.1f} yksikköä rahaa.".format(kerroin*kassassa_rahaa(kassa)))

                    panos = kysy_panos(kassa)
                    kassa = muuta_kassaa(-panos, kassa)

                    if panos > 0:
                        print("Uusi kortti on ...")
                        time.sleep(random.uniform(1, 2))
                        
                        kortti3, pakka = nosta_kortti(pakka)
                        print("\t{}".format(tulosta_kortti(kortti3)))

                        if kortti_välissä(kortti3, kortti1, kortti2):
                            voitto = int(kerroin*panos)
                            print("Voitit {} rahayksikköä! Onneksi olkoon.".format(voitto))
                            kassa = muuta_kassaa(voitto, kassa)
                        else:
                            print("Hävisit {} rahayksikköä.".format(panos))
                    else:
                        print("Et panostanut mitään.")

                kierroksia_jäljellä -= 1
                print()

            if kassassa_rahaa(kassa) == 0:
                print("Rahasi loppuivat.")
                print("Sinulla oli alussa rahaa {} yksikköä ja hävisit ne kaikki.".format(aloituskassa))
                print("Kestit {} {}.".format(len(kassa), "kierroksen" if len(kassa) == 1 else "kierrosta"))
            else:
                print("Sinulle jäi kassaan {} rahayksikköä.".format(kassassa_rahaa(kassa)))
                if (kassassa_rahaa(kassa) > aloituskassa):
                    print("Jäit {} rahayksikköä voitolle! Onneksi olkoon!".format(kassassa_rahaa(kassa)-aloituskassa))
                elif (kassassa_rahaa(kassa) < aloituskassa):
                    print("Hävisit {} rahayksikkö.".format(aloituskassa-kassassa_rahaa(kassa)))
                else:
                    print("Et voittanut etkä hävinnyt mitään.")

            aloita_uusi_peli = kysy_aloitetaanko_uusi_peli() 

    except KeyboardInterrupt as e:
        print()
        print("Lopetit pelin. Hei hei.")
        sys.exit(0)


def tulosta_aloitusviesti(aloituskassa, kierrokset):
    """Tulostaa ruudulle aloitusviestin.

    Parametrit
    ----------
    aloituskassa : float
        Rahan määrä alussa

    kierrokset : int
        Kierrosten lukumäärä
    """
    print(""""ACEY DUCEY" -KORTTIPELI
ALKUPERÄINEN PELI: CREATIVE COMPUTING, MORRISTOWN, NEW JERSEY, USA
PYTHON TOTEUTUS: JUUSO KORHONEN


ACEY-DUCEY -PELIN SÄÄNNÖT:
TIETOKONE JAKAA KAKSI KORTTIA NUMEROPUOLI YLÖSPÄIN.
NYT VOIT ASETTAA PANOKSEN SILLE, ETTÄ SEURAAVA JAETTU
KORTTI OSUU NÄIDEN KAHDEN KORTIN VÄLILLE. JOS VOITAT
SAAT PANOKSESI TUPLANA TAKAISIN. VOIT OHITTAA ASETTAMALLA
PANOKSEN ARVOON '0'.

SINULLA ON ALUSSA {} YKSIKKÖÄ RAHAA JA PELI KESTÄÄ ENIMMILLÄÄN
{} KIERROSTA.

""".format(aloituskassa, kierrokset))


def kysy_aloitetaanko_uusi_peli():
    """Kysyy pelaajalta aloitetaanko uusi peli.

    Palautaa
    --------
    True
        jos uusi peli aloitetaan.
    """
    uusi_peli = input("Aloitetaanko uusi peli (k/e)? ")
    while uusi_peli.lower() not in ('k', 'e'):
        print("Vastaa joko 'k' tai 'e'.")
        uusi_peli = input("Aloitetaanko uusi peli (k/e)? ")

    return uusi_peli.lower() == 'K'





def uusi_kassa(aloituskassa):
    """Palauttaa 'kassan' eli listan, jossa ensimmäisenä arvona on viimeisin
    rahan määrä.

    Parametrit
    ----------
    aloituskassa : int or float
        Rahan määrä alussa

    Palauttaa
    ---------
    array of float
    """
    return [float(aloituskassa)]


def uusi_pakka(pakkojen_lkm=1):
    """Palauttaa korttipakan satunnaisesss järjestyksessä.

    Yksittäinen kortti on esimerkiksi (12, '♥')
    
    Parametrit
    ----------
    pakkojen_lkm : int
        Kuinka monta 52 kortin pakkaa sekoittaa yhteen. Oletus 1.

    Palauttaa
    ---------
    array of (int, str)
    """
    maat = ['♠', '♥', '♦', '♣']
    arvot = list(range(1, 14))

    pakka = pakkojen_lkm * [(arvo, maa) for maa in maat for arvo in arvot]   # Kortit ovat järjestyksessä
    random.shuffle(pakka)   # Sekoita pakka

    return pakka


def kassassa_rahaa(kassa):
    """Palauttaa kassassa olevan rahan määrän.

    Parametrit
    ----------
    pakka : array of float
        Kassa

    Palauttaa
    ---------
    float
        Kassassa olevan rahan määrä
    """
    return kassa[0]


def nosta_kortti(pakka):
    """Nostaa kortin pakan päältä ja palauttaa pakan.

    Parametrit
    ----------
    pakka : arr_like of (int, str)

    Palauttaa
    ---------
    tuple (int, str)
        Nostettu kortti
    arrary of (int, str)
        Pakka ilman nostettua korttia
    """
    nostettu_kortti = pakka[0]
    pakka = pakka[1:]

    return nostettu_kortti, pakka



def tulosta_kortti(kortti):
    """Palauttaa kortin tulostettavassa muodossa.

    Parametrit
    ----------
    kortti : tuple(int, str)
        Tulostettava kortti

    Palauttaa
    ---------
    str
        Kortti muotoiltuna tulostettavaan muotoon
    """
    #padat = [chr(x) for x in range(0x1F0A1, 0x1F0AE)]
    #hertat = [chr(x) for x in range(0x1F0B1, 0x1F0BE)]
    #ruudut = [chr(x) for x in range(0x1F0C1, 0x1F0CE)]
    #ristit = [chr(x) for x in range(0x1F0D1, 0x1F0DE)]

    maat = { 
            '♥': 'hertta',
            '♦': 'ruutu',
            '♠': 'pata',
            '♣': 'risti'}
    arvot = {
            1: 'ässä',
            2: 'kakkonen',
            3: 'kolmonen',
            4: 'nelonen',
            5: 'viitonen',
            6: 'kuutonen',
            7: 'seiska',
            8: 'kasi',
            9: 'ysi',
            10: 'kymppi',
            11: 'jätkä',
            12: 'rouva',
            13: 'kuningas'}

    kortti_str = chr(0x1F0A0 + kortti[0] + 
        (0x10 if kortti[1] == '♥' else
        0x20 if kortti[1] == '♦' else
        0x30 if kortti[1] == '♣' else 0)
        )

    kortti_str += " = ’{}{}’".format(maat[kortti[1]], arvot[kortti[0]])

    return kortti_str


def kysy_aloitetaanko_uusi_peli():
    """Kysyy aloitetaanko uusi peli

    Palauttaa
    ---------
    True
        Jos aloitetaan uusi peli
    """
    return False


def kysy_panos(kassa):
    """Kysyy pelaajalta panoksen. Kassaa ei muuteta.

    Parametrit
    ----------
    kassa : array of float
        Nykyinen kassa

    Palauttaa
    ---------
    int
        Panoksen suuruus
    """
    rahaa_jäljellä = kassassa_rahaa(kassa)

    print("Sinulla on {} rahaa.".format(rahaa_jäljellä))

    panos = -1
    while (panos < 0 or panos > rahaa_jäljellä):
        try:
            panos = int(input("Kuinka paljon haluat panostaa (0 - {})?".format(rahaa_jäljellä)))
        except ValueError as e:
            print("Anna rahan määrä kokonaislukuna. Esimerkiksi: 5, 10, tai 0.")
            panos = -1
    
    return panos


def kortti_välissä(kortti1, kortti2, kortti3):
    """Tarkistaa onko ensimmäinen kortti kahden seuraavan välissä.

    Parametrit
    ----------
    kortti1, kortti2, kortti3 : tuple(int, str)
        Vertailtavat kortit

    Palauttaa
    ---------
    True
        jos kortti1 on korttien 2 ja 3 välissä.
    """
    # Maalla ei ole väliä vertailussa
    arvo1 = kortti1[0]
    arvo2 = kortti2[0]
    arvo3 = kortti3[0]

    return (arvo1 > min(arvo2, arvo3)) and (arvo1 < max(arvo2, arvo3))



def korttien_erotus(kortti1, kortti2):
    """Palauttaa korttien arvojen erotuksen.

    Parametrit
    ----------
    kortti1, kortti2 : tuple(int, str)
        Vertailtavat kortit

    Palauttaa:
    int
        Korttien arvojen väliin jäävien arvojen määrä.
    """
    arvo1 = kortti1[0]
    arvo2 = kortti2[0]

    return abs(arvo2-arvo1)



def muuta_kassaa(määrä, kassa):
    """Muuttaa kassaa annetun määrän verran.

    Parametrit
    ----------
    määrä : float
        Määrä joka lisätään (positiiviset luvut) tai vähennetään (negatiiviset luvut) kassasta.
    kassa : array of float
        Kassa

    Palauttaa
    ---------
    array of float
        Kassa muutoksen jälkeen
    """
    return [kassassa_rahaa(kassa)+määrä] + kassa


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("kassa", type=float, default=100, nargs='?', help="Kassa alussa (oletus: 100)")
    parser.add_argument("kierrokset", type=int, default=10, nargs='?', help="Kierrosten määrä (oletus: 10)")

    args = parser.parse_args()

    aloita_peli(args.kassa, args.kierrokset)

