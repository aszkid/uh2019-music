from flask import Flask, render_template, request
import music_generator as mg
import json
import tensorflow as tf

app = Flask(__name__)

@app.route("/")
def main():
	

	return "AHHHHHHHHHHHH"
	# return render_template('index.html')

@app.route('/gen',methods=['GET'])
def show_stuff(temp,chords,len):
	chs = request.args.get('chords')
	temp = request.args.get('temp')
	mlen = request.args.get('temp')

	config = tf.ConfigProto()
	config.gpu_options.allow_growth = True
	sess = tf.Session(config=config)

	ml_model = mg.load_model('softmax.h5')
	with open('clean_dataset.json','r') as f:
	    training_data = json.loads(f.read()) #reminder that training_data is a huge ass string

	hp_maxlen = 60
	text = mg.text_generate(ml_model,training_data,maxlen=hp_maxlen,temperature=0.9,textlen=60)

	return "temperature = {} lchs = {} len = {}".format(temp,chords,mlen)



if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=80)


#Parameter with list of chords 
#Temperature 
#length of the generated chords 