# lib สร้างขึ้นมาสำหรับส่งข้อมูลเข้าสู่ระบบ Web service สปสช  

ทำไว้ใช้โครงการ บางอย่างยังไม่อัตโนมัติซะทีเดียว มีอันที่ผมลองใช้แล้ว จะมีส่วนการ auth, สร้างโฟเดอร์ และ upload ไฟล์ ลองเอาไปดูเป็นตัวอย่าง หรือจะเอาไปทำ lib ก็ได้ MIT License  

ตัว lib จะทำการ auth ให้อัตโนมัติ  

## วิธีใช้งาน

```python
from RestApi import RestApi 

api = RestApi("https://test.th/webhdfs", "username_hii_amed", "password_hii_amed")

# การสร้าง folder
# https://test.th/webhdfs/v1/hii/test/example_folder
remote_folder = "hii/test/example_folder"
api.mkdirs(remote_folder)

# การ upload file โดยจะอัพโหลดไฟล์ในเครื่องชื่อ test.txt
# ไว้บน hdfs สปสช โฟเดอร์ https://test.th/webhdfs/v1/hii/test/example_folder
# โดยใช้ชื่อไฟล์บน hdfs สปสช ชื่อ testRemote.txt 
# จำเป็นต้องสร้างโฟเดอร์ก่อน
# https://test.th/webhdfs/v1/hii/test/example_folder/testRemote.txt

remote_folder = "hii/test/example_folder" # กำหนดโฟเดอร์ปลายทางบน hdfs สปสช.
api.mkdirs(remote_folder)  # สร้างโฟเดอร์
local_file_location = "/home/thanachai/test.txt"  # ตำแหน่งไฟล์ภายในเครื่องเรา ที่ต้องการ upload
remote_file_location = "hii/test/example_folder/testRemote.txt" # ตำแหน่งไฟล์ปลายทางบน hdfs สปสช.
api.upload_and_overwrite(local_file_location, remote_file_location)  #ทำการ upload
```
