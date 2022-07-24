from lib import os,join,basename,dirname,sys
from lib import pd,np,plt,warnings
from lib import sns,folium
warnings.filterwarnings(action='ignore')
plt.rc('font',family='AppleGothic')

def plots(stay,data1,data2,data3,data4,title:str,x:str,y:str,legend:list):
    plt.figure(figsize=(15,8))
    plt.plot(stay,data1)
    plt.plot(stay,data2)
    plt.plot(stay,data3,'-')
    plt.plot(stay,data4,'-o')
    plt.title(title,fontsize=20)
    plt.grid()
    plt.xlabel(x,fontsize=16)
    plt.ylabel(y,fontsize=16)
    plt.xticks(fontsize=8,rotation=45)
    plt.legend(legend,fontsize=10)
    plt.show()


def barplot_h(data, y:str, x:str, str_color:str):
    print('Head',data.head(),sep='\n')
    print('Info',data.info(),sep='\n')
    print('Shape',data.shape)
    plt.figure(figsize=(15,8))
    plt.barh(data[y],data[x]
    ,label = x,align='center',linewidth = 10)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.grid()
    plt.legend()
    plt.title(x+"별 "+y)
    for i,v in enumerate(data[y]):
        str_val = data[x][i]
        plt.text(data[x][i],v,str_val,fontsize=9,color=str_color,
        horizontalalignment = 'left',verticalalignment = 'center',fontweight = 'bold')
    plt.show()


def sns_lineplot(data, y:str, x:str,hue,title:str):
    if hue == 0:
        print('Head',data.head(),sep='\n')
        print('Info',data.info(),sep='\n')
        print('Shape',data.shape)
        plt.figure(figsize=(14,7))
        plt.grid()
        plt.xticks(rotation=90)
        plt.title(title,fontsize=20)
        plt.xlabel(x,fontsize=15)
        plt.ylabel(y,fontsize=15)
        sns.lineplot(data=data,x=x,y=y)
        plt.show()
    else:
        print('Head',data.head(),sep='\n')
        print('Info',data.info(),sep='\n')
        print('Shape',data.shape)
        plt.figure(figsize=(14,7))
        plt.grid()
        plt.xticks(rotation=60)
        plt.title(title,fontsize=20)
        plt.xlabel(x,fontsize=15)
        plt.ylabel(y,fontsize=15)
        sns.lineplot(data=data,x=x,y=y,hue=hue)
        plt.show()

def sns_barplot(data,y:str,x:str,title:str):
    print('Head',data.head(),sep='\n')
    print('Info',data.info(),sep='\n')
    print('Shape',data.shape)
    plt.figure(figsize=(15,7))
    plt.grid()
    plt.title(title,fontsize=30)
    plt.xlabel(x, fontsize=20)
    plt.ylabel(y, fontsize=20)
    sns.barplot(data=data, x=x, y=y)
    plt.show()

def folium_polyline_coords(data,x:str,y:str,a:str,b:str,c:str,savepath,savename:str,color):
    lists = []
    for n in data.index:
        points = (data.loc[n,x],data.loc[n,y])
        lists.append(points)

    draw_map = folium.Map(location=[data[x].mean(), data[y].mean()], zoom_start=11)

    for n in data.index:
        folium.Marker(location=[data.loc[n, x], data.loc[n, y]],popup=data.loc[n, a]+" : "+
                    data.loc[n, b]+","+data.loc[n, c]).add_to(draw_map)
    lists = []
    for n in data.index:
        points = (data.loc[n, x], data.loc[n, y])
        lists.append(points)
        
    folium.PolyLine(lists,color=color).add_to(draw_map)
    draw_map.save(join(savepath,savename+'.html'))

if __name__ == '__main__':
    # root = sys.argv[1]
    root = r'/Users/dongjin/Documents/GitHub/COVID-19/data'
    save_root = join(dirname(root),'Vis')
    os.makedirs(save_root,exist_ok=True)

    region = pd.read_csv(join(root,"Region.csv"))
    timeprovince = pd.read_csv(join(root,"TimeProvince.csv"))
    timegender = pd.read_csv(join(root,"TimeGender.csv"))
    timeage = pd.read_csv(join(root,"TimeAge.csv"))
    time = pd.read_csv(join(root,"Time.csv"))
    patientinfo = pd.read_csv(join(root,"PatientInfo.csv"))
    patientroute = pd.read_csv(join(root,"PatientRoute.csv"))
    case = pd.read_csv(join(root,"Case.csv"))
    search_trend =pd.read_csv(join(root,'SearchTrend.csv'))
    weather = pd.read_csv(join(root,"Weather.csv"))

    Search=search_trend['date']
    Search1Year=Search[1385:]
    SearchC=search_trend['cold']
    SearchCold=SearchC[1385:]
    SearchF=search_trend['flu']
    SearchFlu=SearchF[1385:]
    SearchP=search_trend['pneumonia']
    SearchPneumonia=SearchP[1385:]
    SearchCorona=search_trend['coronavirus']
    SearchCoronavirus=SearchCorona[1385:]

    plots(Search1Year,SearchCold,SearchFlu,SearchPneumonia,SearchCoronavirus,'검색추이','날짜','검색량',['감기','발열','폐렴','코로나바이러스'])    


    case.columns = ['환자번호','시도','구군','집단감염여부','집단감염장소','확진자누적수','위도','경도']
    
    data_location = pd.DataFrame(case.groupby(['집단감염장소'])['확진자누적수'].max())
    data_location = data_location.sort_values(by=['집단감염장소'], ascending = True).reset_index()
    barplot_h(data_location,'집단감염장소','확진자누적수','Red')


    time.columns = ['날짜','시간','검사자누적숫자','음성누적숫자','양성누적숫자','완치누적숫자','사망누적숫자']
    data_test = time.pivot_table(index='날짜',values='검사자누적숫자',aggfunc=np.sum).reset_index()
    sns_lineplot(data_test,'검사자누적숫자','날짜',0,'날짜별 검사자 누적수')
    
    data_neg = time.groupby(['날짜'])['음성누적숫자'].max().reset_index()
    sns_lineplot(data_neg,'음성누적숫자','날짜',0,'날짜별 음성 누적수')
    
    data_pos = time.groupby(['날짜'])['양성누적숫자'].max().reset_index()
    sns_lineplot(data_pos,'양성누적숫자','날짜',0,'날짜별 양성 누적수')

    data_rel = time.groupby(['날짜'])['완치누적숫자'].max().reset_index()
    sns_lineplot(data_rel,'완치누적숫자','날짜',0,'날짜별 완치 누적수')

    data_dec = time.groupby(['날짜'])['사망누적숫자'].max().reset_index()
    sns_lineplot(data_dec,'사망누적숫자','날짜',0,'날짜별 사망 누적수')

    plt.figure(figsize=(15,7))
    plt.plot(time['날짜'], time['양성누적숫자'], color='red')
    plt.plot(time['날짜'], time['완치누적숫자'], color='green')
    plt.plot(time['날짜'], time['사망누적숫자'], color='black')
    plt.xticks(rotation=90, size=10)
    plt.yticks(size=13)
    plt.grid()
    plt.xlabel('날짜', fontsize=20)
    plt.ylabel('누적숫자', fontsize=20)
    plt.legend(['양성','완치','사망자'], loc='best', fontsize=20)
    plt.title('Corona_Virus 진단별 누적 숫자 추이', size=30)
    plt.show()



    timeage = timeage.drop(['time'],axis=1)
    timeage.columns = ['날짜','연령대','확진자누적수','사망자누적수']

    timeage['날짜'] = pd.to_datetime(timeage['날짜'])
    timeage.loc[timeage['연령대'] == '0s', '연령대'] = '0세이상 10세미만'
    timeage.loc[timeage['연령대'] == '10s', '연령대'] = '10세이상 20세미만'
    timeage.loc[timeage['연령대'] == '20s', '연령대'] = '20세이상 30세미만'
    timeage.loc[timeage['연령대'] == '30s', '연령대'] = '30세이상 40세미만'
    timeage.loc[timeage['연령대'] == '40s', '연령대'] = '40세이상 50세미만'
    timeage.loc[timeage['연령대'] == '50s', '연령대'] = '50세이상 60세미만'
    timeage.loc[timeage['연령대'] == '60s', '연령대'] = '60세이상 70세미만'
    timeage.loc[timeage['연령대'] == '70s', '연령대'] = '70세이상 80세미만'
    timeage.loc[timeage['연령대'] == '80s', '연령대'] = '80세이상'


    timeage['날짜'] = timeage['날짜'].astype(str)
    age_max = timeage.loc[timeage['날짜'] == '2020-03-20'].reset_index(drop=True)

    barplot_h(age_max,'연령대','확진자누적수','red')
    barplot_h(age_max,'연령대','사망자누적수','red')

    timegender.columns = ['날짜','시간','성별','확진자누적수','사망자누적수']
    sns_lineplot(timegender,'확진자누적수','날짜','성별','성별에따른 날짜별 확진자 누적수')
    sns_lineplot(timegender,'사망자누적수','날짜','성별','성별에따른 날짜별 사망자 누적수')


    data = patientinfo.copy()
    data['contact_number'] = data['contact_number'].fillna(0)

    data_infection = data.loc[data['contact_number'] >= 16].reset_index(drop=True)
    columns = ['sex','age','country','province','city','infection_case','contact_number','confirmed_date','released_date']
    data_infection = data_infection.loc[:,columns]
    data_infection.columns = ['성별','연령','국적','시도','구군','감염장소','접촉자수','확진날짜','퇴원날짜']

    data_infection['연령'] = data_infection['연령'].fillna('unknown')
    data_infection.loc[data_infection['연령'] == 'unknown']
    data_infection = data_infection.loc[data_infection['연령'].str.contains('10s|20s|30s|40s|50s|60s|70s')]

    data_infection.loc[data_infection['연령'] == '10s', '연령'] = '10세이상 20세미만'
    data_infection.loc[data_infection['연령'] == '20s', '연령'] = '20세이상 30세미만'
    data_infection.loc[data_infection['연령'] == '30s', '연령'] = '30세이상 40세미만'
    data_infection.loc[data_infection['연령'] == '40s', '연령'] = '40세이상 50세미만'
    data_infection.loc[data_infection['연령'] == '50s', '연령'] = '50세이상 60세미만'
    data_infection.loc[data_infection['연령'] == '60s', '연령'] = '60세이상 70세미만'
    data_infection.loc[data_infection['연령'] == '70s', '연령'] = '70세이상 80세미만'
    data_infection.loc[data_infection['연령'] == '80s', '연령'] = '80세이상'
    
    sns_barplot(data_infection,'접촉자수','연령','연령별 접촉자수')

    data_route = patientroute.copy()
    data_route.columns = ['환자번호','global_num','날짜','시도','구군','type','위도','경도']
    data_route['환자번호'] = data_route['환자번호'].astype(str)

    '''
    가장 많이 돌아다닌 확진자 상위 5명 환자번호 id 
    3009000014    42
    1400000021    38
    3009000013    37
    1100000069    35
    3009000003    33
    '''
    print(data_route['환자번호'].value_counts())

    data_route_many = data_route.loc[data_route['환자번호'].str.contains('3009000014|1400000021|3009000013|1100000069|3009000003')]
    
    data_route_max = data_route_many.loc[data_route_many['환자번호'] == '3009000014']
    data_route_max = data_route_max.reset_index(drop=True)
    geo_data_1st = data_route_max
    folium_polyline_coords(geo_data_1st,'위도','경도','날짜','시도','구군',save_root,'1순위','red')
    
    data_route_2nd = data_route_many.loc[data_route_many['환자번호'] == '1400000021']
    data_route_2nd = data_route_2nd.reset_index(drop=True)
    geo_data_2nd = data_route_2nd
    folium_polyline_coords(geo_data_2nd,'위도','경도','날짜','시도','구군',save_root,'2순위','red')

    data_route_3rd = data_route_many.loc[data_route_many['환자번호'] == '3009000013']
    data_route_3rd = data_route_3rd.reset_index(drop=True)
    geo_data_3rd = data_route_3rd
    folium_polyline_coords(geo_data_3rd,'위도','경도','날짜','시도','구군',save_root,'3순위','red')

    data_route_4th = data_route_many.loc[data_route_many['환자번호'] == '1100000069']
    data_route_4th = data_route_4th.reset_index(drop=True)
    geo_data_4th = data_route_4th
    folium_polyline_coords(geo_data_4th,'위도','경도','날짜','시도','구군',save_root,'4순위','red')

    data_route_5th = data_route_many.loc[data_route_many['환자번호'] == '3009000003']
    data_route_5th = data_route_5th.reset_index(drop=True)
    geo_data_5th = data_route_5th
    folium_polyline_coords(geo_data_5th,'위도','경도','날짜','시도','구군',save_root,'5순위','red')

    

    geo_data = data_route_many
    map_all = folium.Map(location=[geo_data['위도'].mean(), geo_data['경도'].mean()], zoom_start=8)

    for n in geo_data.index:
        # 1위:파란색, 2위:빨간색, 3위:초록색, 4위:오렌지색, 5위:검정색
        if geo_data.loc[n, '환자번호'] == '3009000014':
            icon_color = 'blue'
        elif geo_data.loc[n, '환자번호'] == '1400000021':
            icon_color = 'red'
        elif geo_data.loc[n, '환자번호'] == '3009000013':
            icon_color = 'green'
        elif geo_data.loc[n, '환자번호'] == '1100000069':
            icon_color = 'orange'
        elif geo_data.loc[n, '환자번호'] == '3009000003':
            icon_color = 'black'

        folium.CircleMarker(location=[geo_data.loc[n, '위도'], geo_data.loc[n, '경도']],
                    popup="환자번호 :"+geo_data.loc[n, '환자번호']+" - 날짜:"+geo_data.loc[n, '날짜']+' 시도 :'+geo_data.loc[n, '시도']+
                            " 구군 :"+geo_data.loc[n, '구군'], color=icon_color, fill_color=icon_color, fill=True,
                        radius=9).add_to(map_all)

    lists1 = []
    for n in data_route_max.index:
        points = (data_route_max.loc[n, '위도'], data_route_max.loc[n, '경도'])
        lists1.append(points)
    folium.PolyLine(lists1, color='blue').add_to(map_all)

    lists2 = []
    for n in data_route_2nd.index:
        points = (data_route_2nd.loc[n, '위도'], data_route_2nd.loc[n, '경도'])
        lists2.append(points)
        
    folium.PolyLine(lists2, color='red').add_to(map_all)

    lists3 = []
    for n in data_route_3rd.index:
        points = (data_route_3rd.loc[n, '위도'], data_route_3rd.loc[n, '경도'])
        lists3.append(points)

    folium.PolyLine(lists3, color='green').add_to(map_all)

    lists4 = []
    for n in data_route_4th.index:
        points = (data_route_4th.loc[n, '위도'], data_route_4th.loc[n, '경도'])
        lists4.append(points)

    folium.PolyLine(lists4, color='orange').add_to(map_all)

    lists5 = []
    for n in data_route_5th.index:
        points = (data_route_5th.loc[n, '위도'], data_route_5th.loc[n, '경도'])
        lists5.append(points)

    folium.PolyLine(lists5, color='black').add_to(map_all)

    map_all.save(join(save_root,'all.html'))