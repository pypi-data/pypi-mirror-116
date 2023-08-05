def mapping():
    return [
        {
            "col_name": "COMPANY",
            "col_desc": "数据公司",
            "candidate": [],
            "type": "String",
            "not_null": False,
        },
        {
            "col_name": "SOURCE",
            "col_desc": "数据来源",
            "candidate": [],
            "type": "String",
            "not_null": False,
        },
        {
            "col_name": "TAG",
            "col_desc": "文件标识",
            "candidate": ['_TAG', '_Tag'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "PACK_ID",
            "col_desc": "PACK_ID",
            "candidate": ['PACK_ID'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "MOLE_NAME_EN",
            "col_desc": "分子名英文",
            "candidate": ['MOLE_NAME_EN'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "MOLE_NAME_CH",
            "col_desc": "分子名中文",
            "candidate": ['MOLE_NAME_CH'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "PROD_DESC",
            "col_desc": "PROD_DESC",
            "candidate": ['PROD_DESC'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "PROD_NAME_CH",
            "col_desc": "PROD_NAME_CH",
            "candidate": ['PROD_NAME_CH'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "CORP_NAME_EN",
            "col_desc": "公司名英文",
            "candidate": ['CORP_NAME_EN'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "CORP_NAME_CH",
            "col_desc": "公司名中文",
            "candidate": ['CORP_NAME_CH'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "MNF_NAME_EN",
            "col_desc": "厂家名英文",
            "candidate": ["MNF_NAME_EN"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "MNF_NAME_CH",
            "col_desc": "厂家名中文",
            "candidate": ['MNF_NAME_CH'],
            "type": "Integer",
            "not_null": True,
        },
        {
            "col_name": "PCK_DESC",
            "col_desc": "规格",
            "candidate": ['PCK_DESC'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "DOSAGE",
            "col_desc": "剂型",
            "candidate": ['DOSAGE'],
            "type": "Integer",
            "not_null": True,
        },
        {
            "col_name": "SPEC",
            "col_desc": "规格",
            "candidate": ["SPEC"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "PACK",
            "col_desc": "包装",
            "candidate": ['PACK'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "NFC1",
            "col_desc": "NFC",
            "candidate": ["NFC1"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "NFC1_NAME",
            "col_desc": "NFC1_NAME",
            "candidate": ['NFC1_NAME'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "NFC1_NAME_CH",
            "col_desc": "NFC1_NAME_CH",
            "candidate": ['NFC1_NAME_CH'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "NFC12",
            "col_desc": "NFC12",
            "candidate": ['NFC12'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "NFC12_NAME",
            "col_desc": "NFC12_NAME",
            "candidate": ['NFC12_NAME'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "NFC12_NAME_CH",
            "col_desc": "NFC12_NAME_CH",
            "candidate": ['NFC12_NAME_CH'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "NFC123",
            "col_desc": "NFC123",
            "candidate": ['NFC123'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "NFC123_NAME",
            "col_desc": "NFC123_NAME",
            "candidate": ['NFC123_NAME'],
            "type": "Double",
            "not_null": True,
        },
        {
            "col_name": "CORP_ID",
            "col_desc": "CORP_ID",
            "candidate": ["CORP_ID"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "MNF_TYPE",
            "col_desc": "MNF_TYPE",
            "candidate": ["MNF_TYPE"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "MNF_TYPE_NAME",
            "col_desc": "MNF_TYPE_NAME",
            "candidate": ['MNF_TYPE_NAME'],
            "type": "Double",
            "not_null": True,
        },
        {
            "col_name": "MNF_TYPE_NAME_CH",
            "col_desc": "MNF_TYPE_NAME_CH",
            "candidate": ['MNF_TYPE_NAME_CH'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "MNF_ID",
            "col_desc": "MNF_ID",
            "candidate": ['MNF_ID'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "ATC1_CODE",
            "col_desc": "ATC1_CODE",
            "candidate": ["ATC1_CODE"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "ATC1_DESC",
            "col_desc": "ATC1_DESC",
            "candidate": ["ATC1_DESC"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "ATC2_CODE",
            "col_desc": "ATC2_CODE",
            "candidate": ["ATC2_CODE"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "ATC2_DESC",
            "col_desc": "ATC2_DESC",
            "candidate": ["ATC2_DESC"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "ATC3_CODE",
            "col_desc": "ATC3_CODE",
            "candidate": ["ATC3_CODE"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "ATC3_DESC",
            "col_desc": "ATC3_DESC",
            "candidate": ["ATC3_DESC"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "ATC4_CODE",
            "col_desc": "ATC4_CODE",
            "candidate": ["ATC4_CODE"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "ATC4_DESC",
            "col_desc": "ATC4_DESC",
            "candidate": ["ATC4_DESC"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "ATC1",
            "col_desc": "ATC1",
            "candidate": ["ATC1"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "ATC2",
            "col_desc": "ATC2",
            "candidate": ["ATC2"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "ATC3",
            "col_desc": "ATC3",
            "candidate": ["ATC3"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "ATC4",
            "col_desc": "ATC4",
            "candidate": ["ATC4"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "REMARK",
            "col_desc": "REMARK",
            "candidate": ["REMARK"],
            "type": "String",
            "not_null": False,
        },
    ]
