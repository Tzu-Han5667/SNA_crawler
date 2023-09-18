from Instagram import tag_search
import pandas as pd

topic = "koala"
fin_data = tag_search(topic, 5).main(username='YOUR INSTAGRAM ACCOUNT', password='YOUR INSTAGRAM PASSWORD')
pd.set_option('expand_frame_repr', False)
print(fin_data)