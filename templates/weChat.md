# **提醒！自动化测试反馈**\n#### **请相关同事注意，及时跟进！**

> 项目名称：<font color='info'>{{title}}</font> 
> 测试人员：<font color='info'>{{tester}}</font> 
> 开始时间：<font color='info'>{{begin_time}}</font> 
> 运行时间：<font color='info'>{{runtime}}</font>  
> 测试用例总数：<font color='info'>{{all}}</font>
> 测试用例通过率：<font color='info'>{pass_rate}%</font>
> 成功数: <font color='info'>{{success}}</font>
> 失败数：<font color='warning'>{{fail}}</font>
> 跳过数：<font color='info'>{{skip}}, </font>
> 错误数：<font color='comment'>{{error}}</font>
> **--------------------上一次运行结果--------------------**
> 测试用例总数: <font color='info'>{{ history[-1]['all'] }}</font>
> 测试用例通过率：<font color='info'>{{history[-1]['pass_rate']}}%</font>
> 成功数：<font color='info'>{{history[-1]['success']}}</font>
> 失败数：<font color='warning'>{{history[-1]['fail']}}</font>
> 跳过数：<font color='info'>{{history[-1]['skip']}}</font>
> 错误数：<font color='comment'>{{history[-1]['error']}}</font>
> ##### **报告链接：** [jenkins报告,请点击后进入查看](report_url)