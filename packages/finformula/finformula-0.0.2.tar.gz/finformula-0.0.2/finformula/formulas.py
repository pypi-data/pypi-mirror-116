# -*-coding:utf-8-*-
import numpy as np
import pandas as pd
from scipy.stats import norm
import statsmodels.formula.api as smf
from dateutil.relativedelta import relativedelta
pd.options.mode.chained_assignment = None
from sqlalchemy import create_engine
import pymssql
import datetime


class FinancialFormulas:
    @staticmethod
    def f_MaxDD(R):
        accum_R = np.multiply.accumulate(np.array(R) + 1)
        max_R = [accum_R[:i].max() for i in range(1, len(accum_R) + 1)]
        #     max_R = pd.Series(accum_R).rolling(len(accum_R), min_periods=1).max()
        if max_R[0] < 1:
            max_R[0] = 1
        f_max = (1 - (accum_R / max_R)).max()
        return f_max

    @staticmethod
    def f_RestorePeriod(R, D):
        dates = pd.to_datetime(D)
        accum_R = np.multiply.accumulate(np.array(R) + 1)
        max_R = [accum_R[:i].max() for i in range(1, len(accum_R) + 1)]
        if max_R[0] < 1:
            max_R[0] = 1
        idx = (1 - (accum_R / max_R)).argmax()
        date_diff = (dates[idx + 1:][accum_R[idx + 1:] > max_R[idx + 1]].min() - dates[idx]).days
        return date_diff

    @staticmethod
    def f_vol(R):
        return np.std(R, ddof=1)

    @staticmethod
    def f_AnnVol(R, ReturnStep):
        std = np.std(R, ddof=1)
        sqrt_ls = [*map(np.sqrt, [250, 52, 12, 4, 1])]
        step_sqrt_map = dict(zip([*range(1, 6)], sqrt_ls))
        return std * step_sqrt_map[ReturnStep]

    @staticmethod
    def f_DownsideRisk(R, Rf):
        diff = np.array(R) - np.array(Rf)
        res = np.sqrt(np.square(np.where(diff < 0, 0, diff)).sum() / len(diff))
        return res

    @staticmethod
    def f_VaR(R, CI, T):
        return -(np.array(R).mean() * T - norm.ppf(CI) * np.std(R, ddof=1) * np.sqrt(T))

    @staticmethod
    def f_Beta(R, Rb):
        var = np.var(np.array(Rb), ddof=1)
        cov = np.cov(np.array(R), np.array(R), ddof=1)[0][1]
        return cov / var

    @staticmethod
    def f_TrackError(R, Rb):
        return np.std(np.array(R) - np.array(Rb), ddof=1)

    @staticmethod
    def f_AnnReturn(R, ReturnStep):
        rt_ls = np.array([250, 52, 12, 4, 1]) / len(R)
        step_rt_map = dict(zip([*range(1, 6)], rt_ls))
        res = np.power(np.prod(1 + np.array(R)), step_rt_map[ReturnStep]) - 1
        return res

    @staticmethod
    def f_Sharpe(R, Rf):
        return (np.array(R).mean() - np.array(Rf).mean()) / np.std(R, ddof=1)

    @classmethod
    def f_Jensen(cls, R, Rb, Rf):
        R, Rb, Rf = [*map(np.array, [R, Rb, Rf])]
        return R.mean() - (Rf.mean() + cls.f_Beta(R, Rb) * (Rb.mean() - Rf.mean()))

    @classmethod
    def f_Treynor(cls, R, Rb, Rf):
        R, Rb, Rf = [*map(np.array, [R, Rb, Rf])]
        return (R.mean() - Rf.mean()) / cls.f_Beta(R, Rb)

    @classmethod
    def f_Sortino(cls, R, Rf):
        return (np.array(R).mean() - np.array(Rf).mean()) / cls.f_DownsideRisk(R, Rf)

    @classmethod
    def f_Calmar(cls, R, T):
        return cls.f_AnnReturn(R, T) / cls.f_MaxDD(R)

    @staticmethod
    def f_InfoRatio(R, Rb):
        diff = np.array(R) - np.array(Rb)
        return diff.mean() / np.std(diff, ddof=1)

    @staticmethod
    def f_TM(R, Rb, Rf):
        R, Rb, Rf = [*map(np.array, [R, Rb, Rf])]
        Y = R - Rf
        X = R - Rb
        df = pd.DataFrame({'Y': Y, 'X': X})
        results = smf.ols('Y ~ X + I(X**2)', data=df).fit()
        X_coef, X2_coef, X_p, X2_p = results.params[1], results.params[2], results.pvalues[1], \
                                     results.pvalues[2]
        return [X_coef, X2_coef, X_p, X2_p]

    @staticmethod
    def f_GainProb(R, ReturnStep, D):
        D = pd.to_datetime(D)
        accum_R = np.multiply.accumulate(np.array(R) + 1)
        D_R_map = dict(zip(D, accum_R))
        df = pd.DataFrame({'D': D, 'R': R, 'accum_R': accum_R})
        delta_map = dict(zip([2, 3, 4, 5],
                             [relativedelta(weeks=1), relativedelta(months=1),
                              relativedelta(months=3), relativedelta(years=1)]))
        if ReturnStep == 1:
            result = np.where(np.array(R) > 0, 1, 0).sum() / len(R)
            return result
        else:
            df['begin_date'] = df['D'].apply(
                lambda x: df['D'][df['D'] <= x - delta_map[ReturnStep]].max())
            df['new_accum_R'] = df['begin_date'].apply(
                lambda x: D_R_map[x] if x in D_R_map else np.nan)
            df['return'] = df['accum_R'] / df['new_accum_R'] - 1
            df['label'] = df['return'].apply(lambda x: 1 if x > 0 else 0)
            result = df.dropna()['label'].mean()
            return result


    @staticmethod
    def f_Capture(R, Rb, ReturnStep, D):
        def get_selected_df(R, Rb, ReturnStep, D):
            accum_R = np.multiply.accumulate(np.array(R) + 1)
            accum_Rb = np.multiply.accumulate(np.array(Rb) + 1)
            df = pd.DataFrame(
                {'R': R, 'accum_R': accum_R, 'Rb': Rb, 'accum_Rb': accum_Rb,
                 'D': pd.to_datetime(D)})
            if ReturnStep == 1:
                df.columns = ['new_R', 'accum_R', 'new_Rb', 'accum_Rb', 'D']
                return df
            else:
                ls = []
                count = 0
                while True:
                    if ReturnStep == 2:
                        temp = df['D'].max() - relativedelta(weeks=count)
                    elif ReturnStep == 3:
                        temp = df['D'].max() - relativedelta(months=count)
                    elif ReturnStep == 4:
                        temp = df['D'].max() - relativedelta(months=3 * count)
                    elif ReturnStep == 5:
                        temp = df['D'].max() - relativedelta(years=count)
                    if temp >= df['D'].min():
                        ls.append(temp)
                        count += 1
                    else:
                        break
                new_ls = [
                    df['D'][np.where((df['D'] - ls[i]).dt.days >= 0, (df['D'] - ls[i]).dt.days,
                                     float('inf')).argmin()] for i in range(len(ls))]
                df['new_D'] = df['D'].apply(lambda x: x if x in new_ls else np.nan)
                selected_df = df[df['new_D'].notnull()]
                selected_df['new_R'] = selected_df['accum_R'].rolling(window=2, min_periods=2,
                                                                      axis=0).apply(
                    lambda x: x.tolist()[1] / x.tolist()[0] - 1)
                selected_df['new_Rb'] = selected_df['accum_Rb'].rolling(window=2, min_periods=2,
                                                                        axis=0).apply(
                    lambda x: x.tolist()[1] / x.tolist()[0] - 1)
                return selected_df

        def get_up_result(selected_df):
            selected_df['R_up'] = np.where(selected_df['new_Rb'] > 0, selected_df['new_R'],
                                           np.nan)
            selected_df['Rb_up'] = np.where(selected_df['new_Rb'] > 0, selected_df['new_Rb'],
                                            np.nan)
            selected_df = selected_df[selected_df['R_up'].notnull()]
            up_result = (np.power(np.prod(selected_df['R_up'] + 1),
                                  1 / len(selected_df)) - 1) / (
                                np.power(np.prod(selected_df['Rb_up'] + 1),
                                         1 / len(selected_df)) - 1)
            return up_result

        def get_down_result(selected_df):
            selected_df['R_down'] = np.where(selected_df['new_Rb'] < 0, selected_df['new_R'],
                                             np.nan)
            selected_df['Rb_down'] = np.where(selected_df['new_Rb'] < 0, selected_df['new_Rb'],
                                              np.nan)
            selected_df = selected_df[selected_df['R_down'].notnull()]
            down_result = (np.power(np.prod(selected_df['R_down'] + 1),
                                    1 / len(selected_df)) - 1) / (
                                  np.power(np.prod(selected_df['Rb_down'] + 1),
                                           1 / len(selected_df)) - 1)
            return down_result
        selected = get_selected_df(R, Rb, ReturnStep, D)
        up_result = get_up_result(selected)
        down_result = get_down_result(selected)
        return [up_result, down_result]

    @staticmethod
    def get_df_from_db(query, server, user, passwd, database):
        conn = pymssql.connect(server, user, passwd, database, charset="utf8")
        cursor = conn.cursor()  # 获取游标
        cursor.execute(query)
        column_names = [each_col[0] for each_col in list(cursor.description)]
        data = cursor.fetchall()
        result = pd.DataFrame(data, columns=column_names)
        return result

#
# if __name__ == '__main__':
#     R1 = "0.014523	-0.007157	0.009269	0.007143	-0.002026	-0.020305	0.001036	-0.004141	-0.019751	-0.007423	0.00641	0.009554	-0.014721	0.003202	0.017021	-0.001046	-0.004188	-0.012618	0.00213	-0.007439	0.006424	0.001064	0.008502	-0.015806	-0.010707	-0.003247	-0.008686	0.001095	-0.001094	0.005476	0.001089	-0.002176	-0.006543	0.007684	-0.010893	-0.006608	0.021064	0.009772	0.001075	0.001074	-0.002146	0.006452	-0.007479	0.012917	0.006376	-0.008448	0.00213	0.010627	-0.016824	0.005348	0.003191	-0.00106	-0.002123	0.001064	-0.008502	0.003215	0.017094	0.017857"
#     D1 = "2018/11/13	2018/11/14	2018/11/15	2018/11/16	2018/11/19	2018/11/20	2018/11/21	2018/11/22	2018/11/23	2018/11/26	2018/11/27	2018/11/28	2018/11/29	2018/11/30	2018/12/3	2018/12/4	2018/12/5	2018/12/6	2018/12/7	2018/12/10	2018/12/11	2018/12/12	2018/12/13	2018/12/14	2018/12/17	2018/12/18	2018/12/19	2018/12/20	2018/12/21	2018/12/24	2018/12/25	2018/12/26	2018/12/27	2018/12/28	2019/1/2	2019/1/3	2019/1/4	2019/1/7	2019/1/8	2019/1/9	2019/1/10	2019/1/11	2019/1/14	2019/1/15	2019/1/16	2019/1/17	2019/1/18	2019/1/21	2019/1/22	2019/1/23	2019/1/24	2019/1/25	2019/1/28	2019/1/29	2019/1/30	2019/1/31	2019/2/1	2019/2/11"
#     R1 = [*map(float, R1.split("\t"))]
#     D1 = D1.split("\t")
#     Rb1 = "-0.004931213	0.001635565	0.001708165	-0.007198801	0.009159226	-0.007416996	-0.00135816	-0.004871285	-0.003120715	0.002538814	0.028259176	-0.008821035	-0.004434023	-0.000630291	0.018722391	-0.00010674	-0.004684244	-0.013959471	-0.009071678	-0.007655289	-0.010520677	0.00095465	0.018021779	-0.002676145	-0.004978929	-0.002777771	-0.006044305	0.002989688	0.003356834	-0.005138891	-0.00082576	0.002864066	0.000802124	-0.006794977	0.002559764	0.002617719	-0.00149545	0.021121158	-0.000967376	0.010494577	0.000536826	-0.01432724	0.009649914	-0.006865713	-0.010294295	-0.001736117	-0.003638625	-0.002947571	0.002991725	0.017785255	0.005414017	-0.011406505	0.013367854	-0.012359307	0.0090682	-0.00183299	-0.011391523	0.000697362"
#     Rb1 = [*map(float, Rb1.split("\t"))]
#     print(FinancialFormulas.f_Capture(R1, Rb1, 2, D1))



