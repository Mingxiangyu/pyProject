from wordcloud import WordCloud
f = open('data/alice.txt').read()
wordcloud = WordCloud(background_color="white",width=1000, height=860, margin=2).generate(f)

import matplotlib.pyplot as plt
ax = plt.imshow(wordcloud)
fig = ax.figure
fig.set_size_inches(25,20)
plt.axis("off")
plt.show()

# 作者：ZhangYi
# 链接：https://www.zhihu.com/question/19895141/answer/515535069
# 来源：知乎
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。