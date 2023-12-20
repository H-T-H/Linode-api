import requests
import json

class linode:    
    
    api_url = 'https://api.linode.com/v4/'

    def __init__(self,api_key):
        self.api_key = api_key


    #在该账号中创建实例
    def create_linode(self, type_, region, root_password, image, stackscript_id):
        # 设置请求头
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
        }

        # 创建Linode，提供root密码和操作系统ID
        create_response = requests.post(self.api_url + 'linode/instances', headers=headers, json={
            'type': type_,    # 选择服务器配置类型
            'region': region,        # 选择服务器所在的地区
            'root_pass': root_password,  # 设置root密码
            'image': image,  # 指定操作系统
            'stackscript_id': stackscript_id,#指定stackscript id
        })

        if create_response.status_code == 200:
            linode_data = create_response.json()
            linode_id = linode_data['id']
            linode_ip = linode_data['ipv4'][0]  # 获取Linode的IPv4地址
            print(f"success,ID: {linode_id}, IP: {linode_ip}")
            return linode_ip
        else:
            print(f"error {create_response.status_code}")
            return None
    #删除该账号内所有实例
    def delete_all_linodes(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
            }

        get_response = requests.get(self.api_url + 'linode/instances', headers=headers)

        if get_response.status_code == 200:
            linodes_data = get_response.json()['data']

            for linode in linodes_data:
                linode_id = linode['id']
                delete_response = requests.delete(self.api_url + f'linode/instances/{linode_id}', headers=headers)
                if delete_response.status_code != 200:
                    print(f"Failed to delete Linode instance {linode_id}, HTTP code: {delete_response.status_code}")
                    print(f"Error info: {delete_response.text}")
                else:
                    print(f"Linode instance {linode_id} deleted successfully")
        else:
            print(f"Failed to get Linode instances, HTTP code: {get_response.status_code}")
            print(f"Error info: {get_response.text}")
    
