from flask import Flask,render_template,request
import pickle
import numpy as np

Books=pickle.load(open('BOOK.pkl','rb'))
final_df=pickle.load(open('final_df.pkl','rb'))
scores=pickle.load(open('scores.pkl','rb'))
Num_books=pickle.load(open('books.pkl','rb'))

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html',book_name=list(Books['Book-Title'].values),
    book_author=list(Books['Book-Author'].values),
    book_img=list(Books['Image-URL-M'].values),
    book_votes=list(Books['Ratings'].values),
    
    )

@app.route('/recommend')
def recommend():
    return render_template('recommend.html')

@app.route('/recommendbooks',methods=['POST'])
def recommendbooks():
    user_input=request.form.get('user_input')
    data=[]
    index=np.where(final_df.index==user_input)[0][0]
    boo=sorted(list(enumerate(scores[index])),key=lambda x:x[1],reverse=True)[1:11]
    for i in boo:
        l1=[]
        temp=Num_books[Num_books['Book-Title']==final_df.index[i[0]]]
        l1.extend(list(temp.drop_duplicates('Book-Title')['Book-Title'].values))
        l1.extend(list(temp.drop_duplicates('Book-Title')['Book-Author'].values))
        l1.extend(list(temp.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(l1)
  
    return render_template('recommend.html',data=data)


if __name__=='__main__':
    app.run(debug=True)
