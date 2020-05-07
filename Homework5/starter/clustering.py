from sklearn.cluster import KMeans
from PIL import Image
import numpy as np

def cluster(image,k_value):
	model=KMeans(n_clusters=k_value).fit(image)
	return [model.labels_,model.cluster_centers_]


if __name__=='__main__':
	image=Image.open('trees.png')
	rgb=image.convert('RGB')
	rgb_data=np.array(rgb.getdata(band=None),dtype=object)
	k_values=[3,6,20]
	for k_value in k_values:
		result=cluster(rgb_data,k_value)
		new_rgb_data=[]
		for ele in result[0]:
			feature=result[1][ele].tolist()
			int_feature=[]
			for f in feature:
				int_feature.append(int(f))
			new_rgb_data.append(tuple(int_feature))
		new_image=Image.new('RGB',(350,258))
		new_image.putdata(new_rgb_data)
		new_image.show()






