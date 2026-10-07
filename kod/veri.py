import pandas as pd

def sezon_url(sezon_kodu):
    mesaj =f"https://raw.githubusercontent.com/Char2mant/futbol-veri-aynasi/main/data/fd/{sezon_kodu}/T1.csv"
    return mesaj

veri_listesi = ["1920", "2021", "2122", "2223", "2324", "2425", "2526"]

for veri in veri_listesi:
    adres= sezon_url(veri)
    df= pd.read_csv(adres)
    df.to_csv(f"veri/ham/T1_{veri}.csv", index=False)
    print(f"{veri} sezonu kaydedildi: {df.shape[0]} maç")


