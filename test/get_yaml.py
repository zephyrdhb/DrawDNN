import yaml

# 从 YAML 文件中读取数据
with open("../config.yml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)  # 使用 FullLoader 避免安全漏洞
    print(config.get("shuffle1", False))
    for i, v in config['layers'].items():
        print(i, v)
