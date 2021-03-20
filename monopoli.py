import re
from random import randint
import os

os.system('cls')
def pindah_lokasi(lokasi):
    hasil_dadu = randint(1, 6)
    print()
    print("Dadu yang muncul -> {}".format(hasil_dadu))
    lokasi = lokasi + hasil_dadu
    return lokasi

def cek_harga(nama, negara, index, data_pemain, data_negara):
    jumlah_rumah  = data_pemain[nama]['asset'][negara]['rumah']
    jumlah_hotel =  data_pemain[nama]['asset'][negara]['hotel']
    harga_tanah = data_negara[index]['harga_tanah']
    harga_rumah = data_negara[index]['harga_rumah']
    harga_hotel = data_negara[index]['harga_hotel']
    total_rumah = harga_rumah*jumlah_rumah
    total_hotel = harga_hotel*jumlah_hotel
    total = harga_tanah + total_rumah +total_hotel
    print()
    print("NEGARA {}".format(negara.upper()))
    print("--------------------------------------")
    print("Harga Tanah {:<21}: {}".format(" ", idr_to_string(harga_tanah)))
    print("Harga Rumah {:<3} x {:<14} : {}".format(str(jumlah_rumah), idr_to_string(harga_rumah), idr_to_string(total_rumah)))
    print("Harga Hotel {:<3} x {:<14} : {}".format(str(jumlah_hotel), idr_to_string(harga_hotel), idr_to_string(total_hotel)))
    print("-------------------------------------------  + ")
    print("Total {}> {}".format("-"*27, idr_to_string(total)))
    return total

def tampilkan_aset(nama_pemilik, data_pemain, data_negara):
    list_negara = []
    print()
    for asset in data_pemain[nama_pemilik]['asset']:
        list_negara.append(asset)

    for negara in list_negara:
        print(negara.upper())
        print("---------------")
        print("Rumah : {:<8}".format(str(data_pemain[nama_pemilik]['asset'][negara]['rumah'])))
        print("Hotel : {:<8}".format(str(data_pemain[nama_pemilik]['asset'][negara]['hotel'])))
        print()

    print()

def idr_to_string(nominal):
    count = 0
    str_nominal = str(nominal)
    length = len(str_nominal) - 1
    stack = ""

    while length >= 0:
        stack += str_nominal[length]
        length -= 1

    str_nominal = ""
    for karakter in stack:
        if count == 3:
            count = 0
            str_nominal += "."
        str_nominal += karakter
        count += 1

    stack = ""
    length = len(str_nominal) - 1
    while length >= 0:
        stack += str_nominal[length]
        length -= 1

    return "Rp."+stack

data_pemain = {}
data_negara = {}
pemenang = "Tidak Ada"


pattern = r"(.*)\,(.*)\,(.*)\,(.*)\,(.*)\,(.*)\,(.*)\,(.*)"
i = 0
with open('monopoli_data.csv', 'r') as file:
    for line in file:
        if 'Negara' in line:
            continue
        row = line.strip()
        hasil_regex = re.search(pattern, row)
        nama_negara = hasil_regex[1]
        harga_tanah = int(hasil_regex[2])
        harga_rumah = int(hasil_regex[3])
        harga_hotel = int(hasil_regex[4])
        sewa_tanah = int(hasil_regex[5])
        sewa_rumah = int(hasil_regex[6])
        sewa_hotel = int(hasil_regex[7])
        status_kepemilikan = hasil_regex[8]

        i+=1

        data_negara[i] = {'nama_negara' : nama_negara, 'harga_tanah' : harga_tanah, 'harga_rumah' : harga_rumah, 'harga_hotel' : harga_hotel, 'sewa_tanah' : sewa_tanah, 'sewa_rumah' : sewa_rumah, 'sewa_hotel' : sewa_hotel, 'status_kepemilikan' : status_kepemilikan}
print()
print("Halo! Selamat Datang di Permainan 'Simple Monopoly' by Muhammad Alfarizi Tazkia!")
print()
jumlah_pemain = int(input("Masukan Jumlah Pemain : "))
sisa_pemain = jumlah_pemain
print("Baik, {} pemain siap memasuki dunia monopoli ini!". format(jumlah_pemain))

print()

for index in range(jumlah_pemain):
    nama_pemain = input("Masukan Nama Pemain {} : ".format(str(index+1)))
    total_kekayaan_awal = 200000000
    aset = {}
    posisi_awal = 0
    data_pemain[nama_pemain] = {}
    data_pemain[nama_pemain]['kekayaan'] = total_kekayaan_awal
    data_pemain[nama_pemain]['asset'] = aset
    data_pemain[nama_pemain]['posisi'] = posisi_awal
    data_pemain[nama_pemain]['status'] = 'aktif'

print("Berikut merupakan data negara beserta harganya")
print(" +{}+".format("-"*51))
print(" |{:^5}| {:^20} | {:^20} |".format("No", "Negara", "Harga Tanah"))
print(" +{}+".format("-"*51))
for line in data_negara:
    print(" |{:^5}| {:<20} | {:<20} |".format(str(line), data_negara[line]['nama_negara'], str(data_negara[line]['harga_tanah'])))
print(" +{}+".format("-"*51))

print()
enter = input("UNTUK MEMULAI PERMAINAN TEKAN ENTER")

selesai = False


while selesai == False:
    for index in data_pemain:
        os.system('cls')
        if data_pemain[index]['status'] == 'aktif':
            print()
            print("GILIRAN {} JALAN ! ".format(index.upper()))
            print("------------------------------------------")
            print("Total Kekayaan Sementara : {} ". format(idr_to_string(data_pemain[index]['kekayaan'])))
            print("Total Aset : {} Aset".format(str(len(data_pemain[index]['asset']))))
            print()
            if len(data_pemain[index]['asset']) > 0:
                lihat_asset = input("Ingin melihat daftar aset (y/t)?")
                if lihat_asset.lower() == "y":
                    tampilkan_aset(index, data_pemain, data_negara)
            jalan = input("ENTER untuk melihat hasil dadu ! ")

            index_lokasi = pindah_lokasi(data_pemain[index]['posisi'])

            if index_lokasi > 30:
                index_lokasi = index_lokasi - 30
                data_pemain[index]['kekayaan'] += 20000000
                print("Anda melewati Start, Anda berhak mendapat komisi sebesar Rp.20.000.000")

            negara_terkini = data_negara[index_lokasi]['nama_negara']
            pemilik_negara_terkini = data_negara[index_lokasi]['status_kepemilikan']
            harga_tanah = data_negara[index_lokasi]['harga_tanah']
            harga_rumah = data_negara[index_lokasi]['harga_rumah']
            harga_hotel = data_negara[index_lokasi]['harga_hotel']

            print("* Anda sekarang berada di --> {}".format(negara_terkini.upper()))
            data_pemain[index]['posisi'] = index_lokasi
            print()
            if pemilik_negara_terkini == "-":
                if data_pemain[index]['kekayaan'] - harga_tanah > 0:
                    beli = input("Apakah Anda ingin membeli TANAH di {} (y/t) ?".format(negara_terkini))
                    print()
                    if beli.lower() == "y":
                        data_negara[index_lokasi]['status_kepemilikan'] = index
                        data_pemain[index]['kekayaan'] -= harga_tanah
                        print("Anda Berhasil membeli tanah di negara {}, sisa kekayaan : {}".format(negara_terkini, idr_to_string(data_pemain[index]['kekayaan'])))
                        data_pemain[index]['asset'][negara_terkini] ={'rumah' : 0, 'hotel' : 0, 'status' : 'aktif'}
                else:
                    print("Uang anda gacukup untuk membeli aset ini")
                    print()
            elif pemilik_negara_terkini == index:
                if data_pemain[index]['asset'][negara_terkini]['rumah'] < 4 and data_pemain[index]['kekayaan'] > harga_rumah:
                    beli_rumah = input("Apakah anda ingin membeli rumah di {} (y/t)?".format(negara_terkini))
                    if beli_rumah.lower() == "y":
                        data_pemain[index]['asset'][negara_terkini]['rumah'] += 1
                        print("ANDA BERHASIL MEMILIKI {} RUMAH DI {} !".format(data_pemain[index]['asset'][negara_terkini]['rumah'], negara_terkini))
                        data_pemain[index]['kekayaan'] -= harga_rumah
                        print("Sisa kekayaan : {}".format(idr_to_string(data_pemain[index]['kekayaan'])))
                elif data_pemain[index]['asset'][negara_terkini]['rumah'] >= 4 and data_pemain[index]['kekayaan'] > harga_hotel:
                    beli_hotel = input("Apakah anda ingin membeli hotel di {} (y/t)?".format(negara_terkini))
                    if beli_hotel.lower() == "y":
                        data_pemain[index]['asset'][negara_terkini]['hotel'] += 1
                        print("ANDA BERHASIL MEMILIKI {} HOTEL DI {} !".format(data_pemain[index]['asset'][negara_terkini]['hotel'], negara_terkini))
                        data_pemain[index]['kekayaan'] -= harga_hotel
                        print("Sisa kekayaan : {}".format(idr_to_string(data_pemain[index]['kekayaan'])))
            else:
                print()
                print("OOPSS anda berkunjung ke wilayah milik {}, anda perlu membayar sewanya".format(pemilik_negara_terkini))
                enter = input("ENTER UNTUK MELIHAT RINCIANNYA")
                biaya_sewa = cek_harga(pemilik_negara_terkini, negara_terkini, index_lokasi, data_pemain, data_negara)
                print()
                enter = input("ENTER UNTUK MELAKUKAN PEMBAYARAN")
                if data_pemain[index]['kekayaan']-biaya_sewa <= 0:
                    print()
                    print("Yahh Kamu Bangkrut")
                    print()
                    data_pemain[index]['status'] = 'bangkrut'
                    sisa_pemain -= 1
                    counter = 1
                    print("PELEPASAN ASET {}".format(index))
                    print("-----------------------------------")
                    for line in data_negara:
                        if index == data_negara[counter]['status_kepemilikan']:
                            print("{:<15} - Dijual Ke Bank".format(data_negara[counter]['nama_negara']))
                            data_negara[counter]['status_kepemilikan'] = "-"
                        counter += 1
                else:
                    print("{} - {} : {}".format(str(data_pemain[index]['kekayaan']), str(biaya_sewa), str(data_pemain[index]['kekayaan'] - biaya_sewa)))
                    data_pemain[index]['kekayaan'] -= biaya_sewa
                    print()
                    print("SISA KEKAYAAN {} : {}".format(index, idr_to_string(data_pemain[index]['kekayaan'])))

                print()
                kekayaan_pemilik_negara_before = data_pemain[pemilik_negara_terkini]['kekayaan']
                data_pemain[pemilik_negara_terkini]['kekayaan'] += biaya_sewa
                print("Kekayaan {} saat ini : {} + {} = {}".format(pemilik_negara_terkini, str(kekayaan_pemilik_negara_before), str(biaya_sewa), idr_to_string(data_pemain[pemilik_negara_terkini]['kekayaan'])))

            print()
            enter = input("ENTER UNTUK MELANJUTKAN")

        if sisa_pemain == 1:
            os.system('cls')
            print()
            print("--- PERMAINAN SELESAI ---")
            print()
            for nama_pemenang in data_pemain:
                if data_pemain[nama_pemenang]['status'] == 'aktif':
                    pemenang = nama_pemenang
            print("Pemenang : {} ".format(pemenang))
            selesai = True

