学习笔记

1.pandas基于numpy实现，可进行矢量运算，适合处理复杂的数据统计

2.表格与DataFrame，数据输入输出，数据检查

3.DataFrame的行索引：index；列索引：columns

4.pandas可将数据永久保存，支持：HTML，CSV，JSON，Excel等格式

5.df.to_csv()/read_csv()   //写入csv文件，读取csv文件
  df.head()  //获取前n行数据
  df.tail()  //获取尾部n行数据
  df.shape   //数据规模
  df.describe()   //输出DF的主要数据特征
  
6.获取数据：df[列名]，df[[多个列的列名]]

7.to_excel/read_excel:从excel文件中获取存储数据

8.drop()方法删除一个或多个行或列，df[新列名] = col_new_data

9.loc[],iloc[]选择基于索引值的行和序列号的行，行与列关联选择

10.数据遍历：iterrows(),itertuples(),iteritmes()

11.Series数据结构：一维向量数据