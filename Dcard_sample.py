from Dcard import get_urls, get_contents
import pandas as pd

topic = "感情" ## SEARCHING TOPIC
url = get_urls(topic, 1).main()
fin_overview, fin_comment = get_contents(url).main()
pd.set_option('expand_frame_repr', False)
print(fin_overview, fin_comment)