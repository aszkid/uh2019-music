from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main():
	return 'Howdy ;0 '
	# return render_template('index.html')

@app.route('/temperature=<temp>/lchs=<chords>/length=<len>',methods=['GET'])
def show_stuff(temp,chords,len):
	return "temperature = {} lchs = {} len = {}".format(temp,chords,len)



if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=80)


#Parameter with list of chords 
#Temperature 
#length of the generated chords 