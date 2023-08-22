# **提醒！自动化测试反馈**

## **请相关同事注意，及时跟进！**

#### 项目名称：<font color='#009933'>{{ title }}</font><br/>
#### 测试人员：<font color='#009933'>{{ tester }}</font><br/>
#### 开始时间：<font color='#009933'>{{ begin_time }}</font><br/>
#### 运行时间：<font color='#009933'>{{ runtime }}</font><br/>  
> 测试用例总数：**<font color='#009933'>{{ all }}</font><br/>**
> 测试用例通过率：**<font color='#009933'>{{ pass_rate }}%</font><br/>**
> 成功数: **<font color='#009933'>{{ success }}</font><br/>**
> 失败数：**<font color='#FF6666'>{{ fail }}</font><br/>**
> 跳过数：**<font color='#009999'>{{ skip }} </font><br/>**
> 错误数：**<font color='#CC0066'>{{ error }}</font><br/>**
##### **报告链接：** [jenkins报告,请点击后进入查看](report_url)

**----------------上一次运行结果----------------**<br/>

> 测试用例总数: **<font color='#009933'>{{ history[-2]['all'] }}</font><br/>**
> 测试用例通过率：**<font color='#009933'>{{ history[-2]['pass_rate'] }}%</font><br/>**
> 成功数：**<font color='#009933'>{{ history[-2]['success'] }}</font><br/>**
> 失败数：**<font color='#FF6666'>{{ history[-2]['fail'] }}</font><br/>**
> 跳过数：**<font color='#009999'>{{ history[-2]['skip'] }}</font><br/>**
> 错误数：**<font color='#CC0066'>{{ history[-2]['error'] }}</font><br/>**

