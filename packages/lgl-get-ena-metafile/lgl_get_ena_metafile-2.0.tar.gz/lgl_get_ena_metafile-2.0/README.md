本代码主要通过构筑检索式无头浏览下载ENA数据库中高通量测序数据的元数据

安装通过以下代码

```python
pip install lgl_get_ena_metafile
```

使用需要依次传入3个参数，分别为

input_list_txt：数据文件所在路径

download_path：文件下载路径

chromedriver ：谷歌浏览器驱动程序绝对路径

通过以下代码使用：

```python
from lgl_get_ena_metafile import get_ena_metafile

download_path = r"C:\Users\Huawei\Desktop\test"    ##定义下载地址
input_list_txt = r'C:\Users\Huawei\Desktop\test_sra.txt'  ##定义输入文件路径
chromedriver = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"   ##定义浏览器驱动地址

get_ena_metafile(input_list_txt,download_path,chromedriver) 
```