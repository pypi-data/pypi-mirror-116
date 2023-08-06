import re
import os
import glob

import logging
from logging.handlers import RotatingFileHandler #
import colorlog # 控制台日志输入颜色

# import pandas as pd
# import numpy as np

def process_index(k):
    lst=k.split("|")
    return tuple((lst[-1],"".join(lst[0:-1])))

def equal_df(df):
    # print(df.shape, len(df))
    for i in range(len(df)):
        pass

def astype_str_notna(df):
    '''
    传入参数：数据框里面一列  Series
    return：转换后的一列  Series
    '''
    import pandas as pd
    import numpy as np
    t = []
    for i in df:
        if type(i) == float:
            if not np.isnan(i):
                i = str(int(i))
        if type(i) == int:
            i = str(i)

        t.append(i)
    return pd.Series(t)

# import logging
# import os
# from logging.handlers import RotatingFileHandler #
# import colorlog # 控制台日志输入颜色

log_colors_config = {
  'DEBUG': 'blue',
  'INFO': 'yellow',
  'WARNING': 'cyan',
  'ERROR': 'red',
  'CRITICAL': 'bold_red',
}

def xlsx_to_xls(parent_path,out_path):
    import win32com.client as win32
    fileList=os.listdir(parent_path)  #文件夹下面所有的文件
    num=len(fileList)
    for i in range(num):
        file_Name=os.path.splitext(fileList[i])   #文件和格式分开
        if file_Name[1]=='.xlsx':
            tranfile1=parent_path+'\\'+fileList[i]  #要转换的excel
            tranfile2=out_path+'\\'+file_Name[0]    #转换出来excel
            excel=win32.gencache.EnsureDispatch('excel.application')
            pro=excel.Workbooks.Open(tranfile1)   #打开要转换的excel
            pro.SaveAs(tranfile2+".xls",FileFormat=56)  #另存为xls格式
            # pro.Close()
            # excel.Application.Quit()

def xls_to_xlsx(parent_path,out_path):
    import win32com.client as win32
    fileList=os.listdir(parent_path)  #文件夹下面所有的文件
    num=len(fileList)
    for i in range(num):
        file_Name=os.path.splitext(fileList[i])   #文件和格式分开
        if file_Name[1]=='.xls':
            tranfile1=parent_path+'\\'+fileList[i]  #要转换的excel
            tranfile2=out_path+'\\'+file_Name[0]    #转换出来excel
            excel=win32.gencache.EnsureDispatch('excel.application')
            pro=excel.Workbooks.Open(tranfile1)   #打开要转换的excel
            pro.SaveAs(tranfile2+".xlsx",FileFormat=51)  #另存为xls格式
            pro.Close()
            excel.Application.Quit()

class Log:
    def __init__(self, logname='log.log'):
        self.logname = os.path.join(os.getcwd(), '%s' % logname)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.formatter = colorlog.ColoredFormatter(
            '%(log_color)s[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s',
            log_colors=log_colors_config) # 日志输出格式
        self.info_formatter = colorlog.ColoredFormatter(
            '%(log_color)s [%(levelname)s]- %(message)s',log_colors=log_colors_config) # 日志输出格式

    def console(self, level, message):
    # 创建一个FileHandler，用于写到本地
        fh = logging.handlers.TimedRotatingFileHandler(self.logname, when='MIDNIGHT', interval=1, encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        # 创建一个StreamHandler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.info_formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        fh.close() # 关闭打开的文件

    def debug(self, message):
        self.console('debug', message)

    def info(self, message):
        self.console('info', message)

    def warning(self, message):
        self.console('warning', message)

    def error(self, message):
        self.console('error', message)

def export_dfs_to_xls(d,xls_file_dst,sht):
    if d is not None and d.shape[0]>0:
        d.to_excel(xls_file_dst, sheet_name=sht)

def find_total_row(df,str_xj="小计"):
    row=df.shape[0]
    row=max(-1 * row,-8)

    for i in range(-1,row,-1):
        if df.iloc[i, 0:-2].astype(str).str.contains(str_xj, na=False).any():
            return i
    return 0

def xls_auto_skip_rows(xls_file_src,match_sht_name_str=r"^\d{4}\.[\dz]{1,2}"):
    import pandas as pd
    import numpy as np
    import os

    io=pd.io.excel.ExcelFile(xls_file_src)
    dfs = pd.read_excel(io, sheet_name=None, header=None, index_col=None, skiprows=None)
    df_merge = pd.DataFrame(data=None, columns=["姓名", "年级", "合计"])
    df_concat = pd.DataFrame(data=None, columns=[])
    df_tail_dict_drop= {}
    basename_xls=os.path.basename(xls_file_src)

    lg.debug("\n%s\n当前操作的工作簿为:%s\n%s" % ('-'*100,xls_file_src,'-'*100))
    for sht_name, df in dfs.items():
        # 仅仅读取 XXXX.XX格式的工作表
        if re.match(match_sht_name_str, sht_name):
            lg.debug("{:>25} ==> {:<10} : is checking".format(basename_xls,sht_name))
            # first_row = (df.count(axis=1) >= df.shape[1]).idxmax()                #查找列名所在行数的一种方法，处理10,11月份没有问题，9月份出现问题
            first_row = (df.count(axis=1) >= df.count(axis=1).max()).idxmax()  # 查找列名所在行数的另一种办法
            df.columns = df.loc[first_row]  # 更改当前df的列索引名称
            df.rename(columns=lambda x: str(x).strip("\r\n\t ."), inplace=True)  # 去掉列名首位的空白字符
            df = df.loc[first_row + 1:]
            df=df.apply(lambda x:x.str.strip("\r\n\t .") if x.name=="姓名" else x)    # 去掉列中的空白字符

            row_total=find_total_row(df,"小计")        #定位最后几行中,小计所在行
            if row_total < -1:
                row_tail_drop = row_total * -1 - 1          #准备删除小计行以下的所有行
                # lg.debug("has drop these last row ：{}".format(df.tail(row_tail_drop).index))
                df_tail_dict_drop[sht_name]=df.tail(row_tail_drop)          #将小计行以下的所有行保存到字典中以备查证
                df=df.drop(df.tail(row_tail_drop).index)
            else:
                row_tail_drop = 0

            #检查该列是否存在重复值，如果存在则进行输出。
            if df.duplicated("姓名", keep=False).any() == True:
                # print("\n%s: workboot:%10s ,found below duplicated rows !!!!!!!!!" % (xls_file_src,sht_name))
                lg.info("\n sheet:{:^10} ,found below duplicated rows !!!!!!!!!".format(sht_name))
                # 准备显示重复行内容
                flag_dup = df.loc[df.duplicated("姓名", keep=False)]
                lg.info(flag_dup)
                # print(flag_dup)
                #如果重复值含有空白单元格，则保留末尾的空白单元格，删除前面的重复空白单元格
                flag_dup_na = df.loc[df.duplicated("姓名", keep="last") & (pd.isnull(df["姓名"]))]
                if len(flag_dup_na)>0:
                    drop_list = flag_dup_na.index.tolist()
                    # print("has drop these index row ：" ,drop_list)
                    lg.info("has drop these above row ：{}".format(drop_list))
                    df=df.drop(drop_list)

            df_tmp=df[["姓名", "年级", "合计"]]
            df_tmp=df_tmp.add_suffix('|'+ sht_name)
            # df_tmp.columns=df_tmp.columns.map(lambda x: str(x) +'|'+ sht_name if x!="姓名" else x)
            # tmp = (lambda x: str(x) + '|' + sht_name for x in df_tmp.columns if x.name!="姓名" else x)
            # print(df_tmp,df_tmp.columns)
            #合并各个工作簿的工作表df到一个目标df
            df_merge = pd.merge(df_merge, df[["姓名", "年级", "合计"]], how="outer", on="姓名",suffixes=("", "|" + sht_name))  # 以姓名作为公共列，对多个df数据集进行连接。
            df_concat = pd.concat([df_concat,df_tmp],axis=1,join="outer")  # 对两个数据集进行横向堆叠

            # print("workbook:<%10s>,df.shape:(%3d,%2d),auto skip %2d rows,"
            #       "df_merge：(%d,%d)"
            #       "df_concat：(%d,%d)" %
            #       (sht_name, df.shape[0], df.shape[1], first_row,df_merge.shape[0], df_merge.shape[1],df_concat.shape[0], df_concat.shape[1]))
            lg.warning(" sheet:{:^10},df.shape:({:>3d},{:>3d}),skip head-tail:({:>d},{:>d}),"
                  "df_merge：({},{}),"
                  "df_concat：({},{})".format(
                sht_name, df.shape[0], df.shape[1], first_row, row_tail_drop ,df_merge.shape[0], df_merge.shape[1], df_concat.shape[0],df_concat.shape[1]
                )
            )

        else:
            # print("workbook:<%10s> is ignored" % sht_name)
            lg.debug("{:>25} ==> {:<10} :is ignored".format(basename_xls,sht_name))

    df_merge.columns = df_merge.columns.map(lambda x: str(x).replace("合计","小计"))
    col_xj=df_merge.columns[df_merge.columns.str.find("小计")>-1]                                 #定位小计所在列
    df_merge.loc["pd_sum",col_xj]=df_merge.loc[pd.notnull(df_merge["姓名"]),col_xj].fillna(0).sum()       #对小计列进行垂直合计
    df_merge["合计"]=df_merge[col_xj].fillna(0).sum(axis=1)                                       #对每行进行水平合计
    df_merge = df_merge.drop([ "年级", "小计"],axis=1)
    # df_merge.columns=df_merge.columns.map(lambda x:process_index(x))

    # df_base=df_concat["姓名"].fillna("")
    #对包含姓名的所有列进行比对，将比对结果追加到最后列
    # df_base=df_concat.filter(like="姓名").fillna("")
    df_base=df_concat.loc[:,df_concat.columns.str.contains("姓名")].fillna("")
    df_base_pre=df_base.iloc[:, 0:-1]
    df_base_suf=df_base.iloc[:, 1:]
    df_base_suf.columns=df_base_pre.columns #对两个df列索引进行重命名，防止eq比较出错
    df_base_comp=df_base_pre.eq(df_base_suf)
    df_base_comp.columns=df_base_comp.columns.str.replace("姓名","xmbd")  #对重名列进行重命名，以防止concat堆叠失败
    df_concat=pd.concat([df_concat,df_base_comp],axis=1)

    df_concat.columns = df_concat.columns.str.replace("合计","小计")
    # col_xj=df_concat.columns[df_concat.columns.str.find("小计")>-1]          #定位小计所在列
    # df_concat["合计"] = df_concat[col_xj].fillna(0).sum(axis=1)             # 对每行进行水平合计
    df_concat["合计"] = df_concat.filter(like="小计").fillna(0).sum(axis=1)    # 对每行进行水平合计的第二种办法
    # df_concat.loc["", col_xj] = df_concat.loc[pd.notnull(df_concat["姓名"]), col_xj].fillna(0).sum()  # 对小计列进行垂直合计

    #针对一个工作簿只有一个有效工作表的，或没有有效工作表的，进行处理
    col_xm_last=df_concat.columns[df_concat.columns.str.find("姓名") > -1]
    if len(col_xm_last)>0:
        if len(col_xm_last) > 1:
            idx_col_xm_last=col_xm_last[-2]
        else:
            idx_col_xm_last = col_xm_last[0]
        df_concat.insert(0, "姓名", df_concat.loc[:, idx_col_xm_last])  # 定位倒数第二个个包含姓名的列，将其复制插入到第一列
        # print(col_xm_last, len(col_xm_last), idx_col_xm_last)
    else:
        df_concat=pd.DataFrame()

    if len(df_tail_dict_drop)>0:
        lg.info("workbook {} has drop {} sheet tail data:".format(xls_file_src,len(df_tail_dict_drop)))
        for k,v in df_tail_dict_drop.items():
            lg.info("worksheet {:^10}\n{}".format(k,v))

    return df_merge,df_concat

def drop_dup_empty_row(d,col_name="姓名",sht_name="_del"):
    import pandas as pd

    d = d.reset_index(drop=True)
    if d.shape[0]>0:
        flag_dup_na = d.loc[(pd.isnull(d[col_name]))]
        drop_list = flag_dup_na.index.tolist()
        # print("\nd has drop these index row ：\n",d.loc[drop_list])
        df_tmp = d.loc[drop_list].copy()
        lg.info("\nd has drop these index row ：\n{}".format(d.loc[drop_list]))
        d = d.drop(drop_list)
        return df_tmp
    else:
        return pd.DataFrame()

    
def get_all_files_by_walk(path, pattern=".*.*"):
    file_list = []
    path = os.path.expanduser(path)
    for (dirname, subdir, subfile) in os.walk(path):
        # print('dirname is %s, subdir is %s, subfile is %s' % (dirname, subdir, subfile))
        for f in subfile:
            # print(os.path.join(dirname, f))
            if re.match(pattern, f):
                # print(os.path.join(dirname, f))
                file_list.append(os.path.join(dirname, f))
    return file_list

def get_all_files_by_glob(path, pattern="*.*"):
    file_list = []
    for f in glob.glob(path + '\\' + pattern):
        # print(os.path.join(path, f))
        # lg.debug(os.path.join(path, f))
        file_list.append(os.path.join(path, f))
    return file_list

def get_all_files_by_listdir(path, pattern="*.*",sub_mode=False):
    file_list = []
    files=os.listdir(path)
    for item in files:
        path_tmp=os.path.join(path,item)
        if os.path.isfile(path_tmp):
            if re.match(pattern,item,re.IGNORECASE):
                file_list.append(path_tmp)
        elif sub_mode and os.path.isdir(path_tmp):
            get_all_files_by_listdir(path_tmp)
    return file_list

def out_log(fl):
    import logging

    # 创建Logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # 创建Handler
    # 终端Handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)

    # 文件Handler
    fileHandler = logging.FileHandler(fl, mode='w', encoding='UTF-8')
    fileHandler.setLevel(logging.NOTSET)

    # Formatter
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s')
    consoleHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)

    # 添加到Logger中
    logger.addHandler(consoleHandler)
    logger.addHandler(fileHandler)

    # 打印日志
    # logger.debug('debug 信息')
    # logger.info('info 信息')
    # logger.warning('warn 信息')
    # logger.error('error 信息')
    # logger.critical('critical 信息')
    # logger.debug('%s 是自定义信息' % '这些东西')
    return  logger

def add_format_for_excel(worksheet,row=0,col=0,width=11,fontHeight=20,format="",file_ext="xls"):
    """
    通过xlwt对excel进行格式设置,默认仅对表头进行标注
    :param worksheet:
    :param row:
    :param col:
    :param width:
    :param fontHeight:
    :param format:
    :param file_ext:
    :return:
    """
    import xlwt
    # bold_format = workbook.add_format({
    #     'bold': True,  # 字体加粗
    #     # 'border': 1,  # 单元格边框宽度
    #     'align': 'center',  # 水平对齐方式
    #     'valign': 'vcenter',  # 垂直对齐方式
    #     'fg_color': '#F4B084',  # 单元格背景颜色
    #     'font_color': '#9C0006',
    #     'text_wrap': True,  # 是否自动换行
    # })

    # 为样式创建字体
    font = xlwt.Font()

    # 字体类型
    font.name = '宋体'
    # 字体颜色
    font.colour_index = 0
    # 字体大小，11为字号，20为衡量单位
    font.height = 20 * fontHeight
    # font.bold = True
    # font.underline = True
    # font.italic = True
    # font.num_format_str = '#,##0.00'

    # 设置单元格对齐方式
    alignment = xlwt.Alignment()
    # 0x01(左端对齐)、0x02(水平方向上居中对齐)、0x03(右端对齐)
    # alignment.horz = 0x02
    # 0x00(上端对齐)、 0x01(垂直方向上居中对齐)、0x02(底端对齐)
    # alignment.vert = 0x01
    # 设置自动换行1
    alignment.wrap = 1

    alignment0 = xlwt.Alignment()
    alignment0.wrap = 0

    # 设置边框
    borders = xlwt.Borders()
    # 细实线:1，小粗实线:2，细虚线:3，中细虚线:4，大粗实线:5，双线:6，细点虚线:7
    # 大粗虚线:8，细点划线:9，粗点划线:10，细双点划线:11，粗双点划线:12，斜点划线:13
    borders.left = 0
    borders.right = 0
    borders.top = 0
    borders.bottom = 0
    borders.left_colour = 0
    borders.right_colour = 0
    borders.top_colour = 0
    borders.bottom_colour = 0

    # 设置列宽，一个中文等于两个英文等于两个字符，11为字符数，256为衡量单位
    for _ in range(26):
        worksheet.col(_).width = int(width * 256)

    # 设置背景颜色
    pattern = xlwt.Pattern()
    # 设置背景颜色的模式
    pattern.pattern = 0
    # 背景颜色
    pattern.pattern_fore_colour = 1
    # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...

    # 初始化样式
    style0 = xlwt.XFStyle()

    style0.font = font
    # style0.alignment = alignment
    style0.alignment.wrap = 1
    style0.borders = borders
    # style0.pattern = pattern

    worksheet.set_col_default_width=30
    worksheet.row(row).set_style(style0)
    # worksheet.write(1, 1,None,style = style0)

    # 合并单元格，合并第2行到第4行的第4列到第5列
    # worksheet.write_merge(2, 4, 4, 5, u'合并')

def print_me():
    print("%s\n        Hello,this is zk's lib for python.\n%s" %('-'*70 ,'-'*70))

if __name__=="__main__":
    lg=Log()
    lg.debug("\n{}\n        Hello,this is zk's lib for python.\n{}".format('-'*70 ,'-'*70))
else:
    lg = Log()

# list = get_all_files_by_glob(r"F:\ZK\jwc\绩效\源文件", "[gc][123z]_*.xls")
# with pd.ExcelWriter(r".\wage_dst.xls") as writer:
#     for f in list:
#         xls_auto_skip_rows(f, writer, f.split('\\')[-1][0:2])
#         pass
#     # xls_auto_skip_rows(r"F:\ZK\jwc\绩效\源文件\g3_2020.9-2021.1.xls",writer,"test")