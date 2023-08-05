import pandas as pd
import numpy as np
from ...wrapper.mysql import ViewDatabaseConnector
from ...api.research_api import ResearchApi, DerivedDataApi
from ....util.calculator import *


fund_type_df = DerivedDataApi().get_fund_type_classification()
fund_type_df = pd.read_excel('/Users/huangkejia/Downloads/fund_type/公募私募策略分类.xlsx')
fund_type_df = fund_type_df[['公募or私募','一级分类','二级分类','合并一级分类','合并二级分类']]
fund_type_df = fund_type_df[fund_type_df['公募or私募'] == '私募']
fund_type_dic_1 = fund_type_df[['一级分类','合并一级分类']].drop_duplicates().set_index('一级分类')['合并一级分类'].to_dict()

fund_type_dic_2 = fund_type_df[['二级分类','合并二级分类']].drop_duplicates().set_index('二级分类')['合并二级分类'].to_dict()
research_api = ResearchApi()
fund_info = research_api.get_pf_info()
status = ['封闭运行','开放运行','正常']

fund_info = fund_info[fund_info.STATUS.isin(status)]

record_cds = fund_info.RECORD_CD.dropna().tolist()

col_dic = {
    'fund_id': 'fund_id',
    'start_date':'datetime',
    'cumu_ret':'history_ret',
    'annual_ret':'history_ret_annual',
    'recent_3m_annual_ret':'recent_3m_ret_annual',
    'recent_6m_annual_ret':'recent_6m_ret_annual',
    'y_last_ret_annual':'this_y_ret_annual',
    'recent_2y_annual_ret':'recent_2y_ret_annual',
    'last_year_ret':'this_y_ret',
    'recent_3m_ret':'recent_3m_ret',
    'recent_6m_ret':'recent_6m_ret',
    'recent_1y_ret':'recent_1y_ret',
    'recent_2y_ret':'recent_2y_ret',
    'annual_vol':'history_vol',
    'mdd':'history_mdd',
    'y_last_mdd':'this_y_mdd',
    'recent_3m_mdd':'recent_3m_mdd',
    'recent_6m_mdd':'recent_6m_mdd',
    'recent_1y_mdd':'recent_1y_mdd',
    'recent_2y_mdd':'recent_2y_mdd',
    'sharpe':'sharpe',
    'calmar':'calmar',
    'sortino':'sortino',
    'var':'var',
}

info_dic = {
    'fund_id':'fund_id',
    'desc_name':'desc_name',
    'fund_type_1':'fund_type_1',
    'fund_type_2':'fund_type_2'
}

fund_info_part = fund_info[['RECORD_CD','INVEST_STRATEGY','INVEST_STRATEGY_CHILD','SEC_FULL_NAME']]

fund_info_part = fund_info_part.rename(columns={'RECORD_CD':'fund_id','SEC_FULL_NAME':'desc_name'})

fund_info_part['fund_type_1'] = fund_info_part['INVEST_STRATEGY'].map(fund_type_dic_1)
fund_info_part['fund_type_2'] = fund_info_part['INVEST_STRATEGY_CHILD'].map(fund_type_dic_2)

fund_info_part = fund_info_part[info_dic.keys()].rename(columns=info_dic)
record_cds = fund_info_part.fund_id.dropna().tolist()
nav = pd.DataFrame()
ints = 500
for _i in range(0,len(record_cds),ints):
    try:
        df = research_api.get_pf_nav(record_cds=record_cds[_i:_i+ints], start_date=None, end_date=None)
        df = df.pivot_table(columns = "RECORD_CD"  , values = "ADJ_NAV" , index = "END_DATE")
        df.index = pd.to_datetime(df.index)
        df = df.resample('1W').mean()

        # 去除无净值的数据
        df = df.dropna(axis=0,how='all') 

        for n in df.columns:
        # 去除近期无更新的数据
            if len(df[n][-6:].dropna())<1:
                df.drop(columns=n,inplace=True)
            else:
                pass

        df = df.ffill() 
        for n in df.columns:
            if round(df[n].pct_change().max(),6) == round(df[n].pct_change().min(),6):
                df.drop(columns = n, inplace = True)
            else:
                pass

        # 去除中间pet_change=0超过6周的数据
        for n in df.columns:
            t = df[n].pct_change()[1:] != 0
            loc = t[t==True].index[0]
            max_ = df[n].pct_change()[loc:].rolling(6).max().round(6)==0
            min_ = df[n].pct_change()[loc:].rolling(6).min().round(6)==0

            break_flag = False
            for i in range(len(max_)):
                if (max_[i]==min_[i]==True)==True:
                    break_flag = True
                    df.drop(columns=n,inplace=True)
                    break
                if break_flag == True:
                    break
        fund_nav = pd.concat([nav,df], axis=1)
        res = []
        for fund_id in fund_nav:
            df = fund_nav[[fund_id]].dropna()
            dic = CalculatorBase.get_stat_result(dates=df.index,values=df[fund_id].values)
            dic['fund_id'] = fund_id
            res.append(dic)
        result_df = pd.DataFrame(res)
        result_df = result_df[col_dic.keys()].rename(columns=col_dic)
        result = pd.merge(result_df,fund_info_part,on='fund_id')
        result.to_sql('pf_fund_daily_collection', ViewDatabaseConnector().get_engine(), index = False, if_exists = 'append')
        print(f'finish i {_i}')
    except:
        print(f'boom i {_i}')