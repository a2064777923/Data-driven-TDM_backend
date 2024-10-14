### 項目結構
```commandline
tdm_backend/
│
├── app/
│   ├── __init__.py
│   ├── hotel_overview/   #藍圖
│   │   ├── __init__.py
│   │   ├── routes.py
│   ├── models.py    #模型
│   └── templates/
│       └── ...
│── ssl/  #https相關證書

├── tests/
│   └── ...
│
├── venv/
│   └── ...
│
├── config.py
├── requirements.txt
└── run.py   #入口文件
```