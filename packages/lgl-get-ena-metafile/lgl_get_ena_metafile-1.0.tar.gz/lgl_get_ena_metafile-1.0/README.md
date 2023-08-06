本代码主要通过构筑检索式无头浏览下载ENA数据库中高通量测序数据的元数据

安装通过以下代码

```python
pip install lgl_getenametafile
```

使用需要依次传入4个参数，分别为

chromedriver_path ：谷歌浏览器驱动程序绝对路径

disease_name：疾病名称

drugname_list_path：药物列表绝对路径，后缀为txt的文本文档

download_path：自定义文件下载路径

通过以下代码使用：

```python
from lgl_getpubmed import getPubMed_reference
chromedriver_path = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"  ##浏览器驱动路径
disease_name = 'T-cell lymphoma'                                                          ##疾病名称
download_path = r"C:\Users\Huawei\Desktop"                                                ##下载路径
drugname_list_path = r'C:\Users\Huawei\Desktop\drug_list.txt'                             ##药物名称列表
getPubMed_reference(chromedriver_path, disease_name, drugname_list_path, download_path)  ##浏览器驱动；疾病名称；药物名称列表；下载路径
```