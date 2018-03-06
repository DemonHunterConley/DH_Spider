import jieba
from scipy.misc import imread
import matplotlib.pyplot as plt
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
from PIL import Image
import numpy as np

text = open("F:\学习\临时\献给周总理.txt").read()

wordlist = jieba.cut(text,cut_all = True)

wl_space_split = " ".join(wordlist)

picture = np.array(Image.open("F:\学习\临时\最后一次.jpg"))

my_wordcloud = WordCloud( background_color = 'white',      # 设置背景颜色  
                            mask = picture, # 设置背景图片
                          margin = 5,
                           font_path="C:\\Windows\\Fonts\\STFANGSO.ttf" ,
                            max_words = 2000,              # 设置最大现实的字数  
                            stopwords = STOPWORDS,         # 设置停用词  
                            max_font_size = 50,            # 设置字体最大值  
                            random_state = 30,             # 设置有多少种随机生成状态，即有多少种配色方案  
                            )

# generate word cloud   
my_wordcloud.generate(wl_space_split)

image_colors = ImageColorGenerator(picture)

# recolor wordcloud and show    
my_wordcloud.recolor(color_func=image_colors)  
  
plt.imshow(my_wordcloud)    # 显示词云图  
plt.axis("off")             # 是否显示x轴、y轴下标  
plt.show()  
  
