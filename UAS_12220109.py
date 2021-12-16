#Ujian Akhir Semester IF2112 Pemrograman Komputer
#Salwa Anindya Rahma
#12220109

import json
from PIL import Image
import pandas as pd
import streamlit as st

st.write("Salwa Anindya Rahma - 12220109 - UAS IF2112 Pemrograman Komputer")
st.title("Aplikasi Informasi Produksi Minyak Mentah Seluruh Negara")
image = Image.open("foto atas.png")
st.image(image)
st.write("Selamat datang di aplikasi perminyakan yang menampilkan berbagai hal mengenai Produksi Minyak Mentah dari seluruh negara! Silahkan explore berbagai fitur yang ada dalam aplikasi ini. Enjoy Exploring :)")


f = open("kode_negara_lengkap.json")
data = json.load(f)
df = pd.read_csv("produksi_minyak_mentah.csv")
country_list = [] #data dari json dipindahkan ke list

for country in data:
    country_name = country.get('name')
    country_alpha3 = country.get('alpha-3')
    country_reg = country.get('region')
    country_subreg = country.get('sub-region')
    country_code = country.get('country-code')
    country_list.append([country_name, country_alpha3, country_reg, country_subreg, country_code])
year_max = int(df.max(axis=0)['tahun'])
year_min = int(df.min(axis=0)['tahun'])

#A: Grafik jumlah produksi minyak mentah terhadap waktu (tahun) dari suatu negara N
N = st.selectbox("Negara Produksi Minyak Mentah Yang Ingin Dicari", (country[0] for country in country_list)) 
for country in country_list:
    if country[0] == N: #Dipilih dari index ke-0, yaitu country name sebagai pilihan dalam select box
        country_alpha3 = country[1] #alpha3 merupakan kode negaranya yang akan disimpan
st.info("Jumlah Produksi Minyak Mentah terhadap Waktu (Tahun) " + N)
st.write("Jika grafik blank, maka data tidak tersedia. Silahkan pilih negara lain yang ingin dicari!")
dfA = df.loc[df["kode_negara"] == country_alpha3]
chart_data = dfA[["produksi", "tahun"]] #dari chart data dalam csv, diambil tahun dan produksinya saja untuk grafik
chart_data = chart_data.rename(columns={'tahun':'x'}).set_index('x') #Tahun dijadikan sebagai sumbu-x grafik
st.line_chart(chart_data)

#B: Grafik yang menunjukan B-besar negara dengan jumlah produksi terbesar pada tahun T
B = st.number_input("Jumlah Negara Yang Ingin Dicari",1)
T = st.slider('Tahun Yang Ingin Dicari', year_min, year_max, key = "lala") #Digunakan slider untuk menentukan tahun yang akan dipilih
st.info(str(B)+" Negara dengan Jumlah Produksi Minyak Mentah Terbesar pada Tahun "+str(T))
df2 = df.loc[df['tahun'] == T]
dfB = df2.sort_values(by='produksi', ascending = False) #Disort dari data terbesar ke terkecil
dfB = dfB[:B] #Di ambil B (banyak negara) terbesar 
dfB = dfB[['kode_negara', 'produksi']]
chart_data = dfB.rename(columns={'kode_negara':'x'}).set_index('x') #kode negara dijadikan sumbu-x dalam grafik
st.bar_chart(chart_data)

#C: Grafik yang menunjukan B-besar negara dengan jumlah produksi terbesar secara kumulatif keseluruhan tahun
B2 = st.number_input("Jumlah Negara Yang Ingin Dicari",1,key="lele")
st.info(str(B2)+ " Negara dengan Jumlah Produksi Minyak Mentah Kumulatif Terbesar")
df3 = df.groupby('kode_negara').sum()
df3 = df3.sort_values(by='produksi', ascending = False)
dfC = df3[:B2]
dfC = dfC['produksi']
chart_data = dfC
st.bar_chart(chart_data)

#D
#D.1. Highest all -> Jumlah produksi tertinggi pada keseluruhan tahun
st.info("Informasi Produsen Minyak Mentah Terbesar Kumulatif")
df4 = df.groupby('kode_negara', as_index=False).sum()
df4 = df4.sort_values(by='produksi', ascending = False)
df4 = df4[:1] #Diambil data tertingginya
df4 = df4[['kode_negara', 'produksi']]
curr_code = df4.iloc[0,0]

#Menampilkan negara yang memiliki jumlah produksi minyak terbesar pada keseluruhan tahun
for country in country_list:
    if country[1] == curr_code: 
        st.write("Negara      : "+country[0])
        st.write("Kode Negara : "+country[4])
        st.write("Region      : "+country[2])
        st.write("Sub-Region  : "+country[3])
st.write('Total Produksi : '+str(df4.iloc[0,1]))

#D.2. Lowest all -> Jumlah produksi terendah pada keseluruhan tahun
st.info("Informasi Produsen Minyak Mentah Terkecil Kumulatif")
df5 = df.groupby('kode_negara', as_index=False).sum()
df5 = df5.loc[df5["produksi"] > 0] #Mencari yang produksinya lebih dari 0
df5 = df5.sort_values(by='produksi', ascending = True) #Disort dari data terkecil ke terbesar
df5 = df5[:1] #Di ambil data terkecilnya
df5 = df5[['kode_negara', 'produksi']]
curr_code = df5.iloc[0,0]

#Menampilkan negara yang memiliki jumlah produksi minyak terkecil pada keseluruhan tahun
for country in country_list:
    if country[1] == curr_code:
        st.write("Negara      : "+country[0])
        st.write("Kode Negara : "+country[4])
        st.write("Region      : "+country[2])
        st.write("Sub-Region  : "+country[3])
st.write('Total Produksi : '+str(df5.iloc[0,1]))

#D.3. Highest in a year -> Jumlah produksi tertinggi pada tahun T
B3 = st.slider('Pilih tahun yang diinginkan untuk melihat produsen terbesar/terkecil minyak mentah!', year_min, year_max, key = "biga")
st.info("Informasi Produsen Minyak Mentah Terbesar pada Tahun " + str(B3))
df6 = df.loc[df["tahun"] == B3]
df6 = df6.loc[df6["produksi"] > 0]
df6 = df6.sort_values(by='produksi', ascending = False)
df6 = df6[:1]
df6 = df6[['kode_negara', 'produksi']]
curr_code = df6.iloc[0,0]

#Menampilkan negaranya
for country in country_list:
    if country[1] == curr_code:
        st.write("Negara      : "+country[0])
        st.write("Kode Negara : "+country[4])
        st.write("Region      : "+country[2])
        st.write("Sub-Region  : "+country[3])
st.write('Total produksi : '+str(df6.iloc[0,1]))

#D.4. Lowest in a year -> Jumlah produksi terendah pada tahun T
st.info("Informasi Produsen Minyak Mentah Terkecil pada Tahun " + str(B3))
df7 = df.loc[df["produksi"] > 0]
df7 = df7.loc[df["tahun"] == B3]
df7 = df7.sort_values(by='produksi', ascending = True)
df7 = df7[:1]
df7 = df7[['kode_negara', 'produksi']]
curr_code = df7.iloc[0,0]

#Menampilkan negaranya
for country in country_list:
    if country[1] == curr_code:
        st.write("Negara      : "+country[0])
        st.write("Kode Negara : "+country[4])
        st.write("Region      : "+country[2])
        st.write("Sub-Region  : "+country[3])
st.write('Total Produksi : '+str(df7.iloc[0,1]))

#D.5. ZeroProdInAYear -> Jumlah produksi sama dengan nol pada tahun T
st.info("Informasi Negara Yang Tidak Memproduksi Minyak Mentah pada Tahun "+ str(B3))
df10 = df.loc[df["produksi"] == 0] #untuk mencari yang memiliki jumlah produksi 0
df10 = df10.loc[df10["tahun"] == B3] #disesuaikan dengan tahun berapa yang dipilih user
code_list = df10['kode_negara'].tolist() 
zeroAT_list = [] #membuat list baru untuk negara yang memiliki jumlah produksi 0
for code in code_list:
    for country in country_list:
        if country[1] == code:
            zeroAT_list.append([country[0], country[4], country[2], country[3]])
df11 = pd.DataFrame(zeroAT_list, columns=['Negara','Kode Negara','Region','Sub-Region']) #Membuat data frame berisikan negara, kode, region, subregion
st.table(df11) #Menampilkan df11 dalam bentuk tabel

#D.6. ZeroProdAllTime -> Jumlah produksi sama dengan nol pada keseluruhan tahun
st.info("Informasi Negara Yang Tidak Memproduksi Minyak Mentah Secara Keseluruhan")
df8 = df.groupby('kode_negara', as_index=False).sum() #untuk negara yang di seluruh tahun jumlah produksinya 0
df8 = df8.loc[df8["produksi"] == 0]
code_list = df8['kode_negara'].tolist()
zeroAT_list = []
for code in code_list:
    for country in country_list:
        if country[1] == code:
            zeroAT_list.append([country[0], country[4], country[2], country[3]])
df9 = pd.DataFrame(zeroAT_list, columns=['Negara','Kode Negara','Region','Sub-Region']) #Membuat data frame berisikan negara, kode, region, subregion
st.table(df9) #Menampilkan df9 dalam bentuk tabel
