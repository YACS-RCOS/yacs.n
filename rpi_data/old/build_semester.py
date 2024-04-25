import os

if __name__ == '__main__':
	os.system("SOURCE_URL=https://sis.rpi.edu/reg/zs20230501.htm DEST=out1.csv HEADERS=True python rpi-parse.py")
	os.system("SOURCE_URL=https://sis.rpi.edu/reg/zs20230502.htm DEST=out2.csv HEADERS=False python rpi-parse.py")
	os.system("SOURCE_URL=https://sis.rpi.edu/reg/zs20230503.htm DEST=out3.csv HEADERS=False python rpi-parse.py")
	os.system("cat out1.csv out2.csv out3.csv > out.csv")