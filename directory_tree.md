.
├── OutPut
│   ├── Log
│   ├── Reports
│   │   ├── T 测试报告.html
│   │   ├── T.html
│   │   ├── history.json
│   │   ├── report.html
│   │   ├── test_api 测试报告.html
│   │   └── test_api.html
│   └── __init__.py
├── Pipfile
├── Pipfile.lock
├── README.md
├── cases
│   ├── cases
│   │   ├── test_api.xlsx
│   │   ├── test_openapi_cases.xlsx
│   │   └── test_postman_cases.xlsx
│   ├── templates
│   │   └── template.xlsx
│   └── temporary_file
│       ├── apifox.json
│       ├── openapi.json
│       └── postman.json
├── common
│   ├── __init__.py
│   ├── bif_functions
│   │   ├── __init__.py
│   │   ├── bif_datetime.py
│   │   ├── bif_hashlib.py
│   │   ├── bif_json.py
│   │   ├── bif_list.py
│   │   ├── bif_random.py
│   │   ├── bif_re.py
│   │   ├── bif_str.py
│   │   ├── bif_time.py
│   │   └── random_tools.py
│   ├── config.py
│   ├── crypto
│   │   ├── __init__.py
│   │   ├── encryption_aes.py
│   │   ├── encryption_base64_to_image.py
│   │   ├── encryption_main.py
│   │   ├── encryption_rsa.py
│   │   └── encryption_str.py
│   ├── data_extraction
│   │   ├── __init__.py
│   │   ├── analysis_json.py
│   │   ├── assert_dict.py
│   │   ├── data_extractor.py
│   │   ├── dependent_parameter.py
│   │   └── dict_get.py
│   ├── database
│   │   ├── __init__.py
│   │   ├── do_mongo.py
│   │   ├── execute_sql.py
│   │   ├── do_psycopg.py
│   │   └── do_redis.py
│   ├── variables.py
│   ├── file_handling
│   │   ├── __init__.py
│   │   ├── do_bat_sql.py
│   │   ├── do_excel.py
│   │   ├── excel.py
│   │   ├── get_all_path.py
│   │   ├── get_conf_data.py
│   │   ├── get_excel_init.py
│   │   ├── get_file.py
│   │   ├── get_folder.py
│   │   └── read_file.py
│   ├── random_tools
│   │   ├── __init__.py
│   │   ├── credit_cards
│   │   │   ├── __init__.py
│   │   │   ├── bankcard.py
│   │   │   └── cardbin.csv
│   │   ├── credit_identifiers
│   │   │   ├── __init__.py
│   │   │   ├── address.json
│   │   │   ├── credit_identifier.py
│   │   │   └── unified_social_credit_identifier.py
│   │   ├── emails
│   │   │   ├── __init__.py
│   │   │   ├── email.py
│   │   │   └── free_email.csv
│   │   ├── identification
│   │   │   ├── __init__.py
│   │   │   ├── area.csv
│   │   │   └── id_card.py
│   │   ├── names
│   │   │   ├── __init__.py
│   │   │   ├── first_name_boy.csv
│   │   │   ├── first_name_girl.csv
│   │   │   ├── last_name.csv
│   │   │   └── name.py
│   │   └── phone_numbers
│   │       ├── __init__.py
│   │       ├── phone.py
│   │       └── phone_area.csv
│   ├── utils
│   │   ├── WxworkSms.py
│   │   ├── __init__.py
│   │   ├── captcha.py
│   │   ├── function_run_time.py
│   │   ├── hooks.py
│   │   ├── http_client.py
│   │   ├── logger.py
│   │   ├── mylogger.py
│   │   ├── parsing_openapi.py
│   │   ├── parsing_postman.py
│   │   ├── request.py
│   │   ├── request_processor.py
│   │   ├── retry.py
│   │   └── singleton.py
│   └── validation
│       ├── __init__.py
│       ├── comparator_dict.py
│       ├── comparators.py
│       ├── extractor.py
│       ├── load_modules_from_folder.py
│       ├── loaders.py
│       └── validator.py
├── debug
│   ├── decorator_test.py
│   ├── identify_results.txt
│   └── myf.py
├── excel_converter.py
├── extensions
│   ├── __init__.py
│   ├── ext_method_online.py
│   └── sign.py
├── generate_tree.py
├── image
│   ├── wx.jpg
│   └── zfb.jpg
├── main.py
├── main_personal_information.py
├── pipenv_command.text
├── scripts
│   └── __init__.py
├── temp
│   ├── __init__.py
│   ├── excel_handler.py
│   ├── extent
│   │   ├── __init__.py
│   │   ├── api.py
│   │   ├── config.py
│   │   └── test_api_script.py
│   ├── fun.md
│   ├── get_zl.py
│   ├── mqtt_sender.py
│   ├── parsing_jmeter.py
│   ├── rabbit_mq_sender.py
│   └── test_log.py
└── test_script
    ├── __init__.py
    ├── automation
    │   ├── __init__.py
    │   └── test_api_script.py
    └── script
        ├── __init__.py
        ├── baseclass.py
        └── test_api.py
