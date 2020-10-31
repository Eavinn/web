# coding=utf-8
import random
import re

from . import api
from ihome.utils.captcha.captcha import captcha
from flask import make_response, request, jsonify, current_app
from ihome import redis_store, constants
from ihome.utils.response_code import RET, error_map
from ihome.utils.sms import CCP


@api.route('/image_code')
def get_image_code():
    """获取uuid，redis保存uuid和验证码，返回图片"""
    uuid = request.args.get("cur_id")
    if not uuid:
        return jsonify(errno=RET.PARAMERR, errmsg=error_map[RET.PARAMERR])

    name, text, content = captcha.generate_captcha()
    current_app.logger.info("图片验证码是：%s" % text)
    try:
        redis_store.set("uuid:%s" % uuid, text, constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])

    response = make_response(content)
    response.headers["Content-Type"] = "image/jpg"
    return response


@api.route("/sms_code", methods=["POST"])
def send_sms_code():
    """
    发送短信验证码:
    1. 接收参数(手机号，图片验证码，图片验证码标识)并进行参数校验
    2. 从redis中获取图片验证码(如果取不到，说明图片验证码已过期)
    3. 对比图片验证码，如果一致
    4. 使用云通讯发送短信验证码
        4.1 生成一个6位随机验证码
        4.2 使用云通讯发送短信
        4.3 在redis中存储短信验证码内容
    5. 返回应答，发送短信成功
    """
    # 1. 接收参数(手机号，图片验证码，图片验证码标识)并进行参数校验
    # req_data = request.data
    # req_dict = json.loads(req_data)
    # req_dict = request.get_json()

    req_dict = request.json
    mobile = req_dict.get("mobile")
    image_code = req_dict.get("image_code")
    image_code_id = req_dict.get("image_code_id")

    if not all([mobile, image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    if not re.match(r"^1[35789]\d{9}$", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式不正确")

    # 2. 从redis中获取图片验证码(如果取不到，说明图片验证码已过期)
    try:
        real_image_code = redis_store.get("uuid:%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取图片验证失败")

    if not real_image_code:
        return jsonify(errno=RET.NODATA, errmsg="图片验证码已过期")

    # 3. 对比图片验证码，如果一致
    if real_image_code.upper() != image_code.upper():
        return jsonify(errno=RET.DATAERR, errmsg="图片验证码错误")

    # 4. 使用云通讯发送短信验证码
    # 4.1 随机生成一个6位短信验证码
    sms_code = "%06s" % random.randint(0, 999999)  # 101
    current_app.logger.info("短信验证码是:%s" % sms_code)

    # 4.2 使用云通讯
    # try:
    #     res = CCP().send_template_sms(mobile, [sms_code, int(constants.SMS_CODE_REDIS_EXPIRES/60)], 1)
    # except Exception as e:
    #     current_app.logger.error(e)
    #     return jsonify(errno=RET.THIRDERR, errmsg="发送短信失败")
    #
    # if not res:
    #     # 发送短信验证码失败
    #     return jsonify(errno=RET.THIRDERR, errmsg='发送短信验证码失败')

    # 4.3 在redis中保存短信验证码内容
    try:
        redis_store.set("smscode:%s" % mobile, sms_code, constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存短信验证码失败")

    # 5. 返回应答，发送短信成功
    return jsonify(errno=RET.OK, errmsg="发送短信验证码成功")






