import os


if __name__ == '__main__':
	os.system("python3 foo.py https://sis.rpi.edu/reg/zs20200501.htm out1.csv 1")
	os.system("python3 foo.py https://sis.rpi.edu/reg/zs20200502.htm out2.csv 0")
	os.system("python3 foo.py https://sis.rpi.edu/reg/zs20200503.htm out3.csv 0")
	os.system("cat out1.csv out2.csv out3.csv > out.csv")