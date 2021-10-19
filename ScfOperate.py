import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.scf.v20180416 import scf_client, models


# 将 token 写入环境变量
# 具体参考腾讯云的文档
# https://cloud.tencent.com/document/product/583/18580
def EnvWrite(refresh_token, function_name, clien_id, secret, redirect_uri,
             region, SecretId, SecretKey):
    try:
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "scf.tencentcloudapi.com"  # 就近地域接入

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = scf_client.ScfClient(cred, region, clientProfile)

        req = models.UpdateFunctionConfigurationRequest()
        # 修改
        params = {
            "FunctionName": function_name,
            "Environment": {
                "Variables": [{
                    "Key": "refresh_token",
                    "Value": refresh_token
                }, {
                    "Key": "function_name",
                    "Value": function_name
                }, {
                    "Key": "clien_id",
                    "Value": clien_id
                }, {
                    "Key": "secret",
                    "Value": secret
                }, {
                    "Key": "redirect_uri",
                    "Value": redirect_uri
                }, {
                    "Key": "region",
                    "Value": region
                }, {
                    "Key": "secret_id",
                    "Value": SecretId
                }, {
                    "Key": "secret_key",
                    "Value": SecretKey
                }]
            }
        }
        req.from_json_string(json.dumps(params))

        resp = client.UpdateFunctionConfiguration(req)
        print(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)
