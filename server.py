from flask import Flask, render_template, request
import music_generator as mg
import json
import tensorflow as tf
import prepare as p

app = Flask(__name__)

@app.route("/")
def main():
	# return "AHHHHHHHHHHHH"
	return render_template('index.html')

@app.route('/gen',methods=['GET'])
def show_stuff():
	chs = request.args.get('chords')
	temp = float(request.args.get('temperature'))
	mlen = int(request.args.get('length'))

	cleaned = p.chord_cleaned(chs)
	print(type(cleaned))

	fill = [0]*(60 - len(cleaned))
	fill.extend(cleaned)
	# return str(fill)
	# return str(p.chord_cleaned(chs))
	# return 
	#TODO parse chords 

	config = tf.ConfigProto()
	config.gpu_options.allow_growth = True
	sess = tf.Session(config=config)

	ml_model = mg.load_model('softmax.h5')
	with open('clean_dataset.json','r') as f:
	    training_data = json.loads(f.read()) #reminder that training_data is a huge ass string

	hp_maxlen = 60
	muse = mg.text_generate_w(ml_model,fill,60 - len(cleaned),maxlen=hp_maxlen,temperature=temp,textlen=60)
	return str(muse)
	# return str(text)
	# return "temperature = {} lchs = {} len = {}".format(temp,chords,mlen)



if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=80)


#Parameter with list of chords 
#Temperature 
#length of the generated chords 

# vlc "C:\\Users\\Ted\\Documents\\uh2019-music\\output_midi\\0_1" :no-video :sout=#transcode{acodec=mp3,ab=256}:std{access=file,mux=dummy,dst="C:\Users\Ted\Documents\uh2019-music\output_midi\test.mp3"} vlc://quit