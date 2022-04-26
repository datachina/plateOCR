# 这是一个示例 Python 脚本。

# 按 ⌃R 执行或将其替换为您的代码。
# 按 双击 ⇧ 在所有地方搜索类、文件、工具窗口、操作和设置。
from core.plate_generate.generate import GenPlate


def gen_blue():
    generator = GenPlate(template=r"./data/image/blue.bmp", plate_type='blue')
    generator.gen_batch(1, r'./testInBlue', (94, 24))


def gen_yellow():
    generator = GenPlate(template=r"./data/image/yellow.bmp", plate_type='yellow')
    generator.gen_batch(1, r'./testInYellow', (94, 24))


def gen_green():
    generator = GenPlate(template=r"./data/image/green.bmp", plate_type='green')
    generator.gen_batch(1, r'./testInGreen', (94, 24))


if __name__ == '__main__':
    # gen_blue()
    # gen_yellow()
    gen_green()
