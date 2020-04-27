#!/usr/bin/env python3
# -*- coding: utf8 -*-
import sys   # sys.exit -komennon tuonti
import argparse   # Komentoriviargumenttien parsimiseen
import random   # Korttipakan sekoittamista varten


# Ensimmäiseksi kirjoitamme tarvittavat funktiot

def aloita_peli():
	"""Pelin peruslogiikka on koodattu tänne.
	"""

	tulosta_aloitusviesti()

	vaikeustaso = aloita_uusi_peli()
	while (vaikeustaso != 0):

		arvaukset = uusi_lista()
		pakka = uusi_pakka(vaikeustaso)
		while not pakka_järjestyksessä(pakka):

			#tulosta_tyhjä_pakka(pakka[:], näytä_numerot=True)

			arvaus = pyydä_uusi_arvaus(len(pakka))   # Annetaan pakan koko funktiolle

			arvaukset = lisää_arvaus_listalle(arvaukset, pakka[:], arvaus)
			pakka = muuta_pakkaa(pakka, arvaus)

		# Tänne päästään, kun pakka on järjestyksessä
		arvaukset = lisää_arvaus_listalle(arvaukset, pakka[:], None)
		tulosta_tulokset(arvaukset)

		# Pyydä uutta peliä
		vaikeustaso = aloita_uusi_peli()

	tulosta_lopetusviesti()


def tulosta_aloitusviesti():
	"""Tulostaa aloitusviestin.
	"""

	print("#######################################")
	print(" * * * KÄÄNNÄ KORTIT OIKEIN PÄIN * * * ")
	print("#######################################")
	print()
	print("Tehtävänäsi on saada kaikki kortit oikein päin.")
	print("Et tiedä mitkä kortit ovat oikein ja mitkä väärin")
	print("päin. Voit kääntää yhden kortin kerrallaan.")
	print("Tietokone kertoo sinulle, kun kaikki kortit ovat")
	print("oikein päin.")
	print()
	print("Alussa vähintään yksi kortti on väärin päin.")
	print()


def aloita_uusi_peli():
	"""Tämä funktio kysyy pelaajalta aloitetaanko uusi
	peli ja palauttaa, pelin vaikeustason.

	Palauttaa
	---------
	0 : jos uutta pelia ei aloiteta
	1,2,3 : uuden pelin vaikeustason mukaan
	"""

	print("Aloitetaanko uusi peli?")
	print("Voit valita HELPON pelin (3 korttia), TAVALLISEN")
	print("pelin (4 korttia) tai VAIKEAN pelin (6 korttia).")
	print()
	print("Jos haluat lopettaa, kirjoita LOPETA.")
	print("Mikä on valintasi (HELPPO, TAVALLINEN, vai VAIKEA)?")
	
	# Vaihtoehdoille annetaan numeroarvot
	valinnat = {'lopeta': 0, 'helppo': 1, 'tavallinen': 2, 'vaikea': 3}
	
	# Seuraavaksi pyydetään vastausta, muutetaan kirjaimet pieniksi ja poistetaan ylimääräiset välilyönnit
	valinta = input('? ').lower().strip()   
	while valinta not in valinnat:
		print("Valintaa ei tunnistettu.")
		print("Valitse joko HELPPO, TAVALLINEN, VAIKEA, tai LOPETA.")
		valinta = input('? ').lower().strip()

	if valinnat[valinta] != 0:
		print("Onnea matkaan!")

	return valinnat[valinta]


def uusi_lista():
	"""Tämä funktio palauttaa uuden listan, johon arvaukset
	tallennetaan.
	"""
	return []


def uusi_pakka(vaikeustaso):
	"""Tämä funktio palauttaa uuden pakan, joka on valmiina 
	aloitusjärjestyksessä.

	Parametrit
	----------
	vaikeustaso : int
		Pelin vaikeustaso, joka muuttaa korttien lukumäärän.
		1 = 3 korttia
		2 = 4 korttia
		3 = 6 korttia

	Palauttaa
	---------
	array : Bool
		True tarkoittaa, että kortti on oikein päin
		False tarkoittaa, että kortti on väärin päin
		Esimerkkipakka: [False, True, False, False]
	"""
	korttien_lukumäärät = [3, 4, 6]   # Määrittää vaikeustason
	korttien_lukumäärä = korttien_lukumäärät[vaikeustaso-1]   # Vähennetään yksi, koska listan numerointi alkaa nollasta ja vaikeustaso ykkösestö

	# Palauttaa luvun joka on maksimissaan yksi vähemmän kuin korttien lukumäärä, eli vähintään yksi kortti on käännetty
	oikeinpäin_olevian_korttien_lukumäärä = random.randrange(korttien_lukumäärä)

	# Seuraaaksi muodostetaan lista, jossa on oikea määrä True-kenttiä (kortit oikeinpäin) ja False-kenttiä (kortit väärinpäin)
	pakka = [True]*oikeinpäin_olevian_korttien_lukumäärä + [False]*(korttien_lukumäärä-oikeinpäin_olevian_korttien_lukumäärä)

	# Sitten sekoitetaan kortit
	random.shuffle(pakka)

	# Palautetaan korttipakka
	return pakka


def pakka_järjestyksessä(pakka):
	"""Kertoo onko pakka järjestyksessä.

	Parametrit
	----------
	pakka : arr_like
		Pakka, joka on lista True/False -arvoja.

	Palauttaa
	---------
	Bool
		True, jos pakka on järjestykessä
		False, jos pakka ei ole järjestyksessä
	"""
	# Seuraava rivi vertaa True-kenttien lukumäärää (sum(pakka)) kaikkien korttien lukumäärään (len(pakka))
	# ja palauttaa True, jos nämä ovat samat.
	return sum(pakka) == len(pakka) 


def pyydä_uusi_arvaus(korttien_lukumäärä):
	"""Pyytää uuden arvauksen ja palauttaa käännettävän kortin numeron.

	Parametrit
	----------
	korttien_lukumäärä : int
		Korttien lukumäärä pakassa. 

	Palauttaa
	---------
	int
		Käännettävän kortin numero.
		1 = vasemmanpuoleisin
	"""
	print("Mikä kortti käännetään? Anna numero järjestyksessä vasemmalta")
	print("lähtien. 1 = vasemmanpuoleisin kortti, 2 = siitä seuraavan jne.")
	print()
	print("Anna kortin numero väliltä {}...{}".format(1, korttien_lukumäärä))
	
	try:
		kortin_numero = int(input("? "))
	except ValueError as e:
		kortin_numero = -1   # Jos numero ei kelpaa, asetetaan numero väliaikeisesti -1:ksi

	# Pyydä uutta numeroa kunnes se kelpaa
	while (kortin_numero <= 0 or kortin_numero > korttien_lukumäärä):
		print("Anna kortin numero väliltä {}...{}".format(1, korttien_lukumäärä))

		try:
			kortin_numero = int(input("? "))
		except ValueError as e:
			kortin_numero = -1   # Jos numero ei kelpaa, asetetaan numero väliaikeisesti -1:ksi

	return kortin_numero


def tulosta_tyhjä_pakka(pakka, näytä_numerot=False):
	"""Tulostaa pakan, muttei näytä sen sisältöä.

	Parametrit
	----------
	pakka : arr_like
		Tulostettava pakka

	näytä_numerot : bool
		True, niin tulostetaan myös korttien numerot
	"""
	# Käytetään tulosta_pakka -funktiota tulostamaan pakka
	tulosta_pakka(pakka, näytä_numerot=näytä_numerot, oikein="?", väärin="?")


def tulosta_pakka(pakka, arvaus=None, rivinro=None, näytä_numerot=False, oikein="🂱", väärin="🂠"):
	"""Tulostaa pakan ja näyttää sen sisällön.
	Parametrit
	----------
	pakka : arr_like
		Tulostettava pakka

	näytä_numerot : bool
	"""
	korttien_lukumäärä = len(pakka)

	if näytä_numerot:
		print("   " + " ".join([str(x+1) for x in range(korttien_lukumäärä)]))
		print("   -" + "--"*(korttien_lukumäärä-1))

	print(("{:2d} ".format(rivinro) if rivinro else "   ") + (" ".join([oikein if x else väärin for x in pakka])) + (" [{}]".format(arvaus) if arvaus is not None else ""))	


def lisää_arvaus_listalle(arvaukset, pakka, arvaus):
	"""Lisää arvauksen ja pakan tilan arvauksiin.

	Parametrit
	----------
	arvaukset : arr_like
		Lista arvauksista

	pakka : arr_like
		Pakan tilan ennen arvausta

	arvaus : int
		Arvatun kortin numero

	Palauttaa
	---------
	arr_like
		Uusi lista arvauksista
	"""
	arvaukset.append((pakka, arvaus))
	return arvaukset


def muuta_pakkaa(pakka, arvaus):
	"""Muuttaa pakkaa arvauksen mukaisesti, eli kääntää arvauksen mukaisen kortin
	ympäri.

	Parametrit
	----------
	pakka : arr_like
		Pakka ennen arvausta
	arvaus : int
		Käännettävän kortin numero

	Palauttaa
	---------
	arr_like
		Pakka arvauksen jälkeen
	"""
	pakka[arvaus-1] = not pakka[arvaus-1]   # Tämä muuttaa True:n Falseksi ja päinvastoin
	return pakka


def tulosta_tulokset(arvaukset):
	"""Tulostaa tuloslistauksen.
	"""
	print()
	for i, (pakka, arvaus) in enumerate(arvaukset):
		tulosta_pakka(pakka, arvaus, rivinro=i+1, näytä_numerot=(i == 0))
	print()

	print("Pakka on selvitetty! Tarvitsit {} arvausta.".format(len(arvaukset)-1))
	print()


def tulosta_lopetusviesti():
	"""Tulostaa lopetusviestin.
	"""
	print("Kiitos pelaamisesta!")
	print()
	print("Pelin on Python-kielellä kirjoittanut Juuso Korhonen.")
	print("Alkuperäinen idea lähti Matt Parkerin videosta: https://youtu.be/oCMVUROty0g")
	print()



# Koodin suoritus alkaa täältä
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--apua", action='store_true', default=False, help="Tulosta apuviesti")

	args = parser.parse_args()

	if (args.apua):
		tulosta_apuviesti()
		sys.exit(0)   # Poistu pelistä

	aloita_peli()


