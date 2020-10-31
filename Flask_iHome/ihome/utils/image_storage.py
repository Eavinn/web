# -*- coding: utf-8 -*-

from qiniu import Auth, put_data

# 需要填写你的 Access Key 和 Secret Key
access_key = 'ndNCmYJhZARctIwAJjmg4WZ7iRo95rxc-Vh_u8xb'
secret_key = 'VjZ6YtlUG55BEPiprT9q-RmPlJn1s1Vxm61hfmP1'
# 要上传的空间
bucket_name = 'ihomemeng'


def storage_image(local_file):

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, None, 3600)

    # 上传文件到七牛云
    ret, info = put_data(token, None, local_file)
    print(ret, info)
    if info.status_code == 200:
        return ret.get("key")
    else:
        raise Exception("文件上传到七牛云失败")


if __name__ == '__main__':
    file_name = storage_image('../static/images/EZ0A0437.jpg')
    print(file_name)

