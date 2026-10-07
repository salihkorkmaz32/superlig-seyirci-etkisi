import pandas as pd

pd.set_option("display.max_columns", None)

veri_listesi = ["1920", "2021", "2122", "2223", "2324", "2425", "2526"]
sutunlar= ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR", "HS", "AS", "HST", "AST", "HF", "AF", "HC", "AC", "HY", "AY", "HR", "AR", "B365H", "B365D", "B365A"]

tablolar=[]

for veri in veri_listesi:
    tablo= pd.read_csv(f"veri/ham/T1_{veri}.csv")
    tablo= tablo[sutunlar]
    tablo["sezon"]= veri
    tablolar.append(tablo)

df = pd.concat(tablolar, ignore_index=True)

print(df["Date"].dtype)
df["Date"]= pd.to_datetime(df["Date"], format= "%d/%m/%Y")
print(df["Date"].dtype)
print(df["Date"].min())
print(df["Date"].max())

df["seyircisiz"]= ((df["Date"] >= "2020-03-12") & (df["Date"] <= "2021-06-30")).astype(int)
print(df["seyircisiz"].value_counts())

print(df.shape)

bay = df["HS"].isna().sum()
bay_ = df[df["HS"].isna()]
print(bay , "\n" ,bay_)

bay_maclar= ["sezon", "Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG"]

print(bay_[bay_maclar])

iddia= df["B365H"].isna().sum()
print(iddia)

df= df[~df["HS"].isna()]
df= df.reset_index(drop= True)
print(df.shape)
print(df["HS"].isna().sum())

df["gol_farki"]= df["FTHG"] - df["FTAG"]

a= ["FTHG","FTAG","gol_farki"]
print(df[a].head())

df["ev_kazandi"]=(df["FTR"] == "H").astype(int)
b= ["FTR","ev_kazandi"]
print(df[b].head())

df["toplam_gol"]= df["FTHG"] + df["FTAG"]
c=["FTHG","FTAG","toplam_gol"]
print(df[c].head())

df.to_csv("veri/temiz/superlig_temiz.csv", index=False)


