base_distance = 7
cutoff_distance = 60
#assuming a list of ngos
ngos = ['a','b','c','d','e','f','g','h','i','j'] #id of ngos 
ngo_distance = dict( a=10,b=12,c=1,d=2,e=4,f=5, g=3, h=20, i=30, j=20 )
ngo_trends = dict( a=1, b=6, c=9, d=3, e=8,f=7,g=5,h=10,i=4,j=2 )
near_ngos={}
points = {}

def recommend_nologin( ngo_distance , ngo_trends ): # dictionaries with ngo's ids and distances, trends  
	
	for ngo in ngos:
		if ngo_distance[str(ngo)] < cutoff_distance :
			near_ngos[str(ngo)] = ngo_distance[str(ngo)]
	
	from operator import itemgetter
	sorted_ngo_trends =  sorted(ngo_trends.items(), key=itemgetter(1)) 
	#print sorted_ngo_trends

	for k,v in sorted_ngo_trends:
		if not k in near_ngos:
			sorted_ngo_trends.remove((k,v))
	#print sorted_ngo_trends	

	near_ngo_trends = {}
	v = 1
	for	k,m in sorted_ngo_trends:
		near_ngo_trends[k] = v
		v = v + 1 
	
	print near_ngo_trends

		


	for ngo in ngos :
		if ngo_distance[str(ngo)] < cutoff_distance : #nearby ngos
			print ngo_distance[str(ngo)]
			value = ( base_distance/ngo_distance[str(ngo)] ) +	float(base_distance * ( len(near_ngos) - near_ngo_trends [str(ngo)] )/ len(near_ngos))
			points[str(ngo)] = value
		'''
		else:
			value = float(base_distance * 1.8 *  ( len(near_ngos) - near_ngo_trends [str(ngo)] )/ len(near_ngos))
			points[str(ngo)] = value
		'''	
	print sorted(ngo_trends.items(), key=itemgetter(1))



recommend_nologin(ngo_distance, ngo_trends)
			
