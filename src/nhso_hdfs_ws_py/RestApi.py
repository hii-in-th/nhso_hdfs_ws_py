import requests
import json
import re


class RestApi(object):
    # url example http://aaa.co.com/webhdfs
    def __init__(self, base_url, username, password):
        self.name = "nhso core api" + base_url
        self.base_url = base_url
        self.username = username
        self.password = password
        self.token = ""

    def __check_deep(self, deep):
        if deep < 0:
            return Exception("Deep lost")

    # ใช้สำหรับขอ token จาก user
    # return token
    def __auth_core(self):
        api_url = self.base_url + "/auth-jwt"
        print(api_url)
        payload = json.dumps({"username": self.username, "password": self.password})
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", api_url, headers=headers, data=payload)
        status = response.status_code
        if status == 200:
            token = response.json()["token"]
            return token
        else:
            return Exception(api_url + " code " + str(status))

    # ตรวจสอบว่า Token ยังใช้งานได้อยู่หรือไม่
    # return bool
    def __verify_token_core(self):
        api_url = self.base_url + "/auth-jwt-verify"
        payload = json.dumps({"token": self.token})
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", api_url, headers=headers, data=payload)
        status = response.status_code
        print(api_url + " status code " + str(status))
        if status == 200:
            return True
        else:
            return False

    def __auth(self):
        verify = self.__verify_token_core()
        if verify == False:
            self.token = self.__auth_core()

    # return list
    def __list_file(self, dir_parth, deep=3):
        self.__check_deep(deep)
        api_url = self.base_url + "/v1/" + dir_parth + "?op=LISTSTATUS"
        print(api_url + " deep:" + deep)
        payload = {}
        headers = {"Authorization": "JWT " + self.token}
        response = requests.request("GET", api_url, headers=headers, data=payload)
        status = response.status_code
        if status == 200:
            return response.json()
        elif status == 401:
            self.__auth()
            return self.__list_file(dir_parth, deep - 1)
        else:
            return Exception(api_url + " code " + str(status))

    def list_file(self, dir_parth):
        return self.__list_file(dir_parth, 5)

    # mkdir -p no ruturn
    def __mkdirs(self, dir_parth, deep=3):
        self.__check_deep(deep)
        api_url = self.base_url + "/v1/" + dir_parth + "?op=MKDIRS"
        print(api_url + " deep:" + deep)
        payload = {}
        headers = {"Authorization": "JWT " + self.token}
        response = requests.request("PUT", api_url, headers=headers, data=payload)
        status = response.status_code
        # if status != 200:
        #    return Exception(api_url + " code " + str(status))

        if status == 401:
            self.__auth()
            self.__mkdirs(dir_parth, deep - 1)

    def mkdirs(self, dir_parth):
        self.__mkdirs(dir_parth, 5)

    # มีไฟล์ หรือ ไดเรกทอรี่ที่ระบุอยู่หรือไม่
    def exists(self, dir_or_file_parth):
        print("call Check exists file")
        try:
            self.list_file(dir_or_file_parth)
            print("Check exists file true")
            return True
        except:
            print("Check exists file false")
            return False

    def __move_file_and_rename(self, source_path, destination_path, deep=3):
        self.__check_deep(deep)
        api_url = (
            self.base_url
            + "/v1/"
            + source_path
            + "?op=RENAME&destination=/"
            + destination_path
        )
        print(api_url + " deep:" + deep)
        payload = {}
        headers = {"Authorization": "JWT " + self.token}
        response = requests.request("PUT", api_url, headers=headers, data=payload)
        status = response.status_code
        if status == 401:
            self.__auth()
            self.__move_file_and_rename(source_path, destination_path, deep - 1)

    def move_file_and_rename(self, source_path, destination_path):
        self.__move_file_and_rename(source_path, destination_path, 5)

    def __delete(self, dir_or_file_parth, deep=3):
        self.__check_deep(deep)
        api_url = self.base_url + "/v1/" + dir_or_file_parth + "?op=DELETE"
        print(api_url + " deep:" + deep)
        payload = {}
        headers = {"Authorization": "JWT " + self.token}
        response = requests.request("DELETE", api_url, headers=headers, data=payload)
        status = response.status_code
        if status == 401:
            # 401 Un
            self.__auth()
            self.__delete(dir_or_file_parth, deep - 1)
        elif status == 500:
            # 500 มีไฟล์หรือ โฟเดอร์อยู่ ไม่สามารถลบได้
            return Exception(api_url + " code " + str(status))

        elif status == 200:
            # ไม่มีไฟล์ 200 และ {"boolean": false}
            pass

    def delete(self, dir_or_file_parth):
        self.__delete(dir_or_file_parth)

    def __get_file_name(self, full_parth):
        p = re.compile("/?.+/(.+)$")
        return p.match(full_parth).groups()[0]

    def __upload_and_overwrite(self, local_file_path, nhso_file_path, deep=3):
        self.__check_deep(deep)
        self.__auth()  # ใส่ไว้เลย เพราะเป็น fun ที่ช้า
        api_url = self.base_url + "/v1/" + nhso_file_path + "?op=CREATE"
        print(api_url + " deep:" + deep)
        filename = self.__get_file_name(nhso_file_path)
        payload = {}
        headers = {"Authorization": "JWT " + self.token}
        files = [
            (
                "file",
                (
                    filename,
                    open(local_file_path, "rb"),
                    "application/octet-stream",
                ),
            )
        ]
        response = requests.request(
            "PUT", api_url, headers=headers, data=payload, files=files
        )
        status = response.status_code
        if status == 401:
            # 401 Un
            self.__auth()
            self.__upload_and_overwrite(local_file_path, nhso_file_path, deep - 1)

    def upload_and_overwrite(self, local_file_path, nhso_file_path):
        self.__upload_and_overwrite(local_file_path, nhso_file_path, 3)
