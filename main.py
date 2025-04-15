# flask中文文档  https://dormousehole.readthedocs.io/en/latest/

import json
rs={'data': {'commentCount': 0,
                   'score': 0.0,
                   'tagList': [{'tagName': '全部',
                                'tagNum': 0,
                                'tagScore': 5,
                                'tagType': 0}]},
          'ret': True,
          'statusCode': 200}
# data=['1']
# da='〇'.join(data)
# dat=da.split('孙')
str1=json.dumps(rs)

print(type(rs))
