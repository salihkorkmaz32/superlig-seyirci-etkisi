#KÜTÜPHANELER
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.weightstats import CompareMeans, DescrStatsW
from statsmodels.stats.proportion import proportions_ztest, confint_proportions_2indep
import seaborn as sns

pd.set_option("display.max_columns", None)

df= pd.read_csv("veri/temiz/superlig_temiz.csv", parse_dates=["Date"])

#TANIMLAYICI İSTATİSTİKLER
gol_farkı_ti = df["gol_farki"].describe()
print(gol_farkı_ti)

ort1= df.groupby("seyircisiz")["gol_farki"].mean()
ort2= df.groupby("seyircisiz")["ev_kazandi"].mean()
ort3= df.groupby("seyircisiz")["toplam_gol"].mean()

for ort in (ort1, ort2, ort3):
    print(f"ortalama: {ort}")

#GOL FARKI HİSTOGRAMI
plt.hist(df["gol_farki"], bins=14, align="left")
plt.title("Gol Farkı Dağılımı")
plt.xlabel("Gol Farkı")
plt.ylabel("Maç Sayısı")
plt.savefig("grafikler/gol_farki.png")
plt.show()

#KARŞILAŞTIRMALI HİSTOGRAM
seyircili= df[df["seyircisiz"] ==0]
seyircisiz= df[df["seyircisiz"] ==1]

plt.hist(seyircili["gol_farki"], bins=range(-7, 9), align="left", density=True, alpha= 0.5, label="seyircili")
plt.hist(seyircisiz["gol_farki"], bins=range(-7, 9), align="left", density=True, alpha=0.5, label="seyircisiz")
plt.xlabel("Gol Farkı")
plt.ylabel("Oran")
plt.title("Gol Farkı Seyircili/Seyircisiz")
plt.legend()
plt.savefig("grafikler/gol_farki_seyircili_seyircisiz.png")
plt.show()

#GRUP BAZLI İSTATİSTİKLER
seyircili_ti = seyircili["gol_farki"].describe()
seyircisiz_ti = seyircisiz["gol_farki"].describe()
print(f"seyircili: {seyircili_ti} \nseyircisiz: {seyircisiz_ti}")

#NORMALLİK
print(df["gol_farki"].skew())
print(df["gol_farki"].kurt())
print()
print(seyircili["gol_farki"].skew())
print(seyircili["gol_farki"].kurt())
print()
print(seyircisiz["gol_farki"].skew())
print(seyircisiz["gol_farki"].kurt())

#shapiro testi
w, p = stats.shapiro([df["gol_farki"]])
print(f"W: {w} \np değeri: {p}")

w, p = stats.shapiro(seyircili["gol_farki"])
print(f"W: {w} \np değeri: {p}")

w, p = stats.shapiro(seyircisiz["gol_farki"])
print(f"W: {w} \np değeri: {p}")

#q-q grafikleri
sm.qqplot(seyircili["gol_farki"], line="s")
plt.title("Seyircili Q-Q Grafiği")
plt.savefig("grafikler/seyircili_qq.png")

sm.qqplot(seyircisiz["gol_farki"], line="s")
plt.title("Seyircisiz Q-Q Grafiği")
plt.savefig("grafikler/seyircisiz_qq.png")

#Z DEĞERİ VE AYKIRI DEĞERLER
df["z_score"]= stats.zscore(df["gol_farki"], ddof=1)
print(df["z_score"].head())

z_score_mean= df["z_score"].mean()
z_score_std= df["z_score"].std()
print(f"ortalama: {z_score_mean}  standart sapma: {z_score_std}")


aykiri_deger= df[df["z_score"].abs()>3]
print(len(aykiri_deger))

colons=["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "gol_farki", "z_score"]
print(aykiri_deger[colons].head())

print(aykiri_deger["seyircisiz"].value_counts())

#KUTU GRAFİĞİ
plt.figure()
plt.boxplot([seyircili["gol_farki"], seyircisiz["gol_farki"]], tick_labels=["seyircili","seyircisiz"])
plt.title("Gol_Farkı Kutu Grafiği")
plt.ylabel("Gol Farkı")
plt.xlabel("Dönem")
plt.savefig("grafikler/gol_farki_kutugrafigi.png")
plt.show()

#DİĞER DEĞİŞKENLER
df["sut_farki"]= df["HS"] - df["AS"]
print(df["sut_farki"])

seyircili= df[df["seyircisiz"] ==0]
seyircisiz= df[df["seyircisiz"] ==1]

sut_farki_ort1= seyircisiz["sut_farki"].mean()
sut_farki_ort2= seyircili["sut_farki"].mean()

print(f"ort1: {sut_farki_ort1} \nort2: {sut_farki_ort2}")

liste = ["HS", "AS", "sut_farki", "HST", "AST", "HF", "AF", "HY", "AY", "HR", "AR", "HC", "AC"]
print(df.groupby("seyircisiz")[liste].mean().round(2))

#TOPLAM GOL VE ŞUT FARKI DAĞILIMLARI
def istatistiksel_deger(veri,isim):
    carpiklik = veri.skew()
    basiklik = veri.kurt()
    w,p = stats.shapiro(veri)

    print(f"{isim}: çarpıklık: {carpiklik:.2f}, basıklık: {basiklik:.2f}, w: {w:.2f}, p: {p}")

istatistiksel_deger(seyircisiz["toplam_gol"], "seyircisiz")
istatistiksel_deger(seyircili["toplam_gol"], "seyircili")
print()
istatistiksel_deger(seyircisiz["sut_farki"], "seyircisiz")
istatistiksel_deger(seyircili["sut_farki"], "seyircili")

plt.figure()
plt.hist([seyircisiz["toplam_gol"], seyircili["toplam_gol"]], label=["seyircisiz" , "seyircili"], density= True, alpha=0.5, bins=range(0,11), align="left")
plt.title("Toplam Gol Histogram Grafiği")
plt.xlabel("Toplam Gol")
plt.ylabel("Oran")
plt.legend()
plt.savefig("grafikler/toplam_gol_hist.png")
plt.show()


plt.figure()
plt.hist([seyircisiz["sut_farki"], seyircili["sut_farki"]], label=["seyircisiz", "seyircili"], bins= 20, align="left", alpha=0.5, density= True )
plt.title("Sut Farkı Histogram Grafiği")
plt.xlabel("Şut Farkı")
plt.ylabel("Oran")
plt.savefig("grafikler/sut_farki_hist.png")
plt.show()

#HİPOTEZ TESTLERİ

#t testi

# H0: seyircili ve seyircisiz maçlarda gol farkı açısından fark yoktur.
# H1: seyircili ve seyircisiz maçlarda gol farkı açısından fark vardır.

t,p = stats.ttest_ind(seyircisiz["gol_farki"], seyircili["gol_farki"], equal_var=False)
print(f"t değeri: {t:.4f} , p değeri: {p:.4f}")

d1 = DescrStatsW(seyircisiz["gol_farki"])
d2 = DescrStatsW(seyircili["gol_farki"])

karsilastir= CompareMeans(d1,d2)

t,p, sd= karsilastir.ttest_ind(usevar="unequal")

alt, ust = karsilastir.tconfint_diff(usevar="unequal")

print(f"t: {t:.4f} , p: {p:.4f}, serbestlik derecesi: {sd:.4f}")
print(f"%95 güven aralığı: {alt:.3f}:{ust:.3f}")

#toplam gol ve şut farkı için t testi

# H0: seyircili ve seyircisiz maçlarda toplam gol açısından fark yoktur.
# H1: seyircili ve seyircisiz maçlarda toplam gol açısından fark vardır.

# H0: seyircili ve seyircisiz maçlarda şut farkı açısından fark yoktur.
# H1: seyircili ve seyircisiz maçlarda şut farkı açısından fark vardır.

def welch_t(sutun_adi, isim):
    t,p = stats.ttest_ind(seyircisiz[sutun_adi], seyircili[sutun_adi], equal_var=False)
    print(f"{isim} --> t değeri: {t:.4f} , p değeri: {p:.4f}")

welch_t("gol_farki", "gol farkı")
welch_t("sut_farki", "şut farkı")
welch_t("toplam_gol", "toplam gol")

print()

#mann whitney testi
def man_whitney_u(sutun_adi, isim):
    u,p = stats.mannwhitneyu(seyircisiz[sutun_adi], seyircili[sutun_adi], alternative = "two-sided")
    print(f"{isim} --> u: {u:.4f} , p: {p:.4f}")

man_whitney_u("gol_farki", "gol farkı")
man_whitney_u("sut_farki", "şut farkı")
man_whitney_u("toplam_gol", "toplam gol")

#iki oran z testi

# H0: seyircili ve seyircisiz maçlarda ev sahibinin kazanma oranı açısından fark yoktur.
# H1: seyircili ve seyircisiz maçlarda ev sahibinin kazanma oranı açısından fark vardır.

df_seyircisiz = (seyircisiz["ev_kazandi"] == 1 ).sum()
df_seyircili = (seyircili["ev_kazandi"] == 1).sum()

n_seyircisiz = len(seyircisiz)
n_seyircili = len(seyircili)

z,p = proportions_ztest(count=[df_seyircisiz, df_seyircili], nobs=[n_seyircisiz, n_seyircili])
alt , ust = confint_proportions_2indep(df_seyircisiz , n_seyircisiz , df_seyircili, n_seyircili)

print(f"z: {z:.4f} , p: {p:.4f}")
print(f"oran farkında %95 güven aralığı: {alt:.4f}:{ust:.4f}")

oran_kazanma1= df_seyircisiz/n_seyircisiz
oran_kazanma2= df_seyircili/n_seyircili

print(f"seyircisiz kazanma oranı: {oran_kazanma1:.2f}\nseyircili kazanma oranı: {oran_kazanma2:.2f}")

#ki-kare testi

#H0: seyircili ve seyircisiz dönem arasında maç sonuçları bakımından fark yoktur.
#H1: seyircili ve seyircisiz dönem arasında maç sonuçları bakımından fark vardır.

tablo= pd.crosstab(df["seyircisiz"], df["FTR"])
print(tablo)

ki2, p, sd, beklenen= stats.chi2_contingency(tablo)

print(f"kikare: {ki2:.3f}, p: {p:.3f}, sd:{sd:.3f}")
print(f"\nbeklenen değer: {beklenen}")

#anova

#H0: sezonlar arasında ortalama gol farkı açısından fark yoktur.
#H1: sezonlar arasında ortalama gol farkı açısından fark vardır.

sezon = df["sezon"].unique()
print(sezon)

sezon_gruplari= []
for s in sezon:
    sezon_gruplari.append(df[df["sezon"] == s]["gol_farki"])

f,p = stats.f_oneway(*sezon_gruplari)    
print(f"F: {f:.3f}, p: {p:.3f}")

print(df.groupby("sezon")["gol_farki"].mean().round(3))


#güç analizi
z_alfa = 1.96 
z_beta= 0.84  

s1= seyircisiz["gol_farki"].std()
s2= seyircili["gol_farki"].std()
n1= len(seyircisiz)
n2= len(seyircili)

sh = (s1**2/n1 + s2**2/n2) ** 0.5

mde= (z_alfa + z_beta) * sh
print(f"standart hata: {sh:.3f}, mde: {mde:.3f}")

mde_yuzde = (mde / seyircili["gol_farki"].mean()) * 100
print(f"mde ev avantajının {mde_yuzde:.3f}'ü")

#KORELASYON

#H0: şut farkı ile gol farkı arasında ilişki bakımından fark yoktur.
#H1: şut farkı ile gol farkı arasında ilişki bakımından fark vardır.

r,p = stats.pearsonr(df["gol_farki"], df["sut_farki"])
print(f"r: {r:.4f}, p:{p:.4f}")

rho,p = stats.spearmanr(df["gol_farki"], df["sut_farki"])
print(f"rho: {rho:.4f}, p: {p:.4f}")

#korelasyon matrisi
df["isabetli_sut_farki"]= df["HST"]-df["AST"]
df["korner_farki"]= df["HC"]-df["AC"]
df["faul_farki"]= df["HF"]-df["AF"]
df["sari_kart_farki"]= df["HY"]-df["AY"]

liste= ["gol_farki", "sut_farki", "isabetli_sut_farki", "korner_farki", "faul_farki", "sari_kart_farki"]

korelasyon_matrisi= df[liste].corr()
print(korelasyon_matrisi.round(3))

#ısı haritası
plt.figure()
sns.heatmap(korelasyon_matrisi, cmap="coolwarm", annot=True, vmin=-1, vmax=1, fmt=".2f")
plt.title("Korelasyon Isı Haritası")
plt.tight_layout()
plt.savefig("grafikler/korelasyon_isi_haritasi.png")
plt.show()

#saçılım grafiği
plt.figure()
sns.regplot(x="isabetli_sut_farki", y="gol_farki", data= df, x_jitter=0.3, y_jitter=0.3, scatter_kws={"alpha": 0.3}, line_kws={"color": "red"})
plt.title("İsabetli Şut Farkı ve Gol Farkı Saçılım Grafiği")
plt.xlabel("İsabetli Şut Farkı")
plt.ylabel("Gol Farkı")
plt.tight_layout()
plt.savefig("grafikler/isabetli_sut_gol_fark_sacilim.png")
plt.show()


#REGRESYON

#model1
x= sm.add_constant(df["seyircisiz"])
y= df["gol_farki"]

model = sm.OLS(y,x).fit()
print(model.summary())

#model2 takım kuklalarıyla beraber
ev_sahibi_k = pd.get_dummies(df["HomeTeam"], prefix="ev", drop_first=True, dtype=int)
deplasman_k = pd.get_dummies(df["AwayTeam"], prefix="dep",drop_first= True, dtype=int)

x2 = pd.concat([df["seyircisiz"], ev_sahibi_k, deplasman_k], axis=1)
x2= sm.add_constant(x2)
y2= df["gol_farki"]

model2 = sm.OLS(y2, x2).fit()

print(model2.summary())

#artık analizi
sm.qqplot(model2.resid, line="s")
plt.title("Artıklar için Q-Q Grafiği")
plt.savefig("grafikler/artik_qqplot.png")
plt.show()

plt.figure()
plt.scatter(model2.fittedvalues, model2.resid, alpha=0.3)
plt.axhline(0, color="red")
plt.xlabel("Tahmin Edilen Gol Farkı")
plt.ylabel("Artık")
plt.title("Artık - Gol Farkı Tahmin Grafiği ")
plt.savefig("grafikler/artik_tahmin_grafigi.png")
plt.show()

#TAKIM BAZINDA EV AVANTAJI
pivot = df.pivot_table(index="HomeTeam", columns="seyircisiz", values="gol_farki", aggfunc="mean")
pivot= pivot.dropna()
print(pivot.round(2))

pivot["fark"]= pivot[1] - pivot[0]
pivot["z"]= stats.zscore(pivot["fark"], ddof=1)
print(pivot.sort_values("fark").round(2))
print()
print("fark ortalama:" , pivot["fark"].mean().round(3))

#takımların maç sayıları
pivot2 = df.pivot_table(index="HomeTeam", columns="seyircisiz", values="gol_farki", aggfunc="count")
print(pivot2.round(2).dropna())

#BAHİS ORANLARI 
#eksik oranlar
sutun= ["B365H", "B365D", "B365A"]
sutun_nan = df[sutun].isna().sum()
print(sutun_nan)

#ham olasılıklar ve bahisçi marjı
df["galibiyet_ev_ham"]= 1 / df["B365H"]
df["beraberlik_ham"]= 1 / df["B365D"]
df["galibiyet_dep_ham"]= 1 / df["B365A"]

sutun_bet = ["galibiyet_ev_ham", "beraberlik_ham", "galibiyet_dep_ham"]
print(df[sutun_bet].head())

df["toplam_oran_ham"]= df["galibiyet_ev_ham"] + df["beraberlik_ham"] + df["galibiyet_dep_ham"]
print("toplam ham oran: ", df["toplam_oran_ham"].head())
print("\nortalama ham olasılık: ", df["toplam_oran_ham"].mean())

#normalleştirilmiş olasılıklar
df["galibiyet_ev_normallestirilmis"]= df["galibiyet_ev_ham"] / df["toplam_oran_ham"]
df["beraberlik_normallestirilmis"]= df["beraberlik_ham"] / df["toplam_oran_ham"]
df["galibiyet_dep_normallestirilmis"]= df["galibiyet_dep_ham"] / df["toplam_oran_ham"]

sutun_normallestirilmis= ["galibiyet_ev_normallestirilmis","beraberlik_normallestirilmis","galibiyet_dep_normallestirilmis"]
print(df[sutun_normallestirilmis].head())

df["toplam_oran_normallestirilmis"]= df["galibiyet_ev_normallestirilmis"] + df["beraberlik_normallestirilmis"] + df["galibiyet_dep_normallestirilmis"]
print("normalleştirilmiş oran: " ,df["toplam_oran_normallestirilmis"].head())

#dönemlere göre bahisçi tahmini
liste_ = ["galibiyet_ev_normallestirilmis", "beraberlik_normallestirilmis", "galibiyet_dep_normallestirilmis", "ev_kazandi"]
print(df.groupby("seyircisiz")[liste_].mean().round(3))

#bahis olasılıkları için t testi
seyircisiz = df[df["seyircisiz"] == 1]
seyircili= df[df["seyircisiz"] == 0]

#H0: Bahisçilerin ev sahibine verdiği ortalama kazanma oranları arasında fark yoktur.
#H1: Bahisçilerin ev sahibine verdiği ortalama kazanma oranları arasında fark vardır.

t,p = stats.ttest_ind(seyircisiz["galibiyet_ev_normallestirilmis"], seyircili["galibiyet_ev_normallestirilmis"], equal_var=False, nan_policy="omit")
print(f"t: {t:.3f}, p: {p:.3f}")

#DUYARLILIK ANALİZİ 
#sadece temiz sezonlar
temiz_seyircisiz= df[df["sezon"]==2021]
temiz_seyircili= df[df["sezon"].isin([2223, 2324, 2425, 2526])]

mac_sayisi1= temiz_seyircisiz["gol_farki"].count()
mac_sayisi2= temiz_seyircili["gol_farki"].count()
print(f"seyircisiz maç sayısı: {mac_sayisi1}, seyircili maç sayısı: {mac_sayisi2}")

gol_farki_ort1= temiz_seyircisiz["gol_farki"].mean()
gol_farki_ort2= temiz_seyircili["gol_farki"].mean()
print(f"seyircisiz gol farkı ortalaması: {gol_farki_ort1:.3f}, seyircili gol farkı ortalaması: {gol_farki_ort2:.3f}")

t,p = stats.ttest_ind(temiz_seyircisiz["gol_farki"], temiz_seyircili["gol_farki"], equal_var=False, nan_policy = "omit")
print(f"t: {t:.3f}, p: {p:.3f}")

#aykırı değerler olmadan
aykirisiz= df[df["z_score"].abs() <= 3]
print(f"kalan maç: {len(aykirisiz)}")

aykirisiz_seyircisiz= aykirisiz[aykirisiz["seyircisiz"]== 1]
aykirisiz_seyircili= aykirisiz[aykirisiz["seyircisiz"]== 0]

t,p= stats.ttest_ind(aykirisiz_seyircisiz["gol_farki"], aykirisiz_seyircili["gol_farki"], equal_var=False, nan_policy="omit")
print(f"t: {t:.3f}, p: {p:.3f}")

#SEZON TRENDİ
sezon_ort = df.groupby("sezon")["gol_farki"].mean()

plt.figure()
plt.plot(sezon_ort.index, sezon_ort.values, marker="o")
plt.axvline(2021, color="red", linestyle="--", label="seyircisiz sezon")
plt.title("sezonlara göre ortalama ev avantajı")
plt.xlabel("sezon")
plt.ylabel("ortalama gol farkı")
plt.legend()
plt.xticks(sezon_ort.index, ["19/20", "20/21", "21/22", "22/23", "23/24", "24/25", "25/26"])
plt.savefig("grafikler/sezon_trendi.png")
plt.show()

