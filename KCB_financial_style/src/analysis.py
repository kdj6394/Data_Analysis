from lib import os,glob,sys,join,basename,dirname
from lib import np,pd,plt,sns
plt.rc('font',family='Malgun Gothic')
from lib import warnings
warnings.filterwarnings(action='ignore')
pd.set_option('display.float_format','{:.4f}'.format)

def sns_barh_hue(data:str,x:str,y:str,hue):
    plt.figure(figsize=(19.2,10.8))
    plt.grid()
    plt.title(y+' by '+x,fontsize=25)
    plt.xlabel(y,fontsize=20)
    plt.ylabel(x,fontsize=20)
    ax = sns.barplot(x=y,y=x,hue=hue,data=data)
    for p in ax.patches:
        ax.annotate("%.5f" % p.get_width(), xy=(p.get_width(), p.get_y()+p.get_height()/2),
                xytext=(0,0), textcoords='offset points', ha="left", va="center",color='red',fontweight='bold')
    fig = plt.gcf()
    return fig

def sns_facet_gride(data:str,col:str,hue:str,x:str,y:str):
    plt.figure(figsize=(19.2,10.8))
    ax = sns.FacetGrid(data, col=col,hue=hue, palette = 'RdBu_r', col_wrap=4, height=3,legend_out=True)
    ax.map(plt.plot, x, y, marker='o')
    ax.fig.tight_layout(w_pad=3)
    fig = plt.gcf()
    return fig

def sns_lineplot(x:str,y:str,hue:str,data:str,round_check:str):
    plt.figure(figsize=(19.2,10.8))
    ax = sns.lineplot(x=x,y=y,hue=hue,data=data,marker='o')
    ax.ticklabel_format(style='plain')
    plt.title(y +' by '+ x,fontsize=25)
    plt.xlabel(x,fontsize=20)
    plt.ylabel(y,fontsize=20)
    plt.legend()
    plt.grid()
    for i,v in enumerate(data[y]):
        if round_check == 'round':
            str_val = (int(data[x][i]),round(data[y][i],3))
        else:
            str_val = (int(data[x][i]),int(data[y][i]))
        plt.text(data[x][i],v,str_val,fontsize=10,horizontalalignment = 'left',verticalalignment = 'center',fontweight='bold')

    fig = plt.gcf()
    return fig

def corr_heatmap(corr_data,title,cmap):
    mask = np.zeros_like(corr_data, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    plt.figure(figsize=(19.2,10.8))
    plt.title(title,fontsize=25)
    sns.heatmap(corr_data,square=True,mask=mask,cmap=cmap
                ,annot=True,linewidths=1)
    fig = plt.gcf()
    return fig


if __name__ == '__main__':
    root = sys.argv[1]

    csv_name = 'jeju_financial_life_data.csv'
    csv_file = join(root,csv_name)
    img_save_path = join(dirname(root),'img')
    os.makedirs(img_save_path,exist_ok=True)

    data = pd.read_csv(csv_file,encoding='utf-8')

    # job_ratio,sex,age
    job_ratio = data[['job_majorc','job_smallc','job_public','job_profession','job_self'
                        ,'job_none','job_other']].groupby([data.sex,data.age,data.zip_cd]).mean().reset_index()
    job_ratio = job_ratio.sort_values('job_majorc',ascending=False)
    job_ratio_sex = data[['job_majorc','job_smallc','job_public','job_profession','job_self'
                            ,'job_none','job_other']].groupby([data.sex]).mean().reset_index()
    job_ratio_sex_table = job_ratio_sex.T.reset_index()
    job_ratio_sex_table.columns = ['job','male','female']
    job_ratio_sex_final = pd.melt(job_ratio_sex_table.iloc[1:,:],id_vars = 'job', var_name = 'sex', value_name = 'job_ratio')
    
    bar_fig = sns_barh_hue(data=job_ratio_sex_final,x='job',y='job_ratio',hue='sex')
    bar_fig.savefig(join(img_save_path,'job_ratio by job.png'),dpi=bar_fig.dpi,bbox_inches='tight', pad_inches=0.5)


    # sex&age, avg_income,avg_spend,avg_debt,avg_foreign_spend
    income_spend_debt = data[['avg_income','avg_spend','avg_debt','avg_foreign_spend']].groupby([data.age,data.sex]).mean().reset_index()
    income_spend_debt_table = pd.melt(income_spend_debt, id_vars=['sex','age'],value_vars=['avg_income','avg_spend',
                                'avg_debt','avg_foreign_spend'],value_name='avg')
    income_spend_debt_table.loc[income_spend_debt_table['sex'] == 1,'sex'] = 'male'
    income_spend_debt_table.loc[income_spend_debt_table['sex'] == 2,'sex'] = 'female'
    
    for variable_name in ['avg_income','avg_spend','avg_debt','avg_foreign_spend']:
        x_sex_age = income_spend_debt_table['variable'] == variable_name
        x_sex_age_table = pd.DataFrame(income_spend_debt_table[x_sex_age]).reset_index()
        x_sex_age_table.columns = ["index","sex","age","variable",variable_name]
        print(x_sex_age_table)
        x_fig = sns_lineplot(x='age',y=variable_name,hue='sex',data=x_sex_age_table,round_check='int')
        x_fig.savefig(join(img_save_path,'{}.png'.format(variable_name)),dpi=x_fig.dpi,bbox_inches='tight', pad_inches=0.5)

    # sex&age, all
    all_sex_age_fig = sns_lineplot(x='age',y='avg',hue='variable',data=income_spend_debt_table,round_check='int')
    all_sex_age_fig.savefig(join(img_save_path,'avg_all.png'),dpi=all_fig.dpi,bbox_inches='tight', pad_inches=0.5)


    # sex&age, medium_resid_rat,large_resid_rat,vehicle_own_rat
    visible = data[['medium_resid_rat','large_resid_rat','vehicle_own_rat']]
    visible = visible[visible.medium_resid_rat != -999999]
    visible = visible[visible.large_resid_rat != -999999]
    visible = visible.groupby([data.sex,data.age]).mean().reset_index()
    visible.loc[visible['sex'] == 1,'sex'] = 'male'
    visible.loc[visible['sex'] == 2,'sex'] = 'female'
    visible = pd.DataFrame(visible)

    for visible_name in ['medium_resid_rat','large_resid_rat','vehicle_own_rat']:
        x_visible = visible[['sex','age',visible_name]]
        print(x_visible)
        x_fig = sns_lineplot(x='age',y=visible_name,hue='sex',data=x_visible,round_check='round')
        x_fig.savefig(join(img_save_path,'{}.png'.format(visible_name)),dpi=x_fig.dpi,bbox_inches='tight', pad_inches=0.5)


    # all correlation
    all_corr = data.corr()
    all_corr_fig = corr_heatmap(all_corr,'All correlation','Spectral')
    all_corr_fig.savefig(join(img_save_path,'all_coreelation.png'),dpi=all_corr_fig.dpi)
