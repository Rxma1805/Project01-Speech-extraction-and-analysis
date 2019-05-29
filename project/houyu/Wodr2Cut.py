from common_func import load, cut, token, get_cutfile, get_cutfile

news_content  = load("data/sqlResult_1558435.csv")
print(news_content[0])
print(cut("这是一个测试"))
news_content = [token(n) for n in news_content]
news_content = [' '.join(n) for n in news_content]
news_content = [cut(n) for n in news_content]
print(news_content[0])
get_cutfile("news_cut.txt", news_content)

